from app.core.openai import ConfigOpenAI

BOT_DESCRIPTION="app/services/bot_description.prompt"

class Orchestrator:
    def __init__(self):
        self.openai = ConfigOpenAI()

    def get_answer(self, history):
        _prompt = open(BOT_DESCRIPTION, "r").read()
        
        prompt = [{"role": "system", "content": _prompt}]
        history_item = [{"role": "user", "content": history["question"]}]

        # Get historial
        prompt.extend(history_item)
        chat_completion = self.openai.chat_completion(prompt)
        response = chat_completion["choices"][0]["message"]["content"]

        return {
            "data_points": "",
            "answer":response,
            "thoughts": ""
        }
