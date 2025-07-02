import requests
from bs4 import BeautifulSoup

class WebSearchService:
    def __init__(self, searxng_url="http://localhost:8888"): # Default SearXNG URL
        self.searxng_url = searxng_url

    def search(self, query):
        try:
            params = {
                "q": query,
                "format": "json"
            }
            response = requests.get(f"{self.searxng_url}/search", params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            results = response.json()
            return self._parse_results(results)
        except requests.exceptions.RequestException as e:
            print(f"Error during SearXNG search: {e}")
            return None

    def _parse_results(self, raw_results):
        parsed_results = []
        for result in raw_results.get("results", []):
            parsed_results.append({
                "title": result.get("title"),
                "url": result.get("url"),
                "snippet": result.get("content"),
                "engine": result.get("engine"),
            })
        return parsed_results

    def scrape_article(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # Attempt to extract main content. This is a simplified approach.
            # More sophisticated methods would involve analyzing common article structures.
            paragraphs = soup.find_all('p')
            article_text = '\n'.join([p.get_text() for p in paragraphs])
            return article_text
        except requests.exceptions.RequestException as e:
            print(f"Error scraping article from {url}: {e}")
            return None

    def add_to_search_history(self, query, results):
        # Placeholder for adding to search history
        print(f"Adding to search history: {query}")

    def get_search_history(self):
        # Placeholder for retrieving search history
        print("Retrieving search history")
        return []

    def save_search(self, query, results, name):
        # Placeholder for saving a search
        print(f"Saving search '{name}': {query}")

    def get_saved_searches(self):
        # Placeholder for retrieving saved searches
        print("Retrieving saved searches")
        return []
