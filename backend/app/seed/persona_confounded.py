import datetime
from typing import Dict, Any, List


def get_elena_rostova_data() -> Dict[str, Any]:
    member = {
        "id": "MEM-1002",
        "full_name": "Elena Rostova",
        "age": 36,
        "biological_sex": "FEMALE",
        "cohort": "Neuro-Endocrine & Sleep Architecture",
        "primary_goal": "Deep sleep restoration & chronic stress reduction",
        "baseline_notes": "Corporate executive experiencing chronic evening hyperarousal."
    }

    protocols = [
        {
            "id": "PROT-SUPP-02",
            "name": "Magnesium L-Threonate",
            "category": "SUPPLEMENT",
            "dosage_or_frequency": "400 mg 60 min before sleep",
            "start_date": datetime.date(2026, 4, 1),
            "review_date": datetime.date(2026, 9, 28),
            "target_adherence_rate": 80.0
        },
        {
            "id": "PROT-LIFE-01",
            "name": "Evening Digital Screen Shutdown",
            "category": "LIFESTYLE",
            "dosage_or_frequency": "10:00 PM cutoff",
            "start_date": datetime.date(2026, 4, 1),
            "review_date": datetime.date(2026, 9, 28),
            "target_adherence_rate": 75.0
        }
    ]

    biomarkers = [
        {
            "id": "OBS-BIO-CORT-D0",
            "marker_code": "CORT",
            "marker_name": "Morning Cortisol",
            "value": 22.0,
            "unit": "mcg/dL",
            "optimal_range_min": 6.0,
            "optimal_range_max": 14.0,
            "measurement_date": datetime.date(2026, 4, 1),
            "test_cycle_day": 0
        },
        {
            "id": "OBS-BIO-CORT-D180",
            "marker_code": "CORT",
            "marker_name": "Morning Cortisol",
            "value": 13.8,
            "unit": "mcg/dL",
            "optimal_range_min": 6.0,
            "optimal_range_max": 14.0,
            "measurement_date": datetime.date(2026, 9, 28),
            "test_cycle_day": 180
        },
        {
            "id": "OBS-BIO-GLUC-D0",
            "marker_code": "GLUC",
            "marker_name": "Fasting Blood Glucose",
            "value": 98.0,
            "unit": "mg/dL",
            "optimal_range_min": 70.0,
            "optimal_range_max": 89.0,
            "measurement_date": datetime.date(2026, 4, 1),
            "test_cycle_day": 0
        },
        {
            "id": "OBS-BIO-GLUC-D180",
            "marker_code": "GLUC",
            "marker_name": "Fasting Blood Glucose",
            "value": 91.0,
            "unit": "mg/dL",
            "optimal_range_min": 70.0,
            "optimal_range_max": 89.0,
            "measurement_date": datetime.date(2026, 9, 28),
            "test_cycle_day": 180
        }
    ]

    confounders = [
        {
            "id": "CONF-CAREER-W08",
            "event_type": "LIFE_STRESS",
            "description": "Career transition / resigned high-stress role. Physical training load dropped 70%; sleep opportunity increased.",
            "start_date": datetime.date(2026, 5, 20),
            "end_date": datetime.date(2026, 6, 10),
            "severity": "SEVERE"
        },
        {
            "id": "CONF-ILLNESS-W14",
            "event_type": "ILLNESS",
            "description": "Acute viral upper respiratory infection. HRV crashed, RHR elevated for 6 days.",
            "start_date": datetime.date(2026, 7, 7),
            "end_date": datetime.date(2026, 7, 13),
            "severity": "MODERATE"
        }
    ]

    # 180 daily records: 168 valid days (93.3%), 112 compliant days (62.2%)
    start_date = datetime.date(2026, 4, 1)
    wearables = []
    for day in range(180):
        current_date = start_date + datetime.timedelta(days=day)
        week_num = min(26, (day // 7) + 1)

        # 12 missing days
        if day in [15, 30, 48, 72, 85, 99, 114, 128, 140, 155, 169, 178]:
            wearables.append({
                "recorded_date": current_date,
                "week_number": week_num,
                "total_sleep_hours": None,
                "deep_sleep_hours": None,
                "rem_sleep_hours": None,
                "resting_heart_rate": None,
                "hrv_rmssd": None,
                "strain_score": None,
                "adherence_logged": False
            })
            continue

        # In Week 14 (illness, days 98-104)
        if 98 <= day <= 104:
            hrv = 18.0
            rhr = 74.0
            deep = 0.4
            sleep = 5.8
            rem = 1.0
            strain = 18.0
            is_adherent = False
        # After Week 8 career change (day 56+): deep sleep rises from 0.72 to 1.13h
        elif day >= 56:
            deep = 1.13 + ((day % 3) * 0.05)
            sleep = 7.6 + ((day % 4) * 0.1)
            hrv = 44.0 + ((day % 3) * 1.5)
            rhr = 58.0 - ((day % 2) * 1.0)
            rem = 1.6
            strain = 9.5  # lower strain
            is_adherent = (day % 3 != 0)  # ~66% adherence
        else:
            # Baseline weeks 1-7
            deep = 0.72 + ((day % 3) * 0.04)
            sleep = 6.4 + ((day % 2) * 0.2)
            hrv = 36.0 + ((day % 4) * 1.0)
            rhr = 64.0
            rem = 1.2
            strain = 15.2
            is_adherent = (day % 2 == 0)

        wearables.append({
            "recorded_date": current_date,
            "week_number": week_num,
            "total_sleep_hours": round(sleep, 2),
            "deep_sleep_hours": round(deep, 2),
            "rem_sleep_hours": round(rem, 2),
            "resting_heart_rate": round(rhr, 1),
            "hrv_rmssd": round(hrv, 1),
            "strain_score": round(strain, 1),
            "adherence_logged": is_adherent
        })

    # Adjust adherence to exactly 112 days
    actual_adherent = sum(1 for w in wearables if w["adherence_logged"])
    if actual_adherent != 112:
        diff = 112 - actual_adherent
        for w in wearables:
            if diff > 0 and not w["adherence_logged"] and w["total_sleep_hours"] is not None:
                w["adherence_logged"] = True
                diff -= 1
            elif diff < 0 and w["adherence_logged"]:
                w["adherence_logged"] = False
                diff += 1
            if diff == 0:
                break

    return {
        "member": member,
        "protocols": protocols,
        "biomarkers": biomarkers,
        "confounders": confounders,
        "wearables": wearables
    }
