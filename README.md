# Android App Permission Analyzer

> **Analyze Android APK files and identify risky permission requests with AI-powered contextual insights.**

A Flask-based web application that helps developers and security auditors understand what permissions Android apps are requesting. The app categorizes permissions by risk level and provides AI-driven security analysis powered by Google's Gemini API.

---

## ✨ Features

- **📱 APK Analysis**: Extract and parse Android APK files to identify requested permissions
- **⚠️ Risk Categorization**: Automatically classify permissions into High, Medium, Low, and Unknown risk levels
- **🤖 AI-Powered Insights**: Leverage Google Gemini API to provide contextual security analysis based on app names and permission requests
- **🎨 Interactive Web UI**: User-friendly interface with drag-and-drop file upload and color-coded permission reports
- **🔍 Comprehensive Database**: Built-in permission database with risk assessments and descriptions
- **📊 Detailed Reports**: HTML reports with organized permission breakdowns and security verdicts

---

## 📋 System Requirements

- **Python**: 3.8+ (tested with Python 3.10)
- **OS**: Linux, macOS, or Windows with WSL
- **Storage**: ~200 MB (for dependencies)
- **Optional**: Google Gemini API key for AI analysis features

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/codemage05/Android-App-Permission-Analyzer_.git
cd Android-App-Permission-Analyzer_
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r code/requirements.txt
```

**Note on `androguard` Installation**

If installation fails due to missing build tools, install system dependencies first:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y build-essential python3-dev libxml2-dev libxslt1-dev
pip install -r code/requirements.txt
```

**macOS:**
```bash
brew install libxml2 libxslt
LDFLAGS="-L$(brew --prefix libxml2)/lib -L$(brew --prefix libxslt)/lib" \
CPPFLAGS="-I$(brew --prefix libxml2)/include -I$(brew --prefix libxslt)/include" \
pip install -r code/requirements.txt
```

**Fedora/RHEL:**
```bash
sudo dnf install -y gcc python3-devel libxml2-devel libxslt-devel
pip install -r code/requirements.txt
```

### 4. (Optional) Configure AI Analysis

To enable Google Gemini API for contextual AI analysis:

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

If you skip this step, the app still works—AI analysis will show a message that it's not configured.

### 5. Start the Application

```bash
python3 code/app.py
```

The app will be available at **http://127.0.0.1:5000**

---

## 📖 Usage

### Web Interface

1. Open http://127.0.0.1:5000 in your browser
2. Drag and drop an `.apk` file or click to select one
3. Click "Analyze Now"
4. View the security report with categorized permissions and AI analysis

### Command-Line / API

Upload an APK using curl and save the HTML report:

```bash
curl -s -F "file=@/path/to/app.apk" http://127.0.0.1:5000/upload -o report.html
```

Then open `report.html` in your browser.

### Example with Sample APKs

```bash
# Analyze Calculator
curl -s -F "file=@uploads/Calculator_9.0_.apk" http://127.0.0.1:5000/upload -o calculator_report.html

# Analyze FlashLight
curl -s -F "file=@uploads/FlashLight_.apk" http://127.0.0.1:5000/upload -o flashlight_report.html
```

---

## 🏗️ Project Structure

```
Android-App-Permission-Analyzer_/
├── code/
│   ├── app.py                    # Flask app and route handlers
│   ├── core_analyzer.py          # APK parsing and permission analysis
│   ├── analyzer.py               # Module adapter for imports
│   ├── permissions_db.json       # Permission risk database
│   └── requirements.txt           # Python dependencies
├── templates/
│   ├── index.html                # Upload page
│   └── report.html               # Analysis report page (Jinja2)
├── uploads/                      # Temporary storage for uploaded APKs
├── README.md                     # This file
└── .git/                         # Git repository
```

### Key Files Explained

| File | Purpose |
|------|---------|
| **code/app.py** | Flask application with route handlers (`/` for upload, `/upload` for analysis) |
| **code/core_analyzer.py** | Core logic: APK parsing via androguard, permission analysis, AI integration with Gemini API |
| **code/analyzer.py** | Tiny adapter module to re-export functions from `core_analyzer.py` |
| **code/permissions_db.json** | Curated database mapping Android permissions to risk levels and descriptions |
| **templates/index.html** | User-friendly upload interface with drag-and-drop support |
| **templates/report.html** | Jinja2 template for rendered analysis reports with color-coded risk levels |

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key for AI analysis | Not set (optional) |
| `FLASK_ENV` | Flask environment mode | `development` |

### Permission Database

Edit `code/permissions_db.json` to add or modify permission definitions:

```json
{
  "android.permission.CAMERA": {
    "risk": "High",
    "description": "Allows the app to use your camera..."
  }
}
```

---

## 🧪 Testing

### Manual Testing with Sample APKs

Sample APKs are included in `uploads/` for testing:

```bash
# Start the server
python3 code/app.py

# In another terminal, test with Calculator
curl -s -F "file=@uploads/Calculator_9.0_.apk" http://127.0.0.1:5000/upload -o test_calculator.html

# Test with FlashLight
curl -s -F "file=@uploads/FlashLight_.apk" http://127.0.0.1:5000/upload -o test_flashlight.html
```

---

## 🔒 Security Notes

- **Development Server**: The included Flask development server is for testing only. For production, deploy behind a WSGI server:
  ```bash
  pip install gunicorn
  gunicorn -w 4 -b 0.0.0.0:5000 code.app:app
  ```
  
- **File Uploads**: The app accepts only `.apk` files
- **API Key Safety**: Store `GEMINI_API_KEY` in environment variables, not in code
- **Temporary Files**: Uploaded APKs are automatically deleted after analysis

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
lsof -i :5000
kill -9 <PID>
```

### Permission Database Not Found

Ensure `code/permissions_db.json` exists and is valid JSON.

### AI Analysis Not Working

1. Verify `GEMINI_API_KEY` is set:
   ```bash
   echo $GEMINI_API_KEY
   ```
2. Check that your API key has Generative AI API enabled in Google Cloud Console

### androguard Installation Issues

See the **Install Dependencies** section above for OS-specific solutions.

---

## 📝 Sample Output

**Calculator App Report:**
- App Name: Calculator
- Package: com.google.android.calculator
- Permissions: 2 Low Risk, 4 Unknown
- Verdict: "This app requests no significant permissions. It appears to be safe."

**FlashLight App Report:**
- App Name: FlashLight
- Package: com.example.phoneflashlight11
- Permissions: 1 High Risk (CAMERA), 1 Unknown
- Verdict: "⚠️ This app requires camera access, which is unusual for a flashlight app and may be suspicious."

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please ensure:
- Code is well-documented
- Permission database (`code/permissions_db.json`) is updated for new permissions
- Changes are tested with sample APKs

---

## 📄 License

This project is provided as-is for educational and research purposes.

---

## 🙏 Acknowledgments

- **androguard**: For APK parsing and analysis
- **Flask**: For the web framework
- **Google Gemini API**: For AI-powered security insights
- **Pico CSS**: For minimalist, beautiful styling

---

## 📧 Contact & Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing documentation in this README
- Review Flask logs for detailed error traces

---

**Last Updated:** January 2026
