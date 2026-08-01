from pathlib import Path
import argparse
import pandas as pd
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score


ROOT = Path(__file__).resolve().parents[2]
DATA_DEFAULT = ROOT / 'datasets' / 'resume_dataset_3000.csv'
MODEL_DIR = Path(__file__).resolve().parent


def load_data(path: Path):
    df = pd.read_csv(path)
    # Combine main text and skills (if present)
    df['skills'] = df.get('skills', '').fillna('')
    df['Text'] = df.get('Text', '').fillna('')
    df['input_text'] = (df['Text'].astype(str) + '\n' + df['skills'].astype(str)).str.strip()
    df = df[df['input_text'].str.len() > 0]
    df = df.dropna(subset=['category'])
    return df


def build_model(max_features=20000, ngram=(1, 2)):
    vect = TfidfVectorizer(max_features=max_features, ngram_range=ngram)
    clf = LogisticRegression(max_iter=1000, class_weight='balanced')
    return vect, clf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default=str(DATA_DEFAULT))
    parser.add_argument('--sample', type=int, default=1000,
                        help='Number of rows to sample for quick training (-1 for full dataset)')
    parser.add_argument('--save', action='store_true')
    args = parser.parse_args()

    df = load_data(Path(args.data))
    if args.sample and args.sample > 0:
        df = df.sample(min(args.sample, len(df)), random_state=42)

    X = df['input_text'].values
    y = df['category'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    vect, clf = build_model()
    X_train_t = vect.fit_transform(X_train)
    clf.fit(X_train_t, y_train)

    X_test_t = vect.transform(X_test)
    preds = clf.predict(X_test_t)

    print('Accuracy:', accuracy_score(y_test, preds))
    print('\nClassification report:\n')
    print(classification_report(y_test, preds, zero_division=0))

    if args.save:
        # Save artifacts separately to match predict.py expectations
        joblib.dump(clf, MODEL_DIR / 'model.joblib')
        joblib.dump(vect, MODEL_DIR / 'vectorizer.joblib')
        print('Saved model.joblib and vectorizer.joblib in', MODEL_DIR)


if __name__ == '__main__':
    main()
