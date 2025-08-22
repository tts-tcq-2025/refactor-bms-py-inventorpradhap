from time import sleep
import sys

# --- 1. Configuration / Data Structures ---
# Define acceptable ranges for vital signs
# This makes it easy to add new vitals or change limits
VITAL_THRESHOLDS = {
    "temperature": {"min": 95, "max": 102, "unit": "°F"},
    "pulseRate": {"min": 60, "max": 100, "unit": "bpm"},
    "spo2": {"min": 90, "max": 100, "unit": "%"}, # SpO2 typically doesn't have an upper critical limit for low-risk patients
    # Future vital signs can be added here easily:
    # "bloodPressureSystolic": {"min": 90, "max": 120, "unit": "mmHg"},
    # "bloodPressureDiastolic": {"min": 60, "max": 80, "unit": "mmHg"},
}

# --- 2. I/O Functions (Side Effects) ---
def _perform_critical_alert_animation(duration_seconds=12):
    """
    Performs a visual critical alert animation on the console.
    This is a side effect (I/O) function.
    """
    print("\n!!! CRITICAL ALERT !!!")
    animation_cycles = duration_seconds // 2 # Each cycle is 2 seconds (* then * )
    for _ in range(animation_cycles):
        print('\r* ', end='')
        sys.stdout.flush()
        sleep(1)
        print('\r *', end='')
        sys.stdout.flush()
        sleep(1)
    print("\n") # Newline after animation

def _display_vital_status(vital_name, value, status_message):
    """
    Displays the status of a vital sign.
    This is a side effect (I/O) function.
    """
    print(f"{vital_name}: {value} {status_message}")


# --- 3. Core Logic (Pure Functions) ---
class VitalSignMonitor:
    """
    Monitors vital signs and determines their status based on predefined thresholds.
    Encapsulates vital sign validation logic.
    """
    def __init__(self, thresholds: dict):
        self.thresholds = thresholds

    def _is_within_range(self, vital_name: str, value: float) -> tuple[bool, str]:
        """
        Checks if a specific vital sign value is within its acceptable range.
        This is a pure function.

        Args:
            vital_name: The name of the vital sign (e.g., "temperature").
            value: The measured value of the vital sign.

        Returns:
            A tuple: (True/False if within range, corresponding message)
        """
        if vital_name not in self.thresholds:
            return False, f"Unknown vital sign '{vital_name}'."

        config = self.thresholds[vital_name]
        min_val = config.get("min")
        max_val = config.get("max")
        unit = config.get("unit", "")

        if min_val is not None and value < min_val:
            return False, f"({value}{unit}) is too low (expected >= {min_val}{unit})."
        if max_val is not None and value > max_val:
            return False, f"({value}{unit}) is too high (expected <= {max_val}{unit})."

        return True, f"({value}{unit}) is OK."

    def check_vitals(self, **vitals_readings) -> bool:
        """
        Checks multiple vital signs and determines if all are OK.
        Combines pure function logic with a loop.

        Args:
            **vitals_readings: Keyword arguments where key is vital name
                               and value is the reading (e.g., temperature=98.6).

        Returns:
            True if all vital signs are within acceptable range, False otherwise.
        """
        all_ok = True
        critical_issues_found = []

        for vital_name, value in vitals_readings.items():
            is_ok, message = self._is_within_range(vital_name, value)
            _display_vital_status(vital_name, value, message) # Display status for each vital

            if not is_ok:
                all_ok = False
                critical_issues_found.append(f"{vital_name}: {message}")

        if not all_ok:
            print("\nSummary of critical issues:")
            for issue in critical_issues_found:
                print(f"- {issue}")
            _perform_critical_alert_animation() # Perform animation only if critical
            return False
        else:
            print("\nAll vital signs are within normal limits.")
            return True


# --- Usage Example / Main Execution ---
if __name__ == "__main__":
    monitor = VitalSignMonitor(VITAL_THRESHOLDS)

    print("--- Scenario 1: All Vitals OK ---")
    monitor.check_vitals(temperature=98.6, pulseRate=75, spo2=97)
    print("-" * 30 + "\n")
    sleep(2) # Give a moment between scenarios

    print("--- Scenario 2: Temperature Low ---")
    monitor.check_vitals(temperature=94.0, pulseRate=80, spo2=96)
    print("-" * 30 + "\n")
    sleep(2)

    print("--- Scenario 3: Temperature High ---")
    monitor.check_vitals(temperature=103.0, pulseRate=80, spo2=96)
    print("-" * 30 + "\n")
    sleep(2)

    print("--- Scenario 4: Pulse Rate Low ---")
    monitor.check_vitals(temperature=98.0, pulseRate=55, spo2=98)
    print("-" * 30 + "\n")
    sleep(2)

    print("--- Scenario 5: Pulse Rate High ---")
    monitor.check_vitals(temperature=98.0, pulseRate=105, spo2=98)
    print("-" * 30 + "\n")
    sleep(2)

    print("--- Scenario 6: SpO2 Low ---")
    monitor.check_vitals(temperature=98.5, pulseRate=70, spo2=89)
    print("-" * 30 + "\n")
    sleep(2)

    print("--- Scenario 7: Multiple Vitals Critical ---")
    monitor.check_vitals(temperature=94.0, pulseRate=110, spo2=85)
    print("-" * 30 + "\n")
    sleep(2)

    print("--- Scenario 8: Unknown Vital (for robustness testing) ---")
    monitor.check_vitals(temperature=98.6, respirationRate=15, spo2=97)
    print("-" * 30 + "\n")
    sleep(2)

    # Example of changing limits dynamically (though for age, you'd likely
    # have a Patient class or similar to manage age-based thresholds)
    print("--- Scenario 9: Changing SpO2 limit for a specific case ---")
    # This would typically be a new VitalSignMonitor instance or updated thresholds
    # for a patient group. For demonstration, we'll modify the global one temporarily.
    # In a real system, you'd pass specific thresholds per patient.
    temporary_thresholds = VITAL_THRESHOLDS.copy()
    temporary_thresholds["spo2"]["min"] = 92
    monitor_for_specific_patient = VitalSignMonitor(temporary_thresholds)
    monitor_for_specific_patient.check_vitals(temperature=98.0, pulseRate=75, spo2=91)
    print("-" * 30 + "\n")
