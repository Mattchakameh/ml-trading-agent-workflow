import json

with open("trading_history.json", "r") as file:
    history = json.load(file)

best = None
best_score = -999

for item in history:
    if "Ticker" not in item:
        continue

    score = 0

    if item.get("Decision") == "PAPER TRADE":
        score += 40
    elif item.get("Decision") == "WATCH":
        score += 15

    if item.get("ML Prediction") == "UP":
        score += 25

    score += item.get("ML Confidence", 0) * 20

    if item.get("Risk Level") == "Low to Medium":
        score += 15
    elif item.get("Risk Level") == "Medium":
        score += 8

    if score > best_score:
        best_score = score
        best = {
            "Ticker": item.get("Ticker"),
            "Decision": item.get("Decision"),
            "ML Prediction": item.get("ML Prediction"),
            "Score": round(score, 2)
        }

print("\nBest Trade Opportunity Today:\n")
print(json.dumps(best, indent=4))

with open("best_trade_opportunity.json", "w") as file:
    json.dump(best, file, indent=4)

print("\nSaved to best_trade_opportunity.json")
