from __future__ import annotations
import time
from datetime import datetime
from typing import Any, Dict

import streamlit as st

from utils import greeting_for_now
from state import append_exchange, get_current_model
from services.ollama_client import generate_with_progress


# ---------- Header ----------

def render_header(name: str) -> None:
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
    role = msg["role"]
    avatar = "👤" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        content = msg.get("content", "")
        st.markdown(content, unsafe_allow_html=True)
        if msg.get("attachments"):
            with st.expander("Attachments"):
                for i, f in enumerate(msg["attachments"], start=1):
                    st.write(
                        f"{i}. {getattr(f, 'name', 'file')} ({getattr(f, 'type', 'unknown')})"
                    )

def render_messages() -> None:
    if not st.session_state.messages:
        return
    for msg in st.session_state.messages:
        _render_message(msg)


# ---------- Composer ----------
def render_composer(on_send):
    """
    - Left: attachments toggle
    - Right: chat input (submit via Enter / send icon)
    """
    below_prompt = st.container()

    # Wider clip column (~avatar width) so the input lines up with bubbles WITHOUT negative margins
    col_clip, col_input = st.columns([0.095, 0.905], vertical_alignment="center")

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

    if prompt is not None and prompt.strip():
        model = get_current_model()
        now_ts = datetime.now().strftime("%H:%M")

        user_block = f"""
<div class="section-header">
  <div class="section-title">Prompting… <span class="model-chip">{model}</span></div>
  <div class="section-meta">{now_ts}</div>
</div>
{prompt}
""".strip()

        # Timing (prefer first-token → end)
        t_start_wall = time.perf_counter()
        first_token_time: float | None = None

        with below_prompt:
            with st.container(border=True):
                with st.expander(f"Thinking…  \u00A0\u00A0{now_ts}", expanded=True):
                    st.markdown("_Let's write._")
                    stream_placeholder = st.empty()
                    progress_widget = st.progress(0)
                    status = st.empty()

                    collected: list[str] = []
                    progress_val = 0

                    def on_chunk(chunk: str):
                        nonlocal progress_val, first_token_time
                        if first_token_time is None:
                            first_token_time = time.perf_counter()
                        collected.append(chunk)
                        stream_placeholder.markdown("".join(collected))
                        progress_val = min(95, progress_val + 2)
                        progress_widget.progress(progress_val)
                        status.info(f"Running **{model}**…")

                    try:
                        final_text = generate_with_progress(model, prompt, on_chunk=on_chunk)
                        progress_widget.progress(100)
                        status.success("Completed")
                        st.markdown("…done thinking.")
                    except Exception as e:
                        progress_widget.progress(100)
                        status.error("Failed")
                        final_text = f"**Error:** {e}"
                        st.markdown("…done thinking.")

        t_end = time.perf_counter()
        if first_token_time is not None:
            elapsed = t_end - first_token_time
        else:
            elapsed = t_end - t_start_wall
        elapsed_str = f"{elapsed:.2f}s"

        assistant_block = f"""
<div class="section-header">
  <div class="section-title">Results from <span class="model-chip">{model}</span></div>
  <div class="section-meta">{elapsed_str}</div>
</div>
{final_text}
""".strip()

        append_exchange(user_block, assistant_block, getattr(st.session_state, "attachments_buffer", []))
        st.session_state.attachments_buffer = []
        st.rerun()