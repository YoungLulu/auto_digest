#!/usr/bin/env python3
"""
Test script for the comprehensive scoring system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from summarizer.scoring_system import ComprehensiveScorer
import json


def test_scoring_system():
    """Test the comprehensive scoring system with sample data"""
    
    scorer = ComprehensiveScorer()
    
    # Test data for arXiv paper
    arxiv_item = {
        "id": "2024.01.001",
        "title": "Advanced Code Generation with Large Language Models",
        "abstract": "This paper presents novel techniques for automated code generation using large language models, with applications in software engineering.",
        "authors": ["John Doe", "Jane Smith", "Alice Johnson"],
        "categories": ["cs.AI", "cs.SE"],
        "source": "arxiv",
        "url": "https://arxiv.org/abs/2024.01.001"
    }
    
    # Test LLM scores
    llm_scores = {
        "technical_innovation": 8.5,
        "application_value": 7.0,
        "readability": 9.0,
        "experimental_thoroughness": 8.0
    }
    
    # Calculate comprehensive score
    result = scorer.calculate_comprehensive_score(arxiv_item, llm_scores)
    
    print("=== arXiv Paper Test ===")
    print(f"Title: {arxiv_item['title']}")
    print(f"Authors: {', '.join(arxiv_item['authors'])}")
    print("\nScoring Results:")
    print(json.dumps(result, indent=2))
    print(f"\nFinal Score: {result['final_score']}/10")
    
    # Test data for GitHub repository  
    github_item = {
        "id": "microsoft/vscode",
        "title": "Visual Studio Code",
        "description": "Visual Studio Code is a lightweight but powerful source code editor which runs on your desktop.",
        "stars": 160000,
        "language": "TypeScript",
        "source": "github",
        "url": "https://github.com/microsoft/vscode"
    }
    
    # Test LLM scores for GitHub
    github_llm_scores = {
        "technical_innovation": 7.5,
        "application_value": 9.5,
        "readability": 8.5,
        "experimental_thoroughness": 6.0
    }
    
    # Calculate comprehensive score for GitHub
    github_result = scorer.calculate_comprehensive_score(github_item, github_llm_scores)
    
    print("\n=== GitHub Repository Test ===")
    print(f"Title: {github_item['title']}")
    print(f"Stars: {github_item['stars']:,}")
    print("\nScoring Results:")
    print(json.dumps(github_result, indent=2))
    print(f"\nFinal Score: {github_result['final_score']}/10")
    
    # Test score explanation formatting
    print("\n=== Score Explanation ===")
    explanation = scorer.format_score_explanation(result)
    print(explanation)


def test_gpt_summarizer_integration():
    """Test GPT summarizer integration (mock without API)"""
    
    from summarizer.gpt_summarizer import GPTSummarizer
    
    # Initialize without API key to test fallback behavior
    summarizer = GPTSummarizer()
    
    test_items = [
        {
            "id": "test1",
            "title": "Automated Code Generation with Large Language Models",
            "abstract": "This paper presents a novel approach to automated code generation using LLMs with enhanced reasoning capabilities.",
            "authors": ["Dr. AI Smith", "Prof. Code Generator"],
            "categories": ["cs.AI", "cs.SE"],
            "source": "arxiv",
            "url": "https://arxiv.org/abs/2024.test1"
        },
        {
            "id": "openai/codex",
            "title": "OpenAI Codex",
            "description": "AI system that translates natural language to code",
            "stars": 15000,
            "language": "Python",
            "source": "github", 
            "url": "https://github.com/openai/codex"
        }
    ]
    
    print("\n=== GPT Summarizer Integration Test ===")
    summaries = summarizer.summarize_items(test_items)
    
    for i, summary in enumerate(summaries):
        print(f"\n--- Summary {i+1} ---")
        print(f"Title: {summary.get('title')}")
        print(f"Authors: {summary.get('authors', [])}")
        print(f"Final Score: {summary.get('final_score', 'N/A')}")
        print(f"Technical Highlights: {summary.get('technical_highlights', [])}")
        
        # Check if comprehensive scoring was applied
        if 'comprehensive_scores' in summary:
            individual_scores = summary['comprehensive_scores']['individual_scores']
            print(f"Score breakdown:")
            for key, score in individual_scores.items():
                print(f"  {key}: {score}/10")


if __name__ == "__main__":
    print("Testing AI Code Digest Comprehensive Scoring System\n")
    
    try:
        test_scoring_system()
        test_gpt_summarizer_integration()
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()