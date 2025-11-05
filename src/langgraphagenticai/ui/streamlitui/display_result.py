import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase= self.usecase
        graph = self.graph
        user_message = self.user_message
        # print(user_message)
        if usecase =="Basic Chatbot":
                for event in graph.stream({'messages':("user",user_message)}):
                    print(event.values())
                    for value in event.values():
                        print(value['messages'])
                        with st.chat_message("user"):
                            st.write(user_message)
                        with st.chat_message("assistant"):
                            st.write(value["messages"].content)
        elif usecase == "Chatbot with Tool":
            initial_state = {"messages": [user_message]}
            res = graph.invoke(initial_state)
            # print(res)
            for message in res["messages"]:
                if type(message) == HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message) == ToolMessage:
                    with st.chat_message("ai"):
                        st.write("tool call start")
                        st.write(f"🤖 Tool used: {message.name}")
                        st.write(f"Tool output: {message.content}")
                        st.write("tool call end")
                elif type(message) == AIMessage and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)
                        
        elif usecase == "AI News":
            frequency = self.user_message
            with st.spinner("Fetching and summarizing news... ⏳"):
                result = graph.invoke({"messages": frequency})
                try:
                    # Read the markdown file
                    AI_NEWS_PATH = f"./AINEWS/ai_news_summary_{frequency.lower()}.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()

                    # Display the markdown content in Streamlit
                    st.markdown(markdown_content, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    
        elif usecase == "Movie Recommender":
            user_input = self.user_message
            message = HumanMessage(content=f"Recommend {user_input.get('num_recommendations', 0)} movies in {user_input.get('genre', '')} genre, released in {user_input.get('year', '')}, language {user_input.get('language','English')}. Provide the recommendations in a structured format including title, genre, year,cast(main leads,director),synopsis, rating, and a brief description.")
            with st.spinner("Fetching movie recommendations... ⏳"):
                result = graph.invoke({"messages": [message]})
                print("result:",result)
                try:
                    # Read the markdown file
                    MOVIE_RECOMMENDATIONS_PATH = "./MRs/movie_recommendations.md"
                    with open(MOVIE_RECOMMENDATIONS_PATH, "r", encoding="utf-8") as file:
                        markdown_content = file.read()

                    # Display the markdown content in Streamlit
                    st.markdown(markdown_content, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"Movie Recommendations Not Generated or File not found: {MOVIE_RECOMMENDATIONS_PATH}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")