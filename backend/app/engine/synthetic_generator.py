import datetime
import random
from typing import List, Tuple
from app.models.observation import WearableDailyRecord, BiomarkerObservation
from app.models.protocol import Protocol
from app.models.confounder import ConfounderEvent
from app.schemas.member_create import MemberCreateRequest


def generate_member_synthetic_data(
    req: MemberCreateRequest,
    member_id: str
) -> Tuple[List[Protocol], List[BiomarkerObservation], List[WearableDailyRecord], List[ConfounderEvent]]:
    """
    Generates realistic, mathematically grounded protocols, biomarkers, daily wearable records,
    and confounder events for a custom test case member.
    """
    rng = random.Random(sum(ord(c) for c in member_id) + 42)

    # 180-day window ending today
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=179)

    # --- 1. Protocols ---
    protocols_list: List[Protocol] = []
    input_protocols = req.protocols or [
        {
            "name": "Targeted Longevity Protocol",
            "category": "SUPPLEMENT",
            "dosage_or_frequency": "Standard clinical dose 1x daily",
            "target_adherence_rate": 80.0
        }
    ]

    for idx, p in enumerate(input_protocols):
        prot_data = p if isinstance(p, dict) else p.model_dump()
        prot_id = f"PROT-{member_id[-4:]}-{idx+1:02d}"
        protocols_list.append(Protocol(
            id=prot_id,
            member_id=member_id,
            name=prot_data["name"],
            category=prot_data["category"],
            dosage_or_frequency=prot_data["dosage_or_frequency"],
            start_date=start_date + datetime.timedelta(days=28),  # Protocol starts after baseline
            review_date=end_date,
            target_adherence_rate=prot_data.get("target_adherence_rate", 80.0)
        ))

    # --- 2. Biomarkers ---
    biomarkers_list: List[BiomarkerObservation] = []
    input_biomarkers = req.biomarkers or [
        {
            "marker_code": "APOB",
            "marker_name": "Apolipoprotein B",
            "baseline_value": 125.0,
            "followup_value": 98.0,
            "unit": "mg/dL",
            "optimal_range_min": 40.0,
            "optimal_range_max": 80.0
        },
        {
            "marker_code": "CRP",
            "marker_name": "High-Sensitivity CRP",
            "baseline_value": 2.4,
            "followup_value": 1.1,
            "unit": "mg/L",
            "optimal_range_min": 0.0,
            "optimal_range_max": 1.0
        }
    ]

    for b in input_biomarkers:
        b_data = b if isinstance(b, dict) else b.model_dump()
        code = b_data["marker_code"].upper()
        # Day 0 baseline
        biomarkers_list.append(BiomarkerObservation(
            id=f"OBS-BIO-{member_id[-4:]}-{code}-D0",
            member_id=member_id,
            marker_code=code,
            marker_name=b_data["marker_name"],
            value=float(b_data["baseline_value"]),
            unit=b_data["unit"],
            optimal_range_min=float(b_data["optimal_range_min"]),
            optimal_range_max=float(b_data["optimal_range_max"]),
            measurement_date=start_date,
            test_cycle_day=0
        ))
        # Day 180 follow-up
        biomarkers_list.append(BiomarkerObservation(
            id=f"OBS-BIO-{member_id[-4:]}-{code}-D180",
            member_id=member_id,
            marker_code=code,
            marker_name=b_data["marker_name"],
            value=float(b_data["followup_value"]),
            unit=b_data["unit"],
            optimal_range_min=float(b_data["optimal_range_min"]),
            optimal_range_max=float(b_data["optimal_range_max"]),
            measurement_date=end_date,
            test_cycle_day=180
        ))

    # --- 3. Confounders ---
    confounders_list: List[ConfounderEvent] = []
    confounder_ranges = []
    if req.confounders:
        for idx, c in enumerate(req.confounders):
            c_data = c if isinstance(c, dict) else c.model_dump()
            c_type = c_data["event_type"].upper()
            w = c_data.get("start_week", 8)
            dur = c_data.get("duration_days", 14)
            c_start = start_date + datetime.timedelta(days=(w - 1) * 7)
            c_end = c_start + datetime.timedelta(days=dur)
            conf_id = f"CONF-{member_id[-4:]}-{c_type}-W{w:02d}"

            confounders_list.append(ConfounderEvent(
                id=conf_id,
                member_id=member_id,
                event_type=c_type,
                description=c_data["description"],
                start_date=c_start,
                end_date=c_end,
                severity=c_data.get("severity", "MODERATE")
            ))
            confounder_ranges.append((c_start, c_end, c_data.get("severity", "MODERATE")))

    # --- 4. Wearable Daily Telemetry (180 Days) ---
    wearables_list: List[WearableDailyRecord] = []
    is_non_adherent = req.telemetry_profile == "non_adherent"

    base_rhr = req.baseline_resting_hr
    targ_rhr = req.followup_resting_hr or base_rhr - 5.0
    base_hrv = req.baseline_hrv_rmssd
    targ_hrv = req.followup_hrv_rmssd or base_hrv + 10.0
    base_deep = req.baseline_deep_sleep_hours
    targ_deep = req.followup_deep_sleep_hours or base_deep + 0.4
    base_total = req.baseline_total_sleep_hours
    targ_total = req.followup_total_sleep_hours or base_total + 0.5

    for day_idx in range(180):
        current_date = start_date + datetime.timedelta(days=day_idx)
        week_num = min(26, (day_idx // 7) + 1)

        # Non-adherent case: randomly omit 65% of days
        if is_non_adherent and rng.random() > 0.35:
            wearables_list.append(WearableDailyRecord(
                member_id=member_id,
                recorded_date=current_date,
                week_number=week_num,
                total_sleep_hours=None,
                deep_sleep_hours=None,
                rem_sleep_hours=None,
                resting_heart_rate=None,
                hrv_rmssd=None,
                strain_score=None,
                adherence_logged=False
            ))
            continue

        # Progression fraction from baseline (weeks 1-4) to intervention (weeks 5-26)
        if week_num <= 4:
            progression = 0.0
        else:
            progression = min(1.0, (day_idx - 28) / 152.0)

        rhr_mean = base_rhr + (targ_rhr - base_rhr) * progression
        hrv_mean = base_hrv + (targ_hrv - base_hrv) * progression
        deep_mean = base_deep + (targ_deep - base_deep) * progression
        total_mean = base_total + (targ_total - base_total) * progression

        # Check confounder perturbation
        in_confounder = False
        for c_start, c_end, severity in confounder_ranges:
            if c_start <= current_date <= c_end:
                in_confounder = True
                factor = 1.5 if severity == "SEVERE" else 1.0
                rhr_mean += 8.0 * factor
                hrv_mean -= 14.0 * factor
                deep_mean = max(0.4, deep_mean - 0.4 * factor)
                total_mean = max(4.5, total_mean - 0.8 * factor)
                break

        # Generate realistic daily variance
        cur_rhr = round(rng.gauss(rhr_mean, 1.8), 1)
        cur_hrv = round(max(12.0, rng.gauss(hrv_mean, 3.5)), 1)
        cur_deep = round(max(0.3, rng.gauss(deep_mean, 0.15)), 2)
        cur_total = round(max(4.0, rng.gauss(total_mean, 0.4)), 2)
        cur_rem = round(max(0.5, cur_total * 0.22 + rng.gauss(0, 0.1)), 2)
        cur_strain = round(max(4.0, min(20.0, rng.gauss(11.5, 2.2))), 1)

        # Adherence probability
        if is_non_adherent:
            adherent = rng.random() < 0.28
        elif in_confounder:
            adherent = rng.random() < 0.50
        else:
            adherent = rng.random() < 0.88

        wearables_list.append(WearableDailyRecord(
            member_id=member_id,
            recorded_date=current_date,
            week_number=week_num,
            total_sleep_hours=cur_total,
            deep_sleep_hours=cur_deep,
            rem_sleep_hours=cur_rem,
            resting_heart_rate=cur_rhr,
            hrv_rmssd=cur_hrv,
            strain_score=cur_strain,
            adherence_logged=adherent
        ))

    return protocols_list, biomarkers_list, wearables_list, confounders_list
