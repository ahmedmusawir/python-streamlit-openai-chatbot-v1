# /app.py

import streamlit as st
from backend.chat_logic import ChatLogic

# Initialize ChatLogic
chat_logic = ChatLogic()

# Custom CSS (optional for styling)
custom_css = """
<style>
    /* Custom styles here */
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar for API Key Input
with st.sidebar:
    st.title('ChatGPT Interface')
    api_key = st.text_input('Enter OpenAI API token:', type='password')
    if api_key:
        chat_logic.update_api_key(api_key)
        st.success('API Key updated!')

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    st.text_area("", value=message["content"], height=100, key=message["role"] + str(message["content"][:10]))

# User Input
user_input = st.text_input("Your message:", key="user_input")

if user_input:
    response = chat_logic.get_response(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Clear the input box after sending the message
    st.session_state["user_input"] = ""
