# 🧠 AI Coding Digest - Automated Research Intelligence System

An intelligent system that automatically collects, analyzes, and summarizes the latest AI coding research from arXiv papers and GitHub repositories, powered by advanced language models with comprehensive quality scoring.

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to the project directory
cd ai_code_digest

# Install Python dependencies
pip install -r requirements.txt

# Optional: Install pandoc for PDF generation (Ubuntu/Debian)
sudo apt-get install pandoc texlive-xelatex
```

### 2. Configuration

#### Environment Variables

Create a `.env` file or set the following environment variables:

```bash
# LLM API Keys (choose your provider)
export DEEPSEEK_API_KEY="your-deepseek-api-key"
export OPENROUTER_API_KEY="your-openrouter-api-key" 
export OPENAI_API_KEY="your-openai-api-key"

# GitHub API (optional, for higher rate limits)
export GITHUB_TOKEN="your-github-token"

# Email Configuration (required for email delivery)
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export SMTP_USE_TLS="true"
```

#### Configuration File

Edit `config.json` to customize:

**🔍 Search Configuration:**
- **Keywords**: Custom search terms for research topics
- **arXiv Categories**: Target academic categories (cs.AI, cs.SE, etc.)
- **GitHub Topics**: Repository topics to search
- **Collection Parameters**: Days back, max results, minimum stars

**🤖 LLM Provider Configuration:**
- **Multiple Providers**: DeepSeek, OpenRouter, OpenAI support
- **Provider-specific Settings**: Custom API endpoints and models
- **Flexible Model Selection**: Choose optimal model for your use case

**📊 Output & Email Settings:**
- **Multiple Formats**: JSON, Markdown, HTML, PDF
- **Email Configuration**: SMTP settings (recipient auto-detected from SMTP_USERNAME)

**📋 Quick Configuration Example:**
```json
{
  "data_collection": {
    "keywords": ["code generation", "AI programming", "LLM coding"],
    "arxiv": {"categories": ["cs.AI", "cs.SE", "cs.LG"]},
    "github": {"topics": ["ai-coding", "code-generation"]}
  },
  "llm": {
    "provider": "deepseek",  // or "openrouter", "openai"
    "model": "deepseek-chat"
  },
  "email": {
    "recipient_env": "SMTP_USERNAME"  // Auto-detects from SMTP settings
  }
}
```

See `config.examples.md` for detailed configuration examples.

### 3. Run the System

```bash
# Activate virtual environment first
source venv/bin/activate && source .env

# Run for today's digest (full generation + email)
python runner.py

# Test run without sending email
python runner.py --dry-run

# Run for a specific date
python runner.py --date 2024-01-15

# Verbose output for debugging
python runner.py --verbose

# Send existing reports without regenerating
python send_reports.py

# Test email configuration
python test_email.py

# Debug SMTP connection
python debug_smtp.py
```

## 📁 Project Structure

```
ai_code_digest/
├── collector/              # Data collection modules
│   ├── arxiv_fetcher.py   # arXiv paper fetching
│   ├── github_fetcher.py  # GitHub repository fetching
│   └── cleaner.py         # Data cleaning and deduplication
├── summarizer/            # Analysis and summarization
│   ├── gpt_summarizer.py  # Multi-provider LLM integration
│   ├── scoring_system.py  # Comprehensive scoring algorithm
│   ├── report_generator.py # Multi-format report generation
│   └── prompt_templates/   # LLM prompt templates
├── senders/               # Delivery modules
│   └── email_sender.py    # Email delivery system
├── outputs/               # Generated reports (created automatically)
├── logs/                  # Log files (created automatically)
├── config.json            # Main system configuration
├── config.examples.md     # Configuration examples
├── runner.py              # Main execution script
├── requirements.txt       # Python dependencies
└── README.md              # This documentation
```

## ⚙️ Features

### 🏆 Advanced Comprehensive Scoring System
Our research-backed scoring algorithm evaluates content across 6 critical dimensions:

- **Popularity (25%)**: GitHub stars or arXiv citation potential
- **Technical Innovation (20%)**: Novelty and creativity of technical approaches  
- **Application Value (10%)**: Real-world practical applications
- **Readability (15%)**: Content clarity and accessibility
- **Experimental Thoroughness (15%)**: Comprehensiveness of evaluation
- **Author Influence (15%)**: Reputation of authors/organizations

### 📊 Rich Content Analysis
- **Author Information**: Comprehensive author details and organizational affiliations
- **Technical Highlights**: Key innovations and standout technical features
- **Background Context**: Problem space and research gaps addressed
- **Application Scenarios**: Practical use cases and real-world implications
- **Intelligent Classification**: AI-powered category tagging system

### 🎯 Data Collection
- **arXiv**: Fetches papers from CS.AI, CS.SE, CS.LG categories
- **GitHub**: Searches repositories by topics and keywords
- **Smart Filtering**: Relevance-based filtering and deduplication
- **Configurable Timeframes**: Adjustable lookback periods

### 🤖 LLM Analysis
- **Multiple Provider Support**: DeepSeek, OpenRouter, OpenAI compatibility
- **Advanced Prompts**: Specialized prompts for comprehensive research analysis
- **Structured Summaries**: Background, technical highlights, applications
- **Multi-dimensional Scoring**: LLM-generated quality assessments
- **Flexible Model Selection**: Choose optimal model for your region/needs
- **Batch Processing**: Efficient API usage with rate limiting
- **Fallback Handling**: Graceful degradation when API unavailable

#### 🔄 LLM Provider Comparison
| Provider | Best For | Models Available | API Endpoint |
|----------|----------|------------------|--------------|
| **DeepSeek** | Chinese users, cost-effective | `deepseek-chat`, `deepseek-coder` | `api.deepseek.com` |
| **OpenRouter** | Multi-model access, flexibility | Claude, GPT-4, DeepSeek+ | `openrouter.ai` |
| **OpenAI** | Direct GPT access, latest models | `gpt-4`, `gpt-3.5-turbo` | `api.openai.com` |

### Report Generation
- **Multiple Formats**: JSON, Markdown, HTML, PDF
- **Categorized Content**: Organized by research areas
- **Rich Formatting**: Professional styling and navigation
- **Attachment Support**: Email with multiple report formats

### Email Delivery
- **HTML Content**: Rich formatted email body
- **Multiple Attachments**: PDF, JSON, Markdown files
- **SMTP Flexibility**: Works with Gmail, Outlook, custom servers
- **Error Handling**: Robust delivery with fallback options

## 🛠️ Advanced Configuration

### Custom Keywords

Edit `collector/keywords.json` to add your research interests:

```json
{
  "keywords": [
    "your custom keyword",
    "another research area"
  ],
  "github_topics": [
    "your-topic"
  ]
}
```

### LLM Customization

Modify `summarizer/prompt_templates/classify_summarize.txt` to adjust:
- Analysis criteria
- Output format
- Classification categories
- Relevance scoring

### Scheduled Execution

Set up daily execution with cron:

```bash
# Edit crontab
crontab -e

# Add daily execution at 8 AM
0 8 * * * cd /path/to/ai_code_digest && /usr/bin/python3 runner.py
```

## 🔧 Troubleshooting

### Common Issues

1. **No Papers Found**
   - Check internet connection
   - Verify keywords in `collector/keywords.json`
   - Increase `days_back` in config.json

2. **LLM Errors**
   - Verify `OPENROUTER_API_KEY` is set correctly
   - Check API quota and rate limits
   - Try different model in config.json (e.g., "anthropic/claude-3-sonnet-20240229", "openai/gpt-4")

3. **Email Delivery Failed**
   - Verify SMTP credentials
   - Enable "App Passwords" for Gmail
   - Check firewall/network restrictions

4. **PDF Generation Failed**
   - Install pandoc: `sudo apt-get install pandoc texlive-xelatex`
   - Or install weasyprint: `pip install weasyprint`

### Debug Mode

Run with verbose logging to diagnose issues:

```bash
python runner.py --verbose --dry-run
```

### Log Files

Check `logs/ai_code_digest.log` for detailed execution logs.

## 📊 Output Examples

### 🏆 Comprehensive Scoring Example
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
- Innovative file browsing and editing commands for agents
```

### 📧 Email Subject
```
🧠 AI Coding Digest - 2024-01-15
```

### 📑 Report Categories
- Code Generation
- Code Evaluation  
- Program Synthesis
- Coding Agents
- LLM for Coding
- Automated Testing
- Software Reasoning

### 📁 File Outputs
- `daily_2024-01-15.json` - Machine-readable data with scores
- `daily_2024-01-15.md` - Markdown report with full analysis
- `daily_2024-01-15.html` - Web-viewable report with rich formatting
- `daily_2024-01-15.pdf` - Print-ready report

## 🔒 Security Notes

- Store API keys in environment variables, not in code
- Use app-specific passwords for email accounts
- Regularly rotate API tokens
- Review output before sharing to avoid sensitive information

## 🚀 Ready Commands (Quick Reference)

```bash
# Setup (first time only)
source venv/bin/activate && source .env

# Daily Operations
python runner.py                    # Full digest generation + email
python runner.py --dry-run          # Test without sending email  
python send_reports.py              # Send existing reports only

# Testing & Debugging
python test_email.py                # Test email configuration
python test_email_recipient.py      # Test email recipient configuration
python test_config_system.py        # Test configuration system
python demo_providers.py            # Demo LLM providers
python debug_smtp.py               # Debug SMTP connection
python runner.py --verbose         # Detailed logging

# Scheduling
crontab -e                          # Edit cron jobs
# Add: 0 8 * * * /path/to/run_digest.sh

# Logs & Output
tail -f logs/ai_code_digest.log     # Monitor logs
ls outputs/                         # View generated reports
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

For issues and questions:
1. Check the troubleshooting section above
2. Review log files for error details
3. Create an issue in the repository
4. Contact: yangwanlu@codeck.ai

---

*Generated with Claude Code - AI-powered development assistance*