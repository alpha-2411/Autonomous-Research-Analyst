from newspaper import Article, Config
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger
import asyncio
from concurrent.futures import ThreadPoolExecutor

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def scrape_url(url: str) -> dict:
    """Synchronous URL scraping with retry logic."""
    try:
        config = Config()
        config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        config.request_timeout = 15
        
        article = Article(url, config=config)
        article.download()
        article.parse()
        
        return {
            "title": article.title,
            "text": article.text[:3000],
            "url": url
        }
    except Exception as e:
        logger.warning(f"Failed to extract article from {url}: {e}")
        raise e  # trigger retry

def extract_article(url: str) -> dict:
    """Extract an article with fallback."""
    try:
        logger.info(f"Scraping URL: {url}")
        return scrape_url(url)
    except Exception as e:
        logger.error(f"Final Extraction Error for {url}: {e}")
        return {
            "title": "Error",
            "text": str(e),
            "url": url
        }

async def extract_articles_async(urls: list[str]) -> list[dict]:
    """Extract multiple articles concurrently."""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        tasks = [loop.run_in_executor(pool, extract_article, url) for url in urls]
        results = await asyncio.gather(*tasks)
    return results