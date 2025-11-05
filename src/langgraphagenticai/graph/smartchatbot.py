from langgraph.graph import StateGraph,START,END
from src.langgraphagenticai.state.graph_state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import ChatBotNode
from langgraph.prebuilt import ToolNode,tools_condition
from src.langgraphagenticai.tools.ext_tools import get_tools, create_tool_node
from src.langgraphagenticai.nodes.chatbot_with_tools import ChatbotWithTools
from src.langgraphagenticai.nodes.ai_news_tool import AINewsToolNode
from src.langgraphagenticai.nodes.moviebot_node import MovieBotNode
import streamlit as st 

class Graphbuilder:
    def __init__(self,model):
        self.llm = model
        self.graph_builder = StateGraph(State)
    
    def get_chatbot_graph(self):
        """Takes input from user as a message and returns the accurate message nothing but acts like a assistant to user basis on workflow defined"""
        self.basic_chatbot_node=ChatBotNode(self.llm)
        
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)
        
    def build_chatbot_with_tool(self):
        """Takes input from user as a message and returns the accurate message nothing but acts like a assistant to user basis on workflow defined"""
    
        tools = get_tools()
        tool_node = create_tool_node(tools)
        chatbot_with_tools = ChatbotWithTools(self.llm)
        chatbot_node = chatbot_with_tools.create_chatbot_with_tools(tools)
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        self.graph_builder.add_edge("chatbot",END)
        
    def ai_news_fetcher(self):
        """Fetches latest AI news basis on timeframe selected by user using external APIs"""
        llm = self.llm
        
        ai_news_node = AINewsToolNode(llm)
        
        self.graph_builder.add_node("fetch news",ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize news",ai_news_node.summarize_news)
        self.graph_builder.add_node("save news",ai_news_node.save_news)
        
        self.graph_builder.add_edge(START,"fetch news")
        self.graph_builder.add_edge("fetch news","summarize news")      
        self.graph_builder.add_edge("summarize news","save news")
        self.graph_builder.add_edge("save news",END)
    
    def movie_recommender(self):
        """Recommends movies basis on genre, release year and number of recommendations selected by user using external APIs"""
        llm = self.llm
        
        moviebotnode = MovieBotNode(llm)
    
        
        self.graph_builder.add_node("movie recommender",moviebotnode.movie_recommendation)
        self.graph_builder.add_node("movie_details_alignment",moviebotnode.summarize_movies)
        self.graph_builder.add_node("display movie details",moviebotnode.save_recommendations)
        self.graph_builder.add_edge(START,"movie recommender")
        self.graph_builder.add_edge("movie recommender","movie_details_alignment")
        self.graph_builder.add_edge("movie_details_alignment","display movie details")
        self.graph_builder.add_edge("display movie details",END)
    
    def set_graph_state(self,usecase):
        """Decides which graph to be compiled"""
        if usecase=="Basic Chatbot":
            self.get_chatbot_graph()
        elif usecase=="Chatbot with Tool":
            self.build_chatbot_with_tool()
        elif usecase=="AI News":
            self.ai_news_fetcher()
        elif usecase=="Movie Recommender":
            self.movie_recommender()
        return self.graph_builder.compile()
                