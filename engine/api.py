import os
import asyncio
import concurrent.futures
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent.brain import Brain
from agent.memory import Memory

# Ensure screenshots directory exists for static mounting
os.makedirs("screenshots", exist_ok=True)

app = FastAPI(title="Viora API Server", description="Exposes the Viora agentic system over WebSockets and REST.")

# Allow React app running on localhost:5173 or other local origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount screenshots directory to serve images statically to frontend
app.mount("/screenshots", StaticFiles(directory="screenshots"), name="screenshots")

# Initialize Viora Core
brain = Brain()
memory = Memory()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

class UserMessage(BaseModel):
    message: str

class WSStatusUpdater:
    """Wrapper that matches Rich's console.status().update() signature 
    but sends updates through a WebSocket to the UI."""
    def __init__(self, websocket: WebSocket, loop: asyncio.AbstractEventLoop):
        self.websocket = websocket
        self.loop = loop

    def update(self, msg: str):
        # Fire-and-forget payload over active loop
        asyncio.run_coroutine_threadsafe(
            self.websocket.send_json({"type": "status", "content": msg}),
            self.loop
        )

@app.get("/status")
def get_status():
    return {
        "status": "online",
        "reasoning_model": brain.reasoning_model,
        "router_model": brain.router_model
    }

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    loop = asyncio.get_running_loop()
    
    # Send initial welcome
    await websocket.send_json({"type": "message", "content": "Viora is online. How can I help you today?"})
    
    try:
        while True:
            # Expecting JSON: {"message": "..."}
            data = await websocket.receive_json()
            user_input = data.get("message", "").strip()
            
            if not user_input:
                continue
                
            # Handle termination keywords
            if user_input.lower() in ["exit", "quit", "bye"]:
                await websocket.send_json({"type": "message", "content": "Goodbye!"})
                await websocket.close()
                break
                
            status_updater = WSStatusUpdater(websocket, loop)
            
            # Fetch permanent context in background thread
            context = await loop.run_in_executor(
                executor, memory.get_relevant_context, user_input
            )
            
            # Run the LangGraph execution loop in a background thread to prevent blocking the event loop
            final_response = await loop.run_in_executor(
                executor,
                brain.run,
                user_input,
                15, # max_steps
                status_updater,
                context,
                memory
            )
            
            # Stream final agent response
            await websocket.send_json({"type": "message", "content": final_response})
            
            # Extract and log any facts learned to semantic memory in background
            await loop.run_in_executor(
                executor, memory.log_interaction, user_input, final_response
            )
            
    except WebSocketDisconnect:
        print("Viora WebSocket client disconnected.")
    except Exception as e:
        print(f"WebSocket Error: {e}")
        try:
            await websocket.send_json({"type": "error", "content": str(e)})
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    print("Starting Viora API Server on http://localhost:8000 ...")
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
