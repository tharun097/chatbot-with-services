from src.langgraphagenticai.state.graph_state import State
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
class ChatbotWithTools:
    def __init__(self,llm):
        self.llm = llm
        
    def create_chatbot_with_tools(self,tools):
        """Takes input from user and responds to user with relevent information as user requried, chatbot has enhcanced capabilities using tools"""
        
        llm_with_tools = self.llm.bind_tools(tools)  # Here, you would typically integrate the tools with the LLM.
        
        def chatbot_node(state:State)->dict:
            return {"messages":llm_with_tools.invoke(state['messages'])}
        return chatbot_node
    