from time import sleep
import sys

def alert_vital(message: str) -> None:
    print(message)
    for _ in range(6):
        print('\r* ', end='')
        sys.stdout.flush()
        sleep(1)
        print('\r ', end='')
        sys.stdout.flush()
        sleep(1)

def check_temperature(temperature: float) -> bool:
    if temperature > 102 or temperature < 95:
        alert_vital('Temperature critical!')
        return False
    return True

def check_pulse_rate(pulse_rate: float) -> bool:
    if pulse_rate < 60 or pulse_rate > 100:
        alert_vital('Pulse Rate is out of range!')
        return False
    return True

def check_spo2(spo2: float) -> bool:
    if spo2 < 90:
        alert_vital('Oxygen Saturation out of range!')
        return False
    return True

def vitals_ok(temperature: float, pulse_rate: float, spo2: float) -> bool:
    """
    Check if vital signs are within normal ranges.
    
    Args:
        temperature (float): Body temperature
        pulse_rate (float): Heart rate
        spo2 (float): Oxygen saturation level
    
    Returns:
        bool: True if all vitals are okay, False otherwise
    """
    return (check_temperature(temperature) and 
            check_pulse_rate(pulse_rate) and 
            check_spo2(spo2))
