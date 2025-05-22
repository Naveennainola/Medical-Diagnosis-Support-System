import os
import joblib
import numpy as np

# Load the model and MultiLabelBinarizer
MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")
try:
    rf_model = joblib.load(os.path.join(MODEL_DIR, "disease_model.pkl"))
    mlb = joblib.load(os.path.join(MODEL_DIR, "mlb.pkl"))
    print("✅ Model and binarizer loaded.")
except Exception as e:
    print(f"❌ Failed to load model or binarizer: {e}")
    rf_model = mlb = None

def predict_disease(symptoms):
    """
    Predict disease using selected symptoms from dropdown.
    """
    if not rf_model or not mlb:
        return {"error": "Model not loaded"}

    try:
        if not symptoms:
            return {"error": "No symptoms selected"}

        vector = mlb.transform([symptoms])
        if vector.sum() == 0:
            return {"error": "Selected symptoms not recognized"}

        probs = rf_model.predict_proba(vector)[0]
        top_indices = np.argsort(probs)[::-1][:3]

        return [
            {"disease": rf_model.classes_[i], "confidence": f"{probs[i] * 100:.2f}%"}
            for i in top_indices
        ]
    except Exception as e:
        return {"error": str(e)}


