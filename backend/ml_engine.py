import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression


FEATURES = [
    "voltage",
    "current",
    "active_power",
    "reactive_power",
    "power_factor",
    "frequency",
]


def _feature_matrix(measurements):
    return np.array(
        [
            [float(m[feature]) for feature in FEATURES]
            for m in measurements
        ],
        dtype=float,
    )


def ml_anomaly_detection(measurements):
    """
    Experimental unsupervised anomaly detection using Isolation Forest.

    A minimum number of samples is required before the model is fitted.
    """

    minimum_samples = 8

    if len(measurements) < minimum_samples:
        return {
            "model": "Isolation Forest",
            "status": "INSUFFICIENT_DATA",
            "samples": len(measurements),
            "minimum_samples": minimum_samples,
            "anomalies_detected": 0,
            "results": [],
        }

    X = _feature_matrix(measurements)

    model = IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42,
    )

    predictions = model.fit_predict(X)
    scores = model.decision_function(X)

    results = []

    for index, (prediction, score) in enumerate(
        zip(predictions, scores), start=1
    ):
        results.append(
            {
                "measurement_id": index,
                "classification": (
                    "ANOMALY" if prediction == -1 else "NORMAL"
                ),
                "anomaly_score": round(float(score), 5),
            }
        )

    anomaly_count = sum(
        result["classification"] == "ANOMALY"
        for result in results
    )

    return {
        "model": "Isolation Forest",
        "status": "READY",
        "samples": len(measurements),
        "anomalies_detected": anomaly_count,
        "results": results,
    }


def ml_power_forecast(measurements):
    """
    Experimental short-term active-power forecast using linear regression.
    """

    minimum_samples = 5

    if len(measurements) < minimum_samples:
        return {
            "model": "Linear Regression",
            "status": "INSUFFICIENT_DATA",
            "samples": len(measurements),
            "minimum_samples": minimum_samples,
            "forecast_active_power": None,
        }

    power_values = np.array(
        [float(m["active_power"]) for m in measurements],
        dtype=float,
    )

    X = np.arange(len(power_values)).reshape(-1, 1)
    y = power_values

    model = LinearRegression()
    model.fit(X, y)

    next_index = np.array([[len(power_values)]])
    prediction = float(model.predict(next_index)[0])

    return {
        "model": "Linear Regression",
        "status": "READY",
        "samples": len(measurements),
        "forecast_active_power": round(max(prediction, 0.0), 2),
        "trend_per_sample": round(float(model.coef_[0]), 2),
    }