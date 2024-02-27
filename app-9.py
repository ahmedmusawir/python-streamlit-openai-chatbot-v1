import streamlit as st
from backend.chat_logic import ChatLogic
import openai

# Initialize ChatLogic
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

st.title("MooseBot Chat")

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.container():
        if message['role'] == 'user':
            st.markdown(f"<div class='userMessage'>👤 {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistantMessage'>🤖 {message['content']}</div>", unsafe_allow_html=True)

user_input = st.text_input("You:", "")

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = chat_logic.get_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.experimental_rerun()
