import pytest


def test_create_test_member_with_cohort(client):
    """Test creating a custom test case member with a designated cohort, protocol, biomarkers, and wearables."""
    payload = {
        "id": "MEM-2099",
        "full_name": "Dr. Sarah Connor",
        "age": 44,
        "biological_sex": "FEMALE",
        "cohort": "Longevity & Mitochondrial Health",
        "primary_goal": "Optimize NAD+ metabolism and autonomic HRV recovery",
        "baseline_notes": "Test case user for mitochondrial protocol verification",
        "telemetry_profile": "clean_responder",
        "baseline_resting_hr": 66.0,
        "baseline_hrv_rmssd": 40.0,
        "baseline_deep_sleep_hours": 1.2,
        "baseline_total_sleep_hours": 7.0,
        "followup_resting_hr": 60.0,
        "followup_hrv_rmssd": 52.0,
        "followup_deep_sleep_hours": 1.7,
        "followup_total_sleep_hours": 7.5,
        "protocols": [
            {
                "name": "NMN + Resveratrol Formulation",
                "category": "SUPPLEMENT",
                "dosage_or_frequency": "1000mg sublingual every morning",
                "target_adherence_rate": 85.0
            }
        ],
        "biomarkers": [
            {
                "marker_code": "APOB",
                "marker_name": "Apolipoprotein B",
                "baseline_value": 110.0,
                "followup_value": 85.0,
                "unit": "mg/dL",
                "optimal_range_min": 40.0,
                "optimal_range_max": 80.0
            }
        ]
    }

    # 1. Create member
    response = client.post("/api/v1/members", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["member"]["id"] == "MEM-2099"
    assert data["member"]["full_name"] == "Dr. Sarah Connor"
    assert data["member"]["cohort"] == "Longevity & Mitochondrial Health"
    assert len(data["protocols"]) == 1
    assert len(data["biomarkers"]) == 2  # D0 and D180

    # 2. Verify in list with cohort filter
    list_res = client.get("/api/v1/members", params={"cohort": "Longevity & Mitochondrial Health"})
    assert list_res.status_code == 200
    cohort_members = list_res.json()
    assert any(m["id"] == "MEM-2099" for m in cohort_members)

    # 3. Verify timeline generation (180 days)
    timeline_res = client.get("/api/v1/members/MEM-2099/timeline")
    assert timeline_res.status_code == 200
    timeline = timeline_res.json()
    assert timeline["total_days_recorded"] == 180
    assert len(timeline["daily_records"]) == 180
    assert len(timeline["weekly_rollups"]) == 26
    assert timeline["data_completeness_rate"] >= 90.0

    # 4. Verify benchmark persona protection
    del_protected = client.delete("/api/v1/members/MEM-1001")
    assert del_protected.status_code == 403

    # 5. Delete custom test member
    del_res = client.delete("/api/v1/members/MEM-2099")
    assert del_res.status_code == 200
    get_del = client.get("/api/v1/members/MEM-2099")
    assert get_del.status_code == 404
