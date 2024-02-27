import openai

class ChatLogic:
    def __init__(self):
        self.api_key = None
        self.client = None
        self.messages = []

    def set_api_key(self, api_key):
        self.api_key = api_key
        self.client = openai.ChatCompletion(api_key=api_key)

    def get_response(self, user_input):
        self.messages.append({'role': 'user', 'content': user_input})
        if self.client is None:
            raise ValueError("API Key has not been set.")
        
        completion = self.client.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.5
        )
        
        response = completion.choices[0].message['content']
        self.messages.append({'role': 'assistant', 'content': response})
        return response
