import os
import pytest
from unittest.mock import MagicMock, patch

try:
    from code.core_analyzer import analyze_permissions, get_ai_context_analysis, get_app_details
except ImportError:
    from core_analyzer import analyze_permissions, get_ai_context_analysis, get_app_details


def test_analyze_permissions_high_risk():
    """Verify that known high risk permissions are correctly categorized."""
    perms = ["android.permission.CAMERA", "android.permission.READ_CONTACTS"]
    report, risky_perms = analyze_permissions(perms)

    assert len(report["high_risk"]) == 2
    assert report["high_risk"][0]["name"] == "android.permission.CAMERA"
    assert report["high_risk"][1]["name"] == "android.permission.READ_CONTACTS"
    assert len(report["medium_risk"]) == 0
    assert len(report["low_risk"]) == 0
    assert len(report["unknown"]) == 0
    assert set(risky_perms) == {"android.permission.CAMERA", "android.permission.READ_CONTACTS"}


def test_analyze_permissions_medium_and_low_risk():
    """Verify medium and low risk permission categorization."""
    perms = ["android.permission.READ_EXTERNAL_STORAGE", "android.permission.INTERNET"]
    report, risky_perms = analyze_permissions(perms)

    assert len(report["medium_risk"]) == 1
    assert report["medium_risk"][0]["name"] == "android.permission.READ_EXTERNAL_STORAGE"

    assert len(report["low_risk"]) == 1
    assert report["low_risk"][0]["name"] == "android.permission.INTERNET"

    # Medium risk permissions should be included in risky_perms for AI analysis, but Low risk should not
    assert risky_perms == ["android.permission.READ_EXTERNAL_STORAGE"]


def test_analyze_permissions_unknown():
    """Verify handling of uncommon or custom permissions not in permissions_db.json."""
    perms = ["custom.permission.SUPER_SECRET"]
    report, risky_perms = analyze_permissions(perms)

    assert len(report["unknown"]) == 1
    assert report["unknown"][0]["name"] == "custom.permission.SUPER_SECRET"
    assert "uncommon or custom permission" in report["unknown"][0]["description"]
    assert len(risky_perms) == 0


def test_analyze_permissions_empty():
    """Verify analyzing an empty permission list."""
    report, risky_perms = analyze_permissions([])

    assert report["high_risk"] == []
    assert report["medium_risk"] == []
    assert report["low_risk"] == []
    assert report["unknown"] == []
    assert risky_perms == []


def test_get_ai_context_analysis_empty_risky_perms():
    """Verify AI analysis skips API calls when there are no risky permissions."""
    result = get_ai_context_analysis("Safe App", [])
    assert "This app requests no significant permissions. It appears to be safe." in result


def test_get_ai_context_analysis_missing_api_key(monkeypatch):
    """Verify fallback message when GEMINI_API_KEY environment variable is not configured."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    result = get_ai_context_analysis("Test App", ["android.permission.CAMERA"])
    assert "AI analysis is not configured" in result


@patch("google.generativeai.GenerativeModel")
@patch("google.generativeai.configure")
def test_get_ai_context_analysis_with_mocked_gemini(mock_configure, mock_generative_model, monkeypatch):
    """Verify AI context analysis sends expected prompt and returns model output when API key is set."""
    monkeypatch.setenv("GEMINI_API_KEY", "test_mock_api_key_12345")

    mock_model_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Verdict: [Suspicious]\nA flashlight app should not require camera access."
    mock_model_instance.generate_content.return_value = mock_response
    mock_generative_model.return_value = mock_model_instance

    result = get_ai_context_analysis("Flashlight", ["android.permission.CAMERA"])

    mock_configure.assert_called_once_with(api_key="test_mock_api_key_12345")
    mock_model_instance.generate_content.assert_called_once()
    assert "Verdict: [Suspicious]" in result


def test_get_app_details_invalid_apk():
    """Verify get_app_details handles non-existent or invalid APK files gracefully."""
    app_name, package_name, permissions = get_app_details("/invalid/path/to/nonexistent.apk")

    assert app_name == "Unknown App"
    assert package_name == "unknown.package"
    assert permissions == []
