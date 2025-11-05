from langchain_groq import ChatGroq
import os
import streamlit as st

class GroqLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input = user_controls_input
        
    def load_llm(self):
        """Loads llm by taking inputs from frontend"""
        try:
            groq_api_key = self.user_controls_input["GROQ_API_KEY"]
            selected_model = self.user_controls_input["selected_model"]
            if groq_api_key=="" or os.getenv("GROQ_API_KEY")=="":
                st.error(f"Please check the LLM API KEY is not available")
            elif selected_model=="":
                st.error(f"Please select any of the model")
            llm = ChatGroq(model = selected_model,api_key = groq_api_key)
        except Exception as e:
            raise ValueError(f"The error has encountered:{e}")
        return llm
            