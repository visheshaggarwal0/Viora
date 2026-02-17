from langchain_core.tools import StructuredTool
from skills.web_search import WebSearch
from skills.organizer import Organizer
from skills.system_tools import SystemTools

def get_viora_tools():
    search = WebSearch()
    org = Organizer()
    sys = SystemTools()

    return [

        StructuredTool.from_function(
            name="web_search",
            func=search.run,
            description="Search the web for current events or information."
        ),

        StructuredTool.from_function(
            name="add_todo",
            func=org.add_todo,
            description="Add a task to the todo list."
        ),

        StructuredTool.from_function(
            name="list_todos",
            func=org.list_todos,
            description="List all todo tasks."
        ),

        StructuredTool.from_function(
            name="get_time",
            func=sys.get_time,
            description="Get current date and time."
        ),

        StructuredTool.from_function(
            name="get_os_info",
            func=sys.get_os_info,
            description="Get operating system information."
        ),

        StructuredTool.from_function(
            name="open_app",
            func=sys.open_application,
            description="Open an application on Windows (e.g., 'notepad', 'calc')."
        ),

        StructuredTool.from_function(
            name="list_files",
            func=sys.list_files,
            description="List files and directories in a given path (default is current directory)."
        ),

        StructuredTool.from_function(
            name="read_file",
            func=sys.read_file,
            description="Read the content of a text file."
        ),

        StructuredTool.from_function(
            name="write_file",
            func=sys.write_file,
            description="Write content to a file. Defaults to overwrite ('w'), use mode='a' to append."
        )

    ]
