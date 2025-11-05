from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_community.tools.tavily_search import TavilySearchResults
@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

def get_tools():
    """Returns a list of available tools."""
    tavily_tool = TavilySearchResults(max_results=3)
    tools = [add_numbers, multiply_numbers, tavily_tool]
    return tools

def create_tool_node(tools):
    """Creates a ToolNode for the given tool."""
    return ToolNode(tools=tools)


