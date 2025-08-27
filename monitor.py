from time import sleep
import sys

def blink_alert(times=6, delay=1):
    """Simple blinking alert animation."""
    for _ in range(times):
        print('\r* ', end='')
        sys.stdout.flush()
        sleep(delay)
        print('\r *', end='')
        sys.stdout.flush()
        sleep(delay)

def alert(message):
    """Display critical alert message with blinking animation."""
    print(message)
    blink_alert()

def vitals_ok(temperature, pulseRate, spo2):
    if temperature > 102 or temperature < 95:
        alert('Temperature critical!')
        return False

    if pulseRate < 60 or pulseRate > 100:
        alert('Pulse Rate is out of range!')
        return False

    if spo2 < 90:
        alert('Oxygen Saturation out of range!')
        return False

    return True
