import unittest
from unittest.mock import Mock
from vitals_monitor import VitalsMonitor, VitalSign, AlertHandler

class MockAlertHandler(AlertHandler):
    def __init__(self):
        self.alerts = []

    def alert(self, message: str):
        self.alerts.append(message)

class TestVitalsMonitor(unittest.TestCase):
    def setUp(self):
        self.alert_handler = MockAlertHandler()
        self.monitor = VitalsMonitor(self.alert_handler)

    def test_normal_vitals(self):
        result = self.monitor.vitals_ok(98.6, 75, 95)
        self.assertTrue(result)
        self.assertEqual(len(self.alert_handler.alerts), 0)

    def test_critical_temperature_high(self):
        result = self.monitor.vitals_ok(103, 75, 95)
        self.assertFalse(result)
        self.assertIn("Temperature is critical!", self.alert_handler.alerts)

    def test_critical_temperature_low(self):
        result = self.monitor.vitals_ok(94, 75, 95)
        self.assertFalse(result)
        self.assertIn("Temperature is critical!", self.alert_handler.alerts)

    def test_critical_pulse_rate_high(self):
        result = self.monitor.vitals_ok(98.6, 101, 95)
        self.assertFalse(result)
        self.assertIn("Pulse Rate is critical!", self.alert_handler.alerts)

    def test_critical_pulse_rate_low(self):
        result = self.monitor.vitals_ok(98.6, 59, 95)
        self.assertFalse(result)
        self.assertIn("Pulse Rate is critical!", self.alert_handler.alerts)

    def test_critical_spo2(self):
        result = self.monitor.vitals_ok(98.6, 75, 89)
        self.assertFalse(result)
        self.assertIn("SPO2 is critical!", self.alert_handler.alerts)

if __name__ == '__main__':
    unittest.main()
