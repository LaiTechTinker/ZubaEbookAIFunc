# callbacks.py
# from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.callbacks import BaseCallbackHandler

class GeminiSSECallbackHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs):
        # Gemini streams text chunks
        self.queue.append(token)
