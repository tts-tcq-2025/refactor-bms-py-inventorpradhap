from time import sleep
import sys
#Updated
class VitalsLimits:
    TEMP_MIN = 95
    TEMP_MAX = 102
    PULSE_MIN = 60
    PULSE_MAX = 100
    SPO2_MIN = 90

def alert_vital(message: str) -> None:
    """Display alert message with blinking effect."""
    print(message)
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

def check_temperature(temperature: float) -> bool:
    """Check if temperature is within normal range."""
    if temperature < VitalsLimits.TEMP_MIN or temperature > VitalsLimits.TEMP_MAX:
        alert_vital('Temperature critical!')
        return False
    return True

def check_pulse_rate(pulse_rate: float) -> bool:
    """Check if pulse rate is within normal range."""
    if pulse_rate < VitalsLimits.PULSE_MIN or pulse_rate > VitalsLimits.PULSE_MAX:
        alert_vital('Pulse Rate is out of range!')
        return False
    return True

def check_spo2(spo2: float) -> bool:
    """Check if SPO2 is within normal range."""
    if spo2 < VitalsLimits.SPO2_MIN:
        alert_vital('Oxygen Saturation out of range!')
        return False
    return True

def vitals_ok(temperature: float, pulse_rate: float, spo2: float) -> bool:
    """
    Check if all vital signs are within normal ranges.
    
    Args:
        temperature (float): Body temperature (95-102)
        pulse_rate (float): Heart rate (60-100)
        spo2 (float): Oxygen saturation level (>= 90)
    
    Returns:
        bool: True if all vitals are okay, False otherwise
    """
    checks = [
        check_temperature(temperature),
        check_pulse_rate(pulse_rate),
        check_spo2(spo2)
    ]
    return all(checks)
