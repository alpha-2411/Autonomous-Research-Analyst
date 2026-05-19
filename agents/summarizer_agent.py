from config.llm_config import get_llm
from prompts.research_prompts import SUMMARIZER_PROMPT
from loguru import logger

def summarizer_node(state):
    articles = state.get("extracted_content", [])
    rankings = state.get("source_rankings", "")
    
    if not articles:
        logger.warning("Summarizer Agent: No research evidence found.")
        return {
            "research_summary": "No research evidence could be gathered."
        }
        
    logger.info("Summarizer Agent: Generating comprehensive summary...")

    combined_text = ""
    for article in articles:
        combined_text += f"\nTITLE: {article.get('title')}\nCONTENT: {article.get('text')}\n"
        
    if rankings:
        combined_text += f"\nSOURCE RANKINGS CONTEXT:\n{rankings}\n"

    llm = get_llm()
    prompt = SUMMARIZER_PROMPT.format(combined_text=combined_text)
    
    response = llm.invoke(prompt)
    
    return {
        "research_summary": response.content
    }