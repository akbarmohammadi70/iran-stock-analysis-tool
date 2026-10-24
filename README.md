# Iran Stock Analysis Tool

A Python project demonstrating **LLM tool calling (function calling)** for retrieving Iranian stock market data and generating AI-assisted stock analysis using OpenRouter.

## Overview

This project integrates Python functions with a Large Language Model (LLM) to retrieve stock information and provide data-grounded responses. It demonstrates how to define a tool using JSON Schema, execute the requested function, and return structured results to an LLM.

## Features

- **Stock Data Retrieval:** Retrieve stock information using `pytse-client`.
- **LLM Integration:** Connect to language models through OpenRouter.
- **Function Calling:** Allow the LLM to invoke a Python function to retrieve stock data.
- **JSON Schema:** Define structured tool parameters.
- **Environment Configuration:** Store API credentials in environment variables.
- **Error Handling:** Handle missing API keys and invalid stock symbols.
- **Testing:** Validate tool behavior with Python tests.

## Architecture

```text
User Request
     |
     v
OpenRouter LLM
     |
     v
Function Call: get_stock_info
     |
     v
Python Stock Tool
     |
     v
Iranian Stock Market Data
     |
     v
Structured JSON Result
     |
     v
LLM-Generated Response
```

## Project Structure

```text
iran-stock-analysis-tool/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── schemas/
│   └── schema.json
├── src/
│   ├── __init__.py
│   ├── stock_tool.py
│   └── technical_analysis.py
└── tests/
    └── test_tool.py
```

## Requirements

- Python 3.10+
- An OpenRouter API key
- Internet access
- Access to the stock data source used by `pytse-client`

## Installation

Clone the repository:

```bash
git clone https://github.com/akbarmohammadi70/iran-stock-analysis-tool.git
cd iran-stock-analysis-tool
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Configure the following variables in `.env`:

```dotenv
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Replace the placeholder with your own API key.

## Testing

Run the test script:

```bash
python -m tests.test_tool
```

Or run tests with pytest:

```bash
python -m pytest tests/ -v
```

The test code exercises stock information retrieval, JSON serialization, and invalid-symbol handling. Live-data tests depend on the external data source being available.

## Technologies

- Python
- OpenRouter API
- OpenAI Python SDK
- JSON Schema
- `pytse-client`
- `python-dotenv`
- `pytest`

## Limitations

- Stock data availability depends on the external source and the `pytse-client` library.
- The current implementation retrieves basic stock information; it does not independently calculate historical technical indicators such as RSI or MACD.
- LLM-generated responses may contain inaccuracies and should be checked against reliable market data.
- This project is intended for educational and software engineering purposes, not as a source of guaranteed investment recommendations.

## Security

- Never commit your `.env` file or API keys.
- Keep `.env` in `.gitignore`.
- Publish `.env.example` with placeholder values only.

## Disclaimer

This project is for educational purposes only. It does not provide financial advice. Always verify market data independently before making investment decisions.

## Author

**Akbar Mohammadi**

- GitHub: [@akbarmohammadi70](https://github.com/akbarmohammadi70)

---

If you find this project useful, feel free to star the repository.
