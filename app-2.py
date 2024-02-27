import streamlit as st
from backend.chat_logic import ChatLogic
import os
import openai

chat_logic = ChatLogic()

def display_sidebar():
    # Setting up the Sidebar
    with st.sidebar:
        st.title('MooseBot OpenAI')

        # Checking and Accepting the OpenAI API Key
        if 'OPENAI_API_KEY' in st.secrets:
            st.success('API key already provided!', icon='✅')
            openai.api_key = st.secrets(['OPENAI_API_KEY'])
        else:
            openai.api_key = st.text_input('Enter OpenAI API token:', type='password')

            if not (openai.api_key.startswith('sk') and len(openai.api_key) == 51):
                st.warning('Please enter your credentials!', icon='⚠️')
            
            else:
                st.success('Proceed to your chatbot prompting!', icon='👌')

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
    display_sidebar()
    st.title("Simple Chatbot")
    display_chat()
    chat_interface()

if __name__ == "__main__":
    run()

