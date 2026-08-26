import io
import os
import pytest
from unittest.mock import patch

from code.app import app
import code.app as app_module


@pytest.fixture
def client():
    """Flask test client fixture."""
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = '/tmp/test_uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """Verify index route (GET /) returns status 200 and renders HTML."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Android App Permission Analyzer" in response.data or b"html" in response.data.lower()


def test_upload_no_file(client):
    """Verify POST /upload without file redirects back."""
    response = client.post('/upload', data={}, follow_redirects=False)
    assert response.status_code == 302


def test_upload_empty_filename(client):
    """Verify POST /upload with empty file selection redirects back."""
    data = {
        'file': (io.BytesIO(b""), '')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=False)
    assert response.status_code == 302


def test_upload_non_apk_file(client):
    """Verify POST /upload with non-apk extension returns 400 Bad Request."""
    data = {
        'file': (io.BytesIO(b"dummy text content"), 'malicious.exe')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b"Invalid file type. Please upload an .apk file." in response.data


@patch.object(app_module, "get_app_details")
@patch.object(app_module, "analyze_permissions")
@patch.object(app_module, "get_ai_context_analysis")
def test_upload_valid_apk_success(mock_get_ai, mock_analyze, mock_get_details, client):
    """Verify POST /upload with valid .apk extension parses APK and renders report HTML."""
    mock_get_details.return_value = ("Test Flashlight", "com.example.flashlight", ["android.permission.CAMERA"])
    mock_analyze.return_value = (
        {
            "high_risk": [{"name": "android.permission.CAMERA", "description": "Allows camera access."}],
            "medium_risk": [],
            "low_risk": [],
            "unknown": []
        },
        ["android.permission.CAMERA"]
    )
    mock_get_ai.return_value = "Verdict: [Suspicious] Camera permission is not required for a flashlight app."

    data = {
        'file': (io.BytesIO(b"fake apk binary header content"), 'flashlight.apk')
    }

    response = client.post('/upload', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert b"Test Flashlight" in response.data
    assert b"com.example.flashlight" in response.data
    assert b"android.permission.CAMERA" in response.data
    assert b"Verdict: [Suspicious]" in response.data
