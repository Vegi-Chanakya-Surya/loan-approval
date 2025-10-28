
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import pandas as pd

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

model = load_model()

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    expected = ["applicant_income", "loan_amount", "credit_history", "employment_type"]
    for f in expected:
        if f not in data:
            return jsonify({"error": f"Missing field: {f}"}), 400

    try:
        income = float(data["applicant_income"])
        loan = float(data["loan_amount"])
        credit = str(data["credit_history"])
        emp = str(data["employment_type"])
    except Exception as e:
        return jsonify({"error": f"Invalid input types: {e}"}), 400

    # --- sanity filters ---
    if income <= 0 or loan <= 0:
        return jsonify({
            "status": "Rejected",
            "reason": "Applicant income and loan amount must be positive values."
        }), 400

    ratio = loan / income

    # --- intelligent ratio filter ---
    if ratio > 50:
        return jsonify({
            "status": "Rejected",
            "reason": f"Unrealistic loan-to-income ratio ({ratio:.2f}). Auto-rejected."
        }), 400
    elif ratio > 15:
        return jsonify({
            "status": "High Risk",
            "reason": f"High loan-to-income ratio ({ratio:.2f}). Application flagged for review."
        }), 200

    if model is None:
        return jsonify({"error": "Model not found. Run backend/train_model.py to create model.pkl"}), 500

    df = pd.DataFrame([{
        "applicant_income": income,
        "loan_amount": loan,
        "credit_history": credit,
        "employment_type": emp
    }])

    try:
        pred = model.predict(df)
        prob = None
        if hasattr(model, "predict_proba"):
            prob = float(model.predict_proba(df).max(axis=1)[0])
        status = "Approved" if int(pred[0]) == 1 else "Rejected"
        resp = {"status": status}
        if prob is not None:
            resp["confidence"] = round(prob, 4)
        return jsonify(resp)
    except Exception as e:
        return jsonify({"error": f"Prediction error: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
