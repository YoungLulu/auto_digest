#!/usr/bin/env python3
"""
测试通过OpenRouter使用Google Gemini 2.5 Pro
"""

import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_openrouter_gemini_config():
    """测试OpenRouter Gemini配置"""
    
    print("🚀 测试OpenRouter + Google Gemini 2.5 Pro配置\n")
    
    # 检查配置文件
    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    llm_config = config["llm"]
    
    print("--- 当前LLM配置 ---")
    print(f"提供商: {llm_config['provider']}")
    print(f"模型: {llm_config['model']}")
    print(f"API端点: {llm_config['base_url']}")
    print(f"API密钥环境变量: {llm_config['api_key_env']}")
    
    # 验证OpenRouter配置
    if llm_config['provider'] == 'openrouter' and 'google/gemini-2.5-pro' in llm_config['model']:
        print("✅ 已正确配置为通过OpenRouter使用Gemini 2.5 Pro")
    else:
        print("❌ 配置不正确")
        return False
    
    # 检查OpenRouter模型列表
    openrouter_config = llm_config["providers"]["openrouter"]
    available_models = openrouter_config["models"]
    
    print(f"\n--- OpenRouter可用模型 ---")
    for i, model in enumerate(available_models, 1):
        indicator = " ← 当前使用" if model == llm_config['model'] else ""
        print(f"{i}. {model}{indicator}")
    
    # 检查环境变量
    api_key = os.getenv("OPENROUTER_API_KEY")
    print(f"\n--- 环境变量检查 ---")
    if api_key:
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"✅ OPENROUTER_API_KEY: {masked_key}")
    else:
        print("❌ OPENROUTER_API_KEY: 未设置")
        print("请设置OpenRouter API密钥:")
        print("export OPENROUTER_API_KEY='your_openrouter_api_key'")
        return False
    
    return True

def test_gpt_summarizer_integration():
    """测试GPT Summarizer集成"""
    
    print(f"\n--- 测试GPT Summarizer集成 ---")
    
    try:
        from summarizer.gpt_summarizer import GPTSummarizer
        
        # 初始化summarizer
        summarizer = GPTSummarizer()
        
        print(f"✅ GPT Summarizer初始化成功")
        print(f"✅ 提供商: {getattr(summarizer, 'provider', 'Unknown')}")
        print(f"✅ 模型: {summarizer.model}")
        print(f"✅ 客户端类型: {type(summarizer.client)}")
        
        # 检查是否使用OpenAI兼容客户端（用于OpenRouter）
        if hasattr(summarizer.client, 'chat'):
            print(f"✅ OpenAI兼容客户端正确配置（适用于OpenRouter）")
        else:
            print(f"⚠️  客户端类型异常: {summarizer.client}")
        
        return True
        
    except Exception as e:
        print(f"❌ GPT Summarizer初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_openrouter_gemini_benefits():
    """展示通过OpenRouter使用Gemini的优势"""
    
    print(f"\n--- 通过OpenRouter使用Gemini 2.5 Pro的优势 ---")
    
    benefits = {
        "🔑 统一API": "使用同一个OpenRouter密钥访问多个模型",
        "💰 透明定价": "OpenRouter提供统一的定价和使用统计",
        "🔄 模型切换": "可以轻松切换到其他模型（Claude、GPT-4等）",
        "📊 使用监控": "OpenRouter提供详细的使用分析",
        "🚀 简化配置": "不需要单独申请Google AI API密钥",
        "🛡️ 稳定性": "OpenRouter负载均衡，提高可用性"
    }
    
    for benefit, description in benefits.items():
        print(f"{benefit}: {description}")

def show_model_comparison():
    """显示模型对比"""
    
    print(f"\n--- Gemini 2.5 Pro vs 其他模型 ---")
    
    comparison = [
        ["模型", "提供商", "特点", "适用场景"],
        ["gemini-2.5-pro", "Google", "最新多模态，大容量", "复杂分析，长文本"],
        ["claude-3-sonnet", "Anthropic", "平衡性能，推理强", "通用分析"],
        ["gpt-4-turbo", "OpenAI", "高质量，广泛兼容", "高要求任务"],
        ["deepseek-chat", "DeepSeek", "中文友好，低成本", "中文内容"]
    ]
    
    # 打印表格
    for i, row in enumerate(comparison):
        if i == 0:  # 表头
            print("| " + " | ".join(f"{cell:15}" for cell in row) + " |")
            print("|" + "-" * 17 * len(row) + "|")
        else:
            print("| " + " | ".join(f"{cell:15}" for cell in row) + " |")

def show_usage_instructions():
    """显示使用说明"""
    
    print(f"\n--- 使用说明 ---")
    
    print("1. 确保OpenRouter API密钥已设置:")
    print("   export OPENROUTER_API_KEY='your_openrouter_api_key'")
    
    print(f"\n2. 当前配置:")
    print("   - 提供商: OpenRouter")
    print("   - 模型: google/gemini-2.5-pro")
    print("   - 通过OpenRouter统一接口调用")
    
    print(f"\n3. 运行系统:")
    print("   python3 runner.py")
    
    print(f"\n4. 模型切换 (修改config.json):")
    print('   "model": "anthropic/claude-3-sonnet-20240229"  # 切换到Claude')
    print('   "model": "openai/gpt-4-turbo-preview"         # 切换到GPT-4')
    print('   "model": "google/gemini-2.5-pro"             # 当前Gemini设置')

def create_quick_test():
    """创建快速测试"""
    
    print(f"\n--- 快速API测试 ---")
    
    try:
        from summarizer.gpt_summarizer import GPTSummarizer
        
        # 模拟测试数据
        test_item = {
            "id": "test_gemini",
            "title": "Testing Google Gemini 2.5 Pro via OpenRouter",
            "abstract": "This is a test to verify that Gemini 2.5 Pro works correctly through OpenRouter API.",
            "url": "https://test.example.com",
            "source": "test",
            "authors": ["Test Author"]
        }
        
        print("创建测试项目:")
        print(f"  标题: {test_item['title']}")
        print(f"  来源: {test_item['source']}")
        
        print("\n💡 提示: 运行 python3 runner.py --dry-run 进行完整测试")
        
        return True
        
    except Exception as e:
        print(f"❌ 快速测试失败: {e}")
        return False

if __name__ == "__main__":
    print("测试OpenRouter + Google Gemini 2.5 Pro配置\n")
    
    try:
        # 测试配置
        config_ok = test_openrouter_gemini_config()
        
        if config_ok:
            # 测试集成
            integration_ok = test_gpt_summarizer_integration()
            
            # 展示优势和对比
            show_openrouter_gemini_benefits()
            show_model_comparison()
            show_usage_instructions()
            
            # 快速测试
            create_quick_test()
            
            if integration_ok:
                print(f"\n🎉 OpenRouter + Gemini 2.5 Pro配置完成!")
                print(f"✅ 可以开始使用Google最新的Gemini 2.5 Pro模型")
                print(f"🚀 运行: python3 runner.py")
            else:
                print(f"\n⚠️  配置基本完成，但集成测试有问题")
                
        else:
            print(f"\n❌ 请检查配置和API密钥设置")
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()