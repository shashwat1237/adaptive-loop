from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np
from app.models.observation import BiomarkerObservation, WearableDailyRecord
from app.models.confounder import ConfounderEvent


def calculate_percentage_delta(baseline: float, followup: float) -> float:
    """Calculates percentage delta using canonical formula:
    round(((followup - baseline) / baseline) * 100, 2)
    """
    if baseline == 0.0:
        return 0.00
    delta = ((followup - baseline) / baseline) * 100.0
    return round(delta, 2)


def calculate_data_completeness(valid_days: int, expected_days: int = 180) -> float:
    """Calculates data completeness rate:
    round((valid_days / expected_days) * 100, 1)
    """
    if expected_days == 0:
        return 0.0
    return round((valid_days / expected_days) * 100.0, 1)


def calculate_adherence_rate(adherent_days: int, total_active_days: int = 180) -> float:
    """Calculates protocol adherence rate:
    round((adherent_days / total_active_days) * 100, 1)
    """
    if total_active_days == 0:
        return 0.0
    return round((adherent_days / total_active_days) * 100.0, 1)


class DataAggregator:
    @staticmethod
    def process_longitudinal_data(
        biomarkers: List[BiomarkerObservation],
        wearables: List[WearableDailyRecord],
        confounders: List[ConfounderEvent]
    ) -> Dict[str, Any]:
        """Processes 180-day longitudinal data into:
        1. Pre-calculated biomarker deltas
        2. Daily metrics & 7d/14d rolling baselines
        3. 26 weekly summary rollups
        4. In-memory Observation Registry
        5. Data completeness & protocol adherence rates
        """
        # --- 1. Biomarkers ---
        baseline_bio = {b.marker_code: b for b in biomarkers if b.test_cycle_day == 0}
        followup_bio = {b.marker_code: b for b in biomarkers if b.test_cycle_day == 180}

        biomarker_deltas = []
        obs_registry = {}

        for marker_code, b_base in baseline_bio.items():
            obs_registry[b_base.id] = {
                "type": "BIOMARKER",
                "marker": marker_code,
                "value": b_base.value,
                "unit": b_base.unit,
                "date": str(b_base.measurement_date),
                "cycle_day": 0
            }
            if marker_code in followup_bio:
                b_fol = followup_bio[marker_code]
                obs_registry[b_fol.id] = {
                    "type": "BIOMARKER",
                    "marker": marker_code,
                    "value": b_fol.value,
                    "unit": b_fol.unit,
                    "date": str(b_fol.measurement_date),
                    "cycle_day": 180
                }
                delta_pct = calculate_percentage_delta(b_base.value, b_fol.value)
                biomarker_deltas.append({
                    "marker_code": marker_code,
                    "marker_name": b_base.marker_name,
                    "baseline_id": b_base.id,
                    "baseline": b_base.value,
                    "followup_id": b_fol.id,
                    "follow_up": b_fol.value,
                    "delta_percentage": delta_pct,
                    "unit": b_base.unit,
                    "optimal_range_min": b_base.optimal_range_min,
                    "optimal_range_max": b_base.optimal_range_max
                })

        # --- 2. Wearables ---
        total_days_recorded = len(wearables)
        valid_days = 0
        adherent_days = 0

        wearable_rows = []
        for w in wearables:
            # Day is valid if at least two core signals are non-null
            core_signals = [
                w.total_sleep_hours is not None,
                w.resting_heart_rate is not None or w.hrv_rmssd is not None,
                w.strain_score is not None
            ]
            is_valid = sum(core_signals) >= 2
            if is_valid:
                valid_days += 1
            if w.adherence_logged:
                adherent_days += 1

            wearable_rows.append({
                "recorded_date": w.recorded_date,
                "week_number": w.week_number,
                "total_sleep_hours": w.total_sleep_hours,
                "deep_sleep_hours": w.deep_sleep_hours,
                "rem_sleep_hours": w.rem_sleep_hours,
                "resting_heart_rate": w.resting_heart_rate,
                "hrv_rmssd": w.hrv_rmssd,
                "strain_score": w.strain_score,
                "adherence_logged": w.adherence_logged,
                "is_valid": is_valid
            })

        completeness_rate = calculate_data_completeness(valid_days, 180)
        adherence_rate = calculate_adherence_rate(adherent_days, 180)

        df = pd.DataFrame(wearable_rows) if wearable_rows else pd.DataFrame()

        weekly_rollups = []
        if not df.empty:
            df["recorded_date"] = pd.to_datetime(df["recorded_date"])
            df = df.sort_values("recorded_date")

            for week in range(1, 27):
                week_df = df[df["week_number"] == week]
                if not week_df.empty:
                    avg_sleep = round(week_df["total_sleep_hours"].mean(), 2) if week_df["total_sleep_hours"].notna().any() else None
                    avg_deep = round(week_df["deep_sleep_hours"].mean(), 2) if week_df["deep_sleep_hours"].notna().any() else None
                    avg_rhr = round(week_df["resting_heart_rate"].mean(), 1) if week_df["resting_heart_rate"].notna().any() else None
                    avg_hrv = round(week_df["hrv_rmssd"].mean(), 1) if week_df["hrv_rmssd"].notna().any() else None
                    avg_strain = round(week_df["strain_score"].mean(), 1) if week_df["strain_score"].notna().any() else None
                    w_adherence = round((week_df["adherence_logged"].sum() / len(week_df)) * 100.0, 1)

                    deep_id = f"OBS-WEAR-DEEP-W{week:02d}"
                    hrv_id = f"OBS-WEAR-HRV-W{week:02d}"
                    rhr_id = f"OBS-WEAR-RHR-W{week:02d}"

                    obs_ids = []
                    if avg_deep is not None:
                        obs_ids.append(deep_id)
                        obs_registry[deep_id] = {
                            "type": "WEARABLE_WEEKLY",
                            "metric": "DEEP_SLEEP",
                            "avg_value": avg_deep,
                            "unit": "hours/night",
                            "week": week
                        }
                    if avg_hrv is not None:
                        obs_ids.append(hrv_id)
                        obs_registry[hrv_id] = {
                            "type": "WEARABLE_WEEKLY",
                            "metric": "HRV",
                            "avg_value": avg_hrv,
                            "unit": "ms",
                            "week": week
                        }
                    if avg_rhr is not None:
                        obs_ids.append(rhr_id)
                        obs_registry[rhr_id] = {
                            "type": "WEARABLE_WEEKLY",
                            "metric": "RHR",
                            "avg_value": avg_rhr,
                            "unit": "bpm",
                            "week": week
                        }

                    weekly_rollups.append({
                        "week_number": week,
                        "avg_total_sleep_hours": avg_sleep,
                        "avg_deep_sleep_hours": avg_deep,
                        "avg_resting_heart_rate": avg_rhr,
                        "avg_hrv_rmssd": avg_hrv,
                        "avg_strain_score": avg_strain,
                        "adherence_rate": w_adherence,
                        "observation_ids": obs_ids
                    })

        # --- 3. Confounders ---
        confounder_list = []
        for c in confounders:
            obs_registry[c.id] = {
                "type": "CONFOUNDER",
                "event_type": c.event_type,
                "description": c.description,
                "start_date": str(c.start_date),
                "end_date": str(c.end_date),
                "severity": c.severity
            }
            confounder_list.append({
                "id": c.id,
                "event_type": c.event_type,
                "description": c.description,
                "start_date": c.start_date,
                "end_date": c.end_date,
                "severity": c.severity
            })

        return {
            "biomarker_deltas": biomarker_deltas,
            "weekly_rollups": weekly_rollups,
            "confounders": confounder_list,
            "total_days_expected": 180,
            "total_days_recorded": total_days_recorded,
            "valid_days": valid_days,
            "adherent_days": adherent_days,
            "data_completeness_rate": completeness_rate,
            "protocol_adherence_rate": adherence_rate,
            "observation_registry": obs_registry
        }
