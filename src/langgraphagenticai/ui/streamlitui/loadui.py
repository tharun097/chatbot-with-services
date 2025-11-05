import streamlit as st 
import os

from src.langgraphagenticai.ui.uiconfigload import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}
    
    def load_streamlitui(self):
        print(f"page_title:{self.config.get_page_title()}")
        st.set_page_config(page_title= "🤖 " + self.config.get_page_title(),layout="wide")
        st.header("🤖 " + self.config.get_page_title())
        #initialize session state variables
        if "IsFetchButtonClicked" not in st.session_state or st.session_state.timeframe not in st.session_state:
            st.session_state.IsFetchButtonClicked = False
            st.session_state.timeframe = ""
        st.session_state.movie_genre = ""
        st.session_state.num_recommendations = 0    
        st.session_state.year = 0
        st.session_state.language = ""
        with st.sidebar:
            #get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
            
            #select llm
            self.user_controls["selected_llm"] = st.selectbox("Pick an LLM", llm_options,index=None)
            
            if self.user_controls["selected_llm"] == "Groq":
                #get groq model options
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_model"] = st.selectbox("Pick a model",model_options,index=None)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]=st.text_input("GROQ API KEY",type="password")                
                #validate GROQ API KEY
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
                
            #select relevant usecase
            self.user_controls["selected_usecase"] = st.radio("select relevant usecase",usecase_options,index=None)
            if self.user_controls["selected_usecase"] == "Chatbot with Tool" or self.user_controls["selected_usecase"] == "AI News" or self.user_controls["selected_usecase"] == "Movie Recommender":
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"]=st.text_input("TAVILY API KEY",type="password")
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your TAVILY API KEY to proceed. Don't have? refer : https://app.tavily.com/home")
            
            if self.user_controls["selected_usecase"] == "AI News":
                st.subheader("📰 AI News Explorer")
                
                with st.sidebar:
                    timeframe = st.selectbox("📅 Select Time Frame",["Daily","Weekly","Monthly"],index=0)
                
                if st.button("🔍 Fetch Latest AI News",use_container_width=True,width="stretch"):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = timeframe
            
            years = list(range(2000, 2025))
            
            if self.user_controls["selected_usecase"] == "Movie Recommender":
                st.subheader("🎬 Movie Recommender")
                with st.sidebar:
                    movie_genre = st.selectbox("🍿 Select Movie Genre",["Action","Comedy","Drama","Horror","Romance","Sci-Fi","Documentary"],index=0)
                    num_recommendations = st.slider("🎯 Number of Recommendations",1,20,5)
                    year = st.selectbox("📅 Select Release Year",years,index=len(years)-1)
                    language = st.selectbox("🌐 Select Language",["English","Hindi","Telugu","Kannada","Tamil","Malayalam"],index=0)
                
                if st.button("🎬 Get Movie Recommendations",use_container_width=True,width="stretch"):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.movie_genre = movie_genre
                    st.session_state.num_recommendations = num_recommendations
                    st.session_state.year = year
                    st.session_state.language = language
        return self.user_controls
                
            
            