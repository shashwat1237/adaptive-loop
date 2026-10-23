import pytest


def test_api_health(client):
    # TEST-API-01: Health check
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["version"] == "1.0.0"
    assert data["database"] == "CONNECTED"


def test_api_list_members(client):
    # TEST-API-02: List members
    response = client.get("/api/v1/members")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    ids = [m["id"] for m in data]
    assert "MEM-1001" in ids
    assert "MEM-1002" in ids
    assert "MEM-1003" in ids


def test_api_get_member_detail(client):
    # TEST-API-03: Member detail
    response = client.get("/api/v1/members/MEM-1001")
    assert response.status_code == 200
    data = response.json()
    assert data["member"]["id"] == "MEM-1001"
    assert len(data["protocols"]) == 2
    assert len(data["biomarkers"]) == 6


def test_api_get_member_timeline(client):
    # TEST-API-04: Member timeline
    response = client.get("/api/v1/members/MEM-1001/timeline")
    assert response.status_code == 200
    data = response.json()
    assert data["member_id"] == "MEM-1001"
    assert data["total_days_recorded"] == 180
    assert len(data["daily_records"]) == 180
    assert len(data["weekly_rollups"]) == 26


def test_api_trigger_analysis(client):
    # TEST-API-05: Trigger analysis
    response = client.post("/api/v1/analyses", json={"member_id": "MEM-1001", "force_recompute": True})
    assert response.status_code == 201
    data = response.json()
    assert data["member_id"] == "MEM-1001"
    assert data["status"] == "COMPLETED"
    assert data["final_action"] == "CONTINUE_PROTOCOL"


def test_api_not_found_error_envelope(client):
    # TEST-API-06: 404 error envelope
    response = client.get("/api/v1/analyses/ANL-NONEXISTENT")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "ANALYSIS_NOT_FOUND"
    assert "timestamp" in data["error"]
