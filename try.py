import typer
import os
from dotenv import load_dotenv
from rich.console import Console
from agent.brain import Brain
from agent.memory import Memory
from skills.tools_factory import get_viora_tools

load_dotenv()

app = typer.Typer()
console = Console()
brain = Brain()
memory = Memory()
tools_list = get_viora_tools()
tools_map = {tool.name: tool for tool in tools_list}

def run_agent_loop(user_input: str):
    """Handles the think-act-observe loop for Viora."""
    response = brain.think(user_input)
    
    # Process tool calls if any
    while response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]
            
            console.print(f"[italic yellow]Viora is using {tool_name}...[/italic yellow]")
            
            if tool_name in tools_map:
                try:
                    # LangChain tools take input in different ways; most use 'query' or just positional
                    # For our specific tools, they are simple functions
                    output = tools_map[tool_name].func(**tool_args)
                    brain.add_tool_result(tool_id, output)
                except Exception as e:
                    brain.add_tool_result(tool_id, f"Error: {str(e)}")
            else:
                brain.add_tool_result(tool_id, f"Tool {tool_name} not found.")
        
        # Get next response after tool results
        response = brain.llm.invoke(brain.history)
        brain.history.append(response)

    return response.content

@app.command()
def chat():
    """Start an agentic chat session with Viora."""
    console.print("[bold green]Viora is online. How can I help you today?[/bold green]")
    console.print("[italic]Type 'exit' to quit.[/italic]")
    
    while True:
        try:
            user_input = typer.prompt("You")
            if user_input.lower() in ["exit", "quit"]:
                break
                
            final_response = run_agent_loop(user_input)
            memory.log_interaction(user_input, final_response)
            
            console.print(f"[bold blue]Viora:[/bold blue] {final_response}")
        except KeyboardInterrupt:
            break

@app.command()
def todo(task: str):
    """Add a todo item."""
    from skills.organizer import Organizer
    org = Organizer()
    msg = org.add_todo(task)
    console.print(f"[bold green]{msg}[/bold green]")

@app.command()
def todos():
    """List all pending todos."""
    from skills.organizer import Organizer
    org = Organizer()
    console.print(org.list_todos())

if __name__ == "__main__":
    app()
