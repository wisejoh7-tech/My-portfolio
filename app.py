import os
import io
from flask import Flask, render_template, request, jsonify
import pandas as pd
import ml_models

app = Flask(__name__)
# Ensure maximum file upload size is reasonable (16MB)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/skills")
def skills():
    return render_template("skills.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/analytic")
def analytic():
    return render_template("analytic.html")


@app.route("/diabetes")
def diabetes():
    return render_template("diabetes.html")


@app.route("/hypertension")
def hypertension():
    return render_template("hypertension.html")


@app.route("/ecommerce")
def ecommerce():
    return render_template("ecommerce.html")


@app.route("/typhoid")
def typhoid():
    return render_template("typhoid.html")


@app.route("/retailer")
def retailer():
    return render_template("retailer.html")


# ============================================================================
# Interactive ML Prediction Endpoints (Accept JSON or Form data)
# ============================================================================


def _get_request_data():
    if request.is_json:
        return request.get_json() or {}
    return request.form.to_dict()


@app.route("/predict/diabetes", methods=["POST"])
def predict_diabetes_route():
    data = _get_request_data()
    try:
        age = float(data.get("age", 45))
        bmi = float(data.get("bmi", 28.0))
        glucose = float(data.get("glucose", 120))
        insulin = float(data.get("insulin", 100))
        hba1c = float(data.get("hba1c", 6.0))
    except (ValueError, TypeError) as e:
        return jsonify({"success": False, "error": f"Invalid numeric input: {str(e)}"}), 400

    result = ml_models.predict_diabetes(age, bmi, glucose, insulin, hba1c)
    result["success"] = True
    return jsonify(result)


@app.route("/predict/hypertension", methods=["POST"])
def predict_hypertension_route():
    data = _get_request_data()
    try:
        age = float(data.get("age", 50))
        systolic_bp = float(data.get("systolic_bp", 130))
        diastolic_bp = float(data.get("diastolic_bp", 85))
        bmi = float(data.get("bmi", 26.5))
        heart_rate = float(data.get("heart_rate", 72))
    except (ValueError, TypeError) as e:
        return jsonify({"success": False, "error": f"Invalid numeric input: {str(e)}"}), 400

    result = ml_models.predict_hypertension(age, systolic_bp, diastolic_bp, bmi, heart_rate)
    result["success"] = True
    return jsonify(result)


@app.route("/predict/typhoid", methods=["POST"])
def predict_typhoid_route():
    data = _get_request_data()
    try:
        age = float(data.get("age", 30))
        fever_temp = float(data.get("fever_temp", 38.5))
        abdominal_pain = int(data.get("abdominal_pain", 1))
        widal_test = int(data.get("widal_test", 0))
    except (ValueError, TypeError) as e:
        return jsonify({"success": False, "error": f"Invalid input parameters: {str(e)}"}), 400

    result = ml_models.predict_typhoid(age, fever_temp, abdominal_pain, widal_test)
    result["success"] = True
    return jsonify(result)


@app.route("/predict/ecommerce", methods=["POST"])
def predict_ecommerce_route():
    data = _get_request_data()
    try:
        pages_visited = float(data.get("pages_visited", 5))
        time_spent_min = float(data.get("time_spent_min", 15))
        cart_abandoned = int(data.get("cart_abandoned", 0))
    except (ValueError, TypeError) as e:
        return jsonify({"success": False, "error": f"Invalid input parameters: {str(e)}"}), 400

    result = ml_models.predict_ecommerce_purchase(pages_visited, time_spent_min, cart_abandoned)
    result["success"] = True
    return jsonify(result)


@app.route("/api/dataset-summary", methods=["POST"])
def dataset_summary_route():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded in request."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected."}), 400

    try:
        filename = file.filename.lower()
        if filename.endswith(".csv"):
            df = pd.read_csv(file)
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file)
        else:
            return jsonify({"success": False, "error": "Supported formats are CSV, XLS, XLSX."}), 400

        summary = ml_models.summarize_dataframe(df)
        summary["success"] = True
        return jsonify(summary)
    except Exception as e:
        return jsonify({"success": False, "error": f"Error parsing file: {str(e)}"}), 500


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "healthcare-ml-dashboard"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
