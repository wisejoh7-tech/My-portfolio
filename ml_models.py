"""Machine Learning Engine for Healthcare and E-Commerce Predictions.
Includes model training and inference functions for Diabetes, Hypertension, Typhoid,
and Customer Purchasing Behavior, along with dataset summary utilities.
"""

from typing import Any, Dict
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


def _init_diabetes_model() -> LogisticRegression:
    np.random.seed(42)
    n = 300
    age = np.random.uniform(20, 75, n)
    bmi = np.random.uniform(18, 45, n)
    glucose = np.random.uniform(70, 220, n)
    insulin = np.random.uniform(15, 300, n)
    hba1c = np.random.uniform(4.0, 11.0, n)

    logits = (
        -8.5
        + (age * 0.03)
        + (bmi * 0.08)
        + (glucose * 0.025)
        + (insulin * 0.004)
        + (hba1c * 0.55)
    )
    prob = 1 / (1 + np.exp(-logits))
    y = (prob > 0.5).astype(int)

    x = np.column_stack([age, bmi, glucose, insulin, hba1c])
    model = LogisticRegression(max_iter=1000)
    model.fit(x, y)
    return model


def _init_hypertension_model() -> RandomForestClassifier:
    np.random.seed(42)
    n = 300
    age = np.random.uniform(20, 80, n)
    sbp = np.random.uniform(90, 190, n)
    dbp = np.random.uniform(60, 120, n)
    bmi = np.random.uniform(18, 42, n)
    hr = np.random.uniform(55, 110, n)

    logits = -9.0 + (age * 0.04) + (sbp * 0.04) + (dbp * 0.035) + (bmi * 0.05)
    prob = 1 / (1 + np.exp(-logits))
    y = (prob > 0.5).astype(int)

    x = np.column_stack([age, sbp, dbp, bmi, hr])
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(x, y)
    return model


def _init_typhoid_model() -> LogisticRegression:
    np.random.seed(42)
    n = 300
    age = np.random.uniform(10, 75, n)
    fever = np.random.uniform(36.5, 41.5, n)
    abd_pain = np.random.binomial(1, 0.45, n)
    widal = np.random.binomial(1, 0.35, n)

    logits = -14.0 + (fever * 0.28) + (abd_pain * 1.5) + (widal * 2.8)
    prob = 1 / (1 + np.exp(-logits))
    y = (prob > 0.5).astype(int)

    x = np.column_stack([age, fever, abd_pain, widal])
    model = LogisticRegression(max_iter=1000)
    model.fit(x, y)
    return model


def _init_ecommerce_model() -> RandomForestClassifier:
    np.random.seed(42)
    n = 400
    pages = np.random.uniform(1, 30, n)
    time_spent = np.random.uniform(2, 90, n)
    abandoned = np.random.binomial(1, 0.4, n)

    logits = -3.0 + (pages * 0.15) + (time_spent * 0.05) - (abandoned * 1.8)
    prob = 1 / (1 + np.exp(-logits))
    y = (prob > 0.5).astype(int)

    x = np.column_stack([pages, time_spent, abandoned])
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(x, y)
    return model


# Lazy-loaded model singletons
_DIABETES_MODEL = None
_HYPERTENSION_MODEL = None
_TYPHOID_MODEL = None
_ECOMMERCE_MODEL = None


def get_diabetes_model() -> LogisticRegression:
    global _DIABETES_MODEL
    if _DIABETES_MODEL is None:
        _DIABETES_MODEL = _init_diabetes_model()
    return _DIABETES_MODEL


def get_hypertension_model() -> RandomForestClassifier:
    global _HYPERTENSION_MODEL
    if _HYPERTENSION_MODEL is None:
        _HYPERTENSION_MODEL = _init_hypertension_model()
    return _HYPERTENSION_MODEL


def get_typhoid_model() -> LogisticRegression:
    global _TYPHOID_MODEL
    if _TYPHOID_MODEL is None:
        _TYPHOID_MODEL = _init_typhoid_model()
    return _TYPHOID_MODEL


def get_ecommerce_model() -> RandomForestClassifier:
    global _ECOMMERCE_MODEL
    if _ECOMMERCE_MODEL is None:
        _ECOMMERCE_MODEL = _init_ecommerce_model()
    return _ECOMMERCE_MODEL


def predict_diabetes(age: float, bmi: float, glucose: float, insulin: float, hba1c: float) -> Dict[str, Any]:
    model = get_diabetes_model()
    feats = np.array([[float(age), float(bmi), float(glucose), float(insulin), float(hba1c)]])
    pred = int(model.predict(feats)[0])
    prob = float(model.predict_proba(feats)[0][1])

    risk_level = "High" if prob >= 0.65 else ("Moderate" if prob >= 0.35 else "Low")
    recommendation = (
        "High risk indicated. Medical consultation and blood glucose evaluation recommended."
        if prob >= 0.65
        else (
            "Moderate risk indicated. Routine screening and lifestyle adjustments recommended."
            if prob >= 0.35
            else "Low risk indicated. Maintain healthy diet and active physical routine."
        )
    )
    return {
        "prediction": pred,
        "probability": round(prob * 100, 2),
        "risk_level": risk_level,
        "recommendation": recommendation,
        "features": {
            "age": age,
            "bmi": bmi,
            "glucose": glucose,
            "insulin": insulin,
            "hba1c": hba1c,
        },
    }


def predict_hypertension(
    age: float, systolic_bp: float, diastolic_bp: float, bmi: float, heart_rate: float
) -> Dict[str, Any]:
    model = get_hypertension_model()
    feats = np.array([[float(age), float(systolic_bp), float(diastolic_bp), float(bmi), float(heart_rate)]])
    pred = int(model.predict(feats)[0])
    prob = float(model.predict_proba(feats)[0][1])

    risk_level = "Stage 2 / High Risk" if prob >= 0.65 else ("Elevated / Stage 1" if prob >= 0.35 else "Normal")
    recommendation = (
        "High hypertension probability. Advise clinical blood pressure monitoring and physician consultation."
        if prob >= 0.65
        else (
            "Borderline/Elevated readings. Monitor sodium intake and stress management."
            if prob >= 0.35
            else "Cardiovascular metrics within expected healthy range."
        )
    )
    return {
        "prediction": pred,
        "probability": round(prob * 100, 2),
        "risk_level": risk_level,
        "recommendation": recommendation,
        "features": {
            "age": age,
            "systolic_bp": systolic_bp,
            "diastolic_bp": diastolic_bp,
            "bmi": bmi,
            "heart_rate": heart_rate,
        },
    }


def predict_typhoid(age: float, fever_temp: float, abdominal_pain: int, widal_test: int) -> Dict[str, Any]:
    model = get_typhoid_model()
    feats = np.array([[float(age), float(fever_temp), int(abdominal_pain), int(widal_test)]])
    pred = int(model.predict(feats)[0])
    prob = float(model.predict_proba(feats)[0][1])

    risk_level = (
        "Positive / High Probability"
        if prob >= 0.55
        else ("Indeterminate / Moderate" if prob >= 0.3 else "Negative / Low Probability")
    )
    recommendation = (
        "Symptoms and markers indicate probable Typhoid infection. Blood culture and physician assessment recommended."
        if prob >= 0.55
        else (
            "Mild symptoms present. Observe fever curve and re-test if symptoms persist."
            if prob >= 0.3
            else "Low probability of Typhoid infection based on presented markers."
        )
    )
    return {
        "prediction": pred,
        "probability": round(prob * 100, 2),
        "risk_level": risk_level,
        "recommendation": recommendation,
        "features": {
            "age": age,
            "fever_temp": fever_temp,
            "abdominal_pain": abdominal_pain,
            "widal_test": widal_test,
        },
    }


def predict_ecommerce_purchase(pages_visited: float, time_spent_min: float, cart_abandoned: int) -> Dict[str, Any]:
    model = get_ecommerce_model()
    feats = np.array([[float(pages_visited), float(time_spent_min), int(cart_abandoned)]])
    pred = int(model.predict(feats)[0])
    prob = float(model.predict_proba(feats)[0][1])

    intent = "High Purchase Intent" if prob >= 0.60 else ("Moderate Intent" if prob >= 0.35 else "Low Intent")
    strategy = (
        "Send limited-time offer or checkout reminder immediately."
        if prob >= 0.60
        else (
            "Retarget with related product recommendations and reviews."
            if prob >= 0.35
            else "Deliver general brand engagement and top category highlights."
        )
    )
    return {
        "prediction": pred,
        "purchase_probability": round(prob * 100, 2),
        "intent": intent,
        "strategy": strategy,
        "features": {
            "pages_visited": pages_visited,
            "time_spent_min": time_spent_min,
            "cart_abandoned": cart_abandoned,
        },
    }


def summarize_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """Generates summary statistics, missing values, and column types for a DataFrame."""
    summary = {
        "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "head": df.head(5).to_dict(orient="records"),
        "numeric_stats": df.describe().round(2).to_dict() if not df.empty else {},
    }
    return summary
