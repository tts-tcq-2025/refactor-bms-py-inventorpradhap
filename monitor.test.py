import unittest
from unittest.mock import patch
from monitor import vitals_ok

class TestVitalsMonitor(unittest.TestCase):
    
    @patch('monitor.alert_vital')
    def test_normal_vitals(self, mock_alert):
        """Test when all vitals are normal."""
        self.assertTrue(vitals_ok(98.6, 75, 95))
        mock_alert.assert_not_called()

    @patch('monitor.alert_vital')
    def test_temperature_high(self, mock_alert):
        """Test when temperature is too high."""
        self.assertFalse(vitals_ok(103, 75, 95))
        mock_alert.assert_called_once_with('Temperature')

    @patch('monitor.alert_vital')
    def test_temperature_low(self, mock_alert):
        """Test when temperature is too low."""
        self.assertFalse(vitals_ok(94, 75, 95))
        mock_alert.assert_called_once_with('Temperature')

    @patch('monitor.alert_vital')
    def test_pulse_rate_high(self, mock_alert):
        """Test when pulse rate is too high."""
        self.assertFalse(vitals_ok(98.6, 101, 95))
        mock_alert.assert_called_once_with('Pulse Rate')

    @patch('monitor.alert_vital')
    def test_pulse_rate_low(self, mock_alert):
        """Test when pulse rate is too low."""
        self.assertFalse(vitals_ok(98.6, 59, 95))
        mock_alert.assert_called_once_with('Pulse Rate')

    @patch('monitor.alert_vital')
    def test_spo2_low(self, mock_alert):
        """Test when SPO2 is too low."""
        self.assertFalse(vitals_ok(98.6, 75, 89))
        mock_alert.assert_called_once_with('SPO2')

    @patch('monitor.alert_vital')
    def test_multiple_vitals_out_of_range(self, mock_alert):
        """Test when multiple vitals are out of range."""
        self.assertFalse(vitals_ok(103, 101, 89))
        mock_alert.assert_called_once_with('Temperature')

if __name__ == '__main__':
    unittest.main()
