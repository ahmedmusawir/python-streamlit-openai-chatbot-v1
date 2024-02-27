import openai

class ChatLogic:
    def __init__(self, api_key=None):
        self.api_key = api_key
        if api_key:
            openai.api_key = api_key
            self.client = openai.ChatCompletion.create(model="gpt-3.5-turbo")
        else:
            self.client = None
        self.messages = []

    def update_api_key(self, new_api_key):
        self.api_key = new_api_key
        openai.api_key = new_api_key
        self.client = openai.ChatCompletion.create(model="gpt-3.5-turbo")

    def get_response(self, prompt):
        if not self.api_key or not self.client:
            raise ValueError("API key is not set or client is not initialized.")

        self.messages.append({"role": "user", "content": prompt})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.8
        )
        
        # Assuming the response structure matches the expected format
        response_content = response.choices[0].message['content']
        self.messages.append({"role": "assistant", "content": response_content})
        
        return response_content
