from time import sleep
import sys
from typing import Dict, Any, Tuple, Optional, Callable

# --- 1. Configuration / Data Structures ---
# Define acceptable ranges for vital signs
VITAL_THRESHOLDS: Dict[str, Dict[str, Any]] = {
    "temperature": {"min": 95.0, "max": 102.0, "unit": "°F"},
    "pulseRate": {"min": 60, "max": 100, "unit": "bpm"},
    "spo2": {"min": 90, "max": 100, "unit": "%"},
}

# --- 2. I/O Functions (Side Effects) ---
def _perform_critical_alert_animation(duration_seconds: int = 12) -> None:
    """
    Performs a visual critical alert animation on the console.
    CCN = 2 (1 for loop, 1 base)
    """
    print("\n!!! CRITICAL ALERT !!!")
    animation_cycles = duration_seconds // 2
    for _ in range(animation_cycles): # +1 CCN
        print('\r* ', end='')
        sys.stdout.flush()
        sleep(1)
        print('\r *', end='')
        sys.stdout.flush()
        sleep(1)
    print("\n")

def _display_vital_status(vital_name: str, value: float, status_message: str) -> None:
    """
    Displays the status of a vital sign.
    CCN = 1 (1 base)
    """
    print(f"{vital_name}: {value} {status_message}")

def _display_critical_summary(issues: list[str]) -> None:
    """
    Displays a summary of critical issues.
    CCN = 2 (1 for loop, 1 base)
    """
    print("\nSummary of critical issues:")
    for issue in issues: # +1 CCN
        print(f"- {issue}")

# --- 3. Core Logic (Pure Functions) ---
class VitalSignMonitor:
    """
    Monitors vital signs and determines their status based on predefined thresholds.
    Encapsulates vital sign validation logic.
    """
    def __init__(self, thresholds: Dict[str, Dict[str, Any]]):
        self.thresholds = thresholds # CCN = 1

    def _check_boundary_condition(
        self,
        value: float,
        limit: Optional[float],
        check_func: Callable[[float, float], bool], # e.g., lambda v, l: v < l
        fail_message_template: str,
        unit: str,
        vital_name_for_debug: str = "" # Added for clearer message context
    ) -> Tuple[bool, str]:
        """
        Generic helper to check a single boundary condition.
        CCN = 2 (1 for 'if limit is None', 1 for 'if check_func')
        """
        if limit is None: # +1 CCN
            return True, "" # No limit to check

        if check_func(value, limit): # +1 CCN
            return False, fail_message_template.format(value=value, limit=limit, unit=unit)
        return True, ""

    def _is_within_range(self, vital_name: str, value: float) -> Tuple[bool, str]:
        """
        Checks if a specific vital sign value is within its acceptable range.
        CCN = 3 (1 for 'if vital_name not in', 1 for min check, 1 for max check)
        """
        if vital_name not in self.thresholds: # +1 CCN
            return False, f"Unknown vital sign '{vital_name}'."

        config = self.thresholds[vital_name]
        unit = config.get("unit", "")
        formatted_value_unit = f"({value}{unit})"

        is_min_ok, min_msg = self._check_boundary_condition(
            value, config.get("min"), lambda v, l: v < l,
            f"{formatted_value_unit} is too low (expected >= {{limit}}{{unit}}).",
            unit, vital_name
        )
        if not is_min_ok: # +1 CCN
            return False, min_msg

        is_max_ok, max_msg = self._check_boundary_condition(
            value, config.get("max"), lambda v, l: v > l,
            f"{formatted_value_unit} is too high (expected <= {{limit}}{{unit}}).",
            unit, vital_name
        )
        if not is_max_ok: # +1 CCN
            return False, max_msg

        return True, f"{formatted_value_unit} is OK."

    def check_vitals(self, **vitals_readings: float) -> bool:
        """
        Checks multiple vital signs and determines if all are OK.
        CCN = 3 (1 for loop, 1 for inner if, 1 for outer if)
        """
        critical_issues_found: list[str] = []

        for vital_name, value in vitals_readings.items(): # +1 CCN (for loop)
            is_ok, message = self._is_within_range(vital_name, value)
            _display_vital_status(vital_name, value, message)

            if not is_ok: # +1 CCN (inner if)
                critical_issues_found.append(f"{vital_name}: {message}")

        if critical_issues_found: # +1 CCN (outer if)
            _display_critical_summary(critical_issues_found)
            _perform_critical_alert_animation()
            return False

        print("\nAll vital signs are within normal limits.")
        return True


# --- Usage Example / Main Execution ---
if __name__ == "__main__":
    monitor = VitalSignMonitor(VITAL_THRESHOLDS)

    print("--- Scenario 1: All Vitals OK ---")
    monitor.check_vitals(temperature=98.6, pulseRate=75, spo2=97)
    print("-" * 30 + "\n")
    sleep(2)

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
    monitor.check_vitals(temperature=98.6, respirationRate=15.0, spo2=97)
    print("-" * 30 + "\n")
    sleep(2)

    print("--- Scenario 9: Changing SpO2 limit for a specific case ---")
    temporary_thresholds = VITAL_THRESHOLDS.copy()
    temporary_thresholds["spo2"] = {"min": 92, "max": 100, "unit": "%"}
    monitor_for_specific_patient = VitalSignMonitor(temporary_thresholds)
    monitor_for_specific_patient.check_vitals(temperature=98.0, pulseRate=75, spo2=91)
    print("-" * 30 + "\n")
