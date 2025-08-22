from time import sleep
import sys
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Tuple

@dataclass
class VitalSign:
    name: str
    value: float
    min_limit: float
    max_limit: float

    def is_critical(self) -> bool:
        return not (self.min_limit <= self.value <= self.max_limit)

class AlertHandler(ABC):
    @abstractmethod
    def alert(self, message: str):
        pass

class ConsoleAlertHandler(AlertHandler):
    def alert(self, message: str):
        print(message)
        self._blink_alert()

    def _blink_alert(self, times: int = 6, interval: float = 1):
        for _ in range(times):
            print('\r* ', end='')
            sys.stdout.flush()
            sleep(interval)
            print('\r ', end='')
            sys.stdout.flush()
            sleep(interval)

class VitalsMonitor:
    def __init__(self, alert_handler: AlertHandler):
        self.alert_handler = alert_handler
        self._initialize_vital_limits()

    def _initialize_vital_limits(self):
        self.vital_limits = {
            "temperature": (95, 102),
            "pulse_rate": (60, 100),
            "spo2": (90, 100)
        }

    def check_vital(self, vital: VitalSign) -> bool:
        if vital.is_critical():
            self.alert_handler.alert(f'{vital.name} is critical!')
            return False
        return True

    def vitals_ok(self, temperature: float, pulse_rate: float, spo2: float) -> bool:
        vitals = [
            VitalSign("Temperature", temperature, *self.vital_limits["temperature"]),
            VitalSign("Pulse Rate", pulse_rate, *self.vital_limits["pulse_rate"]),
            VitalSign("SPO2", spo2, *self.vital_limits["spo2"])
        ]
        return all(self.check_vital(vital) for vital in vitals)
