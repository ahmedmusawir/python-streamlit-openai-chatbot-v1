import streamlit as st
from backend.chat_logic import ChatLogic
import os

# Setup OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

if 'chat_logic' not in st.session_state:
    st.session_state.chat_logic = ChatLogic()

def display_chat():
    for message in st.session_state.chat_logic.messages:
        with st.container():
            st.markdown(f"**{message['role'].capitalize()}**: {message['content']}")

def chat_interface():
    user_input = st.text_input("Type your message here...", key="chat_input")
    if st.button('Send'):
        if user_input:  # Check if user_input is not empty
            st.session_state.chat_logic.add_message('user', user_input)
            bot_response = st.session_state.chat_logic.get_response()
            st.session_state.chat_logic.add_message('bot', bot_response)
            # Clear input box after sending message
            st.session_state['chat_input'] = ''
            # Rerun the app to refresh the chat display
            st.experimental_rerun()

def run():
    st.title("Simple Chatbot")
    display_chat()
    chat_interface()

if __name__ == "__main__":
    run()
