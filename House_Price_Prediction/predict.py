import joblib
import pandas as pd

# Load trained pipeline
model = joblib.load("house_price_model.joblib")

print("===== House Price Prediction =====\n")

# Take input from user

area = float(input("Enter area: "))

bedrooms = int(input("Enter bedrooms: "))

bathrooms = int(input("Enter bathrooms: "))

stories = int(input("Enter stories: "))

mainroad = input(
    "Main road (yes/no): "
).lower()

guestroom = input(
    "Guest room (yes/no): "
).lower()

basement = input(
    "Basement (yes/no): "
).lower()

hotwaterheating = input(
    "Hot water heating (yes/no): "
).lower()

airconditioning = input(
    "Air conditioning (yes/no): "
).lower()

parking = int(
    input("Enter parking spaces: ")
)

prefarea = input(
    "Preferred area (yes/no): "
).lower()

furnishingstatus = input(
    "Furnishing status "
    "(furnished/semi-furnished/unfurnished): "
).lower()


# Create DataFrame

new_house = pd.DataFrame(

    [{

        "area": area,

        "bedrooms": bedrooms,

        "bathrooms": bathrooms,

        "stories": stories,

        "mainroad": mainroad,

        "guestroom": guestroom,

        "basement": basement,

        "hotwaterheating": hotwaterheating,

        "airconditioning": airconditioning,

        "parking": parking,

        "prefarea": prefarea,

        "furnishingstatus": furnishingstatus

    }]

)

# Predict

prediction = model.predict(new_house)

# Show Result

print("\n===== Prediction =====")

print(

    f"Predicted House Price: "

    f"{prediction[0]:,.2f}"

)