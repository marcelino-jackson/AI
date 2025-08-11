from __future__ import annotations
import streamlit as st
from typing import Any, Dict
from utils import greeting_for_now

# ---------- Header ----------

def render_header(name: str) -> None:
    """Top greeting + subtle divider + centered subheading."""
    st.markdown(
        f"""<h1 style='text-align:center;margin-top:0.25rem;'>{greeting_for_now(name)}</h1>""",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='opacity:0.15;margin:6px 0;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;opacity:0.75;font-size:1.15rem;'>Start a conversation below.</p>",
        unsafe_allow_html=True,
    )

# ---------- History ----------

def render_history() -> None:
    st.subheader("History")
    if not st.session_state.history:
        st.caption("No past chats yet.")
        return
    for i, chat in enumerate(reversed(st.session_state.history)):
        label = chat.get("title") or f"Chat {i+1}"
        with st.container(border=True):
            cols = st.columns([0.75, 0.25])
            with cols[0]:
                st.write(label)
                last_msg = (chat.get("messages") or [{}])[-1].get("content", "")
                prev = " ".join(last_msg.split()[:10])
                st.caption(prev + ("…" if prev else ""))
            with cols[1]:
                if st.button("Open", key=f"hist_{i}", use_container_width=True):
                    st.session_state.messages = chat["messages"].copy()
                    st.session_state.chat_title = label
                    st.session_state.current_model = chat.get(
                        "model", st.session_state.get("current_model")
                    )
                    st.rerun()

# ---------- Messages ----------

def _render_message(msg: Dict[str, Any]) -> None:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        # timestamp (top-right inside bubble)
        st.markdown(
            f"<span class='msg-ts'>{msg.get('time','')}</span>",
            unsafe_allow_html=True,
        )
        if msg.get("content"):
            st.markdown(msg["content"], help="Markdown supported.")
        if msg["role"] == "assistant" and msg.get("content"):
            with st.expander("Copy text"):
                st.code(msg["content"])
        if msg.get("attachments"):
            with st.expander("Attachments"):
                for i, f in enumerate(msg["attachments"], start=1):
                    st.write(
                        f"{i}. {getattr(f, 'name', 'file')} ({getattr(f, 'type', 'unknown')})"
                    )

def render_messages() -> None:
    if not st.session_state.messages:
        # Header already shows the "Start a conversation below." hint
        pass
    for msg in st.session_state.messages:
        _render_message(msg)

# ---------- Composer ----------

def render_composer(on_send):
    """
    Bottom composer with:
      - left: attachments button (centered vertically)
      - right: chat_input sized by CSS; text left-aligned; Shift+Enter for newline
    """
    bottom = st.empty()

    # Keep the icon aligned to the middle of the (CSS-sized) input container
    col_clip, col_input = st.columns([0.09, 0.91], vertical_alignment="center")

    with col_clip:
        if st.button("📎", key="attach_btn", help="Add attachments", use_container_width=True):
            st.session_state.show_uploader = not st.session_state.show_uploader

    with col_input:
        prompt = st.chat_input(
            placeholder="Type your prompt here… (Enter to send, Shift+Enter for newline)",
            key="composer",
        )

    if st.session_state.show_uploader:
        with st.expander("Attachments (stub)", expanded=True):
            files = st.file_uploader(
                "Upload files", accept_multiple_files=True, label_visibility="collapsed"
            )
            if files:
                st.session_state.attachments_buffer = files

    if prompt is not None:
        on_send(prompt, st.session_state.attachments_buffer)
        st.session_state.attachments_buffer = []
        bottom.write("")
        st.rerun()
