from datetime import datetime, timezone
from fastapi import FastAPI
from .schemas import EnergyMeasurement, MeasurementResponse

app = FastAPI(
    title="Intelligent Energy Analytics API",
    description="API for electrical energy analytics, load monitoring and intelligent energy systems.",
    version="0.2.0"
)

# Temporary in-memory storage
measurements = []


@app.get("/")
def root():
    return {
        "project": "Intelligent Energy Analytics",
        "status": "running",
        "version": "0.2.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/measurements", response_model=MeasurementResponse)
def create_measurement(measurement: EnergyMeasurement):

    measurement_id = len(measurements) + 1

    measurements.append({
        "id": measurement_id,
        "data": measurement
    })

    return MeasurementResponse(
        message="Energy measurement received successfully",
        measurement_id=measurement_id,
        received_at=datetime.now(timezone.utc)
    )


@app.get("/measurements")
def get_measurements():
    return {
        "count": len(measurements),
        "measurements": measurements
    }
