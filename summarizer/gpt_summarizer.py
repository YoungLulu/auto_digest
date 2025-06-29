import json
import openai
from typing import List, Dict, Any, Optional
from pathlib import Path
import time
import re
from .scoring_system import ComprehensiveScorer


class GPTSummarizer:
    def __init__(self, config: dict = None, api_key: Optional[str] = None, model: str = None, base_url: Optional[str] = None):
        # Load configuration
        if config is None:
            config_path = Path("config.json")
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        self.config = config["llm"]
        
        # Use provided parameters or fall back to config
        provider = self.config.get("provider", "openrouter")
        model = model or self.config.get("model", "gpt-3.5-turbo")
        
        # Initialize client based on provider
        self.client = self._initialize_client(provider, api_key, base_url)
        self.model = model
        self.prompt_template = self.load_prompt_template()
        self.scorer = ComprehensiveScorer()
    
    def _initialize_client(self, provider: str, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize the appropriate LLM client based on provider"""
        import os
        
        providers_config = self.config.get("providers", {})
        
        if provider in providers_config:
            provider_config = providers_config[provider]
            api_key = api_key or os.getenv(provider_config["api_key_env"])
            base_url = base_url or provider_config["base_url"]
        else:
            # Fallback to legacy config
            api_key = api_key or os.getenv(self.config.get("api_key_env", "OPENAI_API_KEY"))
            base_url = base_url or self.config.get("base_url")
        
        if not api_key:
            print(f"Warning: No API key found for provider '{provider}'. LLM features will be disabled.")
            return None
        
        try:
            client = openai.OpenAI(
                api_key=api_key,
                base_url=base_url
            )
            return client
        except Exception as e:
            print(f"Error initializing LLM client for provider '{provider}': {e}")
            return None
    
    def load_prompt_template(self) -> str:
        template_path = Path("summarizer/prompt_templates/classify_summarize.txt")
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # Fallback template
            return """Analyze this content and provide a JSON summary with: title, url, background, technical_highlights, potential_applications, target_audience, category_tags, relevance_score, summary.

Content:
Title: {title}
Description: {description}
URL: {url}
Source: {source}

Respond with valid JSON only."""
    
    def summarize_items(self, items: List[Dict[str, Any]], batch_size: int = 5) -> List[Dict[str, Any]]:
        if not self.client:
            print("Warning: No API key provided. Using mock summaries.")
            return self._generate_mock_summaries(items)
        
        summarized_items = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            for item in batch:
                try:
                    summary = self._summarize_single_item(item)
                    if summary:
                        summarized_items.append(summary)
                    
                    # Rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error summarizing item '{item.get('title', 'Unknown')}': {e}")
                    # Add original item with minimal processing
                    fallback_summary = self._create_fallback_summary(item)
                    summarized_items.append(fallback_summary)
        
        return summarized_items
    
    def _summarize_single_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Prepare content for prompt
        title = item.get("title", "No title")
        description = item.get("description") or item.get("abstract", "No description available")
        url = item.get("url", "")
        source = item.get("source", "unknown")
        
        # Additional info based on source
        additional_info = ""
        if source == "github":
            additional_info = f"Stars: {item.get('stars', 0)}, Language: {item.get('language', 'N/A')}, Topics: {item.get('topics', [])}"
        elif source == "arxiv":
            additional_info = f"Authors: {item.get('authors', [])}, Categories: {item.get('categories', [])}"
        
        # Format prompt
        prompt = self.prompt_template.format(
            title=title,
            description=description[:2000],  # Limit description length
            url=url,
            source=source,
            additional_info=additional_info
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert AI research analyst. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean and parse JSON
            content = self._clean_json_response(content)
            summary_data = json.loads(content)
            
            # Extract scoring dimensions from LLM response
            scoring_dimensions = summary_data.get("scoring_dimensions", {})
            
            # Calculate comprehensive score using the scoring system
            comprehensive_scores = self.scorer.calculate_comprehensive_score(item, scoring_dimensions)
            
            # Add comprehensive scoring information
            summary_data["comprehensive_scores"] = comprehensive_scores
            summary_data["final_score"] = comprehensive_scores["final_score"]
            
            # Add original item data
            summary_data["original_id"] = item.get("id")
            summary_data["source"] = source
            summary_data["original_data"] = item
            
            return summary_data
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response content: {content}")
            return None
        except Exception as e:
            print(f"API error: {e}")
            return None
    
    def _clean_json_response(self, content: str) -> str:
        # Remove markdown code blocks if present
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'```\s*$', '', content)
        
        # Remove any leading/trailing non-JSON content
        start = content.find('{')
        end = content.rfind('}') + 1
        
        if start != -1 and end > start:
            content = content[start:end]
        
        return content
    
    def _generate_mock_summaries(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        mock_summaries = []
        
        for item in items:
            summary = self._create_fallback_summary(item)
            mock_summaries.append(summary)
        
        return mock_summaries
    
    def _create_fallback_summary(self, item: Dict[str, Any]) -> Dict[str, Any]:
        title = item.get("title", "No title")
        description = item.get("description") or item.get("abstract", "No description available")
        
        # Basic keyword-based classification
        category_tags = self._classify_by_keywords(title, description)
        relevance_score = self._estimate_relevance(title, description)
        
        # Create fallback scoring dimensions
        fallback_scoring = {
            "technical_innovation": 5.0,
            "application_value": 5.0,
            "readability": 5.0,
            "experimental_thoroughness": 5.0
        }
        
        # Calculate comprehensive score for fallback
        comprehensive_scores = self.scorer.calculate_comprehensive_score(item, fallback_scoring)
        
        return {
            "title": title,
            "url": item.get("url", ""),
            "authors": item.get("authors", []) if item.get("source") == "arxiv" else [item.get("url", "").split("/")[-2] if "/" in item.get("url", "") else "Unknown"],
            "background": "Analysis not available - manual review needed",
            "technical_highlights": ["Manual analysis required"],
            "potential_applications": ["To be determined"], 
            "target_audience": "AI researchers and developers",
            "category_tags": category_tags,
            "relevance_score": relevance_score,
            "summary": f"Manual summary needed for: {title[:100]}...",
            "scoring_dimensions": fallback_scoring,
            "comprehensive_scores": comprehensive_scores,
            "final_score": comprehensive_scores["final_score"],
            "original_id": item.get("id"),
            "source": item.get("source", "unknown"),
            "original_data": item
        }
    
    def _classify_by_keywords(self, title: str, description: str) -> List[str]:
        """Basic keyword-based classification for fallback."""
        text = f"{title} {description}".lower()
        
        # Define keyword patterns for each category
        patterns = {
            "code_generation": ["code generation", "code synthesis", "program generation", "automatic programming"],
            "code_evaluation": ["code evaluation", "code assessment", "code quality", "code metrics", "code analysis"],
            "code_verification": ["code verification", "formal verification", "program verification", "correctness"],
            "program_synthesis": ["program synthesis", "synthesis", "automated synthesis"],
            "coding_agent": ["coding agent", "programming agent", "software agent", "ai agent", "autonomous"],
            "llm_coding": ["llm", "large language model", "language model", "gpt", "transformer", "neural"],
            "automated_testing": ["test generation", "automated testing", "unit test", "test case"],
            "software_reasoning": ["reasoning", "logic", "inference", "proof", "symbolic"],
            "code_repair": ["code repair", "bug fix", "program repair", "debugging", "error correction"],
            "neural_search": ["code search", "semantic search", "code retrieval", "neural search"],
            "benchmark": ["benchmark", "evaluation", "dataset", "corpus", "leaderboard"],
            "survey": ["survey", "review", "analysis", "study", "empirical"],
            "tool": ["tool", "framework", "library", "system", "platform", "implementation"]
        }
        
        matched_categories = []
        for category, keywords in patterns.items():
            if any(keyword in text for keyword in keywords):
                matched_categories.append(category)
        
        # Return top 2 matches, or "other" if no matches
        return matched_categories[:2] if matched_categories else ["other"]
    
    def _estimate_relevance(self, title: str, description: str) -> int:
        """Estimate relevance score based on keywords."""
        text = f"{title} {description}".lower()
        
        # High relevance keywords
        high_relevance = ["code generation", "llm", "programming", "software engineering", "automated", "ai coding"]
        medium_relevance = ["machine learning", "neural", "algorithm", "development", "programming language"]
        
        high_score = sum(1 for keyword in high_relevance if keyword in text)
        medium_score = sum(1 for keyword in medium_relevance if keyword in text)
        
        if high_score >= 2:
            return 8
        elif high_score >= 1:
            return 7
        elif medium_score >= 2:
            return 6
        elif medium_score >= 1:
            return 5
        else:
            return 4


if __name__ == "__main__":
    # Test with mock data
    summarizer = GPTSummarizer()
    
    test_items = [
        {
            "id": "test1",
            "title": "Automated Code Generation with Large Language Models",
            "abstract": "This paper presents a novel approach to automated code generation using LLMs...",
            "url": "https://arxiv.org/abs/2024.test",
            "source": "arxiv"
        }
    ]
    
    summaries = summarizer.summarize_items(test_items)
    print(f"Generated {len(summaries)} summaries")
    print(json.dumps(summaries[0], indent=2))
