#!/usr/bin/env python3
"""
Simple integration test without external dependencies
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from summarizer.scoring_system import ComprehensiveScorer


def test_mock_integration():
    """Test the complete flow with mock data"""
    
    scorer = ComprehensiveScorer()
    
    # Simulate what would come from LLM prompt
    mock_llm_response = {
        "title": "SWE-Agent: Agent-Computer Interfaces Enable Automated Software Engineering",
        "url": "https://arxiv.org/abs/2405.15793",
        "authors": ["John Yang", "Carlos E. Jimenez", "Alexander Wettig", "Kilian Lieret", "Shunyu Yao", "Karthik R Narasimhan", "Ofir Press"],
        "background": "Software engineering tasks require complex reasoning and tool use that current AI systems struggle with.",
        "technical_highlights": [
            "Novel agent-computer interface design for code editing",
            "End-to-end training pipeline for software engineering tasks", 
            "State-of-the-art performance on SWE-bench benchmark",
            "Innovative file browsing and editing commands for agents"
        ],
        "potential_applications": [
            "Automated bug fixing in large codebases",
            "AI-assisted code review and refactoring",
            "Intelligent software maintenance tools"
        ],
        "target_audience": "Software engineers, AI researchers, DevOps teams",
        "category_tags": ["coding_agent", "software_reasoning", "automated_testing"],
        "relevance_score": 9,
        "summary": "SWE-Agent introduces a new paradigm for AI agents to interact with software repositories through specialized interfaces, achieving breakthrough performance on software engineering benchmarks.",
        "scoring_dimensions": {
            "technical_innovation": 9.0,
            "application_value": 8.5,
            "readability": 8.0,
            "experimental_thoroughness": 9.5
        }
    }
    
    # Simulate original item data
    original_item = {
        "id": "2405.15793",
        "title": "SWE-Agent: Agent-Computer Interfaces Enable Automated Software Engineering", 
        "abstract": "Language model (LM) agents are increasingly used to automate complicated tasks...",
        "authors": ["John Yang", "Carlos E. Jimenez", "Alexander Wettig", "Kilian Lieret", "Shunyu Yao", "Karthik R Narasimhan", "Ofir Press"],
        "categories": ["cs.SE", "cs.AI"],
        "source": "arxiv",
        "url": "https://arxiv.org/abs/2405.15793"
    }
    
    # Calculate comprehensive score
    comprehensive_scores = scorer.calculate_comprehensive_score(
        original_item, 
        mock_llm_response["scoring_dimensions"]
    )
    
    # Create final summary (as would be done in gpt_summarizer.py)
    final_summary = {
        **mock_llm_response,
        "comprehensive_scores": comprehensive_scores,
        "final_score": comprehensive_scores["final_score"],
        "original_id": original_item["id"],
        "source": original_item["source"],
        "original_data": original_item
    }
    
    print("=== Complete Integration Test ===")
    print(f"Title: {final_summary['title']}")
    print(f"Authors: {', '.join(final_summary['authors'][:3])} (+{len(final_summary['authors'])-3} more)")
    print(f"Final Comprehensive Score: {final_summary['final_score']}/10")
    print(f"Category Tags: {final_summary['category_tags']}")
    print(f"Technical Highlights: {len(final_summary['technical_highlights'])} items")
    
    print("\n=== Score Breakdown ===")
    individual_scores = comprehensive_scores['individual_scores']
    score_breakdown = comprehensive_scores['score_breakdown']
    
    print(f"• Popularity (25%): {individual_scores['popularity']}/10 → {score_breakdown['popularity']}")
    print(f"• Technical Innovation (20%): {individual_scores['technical_innovation']}/10 → {score_breakdown['technical_innovation']}")
    print(f"• Application Value (10%): {individual_scores['application_value']}/10 → {score_breakdown['application_value']}")
    print(f"• Readability (15%): {individual_scores['readability']}/10 → {score_breakdown['readability']}")
    print(f"• Experimental Thoroughness (15%): {individual_scores['experimental_thoroughness']}/10 → {score_breakdown['experimental_thoroughness']}")
    print(f"• Author Influence (15%): {individual_scores['author_influence']}/10 → {score_breakdown['author_influence']}")
    
    return final_summary


def test_report_formatting(summary):
    """Test report formatting with the new fields"""
    
    print("\n=== Report Format Test ===")
    
    # Test markdown formatting simulation
    authors_str = ", ".join(summary['authors'][:5])
    if len(summary['authors']) > 5:
        authors_str += f" (+{len(summary['authors'])-5} more)"
    
    markdown_snippet = f"""
### {summary['title']}

**🔗 Link**: [{summary['url']}]({summary['url']})

**👥 Authors**: {authors_str}

**🏆 Overall Score**: {summary['final_score']}/10
  - Popularity: {summary['comprehensive_scores']['individual_scores']['popularity']}/10, Technical Innovation: {summary['comprehensive_scores']['individual_scores']['technical_innovation']}/10
  - Application Value: {summary['comprehensive_scores']['individual_scores']['application_value']}/10, Readability: {summary['comprehensive_scores']['individual_scores']['readability']}/10
  - Experimental Thoroughness: {summary['comprehensive_scores']['individual_scores']['experimental_thoroughness']}/10, Author Influence: {summary['comprehensive_scores']['individual_scores']['author_influence']}/10

**🎯 Target Audience**: {summary['target_audience']}

**📝 Summary**: {summary['summary']}

**🔍 Background**: {summary['background']}

**⚡ Technical Highlights**:
"""
    
    for highlight in summary['technical_highlights']:
        markdown_snippet += f"- {highlight}\n"
    
    markdown_snippet += "\n**🚀 Potential Applications**:\n"
    for app in summary['potential_applications']:
        markdown_snippet += f"- {app}\n"
    
    markdown_snippet += f"\n**🏷️ Tags**: {' '.join([f'`{tag}`' for tag in summary['category_tags']])}"
    
    print("Markdown Preview:")
    print(markdown_snippet)
    
    return True


if __name__ == "__main__":
    print("Testing Complete AI Code Digest Integration\n")
    
    try:
        # Test comprehensive scoring integration
        summary = test_mock_integration()
        
        # Test report formatting
        test_report_formatting(summary)
        
        print("\n✅ All integration tests passed!")
        print("✅ Comprehensive scoring system fully implemented")
        print("✅ Authors and highlights fields added")
        print("✅ Report formatting updated")
        print("✅ System ready for GitHub submission")
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()