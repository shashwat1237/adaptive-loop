import datetime
from typing import Dict, Any, List


def get_marcus_vance_data() -> Dict[str, Any]:
    member = {
        "id": "MEM-1001",
        "full_name": "Marcus Vance",
        "age": 42,
        "biological_sex": "MALE",
        "cohort": "Cardiometabolic & Longevity",
        "primary_goal": "Cardiovascular risk mitigation & recovery optimization",
        "baseline_notes": "Active athlete, mild family history of early CVD."
    }

    protocols = [
        {
            "id": "PROT-CARDIO-01",
            "name": "Zone 2 Aerobic Base Training",
            "category": "EXERCISE",
            "dosage_or_frequency": "45 min, 3x/week, HR 125-138 bpm",
            "start_date": datetime.date(2026, 4, 1),
            "review_date": datetime.date(2026, 9, 28),
            "target_adherence_rate": 80.0
        },
        {
            "id": "PROT-SUPP-01",
            "name": "Citrus Bergamot",
            "category": "SUPPLEMENT",
            "dosage_or_frequency": "500 mg daily with evening meal",
            "start_date": datetime.date(2026, 4, 1),
            "review_date": datetime.date(2026, 9, 28),
            "target_adherence_rate": 85.0
        }
    ]

    biomarkers = [
        {
            "id": "OBS-BIO-APOB-D0",
            "marker_code": "APOB",
            "marker_name": "Apolipoprotein B",
            "value": 118.0,
            "unit": "mg/dL",
            "optimal_range_min": 40.0,
            "optimal_range_max": 80.0,
            "measurement_date": datetime.date(2026, 4, 1),
            "test_cycle_day": 0
        },
        {
            "id": "OBS-BIO-APOB-D180",
            "marker_code": "APOB",
            "marker_name": "Apolipoprotein B",
            "value": 94.0,
            "unit": "mg/dL",
            "optimal_range_min": 40.0,
            "optimal_range_max": 80.0,
            "measurement_date": datetime.date(2026, 9, 28),
            "test_cycle_day": 180
        },
        {
            "id": "OBS-BIO-CRP-D0",
            "marker_code": "CRP",
            "marker_name": "High-Sensitivity C-Reactive Protein",
            "value": 2.4,
            "unit": "mg/L",
            "optimal_range_min": 0.0,
            "optimal_range_max": 1.0,
            "measurement_date": datetime.date(2026, 4, 1),
            "test_cycle_day": 0
        },
        {
            "id": "OBS-BIO-CRP-D180",
            "marker_code": "CRP",
            "marker_name": "High-Sensitivity C-Reactive Protein",
            "value": 1.1,
            "unit": "mg/L",
            "optimal_range_min": 0.0,
            "optimal_range_max": 1.0,
            "measurement_date": datetime.date(2026, 9, 28),
            "test_cycle_day": 180
        },
        {
            "id": "OBS-BIO-LDL-D0",
            "marker_code": "LDL",
            "marker_name": "LDL Cholesterol",
            "value": 142.0,
            "unit": "mg/dL",
            "optimal_range_min": 50.0,
            "optimal_range_max": 100.0,
            "measurement_date": datetime.date(2026, 4, 1),
            "test_cycle_day": 0
        },
        {
            "id": "OBS-BIO-LDL-D180",
            "marker_code": "LDL",
            "marker_name": "LDL Cholesterol",
            "value": 116.0,
            "unit": "mg/dL",
            "optimal_range_min": 50.0,
            "optimal_range_max": 100.0,
            "measurement_date": datetime.date(2026, 9, 28),
            "test_cycle_day": 180
        }
    ]

    confounders = []

    # 180 daily wearable records: 172 valid days, 159 adherent days (88.3%)
    start_date = datetime.date(2026, 4, 1)
    wearables = []
    for day in range(180):
        current_date = start_date + datetime.timedelta(days=day)
        week_num = min(26, (day // 7) + 1)

        # 8 missing days distributed across window
        if day in [25, 54, 88, 102, 120, 145, 160, 175]:
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

        progress = day / 180.0
        # HRV trends up from 38 to 49
        hrv = round(38.0 + (11.0 * progress) + ((day % 5) - 2.5), 1)
        # RHR trends down from 62 to 56
        rhr = round(62.0 - (6.0 * progress) + ((day % 4) - 2.0), 1)
        sleep = round(7.2 + ((day % 3) * 0.2), 2)
        deep = round(1.1 + (0.2 * progress), 2)
        rem = round(1.5 + ((day % 4) * 0.1), 2)
        strain = round(13.5 + ((day % 5) * 0.5), 1)

        # 159 adherent days (non-adherent on specific days)
        is_adherent = day not in [10, 22, 33, 47, 65, 78, 92, 115, 130, 142, 155, 168, 172]

        wearables.append({
            "recorded_date": current_date,
            "week_number": week_num,
            "total_sleep_hours": sleep,
            "deep_sleep_hours": deep,
            "rem_sleep_hours": rem,
            "resting_heart_rate": rhr,
            "hrv_rmssd": hrv,
            "strain_score": strain,
            "adherence_logged": is_adherent
        })

    return {
        "member": member,
        "protocols": protocols,
        "biomarkers": biomarkers,
        "confounders": confounders,
        "wearables": wearables
    }
