# Configuration Examples

This document provides examples of how to configure the AI Code Digest system for different use cases.

## 🤖 LLM Provider Configurations

### Example 1: Using DeepSeek (Recommended for Chinese users)

```json
{
  "llm": {
    "provider": "deepseek",
    "model": "deepseek-chat",
    "max_tokens": 1000,
    "temperature": 0.3
  }
}
```

Environment variable:
```bash
export DEEPSEEK_API_KEY="your_deepseek_api_key_here"
```

### Example 2: Using OpenAI GPT-4

```json
{
  "llm": {
    "provider": "openai",
    "model": "gpt-4-turbo-preview",
    "max_tokens": 1000,
    "temperature": 0.3
  }
}
```

Environment variable:
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

### Example 3: Using OpenRouter (Access to multiple models)

```json
{
  "llm": {
    "provider": "openrouter",
    "model": "anthropic/claude-3-sonnet-20240229",
    "max_tokens": 1000,
    "temperature": 0.3
  }
}
```

Environment variable:
```bash
export OPENROUTER_API_KEY="your_openrouter_api_key_here"
```

## 🔍 Search Configuration Examples

### Example 1: Focus on AI Coding Tools

```json
{
  "data_collection": {
    "keywords": [
      "AI code assistant",
      "copilot",
      "code intelligence",
      "developer tools",
      "programming assistant",
      "IDE plugin",
      "code completion",
      "code generation",
      "automated refactoring"
    ],
    "arxiv": {
      "categories": ["cs.AI", "cs.SE", "cs.HC"]
    },
    "github": {
      "topics": [
        "ai-coding",
        "code-generation",
        "developer-tools",
        "ide-plugin",
        "code-assistant"
      ]
    }
  }
}
```

### Example 2: Focus on Machine Learning for Code

```json
{
  "data_collection": {
    "keywords": [
      "neural code synthesis",
      "deep learning for programming",
      "transformer code models",
      "code embeddings",
      "semantic code search",
      "program understanding",
      "code similarity",
      "neural program repair"
    ],
    "arxiv": {
      "categories": ["cs.LG", "cs.AI", "cs.PL", "cs.SE"]
    },
    "github": {
      "topics": [
        "machine-learning",
        "deep-learning",
        "neural-networks",
        "code-analysis",
        "program-synthesis"
      ]
    }
  }
}
```

### Example 3: Focus on Software Engineering Research

```json
{
  "data_collection": {
    "keywords": [
      "software testing",
      "code review",
      "bug detection",
      "vulnerability analysis",
      "static analysis",
      "dynamic analysis",
      "software metrics",
      "code quality",
      "technical debt"
    ],
    "arxiv": {
      "categories": ["cs.SE", "cs.CR", "cs.PL"]
    },
    "github": {
      "topics": [
        "software-engineering",
        "testing",
        "code-quality",
        "static-analysis",
        "security"
      ]
    }
  }
}
```

## 📊 Collection Settings Examples

### Example 1: High Volume Collection

```json
{
  "data_collection": {
    "arxiv": {
      "enabled": true,
      "max_results": 50,
      "days_back": 14
    },
    "github": {
      "enabled": true,
      "max_per_query": 30,
      "days_back": 3,
      "min_stars": 50
    }
  }
}
```

### Example 2: Quality Over Quantity

```json
{
  "data_collection": {
    "arxiv": {
      "enabled": true,
      "max_results": 20,
      "days_back": 30
    },
    "github": {
      "enabled": true,
      "max_per_query": 10,
      "days_back": 7,
      "min_stars": 500
    }
  }
}
```

### Example 3: arXiv Only (Academic Focus)

```json
{
  "data_collection": {
    "arxiv": {
      "enabled": true,
      "max_results": 40,
      "days_back": 21
    },
    "github": {
      "enabled": false
    }
  }
}
```

## 🎯 Specialized Domain Examples

### Example 1: Web Development + AI

```json
{
  "data_collection": {
    "keywords": [
      "AI web development",
      "automated frontend",
      "code generation web",
      "javascript AI",
      "react automation",
      "CSS generation",
      "web assistant"
    ],
    "github": {
      "topics": [
        "web-development",
        "javascript",
        "react",
        "frontend",
        "automation",
        "ai-tools"
      ]
    }
  }
}
```

### Example 2: DevOps + AI

```json
{
  "data_collection": {
    "keywords": [
      "AI DevOps",
      "automated deployment",
      "infrastructure as code",
      "MLOps",
      "CI/CD automation",
      "monitoring AI",
      "cloud automation"
    ],
    "github": {
      "topics": [
        "devops",
        "mlops",
        "ci-cd",
        "infrastructure",
        "automation",
        "cloud"
      ]
    }
  }
}
```

### Example 3: Security + AI

```json
{
  "data_collection": {
    "keywords": [
      "AI security",
      "automated vulnerability detection",
      "code security analysis",
      "malware detection",
      "threat hunting AI",
      "security automation",
      "penetration testing AI"
    ],
    "arxiv": {
      "categories": ["cs.CR", "cs.AI", "cs.SE"]
    },
    "github": {
      "topics": [
        "security",
        "cybersecurity",
        "vulnerability-detection",
        "malware-analysis",
        "threat-intelligence"
      ]
    }
  }
}
```

## 🌐 Language and Region Specific

### Example 1: Chinese AI Research Focus

```json
{
  "data_collection": {
    "keywords": [
      "中文代码生成",
      "人工智能编程",
      "代码智能",
      "程序合成",
      "智能编程助手",
      "code generation",
      "AI programming",
      "Chinese NLP",
      "multilingual code"
    ]
  },
  "llm": {
    "provider": "deepseek",
    "model": "deepseek-chat"
  }
}
```

### Example 2: European Research Focus

```json
{
  "data_collection": {
    "keywords": [
      "European AI research",
      "GDPR compliance AI",
      "ethical AI coding",
      "privacy-preserving code",
      "explainable AI programming",
      "sustainable AI"
    ],
    "arxiv": {
      "categories": ["cs.AI", "cs.CY", "cs.SE"]
    }
  }
}
```

## 📧 Email and Output Configurations

### Example 1: Email Configuration (Auto-detects recipient from SMTP_USERNAME)

```json
{
  "email": {
    "enabled": true,
    "recipient_env": "SMTP_USERNAME",
    "send_attachments": true
  }
}
```

**Note**: The email recipient is automatically determined from your SMTP_USERNAME environment variable. This ensures the digest is sent to the same email address used for SMTP authentication.

### Example 2: Custom Output Formats

```json
{
  "output": {
    "formats": ["json", "markdown", "html"],
    "output_dir": "custom_reports"
  }
}
```

### Example 3: Minimal Email (HTML only, no attachments)

```json
{
  "email": {
    "enabled": true,
    "recipient_env": "SMTP_USERNAME",
    "send_attachments": false
  }
}
```

## 🔧 Complete Configuration Template

Here's a complete configuration template you can customize:

```json
{
  "data_collection": {
    "keywords": [
      "your keyword 1",
      "your keyword 2",
      "your keyword 3"
    ],
    "arxiv": {
      "enabled": true,
      "max_results": 30,
      "days_back": 30,
      "categories": [
        "cs.AI",
        "cs.SE"
      ]
    },
    "github": {
      "enabled": true,
      "max_per_query": 20,
      "days_back": 7,
      "min_stars": 100,
      "topics": [
        "your-topic-1",
        "your-topic-2"
      ]
    }
  },
  "llm": {
    "provider": "deepseek",
    "model": "deepseek-chat",
    "max_tokens": 1000,
    "temperature": 0.3
  },
  "output": {
    "formats": ["html", "pdf"],
    "output_dir": "outputs"
  },
  "email": {
    "enabled": true,
    "recipient_env": "SMTP_USERNAME",
    "send_attachments": true
  }
}
```

Remember to set the appropriate environment variables for your chosen provider!