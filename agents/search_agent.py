from tools.search_tool import web_search
from loguru import logger

def search_node(state):
    query = state["query"]
    logger.info(f"Search Agent: Running query '{query}'")
    
    results = web_search(query)
    
    # Return as list so Annotated operator.add can append it
    return {
        "search_results": results
    }