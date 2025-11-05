import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graph.smartchatbot import Graphbuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.
    """

    ##load ui
    ui = LoadStreamlitUI()
    
    user_input=ui.load_streamlitui()
    print(ui.user_controls)
    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    if st.session_state.IsFetchButtonClicked and user_input.get("selected_usecase") == "AI News":
        user_message = st.session_state.timeframe
    elif st.session_state.IsFetchButtonClicked and  user_input.get("selected_usecase") == "Movie Recommender":
        user_message = {
            "genre": st.session_state.get("movie_genre", ""),
            "num_recommendations": st.session_state.get("num_recommendations", ""),
            "year": st.session_state.get("year", ""),
            "language": st.session_state.get("language","")  # Default language; can be modified to take user input if needed
        }
    else:
        user_message = st.chat_input("Enter your message:")
    
    if user_message:
        try:
            model_obj = GroqLLM(user_input)
            model = model_obj.load_llm()
            
            if not model:
                st.error(f"The model is not found or deprecated:{model}")
                return
            
            #Initialize the use case option and setup the graph accordingly
            usecase = user_input.get("selected_usecase")
            
            graph_builder = Graphbuilder(model)
            try:
                graph = graph_builder.set_graph_state(usecase)
                # print(user_message)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
                
            except Exception as e:
                st.error(f"Error: Graph set up failed here-{e}")
                return
        except e:
            print(f"Error: Graph set up failed- {e}")
            return
            
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    '''if user_message:
        try:
            ## Configure The LLM's
            obj_llm_config=GroqLLM(user_contols_input=user_input)
            model=obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized")
                return
            
            # Initialize and set up the graph based on use case
            usecase=user_input.get("selected_usecase")

            if not usecase:
                    st.error("Error: No use case selected.")
                    return
            
            ## Graph Builder

            graph_builder=GraphBuilder(model)
            try:
                 graph=graph_builder.setup_graph(usecase)
                 print(user_message)
                 DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                 st.error(f"Error: Graph set up failed- {e}")
                 return

        except Exception as e:
             st.error(f"Error: Graph set up failed- {e}")
             return  ''' 
