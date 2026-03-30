# 🤖 AI-Powered QA Agent (Python + Playwright + Claude)

An intelligent QA agent that **automatically explores a website, understands its structure, and generates high-quality test cases using AI**.

![CI](https://github.com/kanakverma89/qa-agent/actions/workflows/ci.yml/badge.svg)

---

## 🚀 Why This Project?

Traditional QA requires:

* Manual test case writing
* Repetitive effort
* Limited coverage

👉 This agent automates that by combining:

* Web scraping
* AI reasoning
* Structured test generation

---

## 🧠 How It Works

```
Target URL
    │
    ▼
crawler/scraper.py       
    └── Extracts inputs, buttons, links, APIs (Playwright / Requests + BeautifulSoup)
    │
    ▼
ai/claude_generator.py   
    └── Sends structured page data → Claude API → returns JSON test cases
    │
    ▼
utils/exporter.py        
    └── Converts JSON → Excel (.xlsx)
```

---

## ✨ Key Features

* 🔍 Intelligent website crawling
* 🧠 AI-generated test cases (UI + API)
* 📊 Structured Excel output
* 🛡️ Security & edge case coverage
* ⚙️ Modular, extensible architecture
* 🔁 CI-enabled with GitHub Actions

---

## 🧱 Project Structure

```
qa-agent/
├── main.py
├── config.py
├── crawler/
│   └── scraper.py
├── ai/
│   └── claude_generator.py
├── utils/
│   └── exporter.py
├── output/
├── .github/workflows/ci.yml
├── requirements.txt
└── .env
```

---

## ⚙️ Setup

### Prerequisites

* Python 3.10+
* Anthropic API Key

---

### Install

```bash
pip install -r requirements.txt
playwright install chromium
```

---

### Configure

Create a `.env` file:

```env
CLAUDE_API_KEY=your_api_key
TARGET_URL=https://automationexercise.com/
OUTPUT_FILE=output/test_cases.xlsx
MODEL=claude-3-haiku-20240307
```

---

### Run

```bash
python -m main
```

---

## 📊 Output

The agent generates **structured test cases** in Excel:

| Title | Type | Steps | Expected | Priority |
| ----- | ---- | ----- | -------- | -------- |

---

## 🧪 Test Coverage

The AI generates:

### ✅ Functional

* Valid user flows
* Navigation scenarios

### ❌ Negative

* Invalid inputs
* Missing fields

### ⚠️ Edge Cases

* Boundary values
* Empty states

### 🔐 Security

* SQL injection
* XSS scenarios

---

## 🔄 CI Pipeline

Runs on every push:

* Python setup
* Dependency install
* Playwright setup
* `flake8` linting
* Import validation

---

## 📦 Dependencies

| Package        | Purpose            |
| -------------- | ------------------ |
| playwright     | Browser automation |
| anthropic      | Claude API         |
| requests       | HTTP calls         |
| beautifulsoup4 | HTML parsing       |
| pandas         | Excel export       |
| openpyxl       | Excel writer       |
| python-dotenv  | Env management     |

---

## ⚠️ Known Limitations

* Single-page scraping (v1)
* Depends on AI response format
* Requires API credits

---

## 🚀 Roadmap

* [ ] Multi-page crawling
* [ ] Playwright test generation
* [ ] Self-healing locators
* [ ] Multi-AI fallback (Claude + OpenAI + Ollama)
* [ ] CI test execution integration

---

## 💡 Use Cases

* QA Engineers → auto-generate test cases
* Test Automation → bootstrap frameworks
* AI QA Research → intelligent test generation
* Teams → improve coverage quickly

---

## 👨‍💻 Author

**Kanak Verma**
QA Automation Engineer | AI-Driven Testing Enthusiast

---

## ⭐ Support

If you find this useful, give it a ⭐ on GitHub!
