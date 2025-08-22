from time import sleep
import sys
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class VitalLimits:
    min_value: float
    max_value: float
    name: str

class VitalsRanges:
    TEMPERATURE = VitalLimits(95, 102, "Temperature")
    PULSE_RATE = VitalLimits(60, 100, "Pulse Rate")
    SPO2 = VitalLimits(90, 100, "SPO2")

def alert_vital(vital_name: str) -> None:
    """Display alert message with blinking effect."""
    print(f'{vital_name} is out of range!')
    blink_alert()

def blink_alert() -> None:
    """Create blinking alert effect."""
    for _ in range(6):
        print('\r* ', end='')
        sys.stdout.flush()
        sleep(1)
        print('\r ', end='')
        sys.stdout.flush()
        sleep(1)

def check_vital(value: float, limits: VitalLimits) -> bool:
    """
    Check if a vital sign is within its specified limits.
    
    Args:
        value: The measured vital sign value
        limits: The limits object containing min and max values
    
    Returns:
        bool: True if vital is within limits, False otherwise
    """
    if value < limits.min_value or value > limits.max_value:
        alert_vital(limits.name)
        return False
    return True

def vitals_ok(temperature: float, pulse_rate: float, spo2: float) -> bool:
    """
    Check if all vital signs are within normal ranges.
    
    Args:
        temperature: Body temperature
        pulse_rate: Heart rate
        spo2: Oxygen saturation level
    
    Returns:
        bool: True if all vitals are okay, False otherwise
    """
    vitals_checks = [
        (temperature, VitalsRanges.TEMPERATURE),
        (pulse_rate, VitalsRanges.PULSE_RATE),
        (spo2, VitalsRanges.SPO2)
    ]
    
    return all(check_vital(value, limits) for value, limits in vitals_checks)
