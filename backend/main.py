from datetime import datetime, timezone, timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import EnergyMeasurement, MeasurementResponse
from .analytics import (
    analyze_measurement,
    calculate_statistics,
    forecast_power,
)
from .ml_engine import (
    ml_anomaly_detection,
    ml_power_forecast,
)
from .database import (
    initialize_database,
    save_measurement,
    load_measurements,
)


# --------------------------------------------------
# APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Intelligent Energy Analytics API",
    description=(
        "Electrical energy monitoring, analytics, "
        "rule-based anomaly detection and machine-learning forecasting API."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

initialize_database()


# --------------------------------------------------
# BASIC API
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "project": "Intelligent Energy Analytics",
        "version": "1.0.0",
        "status": "running",
        "storage": "SQLite",
        "analytics": True,
        "machine_learning": True,
    }


@app.get("/health")
def health_check():

    measurements = load_measurements()

    return {
        "status": "healthy",
        "api": "online",
        "database": "connected",
        "database_engine": "SQLite",
        "stored_measurements": len(measurements),
        "ml_engine": "available",
    }


# --------------------------------------------------
# MEASUREMENTS
# --------------------------------------------------

@app.post("/measurements", response_model=MeasurementResponse)
def create_measurement(measurement: EnergyMeasurement):

    data = measurement.model_dump()

    data["timestamp"] = measurement.timestamp.isoformat()

    measurement_id = save_measurement(data)

    return MeasurementResponse(
        message="Energy measurement stored successfully",
        measurement_id=measurement_id,
        received_at=datetime.now(timezone.utc),
    )


@app.get("/measurements")
def get_measurements():

    measurements = load_measurements()

    return {
        "count": len(measurements),
        "measurements": measurements,
    }


# --------------------------------------------------
# TRADITIONAL ANALYTICS
# --------------------------------------------------

@app.get("/analytics/statistics")
def get_statistics():

    measurements = load_measurements()

    return calculate_statistics(measurements)


@app.get("/analytics/anomalies")
def get_anomalies():

    measurements = load_measurements()

    anomalies = []

    for item in measurements:

        analysis = analyze_measurement(item)

        if analysis["anomaly_detected"]:

            anomalies.append(
                {
                    "measurement_id": item["id"],
                    "timestamp": item["timestamp"],
                    "voltage": item["voltage"],
                    "current": item["current"],
                    "active_power": item["active_power"],
                    "power_factor": item["power_factor"],
                    "frequency": item["frequency"],
                    "analysis": analysis,
                }
            )

    return {
        "total_measurements": len(measurements),
        "anomalies_detected": len(anomalies),
        "anomalies": anomalies,
    }


@app.get("/analytics/forecast")
def get_forecast():

    measurements = load_measurements()

    return forecast_power(measurements)


# --------------------------------------------------
# MACHINE LEARNING
# --------------------------------------------------

@app.get("/ml/anomalies")
def get_ml_anomalies():

    measurements = load_measurements()

    result = ml_anomaly_detection(measurements)

    # Replace sequential ML IDs with real database IDs
    if result.get("results"):

        for index, ml_result in enumerate(result["results"]):

            if index < len(measurements):
                ml_result["measurement_id"] = measurements[index]["id"]

    return result


@app.get("/ml/forecast")
def get_ml_forecast():

    measurements = load_measurements()

    return ml_power_forecast(measurements)


# --------------------------------------------------
# SYNTHETIC DEMONSTRATION DATA
# --------------------------------------------------

@app.post("/demo/load")
def load_demo_dataset():

    existing = load_measurements()

    if existing:

        return {
            "status": "SKIPPED",
            "message": (
                "Database already contains measurements. "
                "Demo data was not inserted to avoid duplicates."
            ),
            "existing_measurements": len(existing),
        }


    base_time = datetime.now(timezone.utc) - timedelta(minutes=19)

    demo_readings = [
        (229.8, 2.10, 455.0, 110.0, 0.97, 50.02),
        (230.4, 2.18, 472.0, 115.0, 0.97, 50.01),
        (231.0, 2.25, 490.0, 120.0, 0.96, 50.00),
        (230.6, 2.32, 505.0, 125.0, 0.96, 49.99),
        (229.9, 2.40, 520.0, 130.0, 0.95, 50.01),

        (230.7, 2.48, 540.0, 135.0, 0.95, 50.02),
        (231.2, 2.55, 558.0, 140.0, 0.95, 50.00),
        (230.5, 2.63, 575.0, 145.0, 0.94, 49.98),

        # Demonstration anomaly:
        # high voltage + low PF + frequency deviation
        (264.5, 4.80, 1095.0, 420.0, 0.72, 51.80),

        (230.8, 2.70, 592.0, 150.0, 0.94, 50.01),
        (231.3, 2.78, 610.0, 155.0, 0.94, 50.00),
        (230.2, 2.85, 625.0, 160.0, 0.93, 49.99),
        (229.7, 2.92, 640.0, 165.0, 0.93, 50.02),
        (230.9, 3.00, 660.0, 170.0, 0.93, 50.01),

        # Demonstration low-voltage anomaly
        (201.0, 3.60, 690.0, 240.0, 0.88, 49.90),

        (231.1, 3.08, 675.0, 175.0, 0.92, 50.00),
        (230.6, 3.15, 690.0, 180.0, 0.92, 49.99),
        (231.4, 3.22, 708.0, 185.0, 0.92, 50.01),
        (230.8, 3.30, 725.0, 190.0, 0.91, 50.00),
        (231.0, 3.38, 742.0, 195.0, 0.91, 50.02),
    ]


    inserted_ids = []


    for index, reading in enumerate(demo_readings):

        timestamp = (
            base_time + timedelta(minutes=index)
        ).isoformat()

        data = {
            "timestamp": timestamp,
            "voltage": reading[0],
            "current": reading[1],
            "active_power": reading[2],
            "reactive_power": reading[3],
            "power_factor": reading[4],
            "frequency": reading[5],
        }

        measurement_id = save_measurement(data)

        inserted_ids.append(measurement_id)


    return {
        "status": "SUCCESS",
        "dataset": "Synthetic demonstration dataset",
        "measurements_inserted": len(inserted_ids),
        "measurement_ids": inserted_ids,
        "note": (
            "Synthetic values are provided only for software "
            "demonstration and ML pipeline testing."
        ),
    }


# --------------------------------------------------
# PROJECT SUMMARY
# --------------------------------------------------

@app.get("/system/summary")
def system_summary():

    measurements = load_measurements()

    statistics = calculate_statistics(measurements)

    rule_results = []

    for item in measurements:

        analysis = analyze_measurement(item)

        if analysis["anomaly_detected"]:
            rule_results.append(item["id"])


    ml_anomalies = ml_anomaly_detection(measurements)

    ml_forecast = ml_power_forecast(measurements)


    return {
        "project": "Intelligent Energy Analytics",
        "version": "1.0.0",
        "database": "SQLite",
        "measurements": len(measurements),
        "statistics": statistics,
        "rule_based_anomalies": len(rule_results),
        "ml_anomaly_model": ml_anomalies["model"],
        "ml_anomaly_status": ml_anomalies["status"],
        "ml_anomalies_detected": ml_anomalies["anomalies_detected"],
        "forecast_model": ml_forecast["model"],
        "forecast_status": ml_forecast["status"],
        "forecast_active_power": ml_forecast["forecast_active_power"],
    }