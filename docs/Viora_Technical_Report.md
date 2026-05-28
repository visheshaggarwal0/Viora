# Viora: An Autonomous Asynchronous Desktop & Web Agent
*Technical Architecture & Feature Summary for Academic Review*

## Abstract / Executive Summary
Viora is a next-generation autonomous AI agent engineered specifically to bridge the gap between deterministic software automation and dynamic LLM reasoning. Unlike traditional chatbots that rely on linear user-prompting, Viora functions as an autonomous **Asynchronous State Machine** orchestrated by LangGraph. It is capable of natively manipulating the host OS, structurally mapping obscured DOM layers in browser environments, extracting latent user intent, and mathematically bypassing computationally heavy reasoning steps through zero-token semantic vector caching.

---

## 🏗️ 1. Core Architecture: The Multi-Agent State Machine
Traditional React implementations suffer from "infinite execution loops" and high hallucination drift when errors occur. Viora fundamentally solves this by decoupling its logic into discrete routing nodes.
- **LangGraph Routing Mechanism**: Viora's cognitive engine is divided into strict structural domains (`Router`, `Planner`, `Reasoner`, `Tools`). 
- **Hybrid Multi-Agent Swarm**: Local LLMs (`gemma3:1b` via Ollama) act as lightning-fast, zero-cost gatekeepers handling Intent Classification and basic rules. Only upon complex validation does the graph delegate execution topology to a heavyweight reasoning node (`Llama-3.3-70b` via Groq) to plan Python callback sequences. This structural mitigation ensures peak token efficiency while maintaining enterprise-level reasoning density.

## 💾 2. Vector Persistence Engine (RAG)
Viora is equipped with true, persistent episodic memory replacing legacy JSON logs.
- **Background Fact Extraction**: Concurrently with the conversational thread, an isolated local LLM evaluates the chat context to silently extract and categorize permanent user variables (e.g., physical locations, software preferences), embedding them into a `viora_facts` ChromaDB table.
- **Semantic Threading**: Utilizing `all-MiniLM-L6-v2` embeddings, Viora matches incoming user queries against the top-K vectors in the database, invisibly sliding pertinent context blocks into her active pipeline before execution begins.

## ⚡ 3. The Topologic Zero-Token Semantic Cache
The majority of LLM architectures waste immense computational resources mathematically calculating repetitive tasks. Viora pioneers a zero-latency bypass routing system.
- **The Routine DB**: Successful Multi-Tool executions are vectorized and logged into a dedicated `viora_routines` table.
- **Graph Short-Circuiting**: Before engaging the Planner or Reasoner nodes, the graph queries the cache. If a sentence exhibits >0.95 semantic similarity to a past routine, Viora bypasses the LLMs entirely. She directly intercepts the cached Python object bounds and loops strictly through physical OS execution without burning a single LLM API token.

## 🌐 4. Heuristic DOM-Vision & Browser Manipulation
Relying on standard web-element selectors for automation yields a brittle agent heavily susceptible to minor frontend updates. Viora overrides this unreliability via Javascript-injection.
- **Dynamic Element Mapping**: Viora utilizes a custom payload injector loaded through Selenium. When a page is rendered, Viora strips all arbitrary div classes and visually maps interactive DOM elements with pinpoint `viora-id` mathematical coordinate tags. 
- **Anti-Bot Circumvention**: Leveraging native PyAutoGUI capabilities anchored by 1.0s physical UI-focus delays, Viora simulates exact human keystroke intervals (`0.05ms`), natively bypassing heavy React and security layer text-pasting blockers on platforms like WhatsApp or Amazon.

## 🖥️ 5. Native OS Hooking & Modularity
Viora operates outside the bounds of browser "sandboxes" or standard execution constraints.
- **Windows Subsystem Interface**: Viora has absolute native access to shell commands, executable (`.exe`) logic paths, clipboard access, physical volume manipulation, and file-writing via native python OS wrappers.
- **Global Path Execution**: Utilizing a compiled Registry Bypass Script (`.bat` wrapper anchored to a specific isolated `.venv`), Viora operates seamlessly globally on the host PC. 

---
### Research Paper Benchmarking Value
For academic context, Viora can be quantitatively validated against traditional agents via four metrics:
1. **Pass@1 Rates**: The ability to solve dynamic, multi-step execution tasks natively on the OS without human rescue.
2. **Time to First Action (TTFA)**: By isolating local routing logic from cloud-side logic bounds, Viora achieves sub-second tool engagement. 
3. **Graph Hallucination Rates**: Isolating the Reasoner block forces determinism to `< 5%` failure arrays.
4. **Token Cost Amortization**: Through the Semantic Cache implementation, consecutive execution workflows mathematically truncate operational processing costs down to 0.
