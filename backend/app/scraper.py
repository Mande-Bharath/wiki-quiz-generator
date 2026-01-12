import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


def validate_wikipedia_url(url: str) -> bool:
    """
    Validate that the URL is a Wikipedia article URL
    """
    return "wikipedia.org/wiki/" in url


def scrape_wikipedia(url: str) -> dict:
    """
    Scrape Wikipedia article title and main text content
    
    Args:
        url: Wikipedia article URL
        
    Returns:
        Dictionary with title, content, and optionally raw_html
    """
    # Validate URL
    if not validate_wikipedia_url(url):
        raise ValueError("Invalid Wikipedia URL. Must be from wikipedia.org/wiki/")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        raise ValueError(f"Failed to fetch Wikipedia article: {str(e)}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title
    title_element = soup.find("h1")
    if not title_element:
        raise ValueError("Could not find article title")
    
    title = title_element.get_text(strip=True)

    # Extract main content (paragraphs)
    # Remove script and style tags first
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get main content area
    main_content = soup.find("div", {"id": "mw-content-text"})
    if not main_content:
        main_content = soup.find("div", {"class": "mw-parser-output"})
    
    if main_content:
        paragraphs = main_content.find_all("p")
    else:
        paragraphs = soup.find_all("p")
    
    # Filter and join paragraphs
    content = " ".join(
        p.get_text(strip=True)
        for p in paragraphs
        if len(p.get_text(strip=True)) > 50
    )
    
    if not content:
        raise ValueError("Could not extract article content")

    logger.info(f"Successfully scraped {title} from {url}")

    return {
        "title": title,
        "content": content,
        "raw_html": response.text  # Store raw HTML for reference
    }
