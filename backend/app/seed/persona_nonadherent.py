import datetime
from typing import Dict, Any, List


def get_david_chen_data() -> Dict[str, Any]:
    member = {
        "id": "MEM-1003",
        "full_name": "David Chen",
        "age": 51,
        "biological_sex": "MALE",
        "cohort": "Metabolic Syndrome & Glycemic Control",
        "primary_goal": "Metabolic regulation & insulin sensitivity",
        "baseline_notes": "Frequent international business traveler with prediabetic baseline HbA1c."
    }

    protocols = [
        {
            "id": "PROT-SUPP-03",
            "name": "Berberine HCl",
            "category": "SUPPLEMENT",
            "dosage_or_frequency": "500 mg 2x/day before main meals",
            "start_date": datetime.date(2026, 4, 1),
            "review_date": datetime.date(2026, 9, 28),
            "target_adherence_rate": 80.0
        },
        {
            "id": "PROT-EXER-02",
            "name": "Post-Dinner 15-Minute Brisk Walk",
            "category": "EXERCISE",
            "dosage_or_frequency": "Daily following evening meal",
            "start_date": datetime.date(2026, 4, 1),
            "review_date": datetime.date(2026, 9, 28),
            "target_adherence_rate": 70.0
        }
    ]

    biomarkers = [
        {
            "id": "OBS-BIO-HBA1C-D0",
            "marker_code": "HBA1C",
            "marker_name": "Hemoglobin A1c",
            "value": 5.9,
            "unit": "%",
            "optimal_range_min": 4.5,
            "optimal_range_max": 5.4,
            "measurement_date": datetime.date(2026, 4, 1),
            "test_cycle_day": 0
        },
        {
            "id": "OBS-BIO-HBA1C-D180",
            "marker_code": "HBA1C",
            "marker_name": "Hemoglobin A1c",
            "value": 5.9,
            "unit": "%",
            "optimal_range_min": 4.5,
            "optimal_range_max": 5.4,
            "measurement_date": datetime.date(2026, 9, 28),
            "test_cycle_day": 180
        },
        {
            "id": "OBS-BIO-INS-D0",
            "marker_code": "INS",
            "marker_name": "Fasting Serum Insulin",
            "value": 14.2,
            "unit": "uIU/mL",
            "optimal_range_min": 2.0,
            "optimal_range_max": 6.0,
            "measurement_date": datetime.date(2026, 4, 1),
            "test_cycle_day": 0
        },
        {
            "id": "OBS-BIO-INS-D180",
            "marker_code": "INS",
            "marker_name": "Fasting Serum Insulin",
            "value": 13.9,
            "unit": "uIU/mL",
            "optimal_range_min": 2.0,
            "optimal_range_max": 6.0,
            "measurement_date": datetime.date(2026, 9, 28),
            "test_cycle_day": 180
        }
    ]

    confounders = [
        {
            "id": "CONF-TRAVEL-W11",
            "event_type": "TRAVEL",
            "description": "Transpacific cross-timezone business travel (Weeks 11–13). Significant circadian disruption.",
            "start_date": datetime.date(2026, 6, 17),
            "end_date": datetime.date(2026, 7, 5),
            "severity": "SEVERE"
        },
        {
            "id": "CONF-TRAVEL-W20",
            "event_type": "TRAVEL",
            "description": "Transatlantic cross-timezone business travel (Weeks 20–21).",
            "start_date": datetime.date(2026, 8, 19),
            "end_date": datetime.date(2026, 9, 2),
            "severity": "MODERATE"
        }
    ]

    # 180 daily records: 115 valid days (63.9%), 50 compliant days (27.8%)
    start_date = datetime.date(2026, 4, 1)
    wearables = []
    # 65 missing days
    missing_days = set(
        list(range(20, 35)) + list(range(70, 90)) + list(range(135, 165))
    )

    for day in range(180):
        current_date = start_date + datetime.timedelta(days=day)
        week_num = min(26, (day // 7) + 1)

        if day in missing_days or len(wearables) - len([w for w in wearables if w["total_sleep_hours"] is None]) >= 115:
            if len([w for w in wearables if w["total_sleep_hours"] is not None]) >= 115:
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

        sleep = 6.2 + ((day % 3) * 0.3)
        deep = 0.8
        rem = 1.1
        rhr = 68.0 + ((day % 4) * 1.5)
        hrv = 32.0 - ((day % 3) * 1.0)
        strain = 11.0

        wearables.append({
            "recorded_date": current_date,
            "week_number": week_num,
            "total_sleep_hours": round(sleep, 2),
            "deep_sleep_hours": round(deep, 2),
            "rem_sleep_hours": round(rem, 2),
            "resting_heart_rate": round(rhr, 1),
            "hrv_rmssd": round(hrv, 1),
            "strain_score": round(strain, 1),
            "adherence_logged": False
        })

    # Ensure exactly 115 valid days and 50 adherent days
    valid_count = 0
    adherent_count = 0
    for w in wearables:
        if w["total_sleep_hours"] is not None:
            if valid_count < 115:
                valid_count += 1
                if adherent_count < 50 and valid_count % 2 == 0:
                    w["adherence_logged"] = True
                    adherent_count += 1
            else:
                w["total_sleep_hours"] = None
                w["deep_sleep_hours"] = None
                w["rem_sleep_hours"] = None
                w["resting_heart_rate"] = None
                w["hrv_rmssd"] = None
                w["strain_score"] = None
                w["adherence_logged"] = False

    return {
        "member": member,
        "protocols": protocols,
        "biomarkers": biomarkers,
        "confounders": confounders,
        "wearables": wearables
    }
