import requests
from bs4 import BeautifulSoup
import json
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
BASE_URL = "https://www.wcrj.net"
ARTICLE_URL = "https://www.wcrj.net/article/"
VALID_STATUS_CODE = 200
FILE_PATH="output/"

@dataclass
class Article:
    heading: str
    topic: List[str]
    categories: List[str]
    authors: List[str]
    url_id:List[str]
    
    

class WebScraper:
    def __init__(self):
        self.session = requests.Session()

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url,timeout=50)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logging.error(f"Failed to fetch {url}: {e}")
            return None

    def parse_articles(self, soup: BeautifulSoup) -> List[Article]:
        articles = []
        headers = soup.select("header h2")
        footers = soup.select("footer")
        author_sections = soup.select('.article-authors')
        article_ids=soup.select("header h2 a")

        for header, footer, author_section,article_id in zip(headers, footers, author_sections,article_ids):
            heading = header.text.strip()
            topics = [tag.text for tag in footer.select('[rel="category tag"]')]
            categories = [tag.text for tag in footer.select('[rel="tag"]')]
            authors = [author.text for author in author_section.select('.author-trigger')]
            id=article_id.get('href').split('/')[-1:]
            articles.append(Article(heading, topics, categories, authors,id))
            
         
        return articles

    def scrape_abstract(self, url: str,url_id:str) -> Dict[str, str]:
        soup = self.fetch_page(url)
        if not soup:
            return {}

        abstract_section = soup.find(class_="abstract-single")
        if not abstract_section:
            logging.warning(f"No abstract found for {url}")
            return {}  
        sections = abstract_section.text.strip()
        abstract_dict = {"key":url_id}
        if url_id in '1636':
            pass
        elif url_id in ['1852']: 
            sections = sections.split('\n')
            for section in sections:
                key, content = section.split(': ', 1)
                abstract_dict[key.strip()] = content.strip()
          
        elif url_id in ['2157']:
            sections = sections = sections.split('\n\n\n')
            for section in sections:
                key, content = section.split(': ', 1)
                abstract_dict[key.strip().replace("\n","")] = content.strip().replace("\n","")
        else:
            sections=sections.split('\n\n')    
            for section in sections:
                key, content = section.split(': ', 1)
                abstract_dict[key.strip()] = content.strip()
        print("Sucess",url_id) 

        return abstract_dict

def save_to_json(data: Dict, filename: str):
    with open(FILE_PATH+filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    scraper = WebScraper()
    url = f"{BASE_URL}/topic/haematological-oncology"
    
    soup = scraper.fetch_page(url)
    if not soup:
        logging.error("Failed to fetch the main page. Exiting.")
        return

    articles = scraper.parse_articles(soup)
    
    # Save article data
    save_to_json([vars(article) for article in articles], 'articles.json')
    
    #Scrape abstracts
    abstracts = []
    for article in articles:
        article_url = f"{ARTICLE_URL}{article.url_id[0].lower()}"
        abstract = scraper.scrape_abstract(article_url,article.url_id[0])
        abstracts.append(abstract)
    
    # Save abstracts
    save_to_json(abstracts, 'abstracts.json')

if __name__ == "__main__":
    main()