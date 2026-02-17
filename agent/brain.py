import os
from typing import List, Optional, Any
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from skills.tools_factory import get_viora_tools

load_dotenv()

class Brain:
    def __init__(self):
        self.provider = os.getenv("VIORA_MODEL_PROVIDER", "groq").lower()
        self.tools = get_viora_tools()
        self.llm = self._initialize_llm()
        self.history: List[BaseMessage] = [
            SystemMessage(content="You are Viora, a helpful personal agentic assistant. "
                                  "You can search the web, manage todos, and provide system info. "
                                  "Be concise, friendly, and proactive.")
        ]

    def _initialize_llm(self):
        if self.provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            return ChatGroq(
                temperature=0,
                model_name="llama-3.3-70b-versatile", # Defaulting to a strong model
                groq_api_key=api_key
            ).bind_tools(self.tools)
        elif self.provider == "gemini":
            api_key = os.getenv("GOOGLE_API_KEY")
            return ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0
            ).bind_tools(self.tools)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def think(self, prompt: str) -> BaseMessage:
        """Processes a prompt and returns the AI message (potentially with tool calls)."""
        self.history.append(HumanMessage(content=prompt))
        response = self.llm.invoke(self.history)
        self.history.append(response)
        return response

    def add_tool_result(self, tool_call_id: str, output: str):
        """Adds a tool result to the history."""
        from langchain_core.messages import ToolMessage
        self.history.append(ToolMessage(content=str(output), tool_call_id=tool_call_id))
