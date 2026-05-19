from tools.scraper_tool import extract_articles_async
import asyncio
from loguru import logger

def extraction_node(state):
    search_results = state.get("search_results", [])
    
    if not search_results:
        logger.warning("Extraction Agent: No search results found.")
        return {"extracted_content": []}
    
    # Get top 3 latest URLs from search results to avoid too many requests
    # Since search_results accumulates, we take the last iteration's results.
    # To keep it simple, we just process all new ones if we had a mechanism,
    # but here we'll just process the last 3 results added.
    urls_to_scrape = [res.get("link") for res in search_results[-3:] if res.get("link")]
    
    logger.info(f"Extraction Agent: Scraping {len(urls_to_scrape)} URLs concurrently...")
    
    try:
        extracted_articles = asyncio.run(extract_articles_async(urls_to_scrape))
    except RuntimeError:
        # If event loop is already running (e.g., in Streamlit), we use nest_asyncio or create new loop
        import nest_asyncio
        nest_asyncio.apply()
        extracted_articles = asyncio.run(extract_articles_async(urls_to_scrape))
        
    logger.info(f"Extraction Agent: Successfully extracted {len(extracted_articles)} articles.")
    
    return {
        "extracted_content": extracted_articles
    }