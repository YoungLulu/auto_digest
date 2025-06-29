# Recent Changes Summary

## 📧 Email Recipient Configuration (Latest Change)

**Issue**: Email recipient was hardcoded in `config.json`, creating security concerns.

**Solution**: Changed email recipient to be automatically detected from `SMTP_USERNAME` environment variable.

### Before:
```json
{
  "email": {
    "recipient": "hardcoded@email.com"
  }
}
```

### After:
```json
{
  "email": {
    "recipient_env": "SMTP_USERNAME"
  }
}
```

### Benefits:
- ✅ **Security**: No email addresses in config files or version control
- ✅ **Simplicity**: Automatically uses same email as SMTP authentication
- ✅ **Consistency**: Follows environment variable pattern like other credentials

---

## 🔧 Configuration System Overhaul (Previous Changes)

### 1. Configurable Search Parameters
- **Keywords**, **arXiv Categories**, and **GitHub Topics** moved to main `config.json`
- Easy customization for different research domains
- No more separate `keywords.json` dependency

### 2. Multiple LLM Provider Support
- **DeepSeek API** integration (`https://api.deepseek.com/v1`)
- **OpenRouter** support (multi-model access)
- **OpenAI** direct API support
- Automatic provider switching and fallback

### 3. Enhanced Configuration Examples
- `config.examples.md`: Comprehensive configuration examples
- `demo_providers.py`: Interactive provider demonstration
- Domain-specific configurations (AI Security, Web Development, etc.)

---

## 🚀 Quick Start with New Configuration

### 1. Set Environment Variables
```bash
# Choose your LLM provider
export DEEPSEEK_API_KEY="your_deepseek_key"     # For Chinese users
export OPENROUTER_API_KEY="your_openrouter_key" # For multi-model access
export OPENAI_API_KEY="your_openai_key"         # For direct OpenAI access

# Email configuration (recipient auto-detected from username)
export SMTP_HOST="smtp.qq.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your_email@qq.com"  # Also used as recipient
export SMTP_PASSWORD="your_app_password"
```

### 2. Update config.json
```json
{
  "data_collection": {
    "keywords": ["your", "custom", "keywords"],
    "arxiv": {"categories": ["cs.AI", "cs.SE"]},
    "github": {"topics": ["your-topics"]}
  },
  "llm": {
    "provider": "deepseek",  // or "openrouter", "openai"
    "model": "deepseek-chat"
  },
  "email": {
    "recipient_env": "SMTP_USERNAME"  // Auto-detects recipient
  }
}
```

### 3. Run the System
```bash
python3 runner.py
```

---

## 🧪 Testing

- `test_config_system.py`: Test configuration loading and providers
- `test_email_recipient.py`: Test email recipient configuration
- `demo_providers.py`: Interactive provider demonstration

---

## 📚 Documentation

- **README.md**: Updated with new features and providers
- **config.examples.md**: Detailed configuration examples for different use cases
- **CHANGES_SUMMARY.md**: This summary document

All changes maintain backward compatibility while enhancing security and flexibility!