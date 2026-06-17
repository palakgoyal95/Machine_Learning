import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# ----------------------------
# 1. Load Dataset
# ----------------------------

df = pd.read_csv("Housing.csv")

print("First 5 rows:\n")

print(df.head())


# ----------------------------
# 2. Check Missing Values
# ----------------------------

print("\nMissing Values:\n")

print(df.isnull().sum())


# Remove missing values

df = df.dropna()


# ----------------------------
# 3. Separate Features and Target
# ----------------------------

X = df.drop("price", axis=1)

y = df["price"]


# ----------------------------
# 4. Find Numerical and
#    Categorical Columns
# ----------------------------

categorical_columns = X.select_dtypes(
    include=["object"]
).columns.tolist()

numeric_columns = X.select_dtypes(
    exclude=["object"]
).columns.tolist()

print("\nCategorical Columns:")

print(categorical_columns)

print("\nNumeric Columns:")

print(numeric_columns)


# ----------------------------
# 5. Create Preprocessor
# ----------------------------

preprocessor = ColumnTransformer(

    transformers=[

        (

            "num",

            "passthrough",

            numeric_columns

        ),

        (

            "cat",

            OneHotEncoder(

                handle_unknown="ignore"

            ),

            categorical_columns

        )

    ]

)


# ----------------------------
# 6. Create Pipeline
# ----------------------------

model = Pipeline(

    steps=[

        (

            "preprocessor",

            preprocessor

        ),

        (

            "regressor",

            RandomForestRegression(
                    n_estimators=300,

                    random_state=42)

        )

    ]

)


# ----------------------------
# 7. Train Test Split
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42

)


# ----------------------------
# 8. Train Model
# ----------------------------

model.fit(

    X_train,

    y_train

)


# ----------------------------
# 9. Make Predictions
# ----------------------------

y_pred = model.predict(

    X_test

)


# ----------------------------
# 10. Evaluate Model
# ----------------------------

mse = mean_squared_error(

    y_test,

    y_pred

)

mae = mean_absolute_error(

    y_test,

    y_pred

)

r2 = r2_score(

    y_test,

    y_pred

)


print("\n===== MODEL PERFORMANCE =====")

print(

    f"Mean Squared Error : {mse:.2f}"

)

print(

    f"Mean Absolute Error : {mae:.2f}"

)

print(

    f"R² Score : {r2:.2f}"

)


# ----------------------------
# 11. Save Model
# ----------------------------

joblib.dump(

    model,

    "house_price_model.joblib"

)

print(

    "\nModel saved as "

    "'house_price_model.joblib'"

)

print(

type(

model.named_steps["regressor"]

)

)


# ----------------------------
# 12. Visualization
# ----------------------------

plt.figure(

    figsize=(8,6)

)

plt.scatter(

    y_test,

    y_pred,

    alpha=0.7

)


# Perfect Prediction Line

plt.plot(

    [y.min(), y.max()],

    [y.min(), y.max()],

    "k--",

    lw=2

)


plt.xlabel(

    "Actual Prices"

)

plt.ylabel(

    "Predicted Prices"

)

plt.title(

    "Actual vs Predicted Prices"

)

plt.show()