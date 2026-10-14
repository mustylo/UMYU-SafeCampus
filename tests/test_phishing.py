import pytest
from app.services.phishing import analyze


def test_obvious_phishing_is_high_risk():
    result = analyze("URGENT: your account will be suspended. Click here and send your password and OTP", "http://192.168.1.1/login")
    assert result["risk"] in {"High", "Critical"}
    assert result["indicators"]


def test_benign_message_is_low_risk():
    assert analyze("The library closes at 6pm.")["risk"] == "Low"


def test_empty_analysis_is_rejected():
    with pytest.raises(ValueError): analyze()


def test_large_submission_is_rejected():
    with pytest.raises(ValueError): analyze("x" * 10001)
