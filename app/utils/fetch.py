import requests
from bs4 import BeautifulSoup
import logging

def fetch_and_clean_html(url):
    """
    Fetches content from a URL and cleans it from script and style tags.
    Returns cleaned HTML as a string.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Use BeautifulSoup to parse and clean the HTML
        soup = BeautifulSoup(response.text, 'lxml')

        # Remove all script and style tags
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        clean_html = str(soup)
        return clean_html

    except requests.RequestException as e:
        logging.error(f'Failed to fetch URL {url}: {e}')
        raise
