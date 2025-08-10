from __future__ import annotations
import streamlit as st
from datetime import datetime

PRIMARY_MAX_WIDTH = 920
USER_BG = "#1f2937"      # slate-800
ASSIST_BG = "#111827"    # gray-900
BORDER = "#2a2f3a"


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        .block-container {{ max-width: {PRIMARY_MAX_WIDTH}px; margin: 0 auto; }}
        /* Hide the Deploy/toolbar entirely */
        [data-testid="stToolbar"], header [data-testid="stHeaderActionElements"] {{ display: none !important; visibility: hidden !important; }}
        /* Sidebar width */
        section[data-testid="stSidebar"] {{ width: 16rem !important; }}
        /* Chat bubbles */
        [data-testid="stChatMessage"] {{
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 10px 14px;
            margin: 8px 0 16px 0;
            background: {ASSIST_BG};
        }}
        [data-testid="stChatMessage-user"] {{ background: {USER_BG}; }}
        /* Timestamp inline */
        .msg-ts {{ float: right; opacity: 0.6; font-size: 0.8rem; }}
        /* Composer height */
        div[data-testid="stChatInput"] textarea {{ min-height: 56px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def greeting_for_now(name: str) -> str:
    hour = datetime.now().hour
    if hour < 12:
        g = "Good morning"
    elif hour < 18:
        g = "Good afternoon"
    else:
        g = "Good evening"
    return f"{g}, {name}"