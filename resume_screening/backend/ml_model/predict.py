import PyPDF2
import pickle
from pathlib import Path


from pathlib import Path
import pickle

import PyPDF2

try:
    import joblib
except ImportError:  # pragma: no cover - joblib usually ships with sklearn
    joblib = None


MODEL_DIR = Path(__file__).resolve().parent


def _load_artifact(*filenames):
    for filename in filenames:
        artifact_path = MODEL_DIR / filename
        if not artifact_path.exists():
            continue

        if artifact_path.suffix == '.joblib' and joblib is not None:
            return joblib.load(artifact_path)

        with artifact_path.open('rb') as artifact_file:
            return pickle.load(artifact_file)

    raise FileNotFoundError(f'Could not find any of: {", ".join(filenames)}')


def extract_text_from_pdf(pdf_file):

    text_parts = []

    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:

        page_text = page.extract_text() or ""
        if page_text:
            text_parts.append(page_text)

    return "\n".join(text_parts).strip()


model = _load_artifact('model.joblib', 'model.pkl', 'model.pk1')
vectorizer = _load_artifact('vectorizer.joblib', 'vectorizer.pkl', 'vectorizer.pk1')


def _to_float(value):
    return float(value)


# Function to predict suitability
def predict_resume(text):

    text = (text or "").strip()

    if not text:
        return {
            "predicted_role": "No readable text detected",
            "confidence": 0.0,
            "top_matches": [],
        }

    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)[0]

    probabilities = model.predict_proba(text_vector)[0]


    classes = model.classes_



    result = []

    for role, score in zip(

        classes,

        probabilities

    ):

        result.append(

            {

                "role": str(role),

                "confidence":

                round(

                    _to_float(score) * 100,

                    2

                )

            }

        )


    result = sorted(

        result,

        key=lambda x:x["confidence"],

        reverse=True

    )


    return {

        "predicted_role":

        str(prediction),


        "confidence":

        _to_float(result[0]["confidence"]),


        "top_matches":

        result[:3]

    }

