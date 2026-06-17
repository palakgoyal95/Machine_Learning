import pickle
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "land_price.pkl"

model = pickle.load(
    open(
        MODEL_FILE,
        "rb"
    )
)

area = float(
    input(
        "Enter Area: "
    )
)

prediction = model.predict(
    [[area]]
)

print(
    "Predicted Price:",
    prediction[0]
)
