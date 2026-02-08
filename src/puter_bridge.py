import streamlit.components.v1 as components
import os

def load_context():
    """Loads project documentation to form the system prompt."""
    try:
        # Load README
        if os.path.exists("README.md"):
            with open("README.md", "r", encoding="utf-8") as f:
                readme = f.read()
        else:
            readme = "No README found."
        
        # Load Risk Rules
        if os.path.exists("config/risk_rules.yaml"):
            with open("config/risk_rules.yaml", "r", encoding="utf-8") as f:
                rules = f.read()
        else:
            rules = "No risk rules found."
            
        context = f"""
        You are the AI Assistant for the 'AI-NIDS' (AI-based Intrusion Detection System) product.
        Your goal is to help users understand the system, how to run it, and what attacks it detects.
        
        --- SYSTEM CONFIGURATION ---
        {rules}
        
        --- DOCUMENTATION ---
        {readme}
        
        --- INSTRUCTIONS ---
        1. Answer based ONLY on the provided context.
        2. Be concise and professional.
        3. If asked about features not in the docs, say 'That is not currently implemented.'
        4. If the user asks 'How do I run this?', provide the command from the README.
        """
        # Escape backticks and quotes for JS string injection
        return context.replace("`", "\`").replace('"', '\\"').replace("\n", "\\n")
    except Exception as e:
        return f"Error loading context: {e}"

def render_chatbot():
    """Renders the HTML/JS Chatbot using Puter.js"""
    
    system_context = load_context()
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://js.puter.com/v2/"></script>
        <style>
            body {{ font-family: 'Helvetica Neue', sans-serif; background-color: #0e1117; color: white; margin: 0; padding: 10px; }}
            #chat-container {{ height: 400px; overflow-y: auto; border: 1px solid #41444e; border-radius: 10px; padding: 10px; background-color: #262730; margin-bottom: 10px; }}
            .message {{ margin-bottom: 10px; padding: 8px 12px; border-radius: 15px; max-width: 80%; word-wrap: break-word; }}
            .user {{ background-color: #00CC96; color: black; align-self: flex-end; margin-left: auto; text-align: right; }}
            .bot {{ background-color: #41444e; color: white; align-self: flex-start; margin-right: auto; }}
            #input-area {{ display: flex; gap: 10px; }}
            #user-input {{ flex-grow: 1; padding: 10px; border-radius: 5px; border: 1px solid #41444e; background-color: #0e1117; color: white; }}
            #send-btn {{ padding: 10px 20px; background-color: #00CC96; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }}
            #send-btn:hover {{ opacity: 0.8; }}
            .typing {{ font-style: italic; color: #a0a0a0; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div id="chat-container">
            <div class="message bot">Hello! I am your AI Security Analyst. Ask me anything about the AI-NIDS system.</div>
        </div>
        <div id="input-area">
            <input type="text" id="user-input" placeholder="Type your question..." onkeypress="handleKeyPress(event)">
            <button id="send-btn" onclick="sendMessage()">Send</button>
        </div>

        <script>
            const systemContext = "{system_context}";
            const chatContainer = document.getElementById('chat-container');
            const userInput = document.getElementById('user-input');

            function appendMessage(text, sender) {{
                const div = document.createElement('div');
                div.className = 'message ' + sender;
                div.textContent = text;
                chatContainer.appendChild(div);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }}

            function handleKeyPress(event) {{
                if (event.key === 'Enter') {{
                    sendMessage();
                }}
            }}

            async function sendMessage() {{
                const text = userInput.value.trim();
                if (!text) return;

                appendMessage(text, 'user');
                userInput.value = '';
                
                // Show typing indicator
                const typingDiv = document.createElement('div');
                typingDiv.className = 'message bot typing';
                typingDiv.textContent = 'Analyzing...';
                typingDiv.id = 'typing-indicator';
                chatContainer.appendChild(typingDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;

                try {{
                    // Combine system context with user query for RAG-like behavior
                    const fullPrompt = systemContext + "\\n\\nUser Query: " + text;
                    
                    const response = await puter.ai.chat(fullPrompt, {{ model: 'gpt-5-nano' }});
                    
                    // Remove typing indicator
                    const typingIndicator = document.getElementById('typing-indicator');
                    if (typingIndicator) typingIndicator.remove();
                    
                    if (response && response.message && response.message.content) {{
                        appendMessage(response.message.content, 'bot');
                    }} else if (typeof response === 'string') {{
                         appendMessage(response, 'bot');
                    }} else {{
                        appendMessage("Error: No response from AI.", 'bot');
                        console.log(response);
                    }}
                }} catch (error) {{
                    const typingIndicator = document.getElementById('typing-indicator');
                    if (typingIndicator) typingIndicator.remove();
                    appendMessage("Error connecting to AI Network: " + error, 'bot');
                }}
            }}
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=500)
