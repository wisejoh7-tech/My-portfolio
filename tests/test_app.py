import io
import pytest
from app import app
import ml_models


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"


def test_html_routes(client):
    routes = [
        "/",
        "/skills",
        "/projects",
        "/analytic",
        "/diabetes",
        "/hypertension",
        "/ecommerce",
        "/typhoid",
        "/retailer",
    ]
    for route in routes:
        res = client.get(route)
        assert res.status_code == 200, f"Failed route {route}"
        assert (
            b"<!DOCTYPE html>" in res.data
            or b"<!doctype html>" in res.data
            or b"<!DOCTYPE HTML" in res.data
        )


def test_predict_diabetes_valid(client):
    payload = {
        "age": 50,
        "bmi": 32.5,
        "glucose": 150,
        "insulin": 180,
        "hba1c": 7.2,
    }
    res = client.post("/predict/diabetes", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "probability" in data
    assert "risk_level" in data
    assert "recommendation" in data
    assert data["probability"] >= 0 and data["probability"] <= 100


def test_predict_diabetes_invalid(client):
    res = client.post("/predict/diabetes", json={"age": "invalid-age"})
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False


def test_predict_hypertension_valid(client):
    payload = {
        "age": 55,
        "systolic_bp": 145,
        "diastolic_bp": 92,
        "bmi": 29.0,
        "heart_rate": 80,
    }
    res = client.post("/predict/hypertension", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "probability" in data
    assert "risk_level" in data


def test_predict_hypertension_invalid(client):
    res = client.post("/predict/hypertension", json={"systolic_bp": "abc"})
    assert res.status_code == 400
    assert res.get_json()["success"] is False


def test_predict_typhoid_valid(client):
    payload = {
        "age": 28,
        "fever_temp": 39.8,
        "abdominal_pain": 1,
        "widal_test": 1,
    }
    res = client.post("/predict/typhoid", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "probability" in data


def test_predict_ecommerce_valid(client):
    payload = {
        "pages_visited": 15,
        "time_spent_min": 35,
        "cart_abandoned": 0,
    }
    res = client.post("/predict/ecommerce", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "purchase_probability" in data
    assert "intent" in data


def test_dataset_summary_csv(client):
    csv_content = b"Patient_ID,Age,BMI,Glucose\n1,25,22.1,95\n2,48,31.0,140\n"
    data = {"file": (io.BytesIO(csv_content), "patients.csv")}
    res = client.post("/api/dataset-summary", data=data, content_type="multipart/form-data")
    assert res.status_code == 200
    result = res.get_json()
    assert result["success"] is True
    assert result["shape"]["rows"] == 2
    assert result["shape"]["columns"] == 4
    assert "Patient_ID" in result["columns"]


def test_dataset_summary_no_file(client):
    res = client.post("/api/dataset-summary", data={})
    assert res.status_code == 400
    assert res.get_json()["success"] is False


def test_ml_models_functions():
    d = ml_models.predict_diabetes(30, 22.0, 90, 45, 5.0)
    assert d["prediction"] in (0, 1)

    h = ml_models.predict_hypertension(30, 115, 75, 22.0, 70)
    assert h["prediction"] in (0, 1)

    t = ml_models.predict_typhoid(25, 37.0, 0, 0)
    assert t["prediction"] in (0, 1)

    e = ml_models.predict_ecommerce_purchase(2, 5, 1)
    assert e["prediction"] in (0, 1)
