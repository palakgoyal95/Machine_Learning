"""Model loading and resume prediction helpers.

Provides `predict_resume(text)` which returns the predicted role, a
confidence score (percentage), and the top matches. The implementation
is robust to classifiers that expose either `predict_proba` or
`decision_function`.
"""

from pathlib import Path
import pickle
import re
import math

import PyPDF2
import numpy as np
from .skills import extract_skills

try:
    import joblib
except Exception:
    joblib = None


MODEL_DIR = Path(__file__).resolve().parent

# These are intentionally broad: a resume can use many different layouts and
# headings. The check guards against analysing invoices, articles, or other
# PDFs as though they were candidate resumes; it is not a validity score.
RESUME_SECTION_MARKERS = (
    "experience", "work history", "employment", "education", "skills",
    "projects", "certifications", "professional summary", "profile",
)


def _load_artifact(*filenames):
    """Try to load the first existing artifact from `filenames`.

    Supports `.joblib` via joblib when available, otherwise falls back
    to pickle.
    """
    for filename in filenames:
        artifact_path = MODEL_DIR / filename
        if not artifact_path.exists():
            continue

        if artifact_path.suffix == '.joblib' and joblib is not None:
            return joblib.load(artifact_path)

        with artifact_path.open('rb') as f:
            return pickle.load(f)

    raise FileNotFoundError(f"Could not find any of: {', '.join(filenames)}")


def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file path or file-like object."""
    text_parts = []
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text:
            text_parts.append(page_text)
    return "\n".join(text_parts).strip()


model = _load_artifact('model.joblib', 'model.pkl', 'model.pickle')
vectorizer = _load_artifact('vectorizer.joblib', 'vectorizer.pkl', 'vectorizer.pickle')


def _to_float(value):
    return float(value)


def _softmax(arr):
    e = np.exp(arr - np.max(arr))
    return e / e.sum()


def _preprocess_text(text: str) -> str:
    """Basic text normalization used before vectorization.

    Keeps changes minimal (collapse whitespace, strip) so it is unlikely
    to diverge from the original training preprocessing.
    """
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def assess_resume_document(text: str) -> dict[str, object]:
    """Check whether extracted PDF text has common resume signals.

    A document is accepted when it contains readable text plus at least two
    independent resume signals. The check never uses protected characteristics.
    """
    normalized = _preprocess_text(text).casefold()
    word_count = len(re.findall(r"[a-z][a-z0-9+#./-]*", normalized))
    if word_count < 40:
        return {
            "is_resume": False,
            "message": "This PDF has too little readable text to verify that it is a resume. Please upload a text-based resume PDF.",
            "signals": [],
        }

    signals = []
    if any(marker in normalized for marker in RESUME_SECTION_MARKERS):
        signals.append("standard resume sections")
    if re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text) or re.search(
        r"(?:linkedin\.com|github\.com|\+?\d[\d\s().-]{7,}\d)", normalized
    ):
        signals.append("contact details")
    if extract_skills(text):
        signals.append("recognised professional skills")
    if re.search(r"\b(?:worked|employment|employed|intern|university|college|bachelor|master|degree)\b", normalized):
        signals.append("employment or education information")

    if len(signals) < 2:
        return {
            "is_resume": False,
            "message": "This PDF does not look like a resume. Please upload a resume containing details such as experience, education, skills, or contact information.",
            "signals": signals,
        }
    return {"is_resume": True, "message": "", "signals": signals}


def predict_resume(text: str):
    """Predict the most likely role for the provided resume text.

    Returns a dict with keys: `predicted_role`, `confidence` (percentage),
    and `top_matches` (list of top 3 roles with confidences).
    """
    text = _preprocess_text(text or "")

    if not text:
        return {
            "predicted_role": "No readable text detected",
            "confidence": 0.0,
            "top_matches": [],
        }

    text_vector = vectorizer.transform([text])

    # safe predict
    prediction = model.predict(text_vector)[0]

    probabilities = None
    if hasattr(model, 'predict_proba'):
        try:
            probabilities = model.predict_proba(text_vector)[0]
        except Exception:
            probabilities = None

    if probabilities is None and hasattr(model, 'decision_function'):
        try:
            scores = model.decision_function(text_vector)
            # decision_function may return shape (n_classes,) or (1, n_classes)
            scores = np.ravel(scores)
            probabilities = _softmax(scores)
        except Exception:
            probabilities = None

    classes = getattr(model, 'classes_', None)

    result = []

    if probabilities is None or classes is None:
        # Fallback: no probabilities available — return prediction alone
        return {
            "predicted_role": str(prediction),
            "confidence": 100.0,
            "top_matches": [{"role": str(prediction), "confidence": 100.0}],
        }

    for role, score in zip(classes, probabilities):
        result.append({
            "role": str(role),
            "confidence": round(_to_float(score) * 100, 2),
        })

    result = sorted(result, key=lambda x: x["confidence"], reverse=True)

    return {
        "predicted_role": str(prediction),
        "confidence": _to_float(result[0]["confidence"]),
        "top_matches": result[:3],
        "skills": extract_skills(text),
    }

