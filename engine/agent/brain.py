import os
import re
import json
from typing import List, Dict, Any, Optional, TypedDict, Annotated, Sequence
import operator
from dotenv import load_dotenv

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage,
    BaseMessage,
)
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from langgraph.graph import StateGraph, END

from skills.tools_factory import get_viora_tools
from config.config_loader import config

load_dotenv()
viora_console = Console()

class VioraState(TypedDict):
    messages: Annotated[list, operator.add]
    user_input: str
    context: str
    intent: str
    plan: str
    status: Any
    memory: Any
    final_response: str
    steps_taken: int
    requested_tools: List[str]

class Brain:
    def __init__(self):
        self.router_provider = config.router_provider.lower()
        self.reasoning_provider = config.reasoning_provider.lower()
        self.router_model = config.router_model
        self.reasoning_model = config.reasoning_model
        self.temperature = config.temperature
        self.max_steps = config.max_steps
        
        self.all_tools = get_viora_tools("ALL")
        self.tool_map = {tool.name: tool for tool in self.all_tools}
        self.should_exit = False
        
        self.router_llm = self._create_llm(model=self.router_model, tools=[], provider=self.router_provider)
        self.reasoning_llm = self._create_llm(model=self.reasoning_model, tools=self.all_tools, provider=self.reasoning_provider)

        # Generate a dynamic tool registry index
        self.tool_registry_str = "\n".join([f"- {t.name}: {t.description}" for t in self.all_tools if t.name != "request_tools"])
        self.history = []

        self.session_tokens = {"prompt": 0, "completion": 0, "total": 0}
        self.last_response_tokens = None
        
        self.graph = self._build_graph()

    # --- LLM Utils ---
    def _create_llm(self, model: str = "llama3.1", tools: List[Any] = None, provider: str = None):
        used_provider = provider if provider else self.reasoning_provider
        if used_provider == "ollama":
            if ":" in model:
                model_tag = model
            elif "llama" in model:
                model_tag = "llama3.1:8b-instruct-q4_K_M"
            elif "gemma" in model:
                model_tag = "gemma3:1b"
            else:
                model_tag = model or "phi3:mini"
            llm = ChatOllama(model=model_tag, temperature=self.temperature)
        elif used_provider == "groq":
            model_map = {
                "gemma3:1b": "gemma2-9b-it",
                "llama3.1": "llama-3.3-70b-versatile",
            }
            model_tag = model_map.get(model, model)
            llm = ChatGroq(model_name=model_tag, temperature=self.temperature)
        else:
            model_tag = model if model and not model.startswith("llama") and not model.startswith("gemma") else "gemini-1.5-flash"
            llm = ChatGoogleGenerativeAI(model=model_tag, temperature=self.temperature)
        return llm.bind_tools(tools) if tools else llm

    def _track_tokens(self, response):
        if hasattr(response, "response_metadata"):
            usage = response.response_metadata.get("token_usage", {})
            if usage:
                self.session_tokens["prompt"] += usage.get("prompt_tokens", 0)
                self.session_tokens["completion"] += usage.get("completion_tokens", 0)
                self.session_tokens["total"] += usage.get("total_tokens", 0)
                self.last_response_tokens = usage

    def get_token_usage(self):
        return {
            "session": self.session_tokens,
            "last": self.last_response_tokens,
            "provider": f"Router:{self.router_provider} | Reasoner:{self.reasoning_provider}",
        }

    # --- Tools Routing Utils ---
    def _get_relevant_tools(self, user_input: str) -> List[Any]:
        user_input = user_input.lower()
        matched_names = set(["request_tools", "terminate"])  # Core tools always available
        
        # Mapping keywords to specific tools
        keyword_map = {
            # TODO skills
            "todo": ["add_todo", "list_todos"],
            "task": ["add_todo", "list_todos"],
            "list": ["list_todos", "list_files"],
            
            # Windows skills
            "notepad": ["open_app"],
            "calc": ["open_app"],
            "open": ["open_app", "browser_open"],
            "time": ["get_time"],
            "clock": ["get_time"],
            "volume": ["set_volume", "mute_volume", "unmute_volume"],
            "vol": ["set_volume", "mute_volume", "unmute_volume"],
            "mute": ["mute_volume"],
            "unmute": ["unmute_volume"],
            "file": ["read_file", "write_file", "list_files"],
            "folder": ["list_files"],
            "directory": ["list_files"],
            "dir": ["list_files"],
            "write": ["write_file", "keyboard_type"],
            "read": ["read_file"],
            "screenshot": ["take_screenshot"],
            "screen": ["take_screenshot"],
            "clipboard": ["clipboard_set", "clipboard_get"],
            "copy": ["clipboard_set", "clipboard_get"],
            "paste": ["clipboard_set", "clipboard_get"],
            "window": ["window_list", "window_focus"],
            "focus": ["window_focus"],
            "click": ["mouse_click", "browser_click"],
            "type": ["keyboard_type", "browser_type"],
            "press": ["keyboard_press"],
            "keyboard": ["keyboard_type", "keyboard_press"],
            "mouse": ["mouse_click"],
            
            # Browser / Search skills
            "search": ["web_search", "google_nav"],
            "google": ["web_search", "google_nav"],
            "who is": ["web_search"],
            "what is": ["web_search"],
            "how to": ["web_search"],
            "browser": ["browser_open", "browser_click", "browser_type", "browser_get_text", "browser_map_elements"],
            "url": ["browser_open"],
            "http": ["browser_open"],
            "web": ["web_search", "browser_open", "browser_get_all_text"],
            "website": ["browser_open", "browser_get_all_text"],
            "scrape": ["browser_get_all_text", "browser_map_elements"],
            "selenium": ["browser_open", "browser_click", "browser_type", "browser_map_elements"],
        }
        
        for kw, tools in keyword_map.items():
            if kw in user_input:
                for t in tools:
                    matched_names.add(t)
                    
        # If very few tools matched (only core ones), add a few default helpers
        if len(matched_names) <= 2:
            matched_names.update(["web_search", "open_app", "take_screenshot"])
            
        return [t for t in self.all_tools if t.name in matched_names]

    # --- LANGGRAPH NODES ---
    
    def node_rules(self, state: VioraState):
        if state["status"]: state["status"].update("Viora is evaluating rules...")
        text = state["user_input"].lower().strip()
        
        if text in ["hi", "hello", "hey", "greetings", "good morning", "good evening", "good afternoon", "yo", "what's up", "sup", "sup?"]:
            resp = "Hello! How can I help you today?"
            return {"messages": [AIMessage(content=resp)], "final_response": resp, "intent": "RULES"}

        if re.fullmatch(r"(?:what is the\s+)?(?:time|clock)", text):
            resp = f"The current time is {self.tool_map['get_time'].invoke({})}"
            return {"messages": [AIMessage(content=resp)], "final_response": resp, "intent": "RULES"}
            
        match = re.fullmatch(r"open\s+([a-zA-Z0-9]+)", text)
        if match:
            resp = self.tool_map["open_app"].invoke({"app_name": match.group(1).strip()})
            return {"messages": [AIMessage(content=resp)], "final_response": resp, "intent": "RULES"}
            
        if re.fullmatch(r"set\s+volume\s+to\s+(\d+)", text):
            vol = re.search(r"(\d+)", text).group(1)
            resp = self.tool_map["set_volume"].invoke({"volume": int(vol)})
            return {"messages": [AIMessage(content=resp)], "final_response": resp, "intent": "RULES"}
            
        if text in ["mute", "mute system", "mute volume"]: 
            resp = self.tool_map["mute_volume"].invoke({})
            return {"messages": [AIMessage(content=resp)], "final_response": resp, "intent": "RULES"}
        if text in ["unmute", "unmute system", "unmute volume"]: 
            resp = self.tool_map["unmute_volume"].invoke({})
            return {"messages": [AIMessage(content=resp)], "final_response": resp, "intent": "RULES"}
        
        if text in ["list todos", "show tasks", "what are my todos", "list tasks", "todos"]:
            resp = f"Your tasks:\n{self.tool_map['list_todos'].invoke({})}"
            return {"messages": [AIMessage(content=resp)], "final_response": resp, "intent": "RULES"}
            
        search_match = re.fullmatch(r"(?:search for|google|duckduckgo)\s+(.+)", text)
        if search_match:
            resp = self.tool_map["web_search"].invoke({"query": search_match.group(1)})
            return {"messages": [AIMessage(content=resp)], "final_response": resp, "intent": "RULES"}
            
        return {"intent": "UNKNOWN"}

    def node_chatbot(self, state: VioraState):
        if state["status"]: state["status"].update("Viora is responding...")
        
        system_msg = """You are Viora, a helpful AI assistant.
- If the user wants to chat, ask questions, or make conversation, respond naturally.
- If the user wants to perform ANY command, system operation, file access, Selenium browser automation, or search the web, you MUST output exactly '[TRIGGER_ORCHESTRATOR]' followed by the task description."""
        
        conv_messages = [m for m in state["messages"] if not isinstance(m, SystemMessage)]
        current_context = [SystemMessage(content=system_msg)] + conv_messages
        if state["context"]:
            current_context.insert(-1, SystemMessage(content=state["context"]))
            
        response = self.router_llm.invoke(current_context)
        self._track_tokens(response)
        
        content = response.content.strip()
        
        if "[TRIGGER_ORCHESTRATOR]" in content:
            return {"intent": "TOOL"}
            
        if "terminate" in content.lower() and len(content) < 15:
            return {"messages": [AIMessage(content="I'm here! How can I help you?")], "final_response": "I'm here! How can I help you?", "intent": "CHAT"}
            
        if state.get("memory"):
            state["memory"].save_semantic_cache(state["user_input"], "CHAT", content)
            
        return {"messages": [response], "final_response": content, "intent": "CHAT"}

    def node_planner(self, state: VioraState):
        if state["status"]: state["status"].update("Viora is planning strategy...")
        planner_llm = self._create_llm(model=self.reasoning_model, tools=None, provider=self.reasoning_provider)
        prompt = SystemMessage(content="You are the Planner.\nGiven the conversation history and user request, create a step-by-step plan of action.\nFocus on tools and order. Respond ONLY with the Plan, starting with 'Plan:'. Do NOT call tools yourself.")
        
        current_context = list(state["messages"])
        if state["context"]:
            current_context.insert(-1, SystemMessage(content=state["context"]))
            
        try:
            plan_resp = planner_llm.invoke(current_context + [prompt])
            self._track_tokens(plan_resp)
            plan_msg = SystemMessage(content=f"Initial Plan generated by Reasoning Engine:\n{plan_resp.content}\n\nExecute this plan to fulfill the request.")
            
            panel = Panel(Markdown(plan_resp.content), title="🧠 [bold magenta]Viora Strategy[/bold magenta]", border_style="magenta", padding=(1, 2))
            if state["status"]: state["status"].update(panel)
            else: viora_console.print(panel)
            
            return {"messages": [plan_msg], "plan": plan_resp.content}
        except Exception as e:
            return {"plan": f"Error planning: {e}"}

    def node_reasoner(self, state: VioraState):
        current_tools = self._get_relevant_tools(state["user_input"])
        
        # Bind dynamically requested tools
        requested_names = state.get("requested_tools", [])
        for name in requested_names:
            if name in self.tool_map:
                current_tools.append(self.tool_map[name])
                
        # Deduplicate tools
        seen = set()
        dedup = []
        for t in current_tools:
            if t.name not in seen:
                dedup.append(t)
                seen.add(t.name)
                
        reasoner = self._create_llm(model=self.reasoning_model, tools=dedup, provider=self.reasoning_provider)
        
        reasoner_system_msg = f"""You are the Reasoning Engine of Viora, a desktop automation and helper assistant.
Your job is to execute the user's request using the bound tools.

DYNAMIC TOOL LOADING:
You only have a small subset of tools loaded in your active session. If you need to perform an action (like reading/writing a file, clicking, typing, taking a screenshot) and the corresponding tool is not currently bound, you MUST first request it using `request_tools(tool_names=["tool_name_here"])`! Do not attempt to guess or use the tool before requesting it.

Available tools you can request:
{self.tool_registry_str}

Be concise. Think step by step."""

        conv_messages = [m for m in state["messages"] if not isinstance(m, SystemMessage)]
        current_context = [SystemMessage(content=reasoner_system_msg)] + conv_messages
        if state["context"]:
            current_context.insert(-1, SystemMessage(content=state["context"]))
            
        try:
            response = reasoner.invoke(current_context)
            self._track_tokens(response)
        except Exception as e:
            err_str = str(e)
            match = re.search(r"<function=([a-zA-Z0-9_]+)>?(\{.*?\})?</function>", err_str)
            if match:
                tool_name = match.group(1)
                try: tool_args = json.loads(match.group(2) or "{}")
                except: tool_args = {}
                tool_id = f"call_manual_{tool_name}"
                response = AIMessage(content="", tool_calls=[{"name": tool_name, "args": tool_args, "id": tool_id}])
            else:
                return {"final_response": f"Reasoning error: {err_str}"}

        if response.tool_calls:
            return {"messages": [response]}
        else:
            if state.get("memory") and state.get("intent") not in ["CACHED_TOOL", "CACHED_CHAT", "CACHED_REASONER"]:
                state["memory"].save_semantic_cache(state["user_input"], "REASONER", response.content)
            return {"messages": [response], "final_response": response.content}

    def node_tools(self, state: VioraState):
        last_message = state["messages"][-1]
        
        # Determine if we should save this payload to the semantic cache
        tool_calls = getattr(last_message, "tool_calls", [])
        if state.get("memory") and tool_calls and state.get("intent") not in ["CACHED_TOOL", "CACHED_CHAT"]:
            state["memory"].save_semantic_cache(state["user_input"], "TOOL", tool_calls)
        
        new_requested = list(state.get("requested_tools", []))
        tool_results = []
        
        for call in tool_calls:
            tool_name = call["name"]
            tool_args = call["args"]
            tool_id = call["id"]
            
            # Fuzzy match override if tool_name is not direct match
            resolved_tool_name = tool_name
            if tool_name not in self.tool_map:
                import difflib
                matches = difflib.get_close_matches(tool_name, self.tool_map.keys(), n=1, cutoff=0.6)
                if matches:
                    resolved_tool_name = matches[0]
                    viora_console.print(f"⚠️ [yellow]Fuzzy matching tool call '{tool_name}' to '{resolved_tool_name}'[/yellow]")
                    
            # Intercept dynamic tool request calls
            if resolved_tool_name == "request_tools":
                import difflib
                requested = tool_args.get("tool_names", [])
                matched_tools = []
                feedback_msgs = []
                for name in requested:
                    if name in self.tool_map:
                        matched_tools.append(name)
                        feedback_msgs.append(f"'{name}' (exact match)")
                    else:
                        matches = difflib.get_close_matches(name, self.tool_map.keys(), n=1, cutoff=0.5)
                        if matches:
                            matched_name = matches[0]
                            matched_tools.append(matched_name)
                            feedback_msgs.append(f"'{matched_name}' (fuzzy matched from '{name}')")
                        else:
                            feedback_msgs.append(f"'{name}' (not found)")
                
                # Add to dynamic requested tools
                for t in matched_tools:
                    if t not in new_requested:
                        new_requested.append(t)
                        
                # Update arguments to reflect matched tools
                tool_args = {"tool_names": matched_tools}
                
            msg = f"🔧 [italic yellow]Using tool:[/italic yellow] [bold cyan]{resolved_tool_name}[/bold cyan]"
            if state["status"]: state["status"].update(msg)
            else: viora_console.print(msg)
                
            if resolved_tool_name not in self.tool_map:
                result = f"Tool {resolved_tool_name} not found."
            else:
                try: 
                    result = self.tool_map[resolved_tool_name].invoke(tool_args)
                    if resolved_tool_name == "request_tools":
                        result = f"Tool registry updated. Loaded: {', '.join(feedback_msgs)}.\nOriginal output: {result}"
                    elif result == "TERMINATE_SESSION":
                        self.should_exit = True
                        result = "DONE"
                except Exception as e: 
                    result = f"Tool error: {str(e)}"
            
            tool_results.append(ToolMessage(content=str(result), tool_call_id=tool_id))
            
        steps = state.get("steps_taken", 0) + 1
        
        if state.get("intent") == "CACHED_TOOL":
            return {"messages": tool_results, "steps_taken": steps, "requested_tools": new_requested, "final_response": "⚡ Executed perfectly from your Semantic Cache!"}
            
        return {"messages": tool_results, "steps_taken": steps, "requested_tools": new_requested}

    # --- GRAPH ARCHITECTURE ---
    def _route_after_rules(self, state: VioraState) -> str:
        if state["intent"] == "RULES": return "end"
        return "node_cache"

    def _route_after_cache(self, state: VioraState) -> str:
        if state["intent"] in ["CACHED_CHAT", "CACHED_REASONER"]: return "end"
        if state["intent"] == "CACHED_TOOL": return "node_tools" 
        return "node_chatbot"

    def _route_after_chatbot(self, state: VioraState) -> str:
        if state["intent"] == "TOOL": return "node_reasoner"
        return "end"

    def _route_after_reasoner(self, state: VioraState) -> str:
        if state.get("final_response"): return "end"
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            if state.get("steps_taken", 0) > 10:
                return "end" # Hard limit
            return "node_tools"
        return "end"

    def _route_after_tools(self, state: VioraState) -> str:
        if state.get("intent") == "CACHED_TOOL": return "end"
        return "node_reasoner"

    def _build_graph(self):
        builder = StateGraph(VioraState)
        
        # Nodes
        builder.add_node("node_rules", self.node_rules)
        builder.add_node("node_cache", self.node_cache)
        builder.add_node("node_chatbot", self.node_chatbot)
        builder.add_node("node_planner", self.node_planner)
        builder.add_node("node_reasoner", self.node_reasoner)
        builder.add_node("node_tools", self.node_tools)
        
        # Edges
        builder.set_entry_point("node_rules")
        builder.add_conditional_edges("node_rules", self._route_after_rules, {"end": END, "node_cache": "node_cache"})
        
        builder.add_conditional_edges("node_cache", self._route_after_cache, {"node_tools": "node_tools", "node_chatbot": "node_chatbot", "end": END})
        
        builder.add_conditional_edges("node_chatbot", self._route_after_chatbot, {"node_reasoner": "node_reasoner", "end": END})
        
        builder.add_conditional_edges("node_reasoner", self._route_after_reasoner, {"node_tools": "node_tools", "end": END})
        builder.add_conditional_edges("node_tools", self._route_after_tools, {"node_reasoner": "node_reasoner", "end": END})
        
        return builder.compile()

    def run(self, user_input: str, max_steps: int = 15, status=None, context: str = "", memory=None) -> str:
        self.last_response_tokens = None # Reset stale tokens from prior execution
        
        if len(self.history) > 14:
            self.history = self.history[-14:]
            
        initial_state = {
            "messages": self.history + [HumanMessage(content=user_input)],
            "user_input": user_input,
            "context": context,
            "intent": "",
            "plan": "",
            "status": status,
            "memory": memory,
            "final_response": "",
            "steps_taken": 0,
            "requested_tools": []
        }
        
        try:
            final_state = self.graph.invoke(initial_state)
            self.history = final_state["messages"]
            
            if final_state.get("final_response"):
                return final_state["final_response"]
            elif self.should_exit:
                return "Goodbye!"
            else:
                return "DONE"
        except Exception as e:
            return f"LangGraph Execution Error: {e}"
