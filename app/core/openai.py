import logging
import os 
import openai
from dotenv import load_dotenv

load_dotenv()

class ConfigOpenAI():
    def __init__(self) -> None:
        openai.api_type = os.getenv('OPENAI_TYPE')
        openai.api_version = os.getenv('OPENAI_VERSION')
        openai.api_key = os.getenv('OPENAI_KEY')
        openai.api_base = os.getenv('OPENAI_BASE')

    def chat_completion(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                stop=["<|im_end|>", "<|im_start|>"],
                top_p=0.2,
                engine=os.getenv('OPENAI_ENGINE'),
                messages=prompt,
                max_tokens=800,
                temperature=0.7
            )
            return response
        except openai.error.OpenAIError as e:
            logging.error(f"Error al obtener chat completion: {e}")
            raise
