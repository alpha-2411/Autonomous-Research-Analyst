from config.llm_config import get_llm
from loguru import logger

def ranking_node(state):
    """Evaluates the extracted sources and ranks them."""
    articles = state.get("extracted_content", [])
    if not articles:
        return {"source_rankings": "No sources to rank."}

    logger.info(f"Ranking Agent: Evaluating {len(articles)} sources...")
    
    llm = get_llm()
    
    prompt = "Evaluate the credibility and relevance of the following sources. Rank them from 1 to 10 and provide a brief justification for each.\n\n"
    for i, article in enumerate(articles, 1):
        prompt += f"Source {i}:\nTitle: {article.get('title')}\nURL: {article.get('url')}\nSnippet: {article.get('text')[:200]}\n\n"
        
    try:
        response = llm.invoke(prompt)
        rankings = response.content
    except Exception as e:
        logger.error(f"Ranking Error: {e}")
        rankings = "Error generating source rankings."
        
    return {
        "source_rankings": rankings
    }
