import streamlit as st
from utils import inject_custom_css
from ui_widgets import render_header, render_sidebar, render_chat_messages, render_composer
from state import initialize_session_state, send_message_with_model


def main():
    st.set_page_config(
        page_title="Chat UI",
        page_icon="💬",
        layout="wide"
    )

    initialize_session_state()
    inject_custom_css()

    render_sidebar()

    render_header()
    render_chat_messages()

    # Handle the composer input
    send_button, user_input = render_composer()

    # Process message when send button clicked
    if send_button and user_input and user_input.strip():
        success = send_message_with_model(user_input.strip())
        if success:
            st.rerun()


if __name__ == "__main__":
    main()