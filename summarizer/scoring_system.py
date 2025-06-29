"""
Comprehensive Scoring System for AI Code Digest
Implements weighted scoring mechanism for research papers and GitHub repositories
"""

from typing import Dict, Any, List
import re
import logging


class ComprehensiveScorer:
    """
    Comprehensive scoring system with the following weights:
    - Popularity (GitHub stars/arXiv citations): 25%
    - Technical Innovation: 20% 
    - Application Value: 10%
    - Readability: 15%
    - Experimental Thoroughness: 15%
    - Author Influence: 15%
    """
    
    def __init__(self):
        self.weights = {
            'popularity': 0.25,
            'technical_innovation': 0.20,
            'application_value': 0.10,
            'readability': 0.15,
            'experimental_thoroughness': 0.15,
            'author_influence': 0.15
        }
        
        # Known influential organizations and conferences
        self.influential_orgs = {
            'google', 'microsoft', 'meta', 'openai', 'anthropic', 'deepmind',
            'stanford', 'mit', 'berkeley', 'cmu', 'harvard', 'oxford', 'cambridge',
            'nvidia', 'huggingface', 'salesforce', 'adobe', 'ibm', 'amazon',
            'tsinghua', 'peking', 'tencent', 'baidu', 'alibaba'
        }
        
        self.top_conferences = {
            'icml', 'neurips', 'iclr', 'aaai', 'ijcai', 'acl', 'emnlp', 'naacl',
            'cvpr', 'iccv', 'eccv', 'kdd', 'www', 'sigir', 'wsdm', 'icse', 'fse'
        }
        
        self.logger = logging.getLogger(__name__)
    
    def calculate_comprehensive_score(self, item: Dict[str, Any], llm_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate comprehensive score for an item
        
        Args:
            item: Original item data
            llm_scores: LLM-generated scores for technical_innovation, application_value, 
                       readability, experimental_thoroughness
        
        Returns:
            Dictionary with individual scores and final weighted score
        """
        scores = {}
        
        # 1. Popularity Score (25%) - from metadata
        scores['popularity'] = self._calculate_popularity_score(item)
        
        # 2-5. LLM-generated scores (60% total)
        scores['technical_innovation'] = llm_scores.get('technical_innovation', 5.0)
        scores['application_value'] = llm_scores.get('application_value', 5.0)
        scores['readability'] = llm_scores.get('readability', 5.0)
        scores['experimental_thoroughness'] = llm_scores.get('experimental_thoroughness', 5.0)
        
        # 6. Author Influence Score (15%) - from metadata
        scores['author_influence'] = self._calculate_author_influence_score(item)
        
        # Calculate weighted final score
        final_score = sum(scores[key] * self.weights[key] for key in self.weights.keys())
        
        return {
            'individual_scores': scores,
            'final_score': round(final_score, 2),
            'score_breakdown': {k: round(scores[k] * self.weights[k], 2) for k in self.weights.keys()}
        }
    
    def _calculate_popularity_score(self, item: Dict[str, Any]) -> float:
        """Calculate popularity score based on stars/citations"""
        source = item.get('source', 'unknown')
        
        if source == 'github':
            stars = item.get('stars', 0)
            # Logarithmic scale for GitHub stars
            if stars >= 10000:
                return 10.0
            elif stars >= 5000:
                return 9.0
            elif stars >= 1000:
                return 8.0
            elif stars >= 500:
                return 7.0
            elif stars >= 100:
                return 6.0
            elif stars >= 50:
                return 5.0
            elif stars >= 10:
                return 4.0
            else:
                return 3.0
        
        elif source == 'arxiv':
            # For arXiv, we estimate based on publication date and venue mentions
            abstract = item.get('abstract', '').lower()
            title = item.get('title', '').lower()
            
            # Check for conference mentions
            conference_score = 0
            for conf in self.top_conferences:
                if conf in abstract or conf in title:
                    conference_score = 2
                    break
            
            # Base score for arXiv papers
            base_score = 5.0 + conference_score
            
            # Adjust based on categories (more prestigious categories get higher scores)
            categories = item.get('categories', [])
            if any('cs.AI' in cat or 'cs.LG' in cat for cat in categories):
                base_score += 1
            
            return min(base_score, 10.0)
        
        return 5.0  # Default score
    
    def _calculate_author_influence_score(self, item: Dict[str, Any]) -> float:
        """Calculate author influence score based on affiliations and known researchers"""
        source = item.get('source', 'unknown')
        score = 5.0  # Base score
        
        if source == 'arxiv':
            authors = item.get('authors', [])
            
            # Check for influential organizations in author affiliations
            author_text = ' '.join(authors).lower() if authors else ''
            
            for org in self.influential_orgs:
                if org in author_text:
                    score += 2
                    break
            
            # Bonus for multiple authors (collaboration indicator)
            if len(authors) >= 5:
                score += 1
            elif len(authors) >= 3:
                score += 0.5
        
        elif source == 'github':
            # For GitHub, check repository owner and contributors
            url = item.get('url', '').lower()
            description = item.get('description', '').lower()
            
            # Check if from influential organizations
            for org in self.influential_orgs:
                if org in url or org in description:
                    score += 2
                    break
            
            # Check star count as proxy for influence
            stars = item.get('stars', 0)
            if stars >= 1000:
                score += 1
        
        return min(score, 10.0)
    
    def format_score_explanation(self, scores: Dict[str, Any]) -> str:
        """Format score explanation for display"""
        individual = scores['individual_scores']
        breakdown = scores['score_breakdown']
        
        explanation = f"**Final Score: {scores['final_score']}/10**\n\n"
        explanation += "**Score Breakdown:**\n"
        explanation += f"• Popularity: {individual['popularity']}/10 (weight 25%) = {breakdown['popularity']}\n"
        explanation += f"• Technical Innovation: {individual['technical_innovation']}/10 (weight 20%) = {breakdown['technical_innovation']}\n"
        explanation += f"• Application Value: {individual['application_value']}/10 (weight 10%) = {breakdown['application_value']}\n"
        explanation += f"• Readability: {individual['readability']}/10 (weight 15%) = {breakdown['readability']}\n"
        explanation += f"• Experimental Thoroughness: {individual['experimental_thoroughness']}/10 (weight 15%) = {breakdown['experimental_thoroughness']}\n"
        explanation += f"• Author Influence: {individual['author_influence']}/10 (weight 15%) = {breakdown['author_influence']}\n"
        
        return explanation