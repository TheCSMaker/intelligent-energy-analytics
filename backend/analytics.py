from statistics import mean


def analyze_measurement(data):
    """
    Analyze one electrical measurement and identify
    basic power-quality anomalies.
    """

    issues = []
    severity = "NORMAL"

    voltage = data["voltage"]
    frequency = data["frequency"]
    power_factor = data["power_factor"]
    current = data["current"]
    active_power = data["active_power"]

    # Voltage analysis
    if voltage < 207:
        issues.append("Low voltage detected")
    elif voltage > 253:
        issues.append("High voltage detected")

    # Frequency analysis
    if frequency < 49.5 or frequency > 50.5:
        issues.append("Frequency deviation detected")

    # Power factor analysis
    if power_factor < 0.85:
        issues.append("Low power factor")

    # Current sanity check
    if current < 0:
        issues.append("Invalid negative current")

    # Power sanity check
    if active_power < 0:
        issues.append("Negative active power detected")

    if issues:
        severity = "ANOMALY"

    return {
        "status": severity,
        "anomaly_detected": len(issues) > 0,
        "issues": issues
    }


def calculate_statistics(measurements):
    """
    Calculate summary statistics from stored measurements.
    """

    if not measurements:
        return {
            "count": 0,
            "average_voltage": 0,
            "average_current": 0,
            "average_active_power": 0,
            "average_power_factor": 0
        }

    return {
        "count": len(measurements),
        "average_voltage": round(
            mean(m["voltage"] for m in measurements), 2
        ),
        "average_current": round(
            mean(m["current"] for m in measurements), 2
        ),
        "average_active_power": round(
            mean(m["active_power"] for m in measurements), 2
        ),
        "average_power_factor": round(
            mean(m["power_factor"] for m in measurements), 3
        )
    }


def forecast_power(measurements, window=5):
    """
    Simple short-term baseline forecast using
    the moving average of recent active-power readings.
    """

    if not measurements:
        return {
            "forecast_active_power": 0,
            "method": "moving_average",
            "samples_used": 0
        }

    recent = measurements[-window:]

    predicted_power = mean(
        m["active_power"] for m in recent
    )

    return {
        "forecast_active_power": round(predicted_power, 2),
        "method": "moving_average",
        "samples_used": len(recent)
    }