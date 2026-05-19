from ddgs import DDGS
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def execute_search_query(query: str, num_results: int) -> list:
    """Execute the DDGS search query with retry logic."""
    results_list = []
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=num_results)
        for result in results:
            results_list.append({
                "title": result.get("title"),
                "link": result.get("href"),
                "snippet": result.get("body")
            })
    return results_list

def web_search(query: str, num_results: int = 5) -> list:
    """Perform a web search using DuckDuckGo."""
    try:
        logger.info(f"Performing web search for: '{query}'")
        return execute_search_query(query, num_results)
    except Exception as e:
        logger.error(f"Search Error for query '{query}': {e}")
        return []