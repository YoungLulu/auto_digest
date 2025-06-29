import arxiv
import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any
from pathlib import Path


class ArxivFetcher:
    def __init__(self, keywords_file: str = "collector/keywords.json"):
        self.keywords_file = Path(keywords_file)
        self.load_keywords()
    
    def load_keywords(self):
        with open(self.keywords_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.keywords = config["keywords"]
            self.categories = config["arxiv_categories"]
    
    def build_query(self, days_back: int = 30) -> str:
        keyword_queries = []
        for keyword in self.keywords:
            keyword_queries.append(f'all:"{keyword}"')
        
        category_queries = []
        for cat in self.categories:
            category_queries.append(f'cat:{cat}')
        
        keyword_part = " OR ".join(keyword_queries)
        category_part = " OR ".join(category_queries)
        
        return f"({keyword_part}) AND ({category_part})"
    
    def fetch_papers(self, max_results: int = 100, days_back: int = 30) -> List[Dict[str, Any]]:
        query = self.build_query(days_back)
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        papers = []
        for result in client.results(search):
            if result.published.replace(tzinfo=None) < cutoff_date:
                continue
                
            paper_data = {
                "id": self._generate_id(result.title, result.authors, result.published),
                "title": result.title,
                "authors": [str(author) for author in result.authors],
                "abstract": result.summary,
                "url": result.entry_id,
                "pdf_url": result.pdf_url,
                "published": result.published.isoformat(),
                "categories": result.categories,
                "source": "arxiv"
            }
            papers.append(paper_data)
        
        return papers
    
    def _generate_id(self, title: str, authors: List, published: datetime) -> str:
        content = f"{title}_{[str(a) for a in authors]}_{published.date()}"
        return hashlib.md5(content.encode()).hexdigest()[:16]


if __name__ == "__main__":
    fetcher = ArxivFetcher()
    papers = fetcher.fetch_papers(max_results=50)
    print(f"Found {len(papers)} papers")
    for paper in papers[:3]:
        print(f"- {paper['title']}")