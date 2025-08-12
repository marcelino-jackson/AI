from __future__ import annotations
import streamlit as st
from datetime import datetime
from typing import Any, Dict, List

DEFAULT_MODEL = ""

def init_state() -> None:
    """Initialize all session_state keys we rely on."""
    if "messages" not in st.session_state:
        st.session_state.messages: List[Dict[str, Any]] = []
    if "history" not in st.session_state:
        st.session_state.history: List[Dict[str, Any]] = []
    if "current_model" not in st.session_state:
        st.session_state.current_model = DEFAULT_MODEL
    if "chat_title" not in st.session_state:
        st.session_state.chat_title = "New chat"
    if "show_uploader" not in st.session_state:
        st.session_state.show_uploader = False
    if "attachments_buffer" not in st.session_state:
        st.session_state.attachments_buffer = []
    if "sidebar_open" not in st.session_state:
        st.session_state.sidebar_open = True
    if "last_result" not in st.session_state:
        st.session_state.last_result = ""

# ---------- Global accessors for the selected model ----------
def get_current_model() -> str:
    """Read the currently selected model anywhere in the app."""
    return st.session_state.get("current_model", DEFAULT_MODEL)

def set_current_model(model_name: str) -> None:
    """Update the selected model in a single place."""
    st.session_state.current_model = model_name

# ---------- Chat state helpers ----------
def append_exchange(user_text: str, assistant_text: str, attachments: List[Any] | None = None) -> None:
    """Append a user/assistant message pair to chat history.

    We stamp BOTH messages with the model used so the UI can show a unified header.
    """
    attachments = attachments or []
    model = get_current_model()
    now = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": user_text,   # already includes our 'Prompting…' header markup
        "time": now,
        "attachments": attachments,
        "model": model,
    })
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_text,  # already includes our 'Results from…' header markup
        "time": now,
        "attachments": [],
        "model": model,
    })

def new_chat() -> None:
    """Archive current chat to history and start a new one."""
    if st.session_state.messages:
        st.session_state.history.append({
            "id": datetime.utcnow().isoformat(),
            "title": st.session_state.chat_title or "Untitled chat",
            "messages": st.session_state.messages.copy(),
            "model": get_current_model(),
        })
    st.session_state.messages = []
    st.session_state.last_result = ""
    st.session_state.chat_title = datetime.now().strftime("Chat %b %d, %I:%M %p")

# Back-compat (kept, not used by the new flow)
def send_message(user_text: str, attachments: List[Any] | None = None) -> None:
    if not user_text and not attachments:
        return
    attachments = attachments or []
    model = get_current_model()
    now = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": user_text,
        "time": now,
        "attachments": attachments,
        "model": model,
    })
    st.session_state.messages.append({
        "role": "assistant",
        "content": "_Stub reply:_ Message received. Wire Ollama next.",
        "time": now,
        "attachments": [],
        "model": model,
    })