import streamlit as st
from backend.chat_logic import ChatLogic
import os

# Assuming you're setting the API key here for simplicity
os.environ["OPENAI_API_KEY"] = "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"

chat_logic = ChatLogic()


def display_chat():
    # Debugging: Print messages to console
    # print("Displaying chat messages:", chat_logic.messages)
    for message in chat_logic.messages:
        with st.container():
            st.markdown(f"**{message['role'].capitalize()}**: {message['content']}")

def chat_interface():
    with st.form("message_form"):
        user_input = st.text_input("Type your message here...", key="chat_input")
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        print("User input:", user_input)  # Debugging: Confirm input is captured
        chat_logic.add_message('user', user_input)
        bot_response = chat_logic.get_response()
        print("Bot response:", bot_response)  # Debugging: Confirm response is generated
        chat_logic.add_message('bot', bot_response)
        display_chat()  # Ensure chat display is updated after adding messages

def run():
    st.title("Simple Chatbot")
    display_chat()
    chat_interface()

if __name__ == "__main__":
    run()

