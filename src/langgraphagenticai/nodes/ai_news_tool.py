from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class AINewsToolNode:
    """Node to fetch and summarize latest AI news using external APIs"""
    def __init__(self, llm):
        self.llm = llm
        self.tavily = TavilyClient()
        self.data = {}
        
    def fetch_news(self, data: dict)->dict:
        """Fetch latest AI news based on the selected timeframe using external APIs"""
        # Placeholder for actual API call to fetch news
        frequency = data['messages'][0].content.lower()
        self.data['frequency'] = frequency
        time_range_map = {'daily': 'd','weekly':'w','monthly':'m','year':'y'}
        days_map = {'daily': 1,'weekly':7,'monthly':30,'year':366}
        
        response = self.tavily.search(
            query="Top Artificial Intelligence (AI) technology news India and globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=20,
            days=days_map[frequency],
            # include_domains=["techcrunch.com", "venturebeat.com/ai", ...]  # Uncomment and add domains if needed
        )
        data['news_data'] = response.get('results', [])
        self.data['news_data'] = data['news_data']
        print(self.data['news_data'])
        return data

    def summarize_news(self, data: dict) -> dict:
        """Summarize the fetched news articles using the LLM"""
        news_items = self.data['news_data']
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize AI news articles into markdown format. For each item include:
            - Date in **YYYY-MM-DD** format in IST timezone
            - Concise sentences summary from latest news
            - Sort news by date wise (latest first)
            - Source URL as link
            Use format:
            ### [Date]
            - [Summary](URL)"""),
            ("user", "Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])
        formatted_prompt = prompt_template.format_prompt(articles=articles_str)
        summary = self.llm.invoke(formatted_prompt)
        data['summary'] = summary.content
        self.data['summary'] = data['summary']
        return self.data
    
    def save_news(self, data):
        """Save or display the summarized news"""
        # Placeholder for saving or displaying the summary
        frequency = self.data['frequency']
        summary = self.data['summary']
        filename = f"./AINEWS/ai_news_summary_{frequency}.md"
        with open(filename, 'w') as f:
            f.write(f"# AI News Summary - {frequency.capitalize()}\n\n")
            f.write(summary)
        self.data['file_path'] = filename
        return self.data