import yfinance as yf
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def calculate_rsi(data, period=14):
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def technical_indicator_agent(hist):
    data = hist.copy()
    data["MA20"] = data["Close"].rolling(window=20).mean()
    data["MA50"] = data["Close"].rolling(window=50).mean()
    data["RSI"] = calculate_rsi(data)
    latest = data.iloc[-1]

    return {
        "Latest Close": round(float(latest["Close"]), 2),
        "MA20": round(float(latest["MA20"]), 2),
        "MA50": round(float(latest["MA50"]), 2),
        "RSI": round(float(latest["RSI"]), 2)
    }


def calculate_macd(data):
    exp12 = data["Close"].ewm(span=12, adjust=False).mean()
    exp26 = data["Close"].ewm(span=26, adjust=False).mean()
    macd = exp12 - exp26
    signal_line = macd.ewm(span=9, adjust=False).mean()
    return macd, signal_line


def macd_agent(hist):
    data = hist.copy()
    data["MACD"], data["MACD Signal"] = calculate_macd(data)
    latest = data.iloc[-1]

    if latest["MACD"] > latest["MACD Signal"]:
        trend = "Bullish"
        reason = "MACD is above the signal line, suggesting positive momentum."
    else:
        trend = "Bearish"
        reason = "MACD is below the signal line, suggesting weaker momentum."

    return {
        "MACD": round(float(latest["MACD"]), 2),
        "MACD Signal": round(float(latest["MACD Signal"]), 2),
        "MACD Trend": trend,
        "MACD Reason": reason
    }


def improved_signal_agent(indicators, macd_result):
    close = indicators["Latest Close"]
    ma20 = indicators["MA20"]
    ma50 = indicators["MA50"]
    rsi = indicators["RSI"]
    macd_trend = macd_result["MACD Trend"]

    if close > ma20 and ma20 > ma50 and rsi < 70 and macd_trend == "Bullish":
        return {
            "Signal": "BUY WATCHLIST",
            "Reason": "Price is in an uptrend, RSI is below overbought levels, and MACD confirms bullish momentum."
        }

    if rsi > 70:
        return {
            "Signal": "AVOID",
            "Reason": "RSI is above 70, which may indicate the stock is overbought."
        }

    if macd_trend == "Bearish":
        return {
            "Signal": "HOLD / WATCH",
            "Reason": "Price trend may be acceptable, but MACD shows weaker momentum."
        }

    if close < ma20 and ma20 < ma50:
        return {
            "Signal": "AVOID",
            "Reason": "Price is below MA20 and MA20 is below MA50, suggesting a downtrend."
        }

    return {
        "Signal": "HOLD / WATCH",
        "Reason": "Indicators are mixed, so it is better to wait for confirmation."
    }


def improved_risk_management_agent(indicators, signal, macd_result):
    rsi = indicators["RSI"]
    macd_trend = macd_result["MACD Trend"]

    if signal["Signal"] == "AVOID":
        risk_level = "High"
        risk_reason = "The signal suggests avoiding the trade due to weak or risky technical conditions."
    elif rsi > 65 and macd_trend == "Bearish":
        risk_level = "High"
        risk_reason = "RSI is near overbought levels and MACD is bearish, increasing downside risk."
    elif rsi > 65:
        risk_level = "Medium"
        risk_reason = "RSI is getting close to overbought levels, so the trade should be monitored carefully."
    elif macd_trend == "Bearish":
        risk_level = "Medium"
        risk_reason = "MACD shows weaker momentum, so the setup carries additional risk."
    else:
        risk_level = "Low to Medium"
        risk_reason = "The technical conditions are acceptable, but market risk still exists."

    return {
        "Risk Level": risk_level,
        "Risk Reason": risk_reason,
        "Max Position Recommendation": "Small position only / paper trade first",
        "Stop Loss Guidance": "Use a predefined stop loss before entering any trade"
    }


def news_sentiment_agent(ticker):
    positive_watchlist = ["NVDA", "MSFT", "AAPL"]
    negative_watchlist = ["TSLA"]

    if ticker in positive_watchlist:
        return {
            "Sentiment": "Positive",
            "Sentiment Reason": f"Recent market sentiment around {ticker} appears relatively strong with positive momentum."
        }

    if ticker in negative_watchlist:
        return {
            "Sentiment": "Negative",
            "Sentiment Reason": f"Recent sentiment around {ticker} appears volatile or weaker, requiring additional caution."
        }

    return {
        "Sentiment": "Neutral",
        "Sentiment Reason": f"No strong directional sentiment detected recently for {ticker}."
    }


def prepare_ml_data(hist):
    data = hist.copy()
    data["Return"] = data["Close"].pct_change()
    data["MA20"] = data["Close"].rolling(window=20).mean()
    data["MA50"] = data["Close"].rolling(window=50).mean()
    data["RSI"] = calculate_rsi(data)
    data["Tomorrow Close"] = data["Close"].shift(-1)
    data["Target"] = (data["Tomorrow Close"] > data["Close"]).astype(int)
    data = data.dropna()

    features = data[["Return", "MA20", "MA50", "RSI"]]
    target = data["Target"]

    return features, target


def train_prediction_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return model, accuracy


def prediction_agent(model, hist):
    X_latest, _ = prepare_ml_data(hist)
    latest_features = X_latest.iloc[[-1]]

    prediction = model.predict(latest_features)[0]
    probability = model.predict_proba(latest_features)[0]

    if prediction == 1:
        return {
            "Prediction": "UP",
            "Confidence": round(float(probability[1]), 2)
        }

    return {
        "Prediction": "DOWN",
        "Confidence": round(float(probability[0]), 2)
    }


def ml_enhanced_decision_agent(signal, risk, sentiment, macd_result, ml_prediction):
    signal_value = signal["Signal"]
    risk_level = risk["Risk Level"]
    sentiment_value = sentiment["Sentiment"]
    macd_trend = macd_result["MACD Trend"]
    prediction = ml_prediction["Prediction"]
    confidence = ml_prediction["Confidence"]

    if (
        signal_value == "BUY WATCHLIST"
        and risk_level in ["Low to Medium", "Medium"]
        and sentiment_value == "Positive"
        and macd_trend == "Bullish"
        and prediction == "UP"
        and confidence >= 0.55
    ):
        return {
            "Final Decision": "PAPER TRADE",
            "Decision Reason": "Signal, risk, sentiment, MACD, and ML prediction are aligned positively.",
            "ML Prediction Used": prediction,
            "ML Confidence": confidence
        }

    if prediction == "DOWN" and confidence >= 0.60:
        return {
            "Final Decision": "WATCH",
            "Decision Reason": "ML predicts downside with meaningful confidence, so monitor instead of trade.",
            "ML Prediction Used": prediction,
            "ML Confidence": confidence
        }

    if signal_value == "AVOID" or risk_level == "High" or sentiment_value == "Negative":
        return {
            "Final Decision": "AVOID",
            "Decision Reason": "One or more major conditions are unfavorable.",
            "ML Prediction Used": prediction,
            "ML Confidence": confidence
        }

    return {
        "Final Decision": "WATCH",
        "Decision Reason": "The setup is mixed or ML confidence is not strong enough.",
        "ML Prediction Used": prediction,
        "ML Confidence": confidence
    }


def portfolio_management_agent(account_size=10000, risk_per_trade_percent=1):
    max_risk_amount = account_size * (risk_per_trade_percent / 100)

    return {
        "Account Size": account_size,
        "Risk Per Trade (%)": risk_per_trade_percent,
        "Maximum Risk Amount": round(max_risk_amount, 2),
        "Capital Management Rule": "Never risk more than predefined amount per trade"
    }


def position_sizing_agent(indicators, portfolio, stop_loss_percent=4):
    entry_price = indicators["Latest Close"]
    stop_loss_price = entry_price * (1 - stop_loss_percent / 100)
    risk_per_share = entry_price - stop_loss_price
    max_risk_amount = portfolio["Maximum Risk Amount"]
    position_size = int(max_risk_amount / risk_per_share)

    return {
        "Entry Price": round(entry_price, 2),
        "Stop Loss Price": round(stop_loss_price, 2),
        "Stop Loss (%)": stop_loss_percent,
        "Risk Per Share": round(risk_per_share, 2),
        "Max Risk Amount": max_risk_amount,
        "Suggested Position Size": position_size
    }


def paper_trading_agent(ticker, indicators, signal, risk, sentiment, decision):
    if decision["Final Decision"] != "PAPER TRADE":
        return {
            "Paper Trade Status": "Not Created",
            "Reason": "Final decision is not PAPER TRADE."
        }

    return {
        "Paper Trade Status": "Created",
        "Trade": {
            "Ticker": ticker,
            "Entry Price": indicators["Latest Close"],
            "Signal": signal["Signal"],
            "Risk Level": risk["Risk Level"],
            "Sentiment": sentiment["Sentiment"],
            "Decision": decision["Final Decision"],
            "Trade Type": "Simulated / Paper Trade",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }


def exit_strategy_agent(indicators, stop_loss_percent=4, take_profit_percent=8):
    entry_price = indicators["Latest Close"]
    stop_loss_price = entry_price * (1 - stop_loss_percent / 100)
    take_profit_price = entry_price * (1 + take_profit_percent / 100)

    risk = entry_price - stop_loss_price
    reward = take_profit_price - entry_price
    risk_reward_ratio = round(reward / risk, 2)

    return {
        "Entry Price": round(entry_price, 2),
        "Stop Loss Price": round(stop_loss_price, 2),
        "Take Profit Price": round(take_profit_price, 2),
        "Risk/Reward Ratio": f"1:{risk_reward_ratio}",
        "Exit Rule": "Exit if stop loss or take profit level is reached"
    }


def ml_enhanced_trading_orchestrator(ticker, account_size=10000, risk_per_trade_percent=1):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="3mo")

    if hist.empty:
        raise ValueError(f"No market data found for ticker: {ticker}")

    indicators = technical_indicator_agent(hist)
    macd_result = macd_agent(hist)
    signal = improved_signal_agent(indicators, macd_result)
    risk = improved_risk_management_agent(indicators, signal, macd_result)
    sentiment = news_sentiment_agent(ticker)

    X, y = prepare_ml_data(hist)
    model, accuracy = train_prediction_model(X, y)
    ml_prediction = prediction_agent(model, hist)

    decision = ml_enhanced_decision_agent(
        signal,
        risk,
        sentiment,
        macd_result,
        ml_prediction
    )

    portfolio = portfolio_management_agent(
        account_size=account_size,
        risk_per_trade_percent=risk_per_trade_percent
    )

    position_size = position_sizing_agent(indicators, portfolio)
    paper_trade = paper_trading_agent(ticker, indicators, signal, risk, sentiment, decision)
    exit_strategy = exit_strategy_agent(indicators)

    return {
        "Ticker": ticker,
        "Indicators": indicators,
        "MACD": macd_result,
        "Signal": signal,
        "Risk": risk,
        "Sentiment": sentiment,
        "ML Prediction": ml_prediction,
        "ML Model Accuracy": round(float(accuracy), 2),
        "Decision": decision,
        "Portfolio": portfolio,
        "Position Sizing": position_size,
        "Exit Strategy": exit_strategy,
        "Paper Trade": paper_trade,
        "Trading Mode": "Analysis + Paper Trading Only"
    }
