import pandas as pd
import pytest

from sensor_report.analysis import (
    load_readings,
    summary_by_sensor,
    find_anomalies,
    daily_mean,
)


def test_load_readings():
    df = load_readings("data/sample_readings.csv")
    assert not df.empty
    assert "temperature" in df.columns
    assert "humidity" in df.columns


def test_summary_by_sensor():
    df = load_readings("data/sample_readings.csv")
    summary = summary_by_sensor(df)
    assert "cuisine" in summary.index
    assert "garage" in summary.index
    assert "salon" in summary.index


def test_find_anomalies():
    df = load_readings("data/sample_readings.csv")
    anomalies = find_anomalies(df, "temperature")
    assert not anomalies.empty
    assert 45.0 in anomalies["temperature"].values


def test_daily_mean():
    df = load_readings("data/sample_readings.csv")
    result = daily_mean(df)
    assert not result.empty
    assert "cuisine" in result.columns


def test_invalid_column():
    df = load_readings("data/sample_readings.csv")
    with pytest.raises(ValueError):
        find_anomalies(df, "invalid_column")
