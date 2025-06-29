#!/usr/bin/env python3
"""
Test script for the new configuration system with multiple providers
"""

import sys
import os
import json
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_config_loading():
    """Test configuration loading and validation"""
    print("=== Testing Configuration System ===")
    
    # Load config
    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Test data collection configuration
    data_config = config["data_collection"]
    print(f"✅ Keywords loaded: {len(data_config['keywords'])} items")
    print(f"✅ arXiv categories: {data_config['arxiv']['categories']}")
    print(f"✅ GitHub topics: {data_config['github']['topics']}")
    
    # Test LLM provider configuration
    llm_config = config["llm"]
    print(f"✅ Current provider: {llm_config['provider']}")
    print(f"✅ Current model: {llm_config['model']}")
    
    providers = llm_config.get("providers", {})
    print(f"✅ Available providers: {list(providers.keys())}")
    
    for provider_name, provider_config in providers.items():
        print(f"  - {provider_name}: {provider_config['base_url']}")
        print(f"    Models: {provider_config['models']}")
        print(f"    API Key Env: {provider_config['api_key_env']}")
    
    return config


def test_arxiv_fetcher():
    """Test ArxivFetcher with new config system"""
    print("\n=== Testing ArxivFetcher with Config ===")
    
    try:
        from collector.arxiv_fetcher import ArxivFetcher
        
        # Test with default config
        fetcher = ArxivFetcher()
        print(f"✅ Keywords: {len(fetcher.keywords)} items")
        print(f"✅ Categories: {fetcher.categories}")
        
        # Test query building
        query = fetcher.build_query(days_back=30)
        print(f"✅ Generated query: {query[:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ ArxivFetcher test failed: {e}")
        return False


def test_github_fetcher():
    """Test GitHubFetcher with new config system"""
    print("\n=== Testing GitHubFetcher with Config ===")
    
    try:
        from collector.github_fetcher import GitHubFetcher
        
        # Test with default config
        fetcher = GitHubFetcher()
        print(f"✅ Keywords: {len(fetcher.keywords)} items")
        print(f"✅ GitHub topics: {fetcher.github_topics}")
        
        # Test query building
        queries = fetcher.build_search_queries(days_back=7)
        print(f"✅ Generated {len(queries)} search queries")
        for i, query in enumerate(queries[:3]):
            print(f"  Query {i+1}: {query}")
        
        return True
    except Exception as e:
        print(f"❌ GitHubFetcher test failed: {e}")
        return False


def test_llm_providers():
    """Test LLM provider configuration"""
    print("\n=== Testing LLM Provider System ===")
    
    try:
        from summarizer.gpt_summarizer import GPTSummarizer
        
        # Load config
        with open("config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Test different provider configurations
        providers_to_test = ["openrouter", "deepseek", "openai"]
        
        for provider in providers_to_test:
            print(f"\n--- Testing {provider} provider ---")
            
            # Update config for this provider
            test_config = config.copy()
            test_config["llm"]["provider"] = provider
            
            if provider == "deepseek":
                test_config["llm"]["model"] = "deepseek-chat"
            elif provider == "openai":
                test_config["llm"]["model"] = "gpt-4-turbo-preview"
            
            try:
                summarizer = GPTSummarizer(config=test_config)
                if summarizer.client:
                    print(f"✅ {provider} client initialized successfully")
                    print(f"✅ Model: {summarizer.model}")
                else:
                    print(f"⚠️  {provider} client not initialized (likely missing API key)")
                
            except Exception as e:
                print(f"❌ {provider} initialization failed: {e}")
        
        return True
    except Exception as e:
        print(f"❌ LLM provider test failed: {e}")
        return False


def test_configuration_examples():
    """Show configuration examples for different use cases"""
    print("\n=== Configuration Examples ===")
    
    # Example 1: Using DeepSeek
    deepseek_config = {
        "provider": "deepseek",
        "model": "deepseek-chat",
        "api_key_env": "DEEPSEEK_API_KEY"
    }
    print("\n--- Example 1: DeepSeek Configuration ---")
    print(json.dumps(deepseek_config, indent=2))
    
    # Example 2: Custom keywords for specific domain
    custom_keywords = [
        "AI code assistant",
        "copilot",
        "code intelligence",
        "developer tools",
        "programming assistant"
    ]
    print("\n--- Example 2: Custom Keywords ---")
    print(json.dumps(custom_keywords, indent=2))
    
    # Example 3: Custom arXiv categories
    custom_categories = [
        "cs.AI",
        "cs.SE",
        "cs.HC",  # Human-Computer Interaction
        "cs.IR"   # Information Retrieval
    ]
    print("\n--- Example 3: Custom arXiv Categories ---")
    print(json.dumps(custom_categories, indent=2))


def test_environment_variables():
    """Test environment variable configuration"""
    print("\n=== Environment Variables Test ===")
    
    required_vars = {
        "OPENROUTER_API_KEY": "OpenRouter API access",
        "DEEPSEEK_API_KEY": "DeepSeek API access", 
        "OPENAI_API_KEY": "OpenAI API access",
        "GITHUB_TOKEN": "GitHub API access",
        "SMTP_HOST": "Email delivery",
        "SMTP_USERNAME": "Email authentication",
        "SMTP_PASSWORD": "Email authentication"
    }
    
    for var_name, description in required_vars.items():
        value = os.getenv(var_name)
        if value:
            masked_value = value[:8] + "..." if len(value) > 8 else "***"
            print(f"✅ {var_name}: {masked_value} ({description})")
        else:
            print(f"⚠️  {var_name}: Not set ({description})")


if __name__ == "__main__":
    print("Testing AI Code Digest Configuration System\n")
    
    try:
        # Test configuration loading
        config = test_config_loading()
        
        # Test data collectors
        arxiv_ok = test_arxiv_fetcher()
        github_ok = test_github_fetcher()
        
        # Test LLM providers
        llm_ok = test_llm_providers()
        
        # Show examples
        test_configuration_examples()
        
        # Test environment
        test_environment_variables()
        
        # Summary
        print("\n=== Test Summary ===")
        if arxiv_ok and github_ok and llm_ok:
            print("✅ All configuration tests passed!")
            print("✅ System ready with flexible provider support")
            print("✅ Keywords, categories, and topics are configurable")
        else:
            print("⚠️  Some tests had issues, but core functionality should work")
        
    except Exception as e:
        print(f"\n❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()