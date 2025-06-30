# 🧠 AI Coding Digest - Automated Research Intelligence System

An intelligent system that automatically collects, analyzes, and summarizes the latest AI coding research from arXiv papers and GitHub repositories, powered by advanced language models with comprehensive quality scoring.

## 🚀 Quick Start

### 1. Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies for PDF generation
# Ubuntu/Debian:
sudo apt-get install pandoc texlive-xelatex

# macOS:
brew install pandoc cairo pango gdk-pixbuf libffi

# Windows:
choco install pandoc miktex
```

### 2. Configuration

#### Environment Variables (.env file)
```bash
# LLM API Keys (choose your provider)
OPENROUTER_API_KEY="your-openrouter-api-key"
DEEPSEEK_API_KEY="your-deepseek-api-key" 
OPENAI_API_KEY="your-openai-api-key"
GOOGLE_API_KEY="your-google-ai-api-key"

# GitHub API (optional, higher rate limits)
GITHUB_TOKEN="your-github-token"

# Email Configuration
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USERNAME="your-email@gmail.com"
SMTP_PASSWORD="your-app-password"
SMTP_USE_TLS="true"
```

#### Key Configuration (config.json)
```json
{
  "data_collection": {
    "keywords": ["code generation", "LLM coding", "AI programming"],
    "arxiv": {"max_results": 50, "days_back": 10},
    "github": {"max_per_query": 10, "min_stars": 100}
  },
  "llm": {
    "provider": "openrouter",
    "model": "anthropic/claude-3-sonnet-20240229"
  },
  "output": {
    "max_items_per_category": 20,
    "max_total_items": 100
  }
}
```

### 3. Run the System

```bash
# Setup environment
source venv/bin/activate && source .env

# Generate today's digest
python runner.py

# Test without sending email
python runner.py --dry-run

# Debug mode
python runner.py --verbose
```

## ⚙️ Features

### 🏆 Two-Stage Quality Ranking System

**Stage 1: Data Collection Sorting**
- arXiv: Latest 50 papers by submission date
- GitHub: Top repositories by stars/activity

**Stage 2: Comprehensive Scoring & Re-ranking**
- **Popularity (25%)**: GitHub stars, arXiv citations
- **Technical Innovation (20%)**: LLM-assessed novelty
- **Application Value (10%)**: Practical utility
- **Readability (15%)**: Content clarity
- **Experimental Thoroughness (15%)**: Evaluation rigor
- **Author Influence (15%)**: Institutional reputation

Final output shows highest-quality research, not just newest.

### 🎯 Data Sources
- **arXiv**: CS.AI, CS.SE, CS.LG, CS.PL categories
- **GitHub**: Configurable topics and keywords
- **Smart Filtering**: Relevance-based deduplication

### 🤖 Multi-Provider LLM Support
| Provider | Best For | Models |
|----------|----------|--------|
| **Google AI** | Latest models, cost-effective | gemini-2.5-pro, gemini-1.5-pro |
| **OpenRouter** | Multi-model access | Claude, GPT-4, Gemini |
| **DeepSeek** | Very cost-effective | deepseek-chat, deepseek-coder |
| **OpenAI** | Direct GPT access | gpt-4, gpt-3.5-turbo |

**Easy Provider Switching:**
```bash
python provider_manager.py google    # Switch to Google AI
python provider_manager.py           # Interactive selection
```
*See `provider_examples.md` for detailed configuration guides.*

### 📊 Output Formats
- **JSON**: Machine-readable with scores
- **Markdown**: Human-readable analysis
- **HTML**: Rich web format
- **PDF**: Print-ready reports
- **Email**: Automated delivery with attachments

## 🖥️ System Compatibility

### Supported Platforms
- ✅ **Linux** (Ubuntu, Debian, CentOS) - Fully tested
- ✅ **macOS** (10.14+) - Fully compatible
- ✅ **Windows** (10/11) - Compatible

### Platform-Specific Setup

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install python3 python3-pip python3-venv pandoc texlive-xelatex
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

#### macOS
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install python3 pandoc cairo pango gdk-pixbuf libffi
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

#### Windows
```powershell
# Install dependencies
choco install pandoc miktex

# Python environment
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 📁 Project Structure

```
ai_code_digest/
├── collector/              # Data collection
│   ├── arxiv_fetcher.py   # arXiv papers
│   ├── github_fetcher.py  # GitHub repos
│   └── cleaner.py         # Deduplication
├── summarizer/            # Analysis engine
│   ├── gpt_summarizer.py  # Multi-provider LLM
│   ├── scoring_system.py  # Quality scoring
│   ├── report_generator.py # Report generation
│   └── prompt_templates/   # LLM prompts
├── senders/               # Delivery
│   └── email_sender.py    # Email system
├── outputs/               # Generated reports
├── config.json            # Main configuration
└── runner.py              # Main script
```

## 🔧 Troubleshooting

### Common Issues

1. **No Data Found**
   - Check internet connection
   - Verify API keys in `.env`
   - Increase `days_back` in config.json

2. **LLM Errors**
   - Verify API key: `OPENROUTER_API_KEY`
   - Check model availability
   - Try different provider in config

3. **Email Delivery Failed**
   - Enable "App Passwords" for Gmail
   - Check SMTP credentials
   - Verify network/firewall settings

4. **PDF Generation Failed**
   - **Linux**: `sudo apt-get install pandoc texlive-xelatex`
   - **macOS**: `brew install pandoc cairo pango gdk-pixbuf libffi`
   - **Windows**: `choco install pandoc miktex`

### Debug Commands
```bash
python runner.py --verbose --dry-run    # Debug without email
python test_email.py                    # Test email config
tail -f logs/ai_code_digest.log         # Monitor logs
```

## 📊 Sample Output

### Comprehensive Scoring Example
```
### SWE-Agent: Agent-Computer Interfaces Enable Automated Software Engineering

**🔗 Link**: [https://arxiv.org/abs/2405.15793](https://arxiv.org/abs/2405.15793)
**👥 Authors**: John Yang, Carlos E. Jimenez, Alexander Wettig (+4 more)

**🏆 Overall Score**: 7.67/10
  - Popularity: 6.0/10, Technical Innovation: 9.0/10
  - Application Value: 8.5/10, Readability: 8.0/10
  - Experimental Thoroughness: 9.5/10, Author Influence: 6.0/10

**⚡ Technical Highlights**:
- Novel agent-computer interface design for code editing
- End-to-end training pipeline for software engineering tasks
- State-of-the-art performance on SWE-bench benchmark
```

## 🚀 Quick Commands Reference

```bash
# Daily Operations
python runner.py                    # Generate & send digest
python runner.py --dry-run          # Test without email
python runner.py --date 2024-01-15  # Specific date

# Provider Management
python provider_manager.py          # Interactive provider selection
python provider_manager.py list     # List all available providers
python provider_manager.py google   # Switch to Google AI
python test_all_providers.py        # Test all provider compatibility

# Testing & Debug
python test_email.py                # Test email setup
python runner.py --verbose         # Detailed logging
python debug_smtp.py               # SMTP debugging

# Monitoring
tail -f logs/ai_code_digest.log     # Real-time logs
ls outputs/                         # View reports
```

## 🔒 Security & Best Practices

- Store API keys in `.env` file, never in code
- Use app-specific passwords for email accounts
- Regularly rotate API tokens
- Review outputs before sharing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests if applicable
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙋‍♂️ Support

For issues and questions:
1. Check troubleshooting section
2. Review log files
3. Create an issue in the repository
4. Contact: yangwanlu@codeck.ai

---

*Generated with Claude Code - AI-powered development assistance*