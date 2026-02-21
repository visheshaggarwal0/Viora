import os
from typing import List, Literal
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

class Router:
    def __init__(self):
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.categories = {
            "GREETING": "Simple conversation, greetings, or small talk. No tools needed.",
            "TODO": "Tasks related to managing todo lists (adding, listing).",
            "SYSTEM": "System-level operations like opening applications (notepad, chrome), listing files, reading/writing files, system status, volume control, and media control.",
            "BROWSER": "Web browser automation using Playwright (navigating, clicking, typing on web pages).",
            "DESKTOP": "Desktop automation using pywinauto (interacting with windows, mouse movements, keyboard typing).",
            "WEB_SEARCH": "Searching the internet for information.",
            "ALL": "General fallback when multiple tools from different categories might be needed."
        }

    def classify(self, query: str) -> str:
        """Classify the user query into a category."""
        categories_text = "\n".join([f"- {k}: {v}" for k, v in self.categories.items()])
        prompt = f"""Classify the user query into exactly ONE of the following categories:
{categories_text}

Query: "{query}"

Return ONLY the category name in uppercase."""
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            category = response.content.strip().upper()
            if category in self.categories:
                return category
            return "ALL"
        except Exception as e:
            print(f"DEBUG: Routing error: {e}")
            return "ALL"
