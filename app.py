import streamlit as st
import requests
import json
from datetime import datetime
import uuid
import time

# Page configuration
st.set_page_config(
    page_title="Syncoria Odoo Assistant",
    page_icon="images/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ChatGPT-like interface
st.markdown("""
<style>
    /* Global styles */
    .stApp {
        background-color: #f0f0f0;
        height: 100vh;
        overflow: hidden;
    }
    
    /* Main content area */
    .main {
        height: 100vh;
        display: flex;
        flex-direction: column;
        padding-bottom: 0 !important;
    }
    
    /* Remove default streamlit footer and extra spacing */
    .stApp > footer {
        display: none;
    }
    
    /* Hide streamlit menu and header */
    .css-1rs6os, .css-17ziqus, .css-1v0mbdj {
        display: none;
    }
    
    /* Hide default streamlit elements */
    .stDeployButton {display: none;}
    .stDecoration {display: none;}
    header[data-testid="stHeader"] {display: none;}
    
    /* Remove default streamlit padding */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: none !important;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }
    
    /* Remove extra spacing from streamlit elements */
    .element-container {
        margin-bottom: 0 !important;
    }
    
    .stForm {
        margin-bottom: 0 !important;
    }
    
    /* Hide any extra content below the app */
    .stApp::after {
        display: none;
    }
    
    /* Ensure no extra margins on main content */
    [data-testid="stAppViewContainer"] {
        padding-bottom: 0 !important;
    }
    
    /* Hide any extra content below the app */
    .stApp::after {
        display: none;
    }
    
    /* Ensure no extra margins on main content */
    [data-testid="stAppViewContainer"] {
        padding-bottom: 0 !important;
    }
    
    /* Sidebar styles */
    .css-1d391kg {
        background-color: #875A7B;
        color: white;
    }
    
    .sidebar-header {
        padding: 1rem;
        border-bottom: 1px solid #2d2d2d;
        margin-bottom: 1rem;
    }
    
    .new-chat-btn {
        background-color: #875A7B;
        border: 1px solid #A0729A;
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 1rem;
        width: 100%;
        font-size: 14px;
    }
    
    .new-chat-btn:hover {
        background-color: #A0729A;
    }
    
    .chat-session {
        background-color: transparent;
        border: none;
        color: #ececec;
        padding: 0.75rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 0.5rem;
        width: 100%;
        text-align: left;
        font-size: 14px;
    }
    
    .chat-session:hover {
        background-color: #A0729A;
    }
    
    .chat-session.active {
        background-color: #7C7BAD;
    }
    
    .chat-title {
        color: #a0729a;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .chat-subtitle {
        color: #8e8ea0;
        font-size: 12px;
    }
    
    .header-container {
        background-color: #875A7B;
        padding: 1rem 2rem;
        border-bottom: 1px solid #A0729A;
        text-align: center;
        position: sticky;
        top: 0;
        z-index: 100;
        margin: 0;
    }
    
    .header-title {
        color: white;
        font-size: 20px;
        font-weight: 700;
        margin: 0;
    }
    
    .session-id {
        color: rgba(255, 255, 255, 0.8);
        font-size: 12px;
        font-family: monospace;
        margin-top: 0.5rem;
    }
    
    .main-container {
        display: flex;
        flex-direction: column;
        height: 100vh;
        margin: 0;
        padding: 0;
    }
    
    .chat-container {
        flex: 1;
        max-width: 900px;
        margin: 0 auto;
        padding: 0 1rem;
        width: 100%;
        overflow-y: auto;
        height: calc(100vh - 140px);
        padding-bottom: 120px;
    }
    
    /* Chat messages */
    .message-container {
        margin-bottom: 1.5rem;
        display: flex;
        width: 100%;
    }
    
    .user-message {
        background: linear-gradient(135deg, #875A7B 0%, #A0729A 100%);
        color: white;
        border-radius: 18px 18px 4px 18px;
        padding: 1rem 1.25rem;
        max-width: 70%;
        margin-left: auto;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        position: relative;
    }
    
    .assistant-message {
        background-color: white;
        border-radius: 18px 18px 18px 4px;
        padding: 1rem 1.25rem;
        max-width: 75%;
        margin-right: auto;
        position: relative;
        border: 1px solid #e5e5e5;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .message-role {
        font-weight: 600;
        font-size: 13px;
        margin-bottom: 0.5rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .user-message .message-role {
        color: rgba(255,255,255,0.9);
    }
    
    .assistant-message .message-role {
        color: #875A7B;
    }
    
    .message-content {
        font-size: 15px;
        line-height: 1.6;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .user-message .message-content {
        color: white !important;
    }
    
    .assistant-message .message-content {
        color: #343541 !important;
    }
    
    .message-content strong {
        font-weight: 600;
    }
    
    .message-content em {
        font-style: italic;
    }
    
    .message-content code {
        background-color: rgba(0,0,0,0.1);
        padding: 2px 4px;
        border-radius: 3px;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 0.9em;
    }
    
    .message-content pre {
        background-color: rgba(0,0,0,0.1);
        padding: 12px;
        border-radius: 8px;
        overflow-x: auto;
        margin: 12px 0;
    }
    
    .message-content pre code {
        background-color: transparent;
        padding: 0;
        font-size: 0.9em;
        white-space: pre;
    }
    
    .user-message .message-content code {
        background-color: rgba(255,255,255,0.2);
    }
    
    .user-message .message-content pre {
        background-color: rgba(255,255,255,0.2);
    }
    
    .message-content ul, .message-content ol {
        margin: 8px 0;
        padding-left: 20px;
    }
    
    .message-content li {
        margin: 4px 0;
        line-height: 1.5;
    }
    
    .message-content h1, .message-content h2, .message-content h3 {
        margin: 16px 0 8px 0;
        font-weight: 600;
    }
    
    .message-content h1 {
        font-size: 1.4em;
    }
    
    .message-content h2 {
        font-size: 1.2em;
    }
    
    .message-content h3 {
        font-size: 1.1em;
    }
    
    .message-content a {
        color: #1a73e8;
        text-decoration: none;
    }
    
    .message-content a:hover {
        text-decoration: underline;
    }
    
    .user-message .message-content a {
        color: rgba(255,255,255,0.9);
    }
    
    .message-content p {
        margin: 0.5em 0;
    }
    
    .message-content p:first-child {
        margin-top: 0;
    }
    
    .message-content p:last-child {
        margin-bottom: 0;
    }
    
    .message-timestamp {
        font-size: 11px;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .user-timestamp {
        color: rgba(255,255,255,0.7);
        text-align: right;
    }
    
    .assistant-timestamp {
        color: #8e8ea0;
        text-align: left;
        padding-left: 2rem;
        padding-right: 4rem;
        margin-top: 0;
    }
    
    .chart-container {
        margin: 1rem 0;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        background-color: white;
        padding: 8px;
    }
    
    /* Style Streamlit image within chart container */
    .chart-container .stImage {
        border-radius: 8px;
    }
    
    .chart-container .stImage > div {
        border-radius: 8px;
    }
    
    .chart-container .stImage img {
        border-radius: 8px;
    }
    
    .chart-decision {
        background: linear-gradient(135deg, #fff9e6, #fef3cd);
        border: 1px solid #ffd700;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.75rem 0;
        font-size: 13px;
        color: #b45309;
        border-left: 4px solid #ffa500;
    }
    
    .chart-decision strong {
        color: #8b4513;
        font-weight: 600;
    }
    
    .thinking-message {
        opacity: 0.8;
        font-style: italic;
    }
    
    .thinking-dots {
        display: inline-block;
        animation: thinking 1.5s infinite;
    }
    
    @keyframes thinking {
        0%, 20% { opacity: 0; }
        50% { opacity: 1; }
        100% { opacity: 0; }
    }
    
    /* Welcome message styling */
    .welcome-message {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 18px 18px 18px 4px;
        padding: 1.5rem;
        max-width: 75%;
        margin: 2rem auto 2rem 0;
        border: 1px solid #A0729A;
        box-shadow: 0 2px 12px rgba(135, 90, 123, 0.08);
    }
    
    .welcome-message .message-role {
        color: #875A7B;
        font-size: 14px;
        margin-bottom: 0.75rem;
    }
    
    .welcome-message .message-content {
        color: #495057;
        font-size: 15px;
        line-height: 1.6;
    }
    
    /* Input area */
    .input-container {
        background-color: #f8f9fa;
        border-top: 1px solid #A0729A;
        padding: 1.5rem;
        position: fixed;
        bottom: 0;
        left: 21rem;
        right: 0;
        z-index: 1000;
        box-shadow: 0 -2px 10px rgba(135, 90, 123, 0.05);
        margin: 0;
    }
    
    .input-wrapper {
        max-width: 900px;
        margin: 0 auto;
        position: relative;
        padding: 0;
    }
    
    .stTextInput > div > div > input {
        background-color: #f8f9fa !important;
        border: 2px solid #e9ecef !important;
        border-radius: 25px !important;
        padding: 14px 20px !important;
        font-size: 15px !important;
        outline: none !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        height: 48px !important;
        box-sizing: border-box !important;
        color: #343541 !important;
        line-height: 1.4 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #875A7B !important;
        background-color: white !important;
        box-shadow: 0 0 0 3px rgba(135, 90, 123, 0.1) !important;
    }
    
    /* Additional input styling */
    .stTextInput > div {
        position: relative !important;
    }
    
    .stTextInput > div > div {
        position: relative !important;
    }
    
    .stTextInput label {
        display: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #8e8ea0 !important;
        opacity: 1 !important;
    }
    
    /* Form button styling */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #875A7B, #A0729A) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 12px 24px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(135, 90, 123, 0.2) !important;
        height: 48px !important;
        width: 100% !important;
        margin-top: 0 !important;
    }
    
    .stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #A0729A, #7C7BAD) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(135, 90, 123, 0.3) !important;
    }
    
    .stFormSubmitButton > button:focus {
        box-shadow: 0 0 0 3px rgba(135, 90, 123, 0.2) !important;
    }
    
    /* Align form elements */
    .stForm > div {
        gap: 0.5rem !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Ensure the input form container doesn't create extra space */
    .input-container .stForm {
        background: transparent;
        border: none;
        padding: 0;
        margin: 0;
    }
    
    .send-button {
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        background: linear-gradient(135deg, #875A7B, #A0729A);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 8px 16px;
        cursor: pointer;
        font-size: 13px;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(135, 90, 123, 0.2);
    }
    
    .send-button:hover {
        background: linear-gradient(135deg, #A0729A, #7C7BAD);
        transform: translateY(-50%) translateY(-1px);
        box-shadow: 0 4px 8px rgba(135, 90, 123, 0.3);
    }
    
    .send-button:disabled {
        background: linear-gradient(135deg, #d0d0d0, #bbb);
        cursor: not-allowed;
        transform: translateY(-50%);
        box-shadow: none;
    }
    
    /* Chat content styling */
    .chat-messages {
        padding: 1rem 0 2rem 0;
        min-height: auto;
    }
    
    /* Ensure proper spacing for messages */
    .message-container:first-child {
        margin-top: 1rem;
    }
    
    .message-container:last-child {
        margin-bottom: 2rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-container {
            padding: 1rem;
        }
        
        .chat-container {
            padding: 0 0.5rem;
            height: calc(100vh - 120px);
            padding-bottom: 100px;
        }
        
        .user-message, .assistant-message, .welcome-message {
            max-width: 85%;
        }
        
        .input-container {
            padding: 0rem;
            left: 0 !important;
            right: 0;
        }
        
        .message-container {
            margin-bottom: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .user-message, .assistant-message, .welcome-message {
            max-width: 95%;
        }
        
        .header-title {
            font-size: 18px;
        }
        
        .stTextInput > div > div > input {
            padding: 12px 50px 12px 16px;
            font-size: 14px;
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    
    /* Override Streamlit's sticky form styling */
    .st-emotion-cache-r421ms {
        border: 1px solid rgba(49, 51, 63, 0.2);
        border-radius: 0.5rem;
        padding: calc(1em - 1px);
        position: sticky;
        bottom: 0;
    }
    
    /* Sidebar toggle button */
    .sidebar-toggle {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1001;
        background: #875A7B;
        color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        cursor: pointer;
        font-size: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .sidebar-toggle:hover {
        background: #A0729A;
        transform: scale(1.1);
    }
    
    /* Hide sidebar when toggled */
    .sidebar-hidden .css-1d391kg {
        margin-left: -21rem;
        transition: margin-left 0.3s ease;
    }
    
    .sidebar-hidden .input-container {
        left: 0 !important;
        transition: left 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar toggle button
st.markdown("""
<button class="sidebar-toggle" onclick="toggleSidebar()">☰</button>
<script>
function toggleSidebar() {
    document.querySelector('.stApp').classList.toggle('sidebar-hidden');
}
</script>
""", unsafe_allow_html=True)

# API base URL
API_BASE_URL = "http://52.72.249.33:8000"

# Initialize session state
if 'current_session_id' not in st.session_state:
    st.session_state.current_session_id = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'sessions' not in st.session_state:
    st.session_state.sessions = {}

def create_new_session():
    """Create a new chat session"""
    try:
        response = requests.get(f"{API_BASE_URL}/session")
        if response.status_code == 200:
            session_data = response.json()
            session_id = session_data['session_id']
            st.session_state.current_session_id = session_id
            st.session_state.chat_history = []
            st.session_state.sessions[session_id] = {
                'created_at': session_data['created_at'],
                'title': f"New chat {len(st.session_state.sessions) + 1}"
            }
            return session_id
        else:
            st.error(f"Failed to create session: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Failed to create new session: {e}")
        return None

def get_chat_history(session_id):
    """Get chat history for a session"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/history",
            json={"session_id": session_id, "limit": 50}
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get chat history: {response.status_code}")
    except Exception as e:
        st.error(f"Failed to get chat history: {e}")
    return None

def send_query(query, session_id):
    """Send query to the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={
                "query": query,
                "session_id": session_id,
                "include_debug": False
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to send query: {response.status_code}")
    except Exception as e:
        st.error(f"Failed to send query: {e}")
    return None

def format_timestamp(timestamp_str):
    """Format timestamp for display"""
    if not timestamp_str:
        return ""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime("%m/%d/%Y %H:%M")
    except:
        return timestamp_str

def process_markdown(content):
    """Convert markdown to HTML"""
    import re
    import html
    
    # Escape HTML entities first to prevent XSS, but preserve line breaks
    content = html.escape(content)
    
    # Handle code blocks first (to avoid interference with other formatting)
    content = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', content, flags=re.DOTALL)
    content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)
    
    # Handle bold and italic text
    content = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', content)  # Bold + italic
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)  # Bold
    content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)  # Italic
    
    # Handle links
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', content)
    
    # Handle headers
    content = re.sub(r'^### (.*$)', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.*$)', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.*$)', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    
    # Handle lists (both unordered and ordered)
    lines = content.split('\n')
    processed_lines = []
    in_ul = False
    in_ol = False
    
    for line in lines:
        if re.match(r'^- ', line):
            if in_ol:
                processed_lines.append('</ol>')
                in_ol = False
            if not in_ul:
                processed_lines.append('<ul>')
                in_ul = True
            processed_lines.append(f'<li>{line[2:]}</li>')
        elif re.match(r'^\d+\. ', line):
            if in_ul:
                processed_lines.append('</ul>')
                in_ul = False
            if not in_ol:
                processed_lines.append('<ol>')
                in_ol = True
            # Extract content after number and dot
            list_content = re.sub(r'^\d+\. ', '', line)
            processed_lines.append(f'<li>{list_content}</li>')
        else:
            if in_ul:
                processed_lines.append('</ul>')
                in_ul = False
            if in_ol:
                processed_lines.append('</ol>')
                in_ol = False
            processed_lines.append(line)
    
    if in_ul:
        processed_lines.append('</ul>')
    if in_ol:
        processed_lines.append('</ol>')
    
    content = '\n'.join(processed_lines)
    
    # Handle line breaks (but preserve existing HTML)
    content = re.sub(r'\n(?!<)', '<br>', content)
    
    return content

def get_session_title(session_id):
    """Get a meaningful title for the session"""
    if session_id in st.session_state.sessions:
        return st.session_state.sessions[session_id]['title']
    return f"Chat {session_id[:8]}"

# Sidebar
with st.sidebar:
    st.image("images/logo.png", width=100)
    st.markdown("""
    <div class="sidebar-header">
        <div class="chat-title">Syncoria Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    
    # New chat button
    if st.button("➕ New Chat", key="new-chat-trigger", help="Create a new chat session"):
        create_new_session()
        st.rerun()
    
    # Chat sessions
    if st.session_state.sessions:
        st.markdown('<div class="chat-title">Recent Chats</div>', unsafe_allow_html=True)
        
        for session_id, session_info in st.session_state.sessions.items():
            is_active = session_id == st.session_state.current_session_id
            
            if st.button(
                session_info['title'],
                key=f"session_{session_id}",
                help=f"Created: {format_timestamp(session_info['created_at'])}",
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_session_id = session_id
                # Load chat history
                history_data = get_chat_history(session_id)
                if history_data:
                    # Process the chat history to handle the new API structure
                    processed_messages = []
                    for msg in history_data.get('messages', []):
                        if msg['role'].lower() == 'user':
                            # For user messages, use either 'query' or 'content'
                            processed_messages.append({
                                'role': 'user',
                                'content': msg.get('query', msg.get('content', '')),
                                'timestamp': msg.get('timestamp', '')
                            })
                        else:
                            # For assistant messages
                            processed_messages.append({
                                'role': 'assistant',
                                'content': msg.get('content', ''),
                                'analysis': msg.get('analysis', msg.get('content', '')),
                                'chart_generated': bool(msg.get('chart_s3_url')),
                                'chart_s3_url': msg.get('chart_s3_url'),
                                'chart_decision_reason': msg.get('chart_decision_reason'),
                                'timestamp': msg.get('timestamp', '')
                            })
                    st.session_state.chat_history = processed_messages
                st.rerun()

# Main content area

# Create session if none exists (BEFORE rendering header)
if not st.session_state.current_session_id:
    create_new_session()

# Header with session ID
header_html = f"""
<div class="header-container">
    <h1 class="header-title">Syncoria Odoo Assistant</h1>
"""
if st.session_state.current_session_id:
    header_html += f'<div class="session-id">Session ID: {st.session_state.current_session_id}</div>'
header_html += "</div>"

st.markdown(header_html, unsafe_allow_html=True)

# Chat messages display
if st.session_state.current_session_id:
    # st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.markdown("""
        <div class="message-container">
            <div class="welcome-message">
                <div class="message-role">Syncoria Assistant</div>
                <div class="message-content">
                    Hello! I'm your Syncoria Odoo Assistant. I can help you analyze your business data, 
                    generate insights, and create visualizations. What would you like to explore today?
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    for message in st.session_state.chat_history:
        st.markdown('<div class="message-container">', unsafe_allow_html=True)
        
        if message['role'] == 'user':
            user_content = process_markdown(message['content'])
            st.markdown(f"""
            <div class="user-message">
                <div class="message-role">You</div>
                <div class="message-content">{user_content}</div>
                <div class="message-timestamp user-timestamp">{format_timestamp(message.get('timestamp', ''))}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Check if this is a thinking message
            is_thinking = message.get('is_thinking', False)
            message_class = "assistant-message"
            if is_thinking:
                message_class += " thinking-message"
            
            # Get content and prepare for HTML rendering
            content = message.get('analysis', message.get('content', ''))
            
            # Process markdown content
            content = process_markdown(content)
            
            if is_thinking:
                content = f'{content}<span class="thinking-dots">...</span>'
            
            # Build the message HTML (without timestamp - we'll handle that separately)
            message_html = f"""
            <div class="{message_class}">
                <div class="message-role">Syncoria Assistant</div>
                <div class="message-content">{content}</div>
            </div>
            """
            
            # Display the message content
            st.markdown(message_html, unsafe_allow_html=True)
            
            # Handle timestamp separately for non-thinking messages to avoid HTML escaping issues
            if not is_thinking:
                timestamp_html = f"""
                <div class="message-timestamp assistant-timestamp">{format_timestamp(message.get('timestamp', ''))}</div>
                """
                st.markdown(timestamp_html, unsafe_allow_html=True)
            
            # Handle charts separately for better Streamlit compatibility
            if not is_thinking:
                # Show chart if available
                if message.get('chart_generated', False) and message.get('chart_s3_url'):
                    chart_url = message.get('chart_s3_url')
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    try:
                        st.image(chart_url, use_column_width=True, caption="Generated Chart")
                    except Exception as e:
                        st.error(f"Error loading chart: {str(e)}")
                        st.markdown(f'<p>Chart URL: <a href="{chart_url}" target="_blank">View Chart</a></p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Show chart decision reason if chart not generated
                elif message.get('chart_generated', None) is False:
                    reason = message.get('chart_decision_reason', '')
                    if reason:
                        st.markdown(f"""
                        <div class="chart-decision">
                            <strong>Chart Decision:</strong> {reason}
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Fixed input area
# st.markdown('<div class="input-container">', unsafe_allow_html=True)
# st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)

# Input form
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([10, 1])
    
    with col1:
        user_input = st.text_input(
            "",
            placeholder="Ask anything about your business data...",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        submit_button = st.form_submit_button("Send", use_container_width=True, type="primary")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Handle form submission
if submit_button and user_input and st.session_state.current_session_id:
    # Add user message to chat history immediately
    user_message = {
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now().isoformat()
    }
    st.session_state.chat_history.append(user_message)
    
    # Force rerun to show the user message immediately
    st.rerun()

# Check if we need to process a query (this handles the case after rerun)
if (st.session_state.chat_history and 
    st.session_state.chat_history[-1]['role'] == 'user' and 
    len(st.session_state.chat_history) > 0):
    
    # Check if this user message needs a response
    needs_response = True
    if len(st.session_state.chat_history) > 1:
        # Check if the last assistant message is a response to the current user message
        last_assistant_msg = None
        for msg in reversed(st.session_state.chat_history[:-1]):
            if msg['role'] == 'assistant':
                last_assistant_msg = msg
                break
        
        # If we have a recent assistant message, don't send another query
        if last_assistant_msg:
            user_time = datetime.fromisoformat(st.session_state.chat_history[-1]['timestamp'].replace('Z', '+00:00'))
            assistant_time = datetime.fromisoformat(last_assistant_msg['timestamp'].replace('Z', '+00:00'))
            if (user_time - assistant_time).total_seconds() < 5:  # Within 5 seconds
                needs_response = False
    
    if needs_response:
        user_query = st.session_state.chat_history[-1]['content']
        
        # Add thinking message to chat history
        thinking_message = {
            'role': 'assistant',
            'content': 'Thinking...',
            'analysis': 'Thinking...',
            'is_thinking': True,
            'timestamp': datetime.now().isoformat()
        }
        st.session_state.chat_history.append(thinking_message)
        
        # Force rerun to show thinking message
        st.rerun()

# Check if we have a thinking message that needs to be processed
if (st.session_state.chat_history and 
    st.session_state.chat_history[-1].get('is_thinking', False)):
    
    # Get the user query (second to last message)
    user_query = st.session_state.chat_history[-2]['content']
    
    # Send query to API
    response = send_query(user_query, st.session_state.current_session_id)
    
    if response:
        # Replace thinking message with actual response
        assistant_message = {
            'role': 'assistant',
            'content': response.get('analysis', ''),
            'analysis': response.get('analysis', ''),
            'chart_generated': response.get('chart_generated', False),
            'chart_s3_url': response.get('chart_s3_url'),
            'chart_decision_reason': response.get('chart_decision_reason'),
            'timestamp': response.get('timestamp')
        }
        st.session_state.chat_history[-1] = assistant_message
        
        # Update session title with first query
        if len(st.session_state.chat_history) == 2:  # First exchange
            st.session_state.sessions[st.session_state.current_session_id]['title'] = user_query[:50] + "..." if len(user_query) > 50 else user_query
    else:
        # Replace thinking message with error message
        error_message = {
            'role': 'assistant',
            'content': "I'm sorry, I encountered an error processing your request. Please try again.",
            'timestamp': datetime.now().isoformat()
        }
        st.session_state.chat_history[-1] = error_message
    
    # Rerun to show actual response
    st.rerun()