import streamlit as st
from backend.chat_logic import ChatLogic

# Custom CSS for styling (Optional)
custom_css = """
<style>
    .stTextInput>div>div>input {
        color: black;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar for API key input
with st.sidebar:
    st.title('Settings')
    entered_api_key = st.text_input('Enter OpenAI API token:', type='password')

# Initialize ChatLogic without API key
chat_logic = ChatLogic()

if entered_api_key:
    chat_logic.set_api_key(entered_api_key)
    user_input = st.text_input("Say something to GPT-3:")

    if user_input:
        # Fetch the response from GPT-3
        response = chat_logic.get_response(user_input)
        st.text_area("GPT-3 says:", value=response, height=300, max_chars=None, key="response")
else:
    st.error("Please enter your OpenAI API key in the sidebar.")
