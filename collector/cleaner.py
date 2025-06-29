import hashlib
import re
from typing import List, Dict, Any, Set
from datetime import datetime


class DataCleaner:
    def __init__(self):
        self.seen_hashes = set()
    
    def clean_and_deduplicate(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cleaned_data = []
        
        for item in data_list:
            # Clean the item
            cleaned_item = self._clean_item(item)
            
            # Check for duplicates
            item_hash = self._generate_content_hash(cleaned_item)
            if item_hash not in self.seen_hashes:
                self.seen_hashes.add(item_hash)
                cleaned_data.append(cleaned_item)
        
        return cleaned_data
    
    def _clean_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        cleaned = item.copy()
        
        # Clean title
        if "title" in cleaned:
            cleaned["title"] = self._clean_text(cleaned["title"])
        
        # Clean description/abstract
        if "description" in cleaned:
            cleaned["description"] = self._clean_text(cleaned["description"])
        if "abstract" in cleaned:
            cleaned["abstract"] = self._clean_text(cleaned["abstract"])
        
        # Normalize dates
        for date_field in ["published", "created_at", "updated_at"]:
            if date_field in cleaned and cleaned[date_field]:
                cleaned[date_field] = self._normalize_date(cleaned[date_field])
        
        # Clean and validate URLs
        if "url" in cleaned:
            cleaned["url"] = self._clean_url(cleaned["url"])
        if "pdf_url" in cleaned:
            cleaned["pdf_url"] = self._clean_url(cleaned["pdf_url"])
        
        return cleaned
    
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common formatting artifacts
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\t+', ' ', text)
        
        # Clean up common academic paper artifacts
        text = re.sub(r'\s*\\\w+\s*', ' ', text)  # LaTeX commands
        text = re.sub(r'\$[^$]*\$', '[MATH]', text)  # Math expressions
        
        return text.strip()
    
    def _normalize_date(self, date_str: str) -> str:
        try:
            # Handle various date formats
            if 'T' in date_str:
                # ISO format
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                # Try parsing common formats
                for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S']:
                    try:
                        dt = datetime.strptime(date_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return date_str  # Return original if can't parse
            
            return dt.isoformat()
        except Exception:
            return date_str
    
    def _clean_url(self, url: str) -> str:
        if not url:
            return ""
        
        # Ensure URL has proper protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return url.strip()
    
    def _generate_content_hash(self, item: Dict[str, Any]) -> str:
        # Generate hash based on key identifying fields
        if item.get("source") == "arxiv":
            content = f"{item.get('title', '')}_{item.get('authors', [])}_{item.get('published', '')}"
        else:  # GitHub
            content = f"{item.get('full_name', '')}_{item.get('created_at', '')}"
        
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def filter_by_relevance(self, items: List[Dict[str, Any]], keywords: List[str]) -> List[Dict[str, Any]]:
        relevant_items = []
        
        for item in items:
            if self._is_relevant(item, keywords):
                relevant_items.append(item)
        
        return relevant_items
    
    def _is_relevant(self, item: Dict[str, Any], keywords: List[str]) -> bool:
        # Combine relevant text fields
        text_fields = []
        if item.get("title"):
            text_fields.append(item["title"].lower())
        if item.get("description"):
            text_fields.append(item["description"].lower())
        if item.get("abstract"):
            text_fields.append(item["abstract"].lower())
        
        combined_text = " ".join(text_fields)
        
        # Check if any keyword appears in the text
        for keyword in keywords:
            if keyword.lower() in combined_text:
                return True
        
        return False


if __name__ == "__main__":
    # Test the cleaner
    cleaner = DataCleaner()
    
    test_data = [
        {
            "title": "  Code Generation with  AI  ",
            "description": "This  is  a  test\n\ndescription  ",
            "url": "github.com/test/repo",
            "created_at": "2024-01-01T12:00:00Z",
            "source": "github"
        }
    ]
    
    cleaned = cleaner.clean_and_deduplicate(test_data)
    print("Cleaned data:", cleaned)