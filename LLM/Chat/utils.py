import streamlit as st
from datetime import datetime

# Updated CSS with model badge styling and taller input
CUSTOM_CSS = """
<style>
    .main > div {
        padding-top: 1rem;
    }

    /* Ensure consistent container widths */
    .block-container {
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .stButton > button {
        background-color: #ff4757 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
    }

    .stButton > button:hover {
        background-color: #ff3838 !important;
        transform: translateY(-1px) !important;
    }

    /* Enhanced text area styling */
    .stTextArea textarea {
        background-color: #2d2d2d !important;
        border: 2px solid #404040 !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
        padding: 1rem !important;
    }

    .stTextArea textarea:focus {
        border-color: #ff4757 !important;
        box-shadow: 0 0 0 2px rgba(255, 71, 87, 0.2) !important;
    }

    /* Aligned chat messages */
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        width: 100%;
        box-sizing: border-box;
        border: 1px solid transparent;
    }

    .chat-message.user {
        background-color: #3742fa;
        margin-left: 0;
        margin-right: 20%;
        border-color: #3742fa;
    }

    .chat-message.assistant {
        background-color: #2d2d2d;
        margin-left: 0;
        margin-right: 0;
        border-color: #404040;
        position: relative;
    }

    /* Model badge styling */
    .model-badge {
        background: linear-gradient(135deg, #ff4757, #ff6b7d);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .message-content {
        line-height: 1.6;
        color: #ffffff;
    }

    /* Consistent spacing */
    .element-container {
        margin-bottom: 1rem;
    }

    /* Enhanced button styling */
    .stButton[data-testid="baseButton-primary"] button {
        background: linear-gradient(135deg, #ff4757, #ff3838) !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(255, 71, 87, 0.3) !important;
    }
</style>
"""


def inject_custom_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def get_greeting():
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 17:
        return "Good afternoon"
    elif 17 <= current_hour < 22:
        return "Good evening"
    else:
        return "Good night"