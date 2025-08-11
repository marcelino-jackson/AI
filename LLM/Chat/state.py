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
        # Actual value gets set in app.py once models are discovered
        st.session_state.current_model = DEFAULT_MODEL
    if "chat_title" not in st.session_state:
        st.session_state.chat_title = "New chat"
    if "show_uploader" not in st.session_state:
        st.session_state.show_uploader = False
    if "attachments_buffer" not in st.session_state:
        st.session_state.attachments_buffer = []

# ---------- Global accessors for the selected model ----------
def get_current_model() -> str:
    """Read the currently selected model anywhere in the app."""
    return st.session_state.get("current_model", DEFAULT_MODEL)

def set_current_model(model_name: str) -> None:
    """Update the selected model in a single place."""
    st.session_state.current_model = model_name

# ---------- Chat state actions ----------
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
    st.session_state.chat_title = datetime.now().strftime("Chat %b %d, %I:%M %p")

def send_message(user_text: str, attachments: List[Any] | None = None) -> None:
    """Append a user message and a placeholder assistant reply."""
    if not user_text and not attachments:
        return

    st.session_state.messages.append({
        "role": "user",
        "content": user_text,
        "time": datetime.now().strftime("%H:%M"),
        "attachments": attachments or [],
    })

    # TODO: replace with real call to Ollama using get_current_model()
    st.session_state.messages.append({
        "role": "assistant",
        "content": "_Stub reply:_ Message received. Wire Ollama next.",
        "time": datetime.now().strftime("%H:%M"),
        "attachments": [],
    })
