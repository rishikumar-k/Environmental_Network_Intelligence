import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

np.random.seed(42)

n = 3000

data = pd.DataFrame({
    "temperature": np.random.uniform(15, 50, n),
    "humidity": np.random.uniform(10, 100, n),
    "smoke": np.random.uniform(0, 500, n),
    "co": np.random.uniform(0, 20, n)
})

# Prototype risk formula
risk_score = (
    data["temperature"] / 50 * 0.30 +
    (1 - data["humidity"] / 100) * 0.20 +
    data["smoke"] / 500 * 0.30 +
    data["co"] / 20 * 0.20
)

data["fire"] = (risk_score > 0.55).astype(int)

X = data.drop("fire", axis=1)
y = data["fire"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))

joblib.dump(model, "models/fire_model.pkl")

print("\nFire model saved successfully!")