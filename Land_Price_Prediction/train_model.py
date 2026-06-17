import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("land.csv")

# Separate features and target variable
X = data[["area"]]
y = data["price"]
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# Train the model
model = LinearRegression()
model.fit(X_train, y_train)
# Make predictions
y_pred = model.predict(X_test)
# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("Mean Squared Error:", mse)
print("Mean Absolute Error:", mae)
print("R² Score:", r2)
# Save the model
with open("land_price.pkl", "wb") as f:
    pickle.dump(model, f)
    
#visualization

plt.scatter(X_test, y_test, color="blue", label="Actual", marker="o", s=100)
plt.scatter(X_test, y_pred, color="red", label="Predicted", marker="x", s=100)
plt.xlabel("Area")
plt.ylabel("Price")
plt.title("Actual vs Predicted Land Prices")
plt.legend()
plt.savefig("land_price_graph.png")
plt.show()



