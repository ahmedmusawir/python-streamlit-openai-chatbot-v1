from openai import OpenAI
import os

class ChatLogic:
    def __init__(self):
        self.messages = []
        if os.environ["OPENAI_API_KEY"]:
            self.client = OpenAI()
        # self.messages = [{'role': "system", 'content': system_prompt}]
        # self.system_prompt = system_prompt        

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_response(self):
        completion = self.client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=self.messages,
            temperature=0.8
        )  
        print('COMPLETION:', completion.choices[0].message.content)
        return completion.choices[0].message.content    
