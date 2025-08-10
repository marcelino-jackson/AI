import streamlit as st
from state import init_state, new_chat, send_message
from ui_widgets import (
    render_header,
    render_history,
    render_messages,
    render_composer,
)
from services.ollama_client import list_models_safe
from utils import inject_css

# Page config MUST be the first Streamlit call
st.set_page_config(
    page_title="Chat UI",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main() -> None:
    # Global CSS + session state
    inject_css()
    init_state()

    # Header
    render_header(name="Marc")

    # Sidebar
    with st.sidebar:
        st.header("Menu")
        if st.button("➕ New", use_container_width=True, type="primary"):
            new_chat()
            st.rerun()

        models = list_models_safe()
        # Ensure the selectbox value is valid before rendering it
        if st.session_state.current_model not in models:
            st.session_state.current_model = models[0] if models else ""

        st.selectbox(
            "Model",
            models,
            key="current_model",
            help="Ollama models installed locally.",
        )

        render_history()

    # Main chat area + composer
    render_messages()
    render_composer(on_send=send_message)

if __name__ == "__main__":
    main()
