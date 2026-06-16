from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / 'land.csv'
MODEL_PATH = BASE_DIR / 'land_price.pkl'
PLOT_PATH = BASE_DIR / 'land_price_visualization.png'
FEATURE_COLUMNS = ['Size']
TARGET_COLUMN = 'Price'


def load_data():
    if not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0:
        raise ValueError(f'{CSV_PATH} is missing or empty.')

    data = pd.read_csv(CSV_PATH)
    required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing_columns = [column for column in required_columns if column not in data.columns]
    if missing_columns:
        raise ValueError(f'Missing columns in land.csv: {missing_columns}')

    data = data[required_columns].copy()
    data.fillna(data.mean(numeric_only=True), inplace=True)
    return data


def main():
    data = load_data()
    x = data[FEATURE_COLUMNS]
    y = data[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = LinearRegression()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    print(f'Mean Squared Error: {mean_squared_error(y_test, y_pred):.2f}')
    print(f'R^2 Score: {r2_score(y_test, y_pred):.2f}')
    print(f'Mean Absolute Error: {mean_absolute_error(y_test, y_pred):.2f}')

    plt.scatter(x_test['Size'], y_test, color='blue', label='Actual Price')
    plt.scatter(x_test['Size'], y_pred, color='red', label='Predicted Price')
    plt.xlabel('Area')
    plt.ylabel('Price')
    plt.title('Land Price Prediction')
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_PATH)
    plt.show()

    with open(MODEL_PATH, 'wb') as file:
        pickle.dump({'model': model, 'features': FEATURE_COLUMNS}, file)

    print(f'Model saved to {MODEL_PATH}')
    print(f'Visualization saved to {PLOT_PATH}')


if __name__ == '__main__':
    main()
