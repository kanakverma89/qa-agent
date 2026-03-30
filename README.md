# QA Agent

An AI-powered QA agent that scrapes a website, analyzes its UI structure, and automatically generates test cases using Claude — exported to Excel.

![CI](https://github.com/kanakverma89/qa-agent/actions/workflows/ci.yml/badge.svg)

## How It Works

```
Target URL
    │
    ▼
crawler/scraper.py       ← HTTP GET + BeautifulSoup → extracts inputs, buttons, links, APIs
    │
    ▼
ai/claude_generator.py   ← sends structured data to Claude → returns JSON test cases
    │
    ▼
utils/exporter.py        ← writes test cases to output/test_cases.xlsx
```

## Project Structure

```
qa-agent/
├── main.py                  # Entry point — orchestrates the full pipeline
├── config.py                # Loads env vars (URL, model, output path, API key)
├── crawler/
│   └── scraper.py           # Scrapes URL, returns inputs/buttons/links/APIs
├── ai/
│   └── claude_generator.py  # Sends page data to Claude, parses JSON response
├── utils/
│   └── exporter.py          # Converts test case JSON to .xlsx via pandas
├── output/
│   └── test_cases.xlsx      # Generated output (git-ignored)
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions — lint + import checks
├── requirements.txt
└── .env                     # Local secrets (not committed)
```

## Setup

### Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

### Install

```bash
pip install -r requirements.txt
playwright install chromium
```

### Configure

Create a `.env` file in the project root:

```env
CLAUDE_API_KEY=sk-ant-...
TARGET_URL=https://automationexercise.com/
OUTPUT_FILE=output/test_cases.xlsx
MODEL=claude-3-sonnet-20240229
```

| Variable        | Default                            | Description                        |
|-----------------|------------------------------------|------------------------------------|
| `CLAUDE_API_KEY`| —                                  | Anthropic API key (required)       |
| `TARGET_URL`    | `https://automationexercise.com/`  | Website to scrape                  |
| `OUTPUT_FILE`   | `output/test_cases.xlsx`           | Path for the generated Excel file  |
| `MODEL`         | `claude-3-sonnet-20240229`         | Claude model to use                |

### Run

```bash
python main.py
```

Output is written to `output/test_cases.xlsx`.

## Generated Test Case Format

Each row in the Excel file contains:

| Column     | Description                                    |
|------------|------------------------------------------------|
| Title      | Short description of the test case             |
| Type       | `positive`, `negative`, `edge`, or `security`  |
| Steps      | Pipe-separated list of test steps              |
| Expected   | Expected result                                |
| Priority   | `high`, `medium`, or `low`                     |

Claude is prompted to cover:
- UI interaction scenarios
- API endpoint checks
- Edge cases (empty input, max length, invalid format)
- Security cases (SQL injection, XSS)

## CI

GitHub Actions runs on every push and pull request to `main`:

- Installs Python 3.13 and dependencies
- Installs Playwright (Chromium)
- Lints with `flake8` (hard-fail on syntax/undefined name errors)
- Verifies all modules import successfully

To enable CI, add `ANTHROPIC_API_KEY` as a repository secret:
**Settings → Secrets and variables → Actions → New repository secret**

## Dependencies

| Package      | Purpose                              |
|--------------|--------------------------------------|
| `playwright` | Headless browser (available for JS-heavy sites) |
| `anthropic`  | Claude API client                    |
| `requests`   | HTTP scraping                        |
| `beautifulsoup4` | HTML parsing                     |
| `pandas`     | DataFrame → Excel export             |
| `openpyxl`   | Excel file writer (pandas backend)   |
| `python-dotenv` | `.env` file loading               |
