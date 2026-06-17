from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "house_price_model.joblib"


model = joblib.load(MODEL_FILE)

features = {
    "area": float(input("Enter area: ")),
    "bedrooms": int(input("Enter bedrooms: ")),
    "bathrooms": int(input("Enter bathrooms: ")),
    "stories": int(input("Enter stories: ")),
    "mainroad": input("Main road (yes/no): ").strip().lower(),
    "guestroom": input("Guest room (yes/no): ").strip().lower(),
    "basement": input("Basement (yes/no): ").strip().lower(),
    "hotwaterheating": input("Hot water heating (yes/no): ").strip().lower(),
    "airconditioning": input("Air conditioning (yes/no): ").strip().lower(),
    "parking": int(input("Enter parking spaces: ")),
    "prefarea": input("Preferred area (yes/no): ").strip().lower(),
    "furnishingstatus": input(
        "Furnishing status (furnished/semi-furnished/unfurnished): "
    ).strip().lower(),
}

input_data = pd.DataFrame([features])
prediction = model.predict(input_data)

print(f"Predicted House Price: {prediction[0]:.2f}")
