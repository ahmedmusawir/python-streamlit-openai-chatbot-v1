import streamlit as st
from backend.chat_logic import ChatLogic
import openai
import os

# Initialize the ChatLogic instance without setting the API key
# chat_logic = ChatLogic()
# Only initialize ChatLogic if the API key is set
chat_logic = ChatLogic()


# Setting up the Sidebar for OpenAI API Key Input
with st.sidebar:
    st.title('OpenAI Chatbot Setup')

    # Check if the API key is provided via st.secrets
    if 'OPENAI_API_KEY' in st.secrets:
        openai.api_key = st.secrets['OPENAI_API_KEY']
        st.success('API key loaded from secrets!', icon='✅')
    else:
        # Prompt the user for the API key if it's not in st.secrets
        entered_api_key = st.text_input('Enter OpenAI API token:', type='password')

        if entered_api_key:
            if entered_api_key.startswith('sk') and len(entered_api_key) == 51:
                # openai.api_key = entered_api_key
                    # Set the API key as an environment variable
                st.session_state['api_key'] = entered_api_key
                openai.api_key = entered_api_key
                st.success('API key set. Ready to proceed!', icon='👌')
            else:
                st.warning('Invalid API key format. Please check your key.', icon='⚠️')

# Main Chatbot Interface
st.title("MooseBot Chat")

# User input
user_input = st.text_input("You:", "")
print('user input 1:', user_input)
print('open ai api key', openai.api_key)

# Handling the user input
if st.button("Send") and openai.api_key:
    if user_input:
        # Add user message to the chat
        chat_logic.add_message("user", user_input)
        
        # Get response
        print('user input 2:', user_input)
        response = chat_logic.get_response(user_input)
        
        # Display the response
        st.text_area("Chatbot:", value=response, height=100, max_chars=None, key="response")
