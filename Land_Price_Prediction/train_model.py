
import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "land.csv"
MODEL_FILE = BASE_DIR / "land_price.pkl"


data = pd.read_csv(DATA_FILE)
data.columns = data.columns.str.lower()

X = data[["area"]]
y = data["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae:.2f}")
print(f"Mean Squared Error: {mse:.2f}")
print(f"R^2 Score: {r2:.2f}")

plt.scatter(X_test, y_test, color="blue", label="Actual")
plt.scatter(X_test, y_pred, color="red", label="Predicted")
plt.xlabel("Area")
plt.ylabel("Price")
plt.title("Actual vs Predicted Land Prices")
plt.legend()
plt.show()

with open(MODEL_FILE, "wb") as file:
    pickle.dump(model, file)

print(f"Model saved to {MODEL_FILE.name}")
