import os
import openai
from openai import OpenAI

class ChatLogic:
    def __init__(self, api_key=None):
        self.messages = []
        self.api_key = api_key
        self.client = None
        if self.api_key:
            openai.api_key = self.api_key
            self.client = OpenAI()

    def add_message(self, role, content):
        """
        Add a message to the conversation.

        Parameters:
        - role: The role of the message sender (e.g., 'user' or 'assistant').
        - content: The content of the message.
        """
        self.messages.append({"role": role, "content": content})

    def get_response(self, user_input):
        """
        Get a response from the OpenAI API based on the conversation history.

        Parameters:
        - user_input: The user's input message as a string.

        Returns:
        - The response content as a string.
        """
        self.add_message('user', user_input)  # Add user message to the conversation
        if self.client is None:
            raise ValueError("API Key has not been set.")
        
        completion = self.client.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.5
        )
        
        response = completion.choices[0].message['content']
        self.add_message('assistant', response)  # Add assistant's response to the conversation
        return response
