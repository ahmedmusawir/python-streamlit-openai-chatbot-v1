import streamlit as st
from backend.chat_logic import ChatLogic
import openai

# Initialize ChatLogic
chat_logic = ChatLogic()

# Setup for OpenAI API Key Input
with st.sidebar:
    st.title('OpenAI Chatbot Setup')

    if 'OPENAI_API_KEY' in st.secrets:
        openai.api_key = st.secrets['OPENAI_API_KEY']
        st.success('API key loaded from secrets!', icon='✅')
    else:
        entered_api_key = st.text_input('Enter OpenAI API token:', type='password')
        if entered_api_key:
            if entered_api_key.startswith('sk') and len(entered_api_key) == 51:
                st.session_state['api_key'] = entered_api_key
                openai.api_key = entered_api_key
                st.success('API key set. Ready to proceed!', icon='👌')
            else:
                st.warning('Invalid API key format. Please check your key.', icon='⚠️')

# Main Chatbot Interface
st.title("MooseBot Chat")

# Initialize messages list in session state if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display existing conversation
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.text_area("You", value=message['content'], height=75, disabled=True)
    else:
        st.text_area("MooseBot", value=message['content'], height=75, disabled=True)

# User input
user_input = st.text_input("You:", "")

# Handling the user input
if st.button("Send") and user_input:
    # Append user message to the conversation history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get response from the chat logic
    response = chat_logic.get_response(user_input)

    # Append response to the conversation history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Clear the user input box (optional, for UX)
    st.experimental_rerun()
