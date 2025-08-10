from __future__ import annotations
import streamlit as st
from datetime import datetime
from typing import Any, Dict, List

DEFAULT_MODEL = "(select a model)"

def init_state() -> None:
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


def new_chat() -> None:
    if st.session_state.messages:
        st.session_state.history.append({
            "id": datetime.utcnow().isoformat(),
            "title": st.session_state.chat_title or "Untitled chat",
            "messages": st.session_state.messages.copy(),
            "model": st.session_state.current_model,
        })
    st.session_state.messages = []
    st.session_state.chat_title = datetime.now().strftime("Chat %b %d, %I:%M %p")


def send_message(user_text: str, attachments: List[Any] | None = None) -> None:
    if not user_text and not attachments:
        return
    st.session_state.messages.append({
        "role": "user",
        "content": user_text,
        "time": datetime.now().strftime("%H:%M"),
        "attachments": attachments or [],
    })
    # TODO: replace with real call to Ollama chat; for now, stub reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": "_Stub reply:_ Message received. Wire Ollama next.",
        "time": datetime.now().strftime("%H:%M"),
        "attachments": [],
    })
