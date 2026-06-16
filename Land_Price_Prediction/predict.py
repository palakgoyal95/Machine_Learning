import pickle

model = pickle.load(
    open(
        "land_price_model.pkl",
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
