import os
from typing import List, Optional, Any
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage, ToolMessage
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from skills.tools_factory import get_viora_tools
from agent.router import Router

load_dotenv()

class Brain:
    def __init__(self):
        self.provider = os.getenv("VIORA_MODEL_PROVIDER", "groq").lower()
        self.router = Router()
        self.history: List[BaseMessage] = [
            SystemMessage(content="You are Viora, a helpful personal agentic assistant. "
                                  "You can search the web, manage todos, and provide system info. "
                                  "Be concise, friendly, and proactive.")
        ]
        # Token usage tracking
        self.session_tokens = {"prompt": 0, "completion": 0, "total": 0}
        self.last_response_tokens = None
        self.current_category = "ALL"

    def _get_llm_for_category(self, category: str):
        """Returns an LLM bound with tools for a specific category."""
        tools = get_viora_tools(category)
        
        if self.provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            llm = ChatGroq(
                temperature=0,
                model_name="llama-3.1-8b-instant",
                groq_api_key=api_key
            )
            return llm.bind_tools(tools) if tools else llm
        elif self.provider in ["gemini", "google"]:
            api_key = os.getenv("GOOGLE_API_KEY")
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0
            )
            return llm.bind_tools(tools) if tools else llm
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def think(self, prompt: str) -> BaseMessage:
        """Processes a prompt and returns the AI message."""
        self.history.append(HumanMessage(content=prompt))
        
        # Classify intent and get specialized LLM
        self.current_category = self.router.classify(prompt)
        llm = self._get_llm_for_category(self.current_category)
        
        response = llm.invoke(self.history)
        self.history.append(response)
        
        # Track token usage
        self._track_tokens(response)
        
        return response

    def think_after_tools(self) -> BaseMessage:
        """Gets next response after tool results, using the current category LLM."""
        llm = self._get_llm_for_category(self.current_category)
        response = llm.invoke(self.history)
        self.history.append(response)
        
        # Track token usage
        self._track_tokens(response)
        
        return response
    
    def _track_tokens(self, response: BaseMessage):
        """Extract and track token usage from response metadata."""
        if hasattr(response, 'response_metadata') and response.response_metadata:
            usage = response.response_metadata.get('token_usage', {})
            if usage:
                prompt_tokens = usage.get('prompt_tokens', 0)
                completion_tokens = usage.get('completion_tokens', 0)
                total_tokens = usage.get('total_tokens', 0)
                
                # Update session totals
                self.session_tokens['prompt'] += prompt_tokens
                self.session_tokens['completion'] += completion_tokens
                self.session_tokens['total'] += total_tokens
                
                # Store last response tokens
                self.last_response_tokens = {
                    'prompt': prompt_tokens,
                    'completion': completion_tokens,
                    'total': total_tokens
                }
    
    def get_token_usage(self) -> dict:
        """Get current session token usage statistics."""
        return {
            'session': self.session_tokens.copy(),
            'last_response': self.last_response_tokens.copy() if self.last_response_tokens else None,
            'provider': self.provider,
            'model': self._get_model_name(),
            'category': self.current_category
        }
    
    def _get_model_name(self) -> str:
        """Get the current model name."""
        if self.provider == "groq":
            return "llama-3.1-8b-instant"
        elif self.provider in ["gemini", "google"]:
            return "gemini-1.5-flash"
        return "unknown"

    def add_tool_result(self, tool_call_id: str, output: str):
        """Adds a tool result to the history."""
        self.history.append(ToolMessage(content=str(output), tool_call_id=tool_call_id))
