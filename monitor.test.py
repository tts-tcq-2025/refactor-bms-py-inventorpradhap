import unittest
from unittest.mock import patch
import io
from monitor import vitals_ok

class MonitorTest(unittest.TestCase):
    def test_not_ok_when_any_vital_out_of_range(self):
        # Basic pass/fail checks
        self.assertFalse(vitals_ok(99, 102, 70))   # high pulse, low spo2
        self.assertTrue(vitals_ok(98.1, 70, 98))   # all normal

    def test_temperature_alert_message(self):
        with patch('sys.stdout', new_callable=io.StringIO) as fake_out:
            vitals_ok(103, 70, 95)  # Temperature high
            output = fake_out.getvalue()
            self.assertIn("Temperature critical!", output)

    def test_pulse_alert_message(self):
        with patch('sys.stdout', new_callable=io.StringIO) as fake_out:
            vitals_ok(98, 120, 95)  # Pulse high
            output = fake_out.getvalue()
            self.assertIn("Pulse Rate is out of range!", output)

    def test_spo2_alert_message(self):
        with patch('sys.stdout', new_callable=io.StringIO) as fake_out:
            vitals_ok(98, 70, 85)  # Low oxygen
            output = fake_out.getvalue()
            self.assertIn("Oxygen Saturation out of range!", output)

if __name__ == '__main__':
    unittest.main()
