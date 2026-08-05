"""
Machine Learning detection engine.

Uses a trained Logistic Regression classifier to predict
whether a prompt is benign or malicious.

"""



from pathlib import Path
import joblib
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

classifier = joblib.load(BASE_DIR / "models" / "promptguard_classifier.pkl")
label_encoder = joblib.load(BASE_DIR / "models" / "label_encoder.pkl")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def detect_ml_prompt(prompt):

    embedding = model.encode([prompt])

    prediction = classifier.predict(embedding)[0]

    probability = classifier.predict_proba(embedding)[0]

    label = label_encoder.inverse_transform([prediction])[0]

    malicious_probability = probability[1]

    safe = True
    risk = "SAFE"
    recommendation = "Prompt appears safe to process."

    if malicious_probability >= 0.90:
        safe = False
        risk = "HIGH"
        recommendation = "Block this prompt before forwarding it to the LLM."

    elif malicious_probability >= 0.70:
        safe = False
        risk = "MEDIUM"
        recommendation = "Manual review recommended before forwarding."

    elif malicious_probability >= 0.55:
        safe = False
        risk = "LOW"
        recommendation = "Potentially suspicious prompt. Log and monitor."

    return {
        "safe": safe,
        "risk": risk,
        "prediction": label,
        "benign_probability": round(float(probability[0]) * 100, 2),
        "malicious_probability": round(float(probability[1]) * 100, 2),
    }