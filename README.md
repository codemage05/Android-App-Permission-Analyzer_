# Android App Permission Analyzer — quick start

This small Flask app analyzes an uploaded Android APK and reports requested permissions grouped by risk.

Quick steps to run locally (recommended: inside a virtualenv):

1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies

```bash
python3 -m pip install -r requirements.txt
```

3. (Optional) Configure Gemini AI API key for contextual AI analysis

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

If you don't set this, the AI section will show a message saying AI analysis is not configured.

4. Start the Flask app

```bash
python3 app.py
```

The app listens on http://127.0.0.1:5000 by default.

Example curl command to POST an APK to the `/upload` endpoint (saves the rendered HTML):

```bash
curl -s -S -F "file=@/path/to/your/app.apk" http://127.0.0.1:5000/upload -o report.html

# then open report.html in a browser or inspect it
```

Notes and troubleshooting

- If `androguard` install fails, it may need additional system packages (libxml2, libxslt, build-essential, etc.). Share the pip install error and I can suggest exact commands for your distro.
- This uses the Flask development server; for production deploy behind a WSGI server (gunicorn, uWSGI).

Files of interest

- `app.py` — Flask app and upload handling
- `core_analyzer.py` — APK parsing and permission analysis logic
- `analyzer.py` — small adapter so `app.py` can import the analyzer functions
- `templates/` — Jinja2 templates used for upload and report pages

# Android-App-Permission-Analyzer\_

Hackathon Project
