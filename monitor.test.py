import unittest
from unittest.mock import patch
from monitor import vitals_ok

class TestVitalsMonitor(unittest.TestCase):
    
    @patch('monitor.alert_vital')
    def test_normal_vitals(self, mock_alert):
        self.assertTrue(vitals_ok(98.6, 75, 95))
        mock_alert.assert_not_called()

    @patch('monitor.alert_vital')
    def test_temperature_high(self, mock_alert):
        self.assertFalse(vitals_ok(103, 75, 95))
        mock_alert.assert_called_once_with('Temperature critical!')

    @patch('monitor.alert_vital')
    def test_temperature_low(self, mock_alert):
        self.assertFalse(vitals_ok(94, 75, 95))
        mock_alert.assert_called_once_with('Temperature critical!')

    @patch('monitor.alert_vital')
    def test_pulse_rate_high(self, mock_alert):
        self.assertFalse(vitals_ok(98.6, 101, 95))
        mock_alert.assert_called_once_with('Pulse Rate is out of range!')

    @patch('monitor.alert_vital')
    def test_pulse_rate_low(self, mock_alert):
        self.assertFalse(vitals_ok(98.6, 59, 95))
        mock_alert.assert_called_once_with('Pulse Rate is out of range!')

    @patch('monitor.alert_vital')
    def test_spo2_low(self, mock_alert):
        self.assertFalse(vitals_ok(98.6, 75, 89))
        mock_alert.assert_called_once_with('Oxygen Saturation out of range!')

    @patch('monitor.alert_vital')
    def test_multiple_vitals_critical(self, mock_alert):
        self.assertFalse(vitals_ok(103, 101, 89))
        # Will stop at first failure (temperature)
        mock_alert.assert_called_once_with('Temperature critical!')

if __name__ == '__main__':
    unittest.main()
