from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "Housing.csv"
MODEL_FILE = BASE_DIR / "house_price_model.joblib"
PLOT_FILE = BASE_DIR / "house_price_predictions.png"


data = pd.read_csv(DATA_FILE)

X = data.drop("price", axis=1)
y = data["price"]

categorical_columns = X.select_dtypes(include="str").columns
numeric_columns = X.select_dtypes(exclude="str").columns

preprocessor = ColumnTransformer(
    transformers=[
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_columns),
        ("numeric", "passthrough", numeric_columns),
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=200, random_state=42)),
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f"Model type: {type(model.named_steps['regressor'])}")
print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred):.2f}")
print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred):.2f}")
print(f"R^2 Score: {r2_score(y_test, y_pred):.2f}")

plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color="teal", alpha=0.7, label="Predicted")

min_price = min(y_test.min(), y_pred.min())
max_price = max(y_test.max(), y_pred.max())
plt.plot(
    [min_price, max_price],
    [min_price, max_price],
    color="red",
    linewidth=2,
    label="Perfect Prediction",
)

plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted House Prices")
plt.legend()
plt.tight_layout()
plt.savefig(PLOT_FILE)
plt.show()

joblib.dump(model, MODEL_FILE)

print(f"Model saved to {MODEL_FILE.name}")
print(f"Graph saved to {PLOT_FILE.name}")
