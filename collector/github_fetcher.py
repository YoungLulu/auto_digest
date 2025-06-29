import json
import hashlib
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path
import time


class GitHubFetcher:
    def __init__(self, keywords_file: str = "collector/keywords.json", token: Optional[str] = None):
        self.keywords_file = Path(keywords_file)
        self.token = token
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AI-Code-Digest-Bot"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
        
        self.load_keywords()
    
    def load_keywords(self):
        with open(self.keywords_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.keywords = config["keywords"]
            self.github_topics = config.get("github_topics", [])
    
    def build_search_queries(self, days_back: int = 7) -> List[str]:
        cutoff_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        queries = []
        
        # Topic-based queries
        for topic in self.github_topics:
            query = f"topic:{topic} stars:>20 created:>{cutoff_date}"
            queries.append(query)
        
        # Keyword-based queries in description
        for keyword in self.keywords[:5]:  # Limit to avoid API rate limits
            query = f'"{keyword}" in:description,readme stars:>10 created:>{cutoff_date} fork:false'
            queries.append(query)
        
        return queries
    
    def fetch_repositories(self, max_per_query: int = 20, days_back: int = 7) -> List[Dict[str, Any]]:
        queries = self.build_search_queries(days_back)
        all_repos = []
        seen_ids = set()
        
        for query in queries:
            try:
                repos = self._search_repositories(query, max_per_query)
                for repo in repos:
                    if repo["id"] not in seen_ids:
                        all_repos.append(repo)
                        seen_ids.add(repo["id"])
                
                # Rate limiting - GitHub allows 30 requests per minute for search
                time.sleep(2)
                
            except Exception as e:
                print(f"Error fetching repositories for query '{query}': {e}")
                continue
        
        return all_repos
    
    def _search_repositories(self, query: str, per_page: int = 20) -> List[Dict[str, Any]]:
        url = "https://api.github.com/search/repositories"
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": min(per_page, 100)
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 403:
            print("GitHub API rate limit exceeded")
            return []
        
        response.raise_for_status()
        data = response.json()
        
        repos = []
        for item in data.get("items", []):
            repo_data = {
                "id": self._generate_id(item["full_name"], item["created_at"]),
                "name": item["name"],
                "full_name": item["full_name"],
                "description": item.get("description", ""),
                "url": item["html_url"],
                "stars": item["stargazers_count"],
                "forks": item["forks_count"],
                "language": item.get("language", ""),
                "topics": item.get("topics", []),
                "created_at": item["created_at"],
                "updated_at": item["updated_at"],
                "owner": item["owner"]["login"],
                "source": "github"
            }
            repos.append(repo_data)
        
        return repos
    
    def _generate_id(self, full_name: str, created_at: str) -> str:
        content = f"{full_name}_{created_at}"
        return hashlib.md5(content.encode()).hexdigest()[:16]


if __name__ == "__main__":
    # Test without token (limited rate)
    fetcher = GitHubFetcher()
    repos = fetcher.fetch_repositories(max_per_query=10)
    print(f"Found {len(repos)} repositories")
    for repo in repos[:3]:
        print(f"- {repo['full_name']} ({repo['stars']} stars)")