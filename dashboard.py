import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="Trading Agent Dashboard", layout="wide")

st.title("Trading Agent Dashboard")

st.header("Best Trade Opportunity Today")

if os.path.exists("best_trade_opportunity.json"):
    with open("best_trade_opportunity.json", "r") as file:
        best_trade = json.load(file)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ticker", best_trade.get("Ticker", "N/A"))
    col2.metric("Decision", best_trade.get("Decision", "N/A"))
    col3.metric("ML Prediction", best_trade.get("ML Prediction", "N/A"))
    col4.metric("Score", best_trade.get("Score", "N/A"))
else:
    st.warning("Run best_trade_engine.py first.")

st.divider()

st.header("Latest Notifications")

if os.path.exists("notifications.json"):
    with open("notifications.json", "r") as file:
        notifications = json.load(file)

    if notifications:
        latest = notifications[-1]
        st.success(f"[{latest.get('Level')}] {latest.get('Message')}")

        df_notif = pd.DataFrame(notifications[::-1])
        st.dataframe(df_notif, width="stretch")
    else:
        st.info("No notifications yet.")
else:
    st.warning("No notifications.json found. Run notification_engine.py first.")

st.divider()

st.header("Trading Activity History")

if os.path.exists("trading_history.json"):
    with open("trading_history.json", "r") as file:
        history = json.load(file)

    if history:
        rows = []
        for item in history:
            order = item.get("Order Result", {})
            rows.append({
                "Timestamp": item.get("Timestamp"),
                "Ticker": item.get("Ticker"),
                "Decision": item.get("Decision"),
                "ML Prediction": item.get("ML Prediction"),
                "ML Confidence": item.get("ML Confidence"),
                "Risk Level": item.get("Risk Level"),
                "Position Size": item.get("Suggested Position Size"),
                "Order Status": order.get("Order Status")
            })

        df = pd.DataFrame(rows)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Runs", len(df))
        col2.metric("Paper Trades Submitted", (df["Order Status"] == "Submitted").sum())
        col3.metric("Watch Decisions", (df["Decision"] == "WATCH").sum())
        col4.metric("Avoid Decisions", (df["Decision"] == "AVOID").sum())

        st.dataframe(df, width="stretch")
    else:
        st.info("No trading history yet.")
else:
    st.warning("Run app.py or daily_scanner.py first.")
