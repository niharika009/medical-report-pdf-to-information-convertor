import os
from flask import Flask, request, render_template
from extract import extract_text_pdf
from preprocess import clean_text
from summarize import summarize_text
from lab_extractor import extract_lab_values_dynamic
from config import MAX_UPLOAD_SIZE_MB

# Paths for templates and static
template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'templates')
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE_MB * 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files or request.files['file'].filename == '':
        return "No file uploaded", 400
    f = request.files['file']
    data = f.read()

    raw_text, _ = extract_text_pdf(data)
    cleaned = clean_text(raw_text)
    summary = summarize_text(cleaned)
    labs = extract_lab_values_dynamic(cleaned)

    return render_template('result.html',
                           summary=summary,
                           labs=labs,
                           full_text=cleaned[:5000])

if __name__ == "__main__":
    app.run(debug=True)
