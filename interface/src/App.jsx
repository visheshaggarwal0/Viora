import React, { useState, useEffect, useRef } from 'react';

// Escape HTML helper for code blocks
const escapeHTML = (text) => {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
};

// Custom lightweight parser for code, lists, and bold markup
const formatMessageContent = (text) => {
  if (!text) return '';
  
  let formatted = text;

  // Code blocks: ```python ... ```
  formatted = formatted.replace(/```(?:[a-zA-Z0-9]+)?([\s\S]*?)```/g, (match, code) => {
    return `<pre style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08); padding: 12px; border-radius: 8px; font-family: 'Fira Code', monospace; font-size: 13px; overflow-x: auto; margin: 8px 0; color: #a5d6ff;"><code>${escapeHTML(code.trim())}</code></pre>`;
  });

  // Inline code: `var`
  formatted = formatted.replace(/`([^`\n]+)`/g, '<code style="background: rgba(255,255,255,0.06); padding: 2px 6px; border-radius: 4px; font-family: \'Fira Code\', monospace; font-size: 13px; color: #ff7b72;">$1</code>');

  // Bold markup: **text**
  formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

  // List bullets: - item
  formatted = formatted.replace(/^\s*-\s+(.+)$/gm, '<li style="margin-left: 20px; margin-bottom: 4px;">$1</li>');

  // Wrap list items in ul tags
  formatted = formatted.replace(/((?:<li style="[^"]+">.*?<\/li>\s*)+)/g, '<ul style="margin: 8px 0;">$1</ul>');

  // Replace line breaks (except within <pre> blocks)
  // Split by pre blocks first to avoid replacing breaks inside code
  const parts = formatted.split(/(<pre[\s\S]*?<\/pre>)/);
  formatted = parts.map(part => {
    if (part.startsWith('<pre')) return part;
    return part.replaceAll('\n', '<br />');
  }).join('');

  return formatted;
};

// Check if message response reports a screenshot
const parseScreenshotUrl = (text) => {
  if (!text) return null;
  const match = text.match(/Screenshot saved to (screenshots[\\/][a-zA-Z0-9_\-\.]+\.png)/i);
  if (match) {
    const filename = match[1].replace(/\\/g, '/').split('/').pop();
    return `http://localhost:8000/screenshots/${filename}`;
  }
  return null;
};

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [status, setStatus] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [logs, setLogs] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  
  const ws = useRef(null);
  const messagesEndRef = useRef(null);
  const logsEndRef = useRef(null);

  // Auto-scroll helpers
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages, isThinking]);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  // WebSocket Connection
  useEffect(() => {
    connectWebSocket();
    return () => {
      if (ws.current) ws.current.close();
    };
  }, []);

  const connectWebSocket = () => {
    setStatus('Connecting to Viora API...');
    ws.current = new WebSocket('ws://localhost:8000/chat');

    ws.current.onopen = () => {
      setIsConnected(true);
      setStatus('');
    };

    ws.current.onclose = () => {
      setIsConnected(false);
      setStatus('Disconnected from server. Reconnecting...');
      setTimeout(connectWebSocket, 3000);
    };

    ws.current.onerror = () => {
      setIsConnected(false);
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const timestamp = new Date().toLocaleTimeString();

      if (data.type === 'status') {
        // Intermediary thought/tool logs from LangGraph
        setIsThinking(true);
        setStatus(data.content);
        
        // Log tools or strategy shifts to timeline
        const isTool = data.content.includes('🔧');
        setLogs(prev => [...prev, {
          time: timestamp,
          content: data.content,
          type: isTool ? 'tool' : 'thinking'
        }]);
      } 
      else if (data.type === 'message') {
        // Final agent answer response
        setIsThinking(false);
        setStatus('');
        
        const screenshotUrl = parseScreenshotUrl(data.content);
        
        setMessages(prev => [...prev, {
          sender: 'viora',
          content: data.content,
          screenshot: screenshotUrl
        }]);

        setLogs(prev => [...prev, {
          time: timestamp,
          content: '✔ Task Execution Finished.',
          type: 'success'
        }]);
      }
      else if (data.type === 'error') {
        setIsThinking(false);
        setStatus('');
        setMessages(prev => [...prev, {
          sender: 'viora',
          content: `❌ Error: ${data.content}`,
          isError: true
        }]);
      }
    };
  };

  const sendMessage = (e) => {
    e.preventDefault();
    if (!inputValue.trim() || !isConnected) return;

    // Send user message
    ws.current.send(JSON.stringify({ message: inputValue }));
    
    setMessages(prev => [...prev, {
      sender: 'user',
      content: inputValue
    }]);

    setLogs(prev => [...prev, {
      time: new Date().toLocaleTimeString(),
      content: `User query: "${inputValue}"`,
      type: 'user'
    }]);

    setInputValue('');
    setIsThinking(true);
    setStatus('Evaluating intent...');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      {/* Premium Header */}
      <header className="app-header">
        <div className="brand-section">
          <div className="brand-logo"></div>
          <h1 className="brand-name">VIORA</h1>
        </div>
        <div className="status-badge">
          <div className={`status-dot ${isConnected ? '' : 'offline'}`}></div>
          {isConnected ? 'API Connected' : 'Connecting...'}
        </div>
      </header>

      {/* Main Workspace Layout */}
      <main className="app-container">
        {/* Left Side Execution Timeline Log */}
        <section className="sidebar-panel">
          <div className="panel-header">
            <span>Execution Logs</span>
            <span style={{ fontSize: '11px', background: 'rgba(255,255,255,0.06)', padding: '2px 8px', borderRadius: '10px', color: 'var(--text-secondary)' }}>
              Real-time
            </span>
          </div>
          <div className="panel-body">
            {logs.length === 0 ? (
              <div style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '40px 0', fontSize: '13px' }}>
                No active execution timeline logs.
              </div>
            ) : (
              logs.map((log, idx) => (
                <div key={idx} className={`log-item ${log.type}`}>
                  <div>
                    <span className="log-time">{log.time}</span>
                    <p className="log-content" style={{
                      color: log.type === 'tool' ? 'var(--accent-blue)' : 
                             log.type === 'success' ? 'var(--accent-green)' : 
                             log.type === 'user' ? 'var(--text-primary)' : 'var(--text-secondary)'
                    }}>
                      {log.content}
                    </p>
                  </div>
                </div>
              ))
            )}
            <div ref={logsEndRef} />
          </div>
        </section>

        {/* Right Side Chat panel */}
        <section className="chat-panel">
          <div className="messages-list">
            {messages.length === 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-secondary)' }}>
                <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: 'rgba(157, 78, 221, 0.1)', border: '1px solid rgba(157, 78, 221, 0.2)', marginBottom: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '20px' }}>
                  🔮
                </div>
                <h3>Welcome to Viora Agentic Interface</h3>
                <p style={{ fontSize: '13px', marginTop: '6px' }}>Type a chat message or a local execution command to start.</p>
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div key={idx} className={`message-row ${msg.sender === 'user' ? 'user' : 'agent'}`}>
                  <div className="message-bubble">
                    <div className="message-sender">{msg.sender === 'user' ? 'You' : 'Viora'}</div>
                    <div 
                      dangerouslySetInnerHTML={{ __html: formatMessageContent(msg.content) }} 
                      style={{ color: msg.isError ? '#ff5555' : 'inherit' }}
                    />
                    
                    {/* Render screenshots dynamically inline if present */}
                    {msg.screenshot && (
                      <div className="screenshot-container">
                        <img 
                          src={msg.screenshot} 
                          alt="Viora Action Capture" 
                          className="screenshot-preview"
                          onClick={() => window.open(msg.screenshot, '_blank')}
                        />
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}

            {/* Spinner indicator when agent is planning/executing tools */}
            {isThinking && (
              <div className="agent-thinking-bubble">
                <div className="spinner"></div>
                <span>{status || 'Viora is thinking...'}</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* User Input Section */}
          <form className="input-section" onSubmit={sendMessage}>
            <div className="input-wrapper">
              <input
                type="text"
                className="chat-input"
                placeholder={isConnected ? "Send a message or desktop command..." : "Waiting for API server..."}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                disabled={!isConnected}
              />
              <button type="submit" className="send-btn" disabled={!isConnected || !inputValue.trim()}>
                Send
              </button>
            </div>
          </form>
        </section>
      </main>
    </div>
  );
}

export default App;
