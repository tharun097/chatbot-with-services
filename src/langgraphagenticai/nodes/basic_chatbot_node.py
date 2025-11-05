from src.langgraphagenticai.state.graph_state import State
from src.langgraphagenticai.LLMs.groqllm import GroqLLM

class ChatBotNode:
    def __init__(self,model):
        self.llm = model
    def process(self,state:State)->dict:
        """Takes input from user and responds to user with relevent information as user requried"""
        return {"messages":self.llm.invoke(state['messages'])}