from langchain_core.prompts import ChatPromptTemplate
from tavily import TavilyClient
import json

class MovieBotNode:
    """Node to recommend movies based on user preferences using external APIs"""
    def __init__(self, llm):
        self.llm = llm
        self.tavily = TavilyClient()
        self.data = {}
        
    def movie_recommendation(self, data: dict) -> dict:
        """Fetch movie recommendations based on genre, release year, language, and number of recommendations"""
        # data = data['messages'][0].content
        print(data,type(data))
        # data = json.loads(data)
        # genre = data.get('genre', '')
        # year = data.get('year', '')
        # language = data.get('language', '')
        # num_recommendations = data.get('num_recommendations', '')
        
        query = "As you've access to all movie contents" + data["messages"][0].content + "Note:strictly,Fetch movie recommendations based on genre, release year, language, and number of recommendations"
        print(query)
        response = self.tavily.search(
            query=query,
            topic="general",
            include_answer="advanced"
        )
        
        data['movie_data'] = response.get('results', [])
        print(data['movie_data'])
        self.data['movie_data'] = data['movie_data']
        print(self.data['movie_data'])
        return data

    def summarize_movies(self, data: dict) -> dict:
        """Summarize the fetched movie recommendations using the LLM"""
        movie_items = self.data['movie_data']
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize movie recommendations into markdown format. For each item include:
            - Movie Title
            - Release Year
            - Genre
            - Cast & Crew
            - Language
            - Brief Description
            - Source URL as link
            Use format:
            ### Movie Title (Release Year)
            - Genre: [Genre]
            - Language: [Language]
            - Cast & Crew: [Cast & Crew]
            - Synopsis: [Brief Description]
            - [Source URL](URL)
            Note:strictly,Fetch movie recommendations based on genre, release year, language, and number of recommendations.Don't show prompt details,just show the recommendations in a specified format and also ensure there are no empty fields in the output. If any field is missing in the data, omit that field from the output for that movie."
            """),
            ("user", "Movies:\n{movies}")
        ])
        prompt_formatted = prompt_template.format_prompt(movies="\n\n".join([
            f"Title: {item.get('title', '')}\nYear: {item.get('year', '')}\nGenre: {item.get('genre', '')}\nLanguage: {item.get('language', '')}\nDescription: {item.get('description', '')}\nURL: {item.get('url', '')}"
            for item in movie_items
        ]))
        print(prompt_formatted)
        aligned_content = self.llm.invoke(prompt_formatted)
        # print(aligned_content.content)
        data['aligned_content'] = aligned_content.content   
        self.data['aligned_content'] = data['aligned_content']
        return self.data
    
    def save_recommendations(self, data: dict) -> dict:
        """Save the summarized movie recommendations to a markdown file"""
        aligned_content = self.data.get('aligned_content', '')
        with open("./MRs/movie_recommendations.md", "w", encoding="utf-8") as file:
            file.write("# Movie Recommendations\n\n")
            file.write(aligned_content)
        return data