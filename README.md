# Viora 🤖

**Viora** is an advanced AI-powered automation assistant for Windows that combines natural language understanding with comprehensive browser and desktop control capabilities. Built with LangChain and powered by LLMs (Groq/Google), Viora can automate complex workflows, control applications, and assist with daily tasks.

## ✨ Features

### 🌐 Browser Automation (26 Tools)
- **Navigation & Control**: Navigate URLs, manage tabs, browser history
- **Form Handling**: Submit forms, select dropdowns, check checkboxes, upload files
- **Page Interaction**: Click, type, scroll, hover, right-click elements
- **Data Extraction**: Extract links, tables, text, count elements
- **Screenshots**: Capture full pages or specific elements

### 🖥️ Desktop Automation (21 Tools)
- **Window Management**: List, focus, minimize, maximize, close, resize, move windows
- **Mouse Control**: Move, click, double-click, drag-and-drop, scroll, right-click
- **Keyboard Control**: Press keys, hotkeys, type text
- **Screen Capture**: Screenshots, region capture, pixel color detection

### 🛠️ System Tools (17 Tools)
- **File Operations**: Read, write, list files
- **System Info**: CPU, RAM, battery status, OS info
- **Audio Control**: Volume control, mute/unmute
- **Media Control**: Play/pause, next/previous track
- **Clipboard**: Read/write clipboard content
- **App Launching**: Open applications with smart aliases
- **Web Tools**: Read and summarize web pages
- **Search**: DuckDuckGo web search

### 📝 Productivity Tools
- **Todo Management**: Add, list, complete tasks
- **Memory**: Store and retrieve notes
- **Journal**: Track daily activities

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Windows OS
- API keys for Groq or Google AI

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/viora.git
cd viora
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers**
```bash
playwright install chromium
```

4. **Set up environment variables**
Create a `.env` file in the project root:
```env
VIORA_MODEL_PROVIDER=groq  # or "google"
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here  # if using Google
```

5. **Run Viora**
```bash
python main.py chat
```

## 💡 Usage Examples

### Browser Automation
```
"Navigate to google.com and search for Python tutorials"
"Open example.com, extract all links, and take a screenshot"
"Fill out the form on this page with my information"
"Open 3 tabs with different URLs and list them"
```

### Desktop Automation
```
"List all open windows"
"Focus the Chrome window and maximize it"
"Move mouse to (500, 300) and click"
"Drag from (100, 100) to (500, 500)"
"Type 'Hello World' and press Enter"
```

### System Control
```
"Set volume to 50%"
"What's my system status?"
"Open Calculator"
"Take a screenshot"
"Read the content of example.txt"
```

### Productivity
```
"Add 'Buy groceries' to my todo list"
"What are my todos?"
"Remember that the meeting is at 3 PM"
```

## 📁 Project Structure

```
viora/
├── agent/
│   ├── brain.py          # Core LLM agent logic
│   └── memory.py         # Memory management
├── skills/
│   ├── browser_tools.py  # Browser automation (Playwright)
│   ├── desktop_tools.py  # Desktop automation (pywinauto/PyAutoGUI)
│   ├── system_tools.py   # System utilities
│   ├── web_tools.py      # Web scraping
│   ├── web_search.py     # DuckDuckGo search
│   ├── organizer.py      # Todo/journal management
│   └── tools_factory.py  # Tool registration
├── data/
│   ├── memory.json       # Persistent memory storage
│   └── organizer.json    # Todo/journal storage
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── .env                  # Environment variables (create this)
```

## 🔧 Configuration

### Model Providers

**Groq (Default)**
- Fast inference with Llama models
- Free tier available
- Get API key: https://console.groq.com

**Google AI**
- Gemini models
- Get API key: https://makersuite.google.com/app/apikey

Set your provider in `.env`:
```env
VIORA_MODEL_PROVIDER=groq  # or "google"
```

## 🛡️ Safety Features

- **PyAutoGUI Failsafe**: Move mouse to top-left corner to abort automation
- **Error Recovery**: Robust error handling prevents crashes
- **Browser Isolation**: Each browser session is sandboxed

## 📊 Tool Count

**Total: 64 Tools**
- Browser Automation: 26 tools
- Desktop Automation: 21 tools
- System & Utilities: 17 tools

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- Browser automation powered by [Playwright](https://playwright.dev/)
- Desktop automation using [pywinauto](https://github.com/pywinauto/pywinauto) and [PyAutoGUI](https://github.com/asweigart/pyautogui)
- LLM providers: [Groq](https://groq.com/) and [Google AI](https://ai.google.dev/)

## ⚠️ Disclaimer

Viora is a powerful automation tool. Use responsibly and ensure you have proper permissions before automating tasks on websites or systems you don't own.

---

**Made with ❤️ for automation enthusiasts**
