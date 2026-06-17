import pickle

model = pickle.load(
    open(
        "land_price.pkl",
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