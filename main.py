import sys
import warnings

# Suppress pywinauto COM threading warning
warnings.filterwarnings("ignore", message="Revert to STA COM threading mode")

# Set pywinauto threading mode before it's imported
try:
    import pywinauto
    pywinauto.threaded_mode = 'STA'
except:
    pass

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
# tools_map still needs all tools to execute them when called
all_tools = get_viora_tools("ALL")
tools_map = {tool.name: tool for tool in all_tools}

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
        response = brain.think_after_tools()  # Use brain method to ensure tracking

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
            
            # Display token usage if using Groq
            if brain.provider == "groq":
                usage = brain.get_token_usage()
                if usage['last_response']:
                    last = usage['last_response']
                    session = usage['session']
                    category = usage.get('category', 'ALL')
                    console.print(
                        f"[dim]📂 Intent: [bold]{category}[/bold] | 💬 Tokens: {last['total']} "
                        f"(p: {last['prompt']}, c: {last['completion']}) | "
                        f"Session: {session['total']:,}[/dim]"
                    )
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {str(e)}")
            console.print("[italic]Viora recovered from the error and is ready for the next command.[/italic]")

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

@app.command()
def open(app_name: str):
    """Open a Windows application (e.g. notepad, chrome)."""
    from skills.system_tools import SystemTools
    console.print(f"[italic yellow]Opening {app_name}...[/italic yellow]")
    msg = SystemTools.open_application(app_name)
    console.print(f"[bold green]{msg}[/bold green]")

if __name__ == "__main__":
    app()
