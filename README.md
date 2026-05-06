# ML-Enhanced Trading Agent Workflow

An end-to-end hybrid trading agent built with:

- Python
- Machine Learning (Random Forest)
- Technical Analysis
- Alpaca Paper Trading
- Docker
- Streamlit-ready architecture

## Features

### Market Analysis
- Real market data using Yahoo Finance
- Technical indicators:
  - MA20
  - MA50
  - RSI
  - MACD

### Signal & Risk Engine
- Buy / Hold / Avoid logic
- Risk management layer
- Stop loss guidance
- Position sizing

### ML Prediction Layer
- Random Forest prediction model
- Next-day direction prediction:
  - UP
  - DOWN
- Confidence scoring
- Model accuracy tracking

### Paper Trading Workflow
- Paper trade simulation
- Broker integration with Alpaca
- Entry analysis
- Exit strategy
- Trade review logic

### Engineering Layer
- Dockerized execution
- Environment variable management (.env)
- Modular agent architecture
- JSON report persistence

## Project Structure

trading-agent-workflow/
├── app.py
├── agents.py
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── reports/

## Run Locally

```bash
pip3 install -r requirements.txt
python3 app.py
git init
git status
git add .
git commit -m "Initial trading agent workflow"
cat .gitignore
