from datetime import datetime
from pydantic import BaseModel, Field


class EnergyMeasurement(BaseModel):
    timestamp: datetime

    voltage: float = Field(..., gt=0, description="RMS voltage in volts")
    current: float = Field(..., ge=0, description="RMS current in amperes")

    active_power: float = Field(..., description="Active power in watts")
    reactive_power: float = Field(..., description="Reactive power in VAR")

    power_factor: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="Electrical power factor"
    )

    frequency: float = Field(
        ...,
        gt=0,
        description="Supply frequency in Hz"
    )


class MeasurementResponse(BaseModel):
    message: str
    measurement_id: int
    received_at: datetime
