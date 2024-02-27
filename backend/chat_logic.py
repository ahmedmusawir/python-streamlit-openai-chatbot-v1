import os
from openai import OpenAI
import streamlit as st

class ChatLogic:
    def __init__(self, api_key=None):
        self.messages = []
        self.api_key = st.session_state.get('api_key', None)
        self.client = None
        if self.api_key:
            # Set the API key in the environment variable as required
            os.environ['OPENAI_API_KEY'] = self.api_key
            # Initialize the OpenAI client
            self.client = OpenAI()

    def add_message(self, role, content):
        """
        Add a message to the conversation.

        Parameters:
        - role: The role of the message sender (e.g., 'user' or 'assistant').
        - content: The content of the message.
        """
        self.messages.append({"role": role, "content": content})

    def get_response_stream(self, user_input):
        # Ensure the API key and client are set
        if not self.api_key or not self.client:
            yield "API key is not set or client initialization failed."
            return

        # Add the user input to the messages
        self.add_message("user", user_input)

        try:
            # Use the client to create a chat completion with streaming
            stream = self.client.chat.completions.create(
                model="gpt-4",  # or another model version you prefer
                messages=self.messages,
                stream=True,
            )

            # Iterate over the streamed response
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
        except Exception as e:
            yield str(e)
