import json
import sys
import os
from androguard.core.apk import APK
import google.generativeai as genai

try:
    with open('permissions_db.json', 'r') as f:
        PERMISSIONS_DB = json.load(f)
except FileNotFoundError:
    print("Error: permissions_db.json not found.")
    PERMISSIONS_DB = {}

def get_app_details(apk_path):
    """
    Extracts app name, package name, and permissions from an APK file.
    """
    try:
        apk = APK(apk_path)
        permissions = apk.get_permissions()
        app_name = apk.get_app_name()
        package_name = apk.get_package()
        return app_name, package_name, permissions
    except Exception as e:
        print(f"Error processing APK: {e}")
        return "Unknown App", "unknown.package", []


def analyze_permissions(permission_list):
    """
    Analyzes a list of permissions and returns a risk report.
    """
    report = {
        "high_risk": [],
        "medium_risk": [],
        "low_risk": [],
        "unknown": []
    }
    
    risky_perms_for_ai = []

    for perm in permission_list:
        if perm in PERMISSIONS_DB:
            info = PERMISSIONS_DB[perm]
            risk_level = info['risk'].lower()
            report_item = {
                "name": perm,
                "description": info['description']
            }
            report[f"{risk_level}_risk"].append(report_item)
            
            if risk_level in ["high", "medium"]:
                risky_perms_for_ai.append(perm)
        else:
            report["unknown"].append({
                "name": perm,
                "description": "This is an uncommon or custom permission not in our database."
            })
            
    return report, risky_perms_for_ai

def get_ai_context_analysis(app_name, risky_permission_list):
    """
    Uses the Gemini API to check if permissions are suspicious for the app type.
    """
    if not risky_permission_list:
        return "This app requests no significant permissions. It appears to be safe."

    try:
       
        # Read API key from environment for safety. Set GEMINI_API_KEY in your environment
        # if you want AI contextual analysis. If not set, skip AI analysis.
        API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_GOES_HERE")
        if API_KEY == "YOUR_GEMINI_API_KEY_GOES_HERE":
            return "AI analysis is not configured. Set the GEMINI_API_KEY environment variable to enable it."

        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')

        permission_str = ", ".join(risky_permission_list)
        
        prompt = f"""
        Act as a mobile security expert.
        An app named '{app_name}' is requesting the following risky permissions:
        {permission_str}

        Based ONLY on the app's name (e.g., 'Flashlight', 'Calculator', 'NotePad'), do these permissions seem suspicious or unnecessary?
        Give me a one-paragraph summary for a non-technical user.
        Start with a clear verdict: "Verdict: [Appears Safe]" or "Verdict: [Suspicious]" or "Verdict: [Highly Suspicious]".
        Then, explain why in simple terms.
        """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"AI analysis failed: {e}")
        return f"Could not perform AI contextual analysis. Error: {e}"

# testing the script from the command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <path_to_apk>")
    else:
        apk_file = sys.argv[1]
        print(f"Analyzing {apk_file}...")
        
        app_name, pkg_name, perms = get_app_details(apk_file)
        print(f"App Name: {app_name}")
        print(f"Package: {pkg_name}\n")
        
        report, risky_perms = analyze_permissions(perms)
        
        print("--- ANALYSIS REPORT ---")
        print(json.dumps(report, indent=2))
        
        print("\n--- AI SUMMARY ---")
        ai_summary = get_ai_context_analysis(app_name, risky_perms)
        print(ai_summary)