import aiohttp
import logging
from urllib.parse import quote_plus
from typing import Tuple, List
import os

# Configure logging
logger = logging.getLogger(__name__)

async def perform_web_search(query: str) -> Tuple[str, List[str]]:
    """
    Perform safe web search with error handling and validation
    
    Args:
        query: Search query (1-100 characters)
    
    Returns:
        Tuple containing (summary, list_of_links) or fallback values
    
    Raises:
        ValueError: For invalid input parameters
    """
    # Validate input
    if not query or len(query) > 100:
        raise ValueError("Query must be 1-100 characters")
    
    try:
        # Sanitize query
        encoded_query = quote_plus(query)
        api_key = os.getenv("SEARCH_API_KEY")
        
        async with aiohttp.ClientSession(
            headers={
                "User-Agent": "MySearchBot/1.0",
                "Authorization": f"Bearer {api_key}"
            },
            timeout=aiohttp.ClientTimeout(total=10)
        ) as session:
            url = f"https://api.searchengine.com/search?q={encoded_query}"
            
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

                # Validate response structure
                if not all(key in data for key in ["summary", "results"]):
                    logger.error("Invalid API response structure")
                    return "No summary available", []
                
                # Process results
                summary = data.get("summary", "No summary available")
                links = [result["url"] for result in data.get("results", [])[:3] if "url" in result]
                
                return summary, links

    except aiohttp.ClientError as e:
        logger.error(f"Network error: {str(e)}")
        return "Search service unavailable", []
    
    except (KeyError, ValueError) as e:
        logger.error(f"Data parsing error: {str(e)}")
        return "Error processing results", []
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "Search failed", []