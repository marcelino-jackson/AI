import streamlit as st
from services.ollama_client import get_models, generate_text


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "current_model" not in st.session_state:
        models = get_models_list()
        st.session_state.current_model = models[0] if models else None

    if "models_list" not in st.session_state:
        st.session_state.models_list = []

    if "last_input" not in st.session_state:
        st.session_state.last_input = ""


def get_current_model():
    return st.session_state.get("current_model")


def set_current_model(model_name):
    st.session_state.current_model = model_name


def get_models_list():
    if not st.session_state.get("models_list"):
        try:
            models = get_models()
            st.session_state.models_list = models if models else []
        except:
            st.session_state.models_list = []
    return st.session_state.models_list


def append_message(role, content, model=None):
    message = {
        "role": role,
        "content": content,
        "model": model  # Store which model was used
    }
    st.session_state.messages.append(message)


def send_message_with_model(user_message):
    current_model = st.session_state.current_model

    if not current_model:
        return False

    try:
        # Add user message (no model needed for user messages)
        append_message("user", user_message)

        # Generate response with current model
        response = generate_text(current_model, user_message)

        if response:
            # Add assistant message with model information
            append_message("assistant", response, current_model)
            return True
        return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False