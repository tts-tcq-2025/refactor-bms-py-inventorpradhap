import unittest
from unittest.mock import patch
import io
from monitor import vitals_ok

class TestVitalsMonitor(unittest.TestCase):

    @patch('monitor.alert')  # Mock alert to silence blinking animation during tests
    def test_temperature_high(self, mock_alert):
        result = vitals_ok(103, 70, 95)
        self.assertFalse(result)
        mock_alert.assert_called_once_with('Temperature critical!')

    @patch('monitor.alert')
    def test_temperature_low(self, mock_alert):
        result = vitals_ok(94, 70, 95)
        self.assertFalse(result)
        mock_alert.assert_called_once_with('Temperature critical!')

    @patch('monitor.alert')
    def test_pulse_rate_low(self, mock_alert):
        result = vitals_ok(98, 50, 95)
        self.assertFalse(result)
        mock_alert.assert_called_once_with('Pulse Rate is out of range!')

    @patch('monitor.alert')
    def test_pulse_rate_high(self, mock_alert):
        result = vitals_ok(98, 105, 95)
        self.assertFalse(result)
        mock_alert.assert_called_once_with('Pulse Rate is out of range!')

    @patch('monitor.alert')
    def test_spo2_low(self, mock_alert):
        result = vitals_ok(98, 70, 85)
        self.assertFalse(result)
        mock_alert.assert_called_once_with('Oxygen Saturation out of range!')

    @patch('monitor.alert')
    def test_multiple_vitals_critical(self, mock_alert):
        # The alert should be triggered for the first critical value found
        result = vitals_ok(103, 105, 85)
        self.assertFalse(result)
        mock_alert.assert_called_once_with('Temperature critical!')

    @patch('monitor.alert')
    def test_normal_vitals(self, mock_alert):
        result = vitals_ok(98, 70, 98)
        self.assertTrue(result)
        mock_alert.assert_not_called()

if __name__ == '__main__':
    unittest.main()
