import os
import json
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

load_dotenv()

client = TradingClient(
    api_key=os.getenv("ALPACA_API_KEY"),
    secret_key=os.getenv("ALPACA_SECRET_KEY"),
    paper=True
)

with open("final_trading_report.json", "r") as file:
    report = json.load(file)

ticker = report["Ticker"]
stop_loss = report["Exit Strategy"]["Stop Loss Price"]
take_profit = report["Exit Strategy"]["Take Profit Price"]

try:
    position = client.get_open_position(ticker)
    current_price = float(position.current_price)
    qty = abs(float(position.qty))

    if current_price <= stop_loss:
        decision = "SELL - Stop Loss Hit"
    elif current_price >= take_profit:
        decision = "SELL - Take Profit Hit"
    else:
        decision = "HOLD"

    result = {
        "Ticker": ticker,
        "Current Price": current_price,
        "Stop Loss": stop_loss,
        "Take Profit": take_profit,
        "Quantity": qty,
        "Exit Decision": decision
    }

    if decision.startswith("SELL"):
        order = client.submit_order(
            order_data=MarketOrderRequest(
                symbol=ticker,
                qty=qty,
                side=OrderSide.SELL,
                time_in_force=TimeInForce.DAY
            )
        )

        result["Exit Order"] = {
            "Status": "Submitted",
            "Order ID": str(order.id),
            "Side": str(order.side),
            "Quantity": str(order.qty)
        }

except Exception as e:
    result = {
        "Ticker": ticker,
        "Exit Decision": "No Position / Manual Review",
        "Reason": str(e)
    }

print(json.dumps(result, indent=4))

with open("auto_exit_result.json", "w") as file:
    json.dump(result, file, indent=4)

