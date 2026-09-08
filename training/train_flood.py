import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

np.random.seed(42)

# Generate prototype training data
n = 3000

data = pd.DataFrame({
    "water_level": np.random.uniform(10, 150, n),
    "rainfall": np.random.uniform(0, 150, n),
    "soil_moisture": np.random.uniform(20, 100, n),
    "water_rise_rate": np.random.uniform(0, 20, n)
})

# Prototype labeling rule used to create training labels
risk_score = (
    data["water_level"] / 150 * 0.35 +
    data["rainfall"] / 150 * 0.25 +
    data["soil_moisture"] / 100 * 0.20 +
    data["water_rise_rate"] / 20 * 0.20
)

data["flood"] = (risk_score > 0.55).astype(int)

X = data.drop("flood", axis=1)
y = data["flood"]

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

joblib.dump(model, "models/flood_model.pkl")

print("\nFlood model saved successfully!")