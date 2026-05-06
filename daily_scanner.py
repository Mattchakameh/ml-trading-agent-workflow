from dotenv import load_dotenv
import json
from datetime import datetime

from agents import ml_enhanced_trading_orchestrator

load_dotenv()

WATCHLIST = ["AAPL", "NVDA", "MSFT"]


def save_trade_log(log_entry):
    file_path = "trading_history.json"

    try:
        with open(file_path, "r") as file:
            history = json.load(file)
    except:
        history = []

    history.append(log_entry)

    with open(file_path, "w") as file:
        json.dump(history, file, indent=4)


def run_daily_scanner():
    for ticker in WATCHLIST:
        print(f"Scanning {ticker}...")

        result = ml_enhanced_trading_orchestrator(ticker)

        log_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Ticker": ticker,
            "Decision": result["Decision"]["Final Decision"],
            "ML Prediction": result["ML Prediction"]["Prediction"],
            "ML Confidence": result["ML Prediction"]["Confidence"],
            "Risk Level": result["Risk"]["Risk Level"],
            "Suggested Position Size": result["Position Sizing"]["Suggested Position Size"],
            "Order Result": {
                "Order Status": "Scanner Only"
            }
        }

        save_trade_log(log_entry)

    print("Daily scanner completed.")


if __name__ == "__main__":
    run_daily_scanner()
from dotenv import load_dotenv
import json
from datetime import datetime

from agents import ml_enhanced_trading_orchestrator

load_dotenv()

WATCHLIST = ["AAPL", "NVDA", "MSFT"]


def save_trade_log(log_entry):
    file_path = "trading_history.json"

    try:
        with open(file_path, "r") as file:
            history = json.load(file)
    except:
        history = []

    history.append(log_entry)

    with open(file_path, "w") as file:
        json.dump(history, file, indent=4)


def run_daily_scanner():
    for ticker in WATCHLIST:
        print(f"Scanning {ticker}...")

        result = ml_enhanced_trading_orchestrator(ticker)

        log_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Ticker": ticker,
            "Decision": result["Decision"]["Final Decision"],
            "ML Prediction": result["ML Prediction"]["Prediction"],
            "ML Confidence": result["ML Prediction"]["Confidence"],
            "Risk Level": result["Risk"]["Risk Level"],
            "Suggested Position Size": result["Position Sizing"]["Suggested Position Size"],
            "Order Result": {
                "Order Status": "Scanner Only"
            }
        }

        save_trade_log(log_entry)

    print("Daily scanner completed.")


if __name__ == "__main__":
    run_daily_scanner()

