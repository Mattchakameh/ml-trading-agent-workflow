from dotenv import load_dotenv
import json
import os
from datetime import datetime

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from agents import ml_enhanced_trading_orchestrator

load_dotenv()


def submit_paper_trade(ticker, qty):
    alpaca_client = TradingClient(
        api_key=os.getenv("ALPACA_API_KEY"),
        secret_key=os.getenv("ALPACA_SECRET_KEY"),
        paper=True
    )

    market_order = MarketOrderRequest(
        symbol=ticker,
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY
    )

    order = alpaca_client.submit_order(order_data=market_order)

    return {
        "Order Status": "Submitted",
        "Order ID": str(order.id),
        "Ticker": str(order.symbol),
        "Quantity": str(order.qty),
        "Side": str(order.side)
    }


def save_trade_log(log_entry):
    file_path = "trading_history.json"

    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump([], file)

    with open(file_path, "r") as file:
        history = json.load(file)

    history.append(log_entry)

    with open(file_path, "w") as file:
        json.dump(history, file, indent=4)


def main():
    ticker = input("Enter stock ticker: ").strip().upper()

    if not ticker:
        ticker = "AAPL"

    print(f"\nRunning Trading Agent for: {ticker}")

    result = ml_enhanced_trading_orchestrator(ticker)

    decision = result["Decision"]["Final Decision"]
    qty = result["Position Sizing"]["Suggested Position Size"]

    order_result = {
        "Order Status": "Not Submitted"
    }

    if decision == "PAPER TRADE" and qty > 0:
        print("\nSubmitting Paper Trade to Alpaca...\n")
        order_result = submit_paper_trade(ticker, qty)
        print(json.dumps(order_result, indent=4))
    else:
        print("\nNo paper trade submitted.")
        print(f"Decision: {decision}")

    log_entry = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Ticker": ticker,
        "Decision": decision,
        "ML Prediction": result["ML Prediction"]["Prediction"],
        "ML Confidence": result["ML Prediction"]["Confidence"],
        "Risk Level": result["Risk"]["Risk Level"],
        "Suggested Position Size": qty,
        "Order Result": order_result
    }

    save_trade_log(log_entry)

    print("\nTrade activity saved to trading_history.json")

if __name__ == "__main__":
    main()
