import streamlit as st
from backend.chat_logic import ChatLogic
import openai

# Initialize ChatLogic with API key setup
chat_logic = ChatLogic()

# Custom CSS for chat bubbles
custom_css = """
<style>
.userMessage {
    color: black;
    background-color: #f0f2f6;
    border-radius: 20px;
    padding: 10px;
    margin: 5px 0;
}
.assistantMessage {
    color: black;
    background-color: #daf1e0;
    border-radius: 20px;
    padding: 10px;
    margin: 5px 0;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar for OpenAI API Key
with st.sidebar:
    st.title('OpenAI Chatbot Setup')

    if 'OPENAI_API_KEY' in st.secrets:
        openai.api_key = st.secrets['OPENAI_API_KEY']
        chat_logic.api_key = openai.api_key  # Ensure the backend uses the same API key
        st.success('API key loaded from secrets!', icon='✅')
    else:
        entered_api_key = st.text_input('Enter OpenAI API token:', type='password')
        if entered_api_key:
            if entered_api_key.startswith('sk') and len(entered_api_key) == 51:
                st.session_state['api_key'] = entered_api_key
                openai.api_key = entered_api_key
                chat_logic.api_key = openai.api_key  # Ensure the backend uses the same API key
                st.success('API key set. Ready to proceed!', icon='👌')
            else:
                st.warning('Invalid API key format. Please check your key.', icon='⚠️')

st.title("MooseBot Chat")

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.container():
        # Display message with custom CSS
        if message['role'] == 'user':
            st.markdown(f"<div class='userMessage'>👤 {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistantMessage'>🤖 {message['content']}</div>", unsafe_allow_html=True)        

# Prepare the input form
user_input = st.text_input("You:", key="input")

# When the user submits a message
if st.button("Send", key="send") and user_input:
    # Add user message to the chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Prepare a placeholder for the assistant message
    placeholder = st.empty()
    full_response = ""
    
    # Stream responses
    for part in chat_logic.get_response_stream(user_input):
        full_response += part
        placeholder.markdown(f"<div class='assistantMessage'>🤖 {full_response}▌</div>", unsafe_allow_html=True)

    # Finalize streaming and display
    placeholder.markdown(f"<div class='assistantMessage'>🤖 {full_response}</div>", unsafe_allow_html=True)
    
    # Append the full response to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Clear the input box after sending the message
    # This is done by deleting the specific key from the session state
    del st.session_state["input"]

    # Move the input form to the bottom of the messages
    st.experimental_rerun()


