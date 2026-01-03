import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from analyzer import get_app_details, analyze_permissions, get_ai_context_analysis

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB max upload size
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Main upload page
@app.route('/')
def index():
    return render_template('index.html')

#Upload and analyze file 
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file and file.filename.endswith('.apk'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(filepath)
            
            # This is where the magic happens
            
            #  Core analysis
            app_name, pkg_name, permissions_list = get_app_details(filepath)
            report, risky_perms_for_ai = analyze_permissions(permissions_list)
            
            # AI Analysis
            ai_summary = get_ai_context_analysis(app_name, risky_perms_for_ai)
            # 
            
            # Clean up the uploaded file
            os.remove(filepath) 
            
            # Render the results page
            return render_template('report.html', 
                                   app_name=app_name, 
                                   package_name=pkg_name,
                                   report=report,
                                   ai_summary=ai_summary)
                                   
        except Exception as e:
            # Clean up if analysis fails
            if os.path.exists(filepath):
                os.remove(filepath)
            print(f"An error occurred: {e}")
            return "An error occurred during analysis.", 500
        
    else:
        return "Invalid file type. Please upload an .apk file.", 400

if __name__ == '__main__':
    app.run(debug=True)
