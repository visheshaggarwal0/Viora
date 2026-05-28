from typing import Optional

class GeneralSkills:
    """General skills for the assistant, like greetings and session management."""

    def terminate(self) -> str:
        """Terminates the current assistant session."""
        return "TERMINATE_SESSION"

    def greeting(self, name: Optional[str] = None) -> str:
        """
        Sends a warm greeting to the user.
        Args:
            name: Optional name of the user to greet.
        """
        if name:
            return f"Hello {name}! How can I help you today?"
        return "Hi there! I'm Viora, your AI assistant. How can I help you today?"

    def request_tools(self, tool_names: list) -> str:
        """
        Request additional tools to be loaded into your active session if you need capabilities from other categories (e.g. windows_skills, todo_skills) during execution.
        Args:
            tool_names: List of tool names to load.
        """
        return f"Requested tools: {tool_names}. They are now bound and ready to use."
