import pytest
from app.engine.aggregator import (
    calculate_percentage_delta,
    calculate_data_completeness,
    calculate_adherence_rate,
    DataAggregator
)


def test_calculate_percentage_delta_standard():
    # TEST-MATH-01: Baseline: 118.0, Follow-up: 94.0 -> Delta: -20.34%
    delta = calculate_percentage_delta(118.0, 94.0)
    assert delta == -20.34


def test_calculate_percentage_delta_zero_baseline():
    # TEST-MATH-02: Zero baseline handling
    delta = calculate_percentage_delta(0.0, 10.0)
    assert delta == 0.00


def test_calculate_data_completeness():
    # TEST-MATH-03: 168 valid days out of 180 expected -> 93.3%
    completeness = calculate_data_completeness(168, 180)
    assert completeness == 93.3


def test_calculate_adherence_rate():
    # TEST-MATH-04: 112 compliant days out of 180 active -> 62.2%
    adherence = calculate_adherence_rate(112, 180)
    assert adherence == 62.2


def test_process_longitudinal_data_empty():
    res = DataAggregator.process_longitudinal_data([], [], [])
    assert res["total_days_expected"] == 180
    assert res["total_days_recorded"] == 0
    assert res["data_completeness_rate"] == 0.0
    assert res["protocol_adherence_rate"] == 0.0
    assert res["biomarker_deltas"] == []
    assert res["observation_registry"] == {}
