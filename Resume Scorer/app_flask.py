# Resume Scorer Flask App for Render Deployment

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from resume_scorer import score_resume
import PyPDF2
import docx
import io
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests from your portfolio

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Scorer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
        }
        
        h1 {
            text-align: center;
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
        }
        
        .section {
            margin-bottom: 30px;
        }
        
        .section-title {
            font-size: 1.2em;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }
        
        .section-title::before {
            content: '';
            width: 4px;
            height: 20px;
            background: #667eea;
            margin-right: 10px;
            border-radius: 2px;
        }
        
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            font-family: 'Consolas', 'Monaco', monospace;
            resize: vertical;
            transition: border-color 0.3s;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .upload-area {
            border: 2px dashed #e0e0e0;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
            transition: all 0.3s;
            cursor: pointer;
            margin-bottom: 15px;
        }
        
        .upload-area:hover {
            border-color: #667eea;
            background: #f8f9ff;
        }
        
        .upload-area.dragover {
            border-color: #667eea;
            background: #f0f3ff;
        }
        
        input[type="file"] {
            display: none;
        }
        
        .file-info {
            margin-top: 10px;
            color: #4caf50;
            font-weight: 500;
        }
        
        .btn-primary {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin: 20px 0;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        
        .btn-primary:active {
            transform: translateY(0);
        }
        
        .btn-primary:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .results {
            display: none;
            margin-top: 30px;
            padding: 30px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
        }
        
        .results.show {
            display: block;
        }
        
        .score-display {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .score-number {
            font-size: 4em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .score-label {
            font-size: 1.2em;
            color: #666;
        }
        
        .metrics {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .metric {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .metric-label {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .keywords-section {
            background: white;
            padding: 20px;
            border-radius: 10px;
        }
        
        .keywords-section h3 {
            color: #333;
            margin-bottom: 15px;
        }
        
        .keywords {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        
        .keyword {
            background: #667eea;
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        
        .loading.show {
            display: block;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            display: none;
        }
        
        .error.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Resume Scorer</h1>
        <p class="subtitle">AI-Powered Resume Analysis</p>
        
        <div class="section">
            <div class="section-title">Job Description</div>
            <textarea id="jobDescription" rows="8" placeholder="Paste the job description here..."></textarea>
        </div>
        
        <div class="section">
            <div class="section-title">Resume</div>
            <div class="upload-area" id="uploadArea">
                <div style="font-size: 3em; margin-bottom: 10px;">📄</div>
                <div style="font-size: 1.1em; margin-bottom: 5px;">Drop resume file here or click to upload</div>
                <div style="color: #999; font-size: 0.9em;">Supports PDF, DOCX, and TXT files</div>
                <input type="file" id="fileInput" accept=".pdf,.docx,.txt">
            </div>
            <div class="file-info" id="fileInfo"></div>
            <div style="text-align: center; margin: 15px 0; color: #999;">- OR -</div>
            <textarea id="resumeText" rows="8" placeholder="Or paste your resume text here..."></textarea>
        </div>
        
        <button class="btn-primary" id="scoreBtn">Score Resume</button>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <div>Analyzing resume...</div>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="results" id="results">
            <div class="score-display">
                <div class="score-label">Final Score</div>
                <div class="score-number" id="scoreNumber">--</div>
                <div style="color: #666;">out of 10</div>
            </div>
            
            <div class="metrics">
                <div class="metric">
                    <div class="metric-label">Semantic Similarity</div>
                    <div class="metric-value" id="similarity">--%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Keyword Coverage</div>
                    <div class="metric-value" id="coverage">--%</div>
                </div>
            </div>
            
            <div class="keywords-section">
                <h3>Matched Keywords (<span id="matchCount">0</span>/<span id="totalCount">0</span>)</h3>
                <div class="keywords" id="keywords"></div>
            </div>
        </div>
    </div>
    
    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const fileInfo = document.getElementById('fileInfo');
        const scoreBtn = document.getElementById('scoreBtn');
        const loading = document.getElementById('loading');
        const results = document.getElementById('results');
        const errorDiv = document.getElementById('error');
        
        let selectedFile = null;
        
        // Upload area click
        uploadArea.addEventListener('click', () => fileInput.click());
        
        // File selection
        fileInput.addEventListener('change', (e) => {
            selectedFile = e.target.files[0];
            if (selectedFile) {
                fileInfo.textContent = `✓ ${selectedFile.name}`;
                document.getElementById('resumeText').value = '';
            }
        });
        
        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            selectedFile = e.dataTransfer.files[0];
            if (selectedFile) {
                fileInfo.textContent = `✓ ${selectedFile.name}`;
                document.getElementById('resumeText').value = '';
            }
        });
        
        // Score button
        scoreBtn.addEventListener('click', async () => {
            const jobDesc = document.getElementById('jobDescription').value.trim();
            const resumeText = document.getElementById('resumeText').value.trim();
            
            if (!jobDesc) {
                showError('Please enter a job description');
                return;
            }
            
            if (!selectedFile && !resumeText) {
                showError('Please upload a resume file or paste resume text');
                return;
            }
            
            // Prepare data
            const data = {
                job_description: jobDesc,
                resume_text: resumeText
            };
            
            // Read file if uploaded
            if (selectedFile) {
                const reader = new FileReader();
                reader.onload = async (e) => {
                    data.resume_file = e.target.result;
                    data.file_type = selectedFile.type;
                    await scoreResume(data);
                };
                reader.readAsDataURL(selectedFile);
            } else {
                await scoreResume(data);
            }
        });
        
        async function scoreResume(data) {
            // Show loading
            loading.classList.add('show');
            results.classList.remove('show');
            errorDiv.classList.remove('show');
            scoreBtn.disabled = true;
            
            try {
                const response = await fetch('/score', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.error) {
                    showError(result.error);
                } else {
                    displayResults(result);
                }
            } catch (error) {
                showError('Failed to score resume: ' + error.message);
            } finally {
                loading.classList.remove('show');
                scoreBtn.disabled = false;
            }
        }
        
        function displayResults(result) {
            // Score
            const scoreNumber = document.getElementById('scoreNumber');
            scoreNumber.textContent = result.score.toFixed(2);
            
            // Color code score
            if (result.score >= 8) {
                scoreNumber.style.color = '#4CAF50';
            } else if (result.score >= 6) {
                scoreNumber.style.color = '#FF9800';
            } else {
                scoreNumber.style.color = '#F44336';
            }
            
            // Metrics
            document.getElementById('similarity').textContent = (result.similarity * 100).toFixed(1) + '%';
            document.getElementById('coverage').textContent = (result.coverage * 100).toFixed(1) + '%';
            
            // Keywords
            document.getElementById('matchCount').textContent = result.matched_keywords.length;
            document.getElementById('totalCount').textContent = result.total_keywords;
            
            const keywordsDiv = document.getElementById('keywords');
            keywordsDiv.innerHTML = '';
            
            if (result.matched_keywords.length > 0) {
                result.matched_keywords.forEach(keyword => {
                    const span = document.createElement('span');
                    span.className = 'keyword';
                    span.textContent = keyword;
                    keywordsDiv.appendChild(span);
                });
            } else {
                keywordsDiv.innerHTML = '<div style="color: #999;">No keywords matched</div>';
            }
            
            // Show results
            results.classList.add('show');
            results.scrollIntoView({ behavior: 'smooth' });
        }
        
        function showError(message) {
            errorDiv.textContent = message;
            errorDiv.classList.add('show');
            setTimeout(() => {
                errorDiv.classList.remove('show');
            }, 5000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/score', methods=['POST'])
def score():
    """Handle resume scoring requests"""
    try:
        data = request.json
        job_text = data.get('job_description', '')
        resume_text = data.get('resume_text', '')
        resume_file = data.get('resume_file', '')
        file_type = data.get('file_type', '')
        
        # Parse resume file if provided
        if resume_file:
            resume_text = parse_resume_file(resume_file, file_type)
        
        # Validate inputs
        if not job_text or not resume_text:
            return jsonify({'error': 'Missing job description or resume'}), 400
        
        # Score the resume
        results = score_resume(resume_text, job_text)
        
        # Send results
        return jsonify({
            'success': True,
            'score': results['final_score'],
            'similarity': round(results['similarity'], 4),
            'coverage': round(results['coverage'], 4),
            'matched_keywords': results['matched_keywords'],
            'total_keywords': len(results['raw_keywords'])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def parse_resume_file(file_data, file_type):
    """Parse resume file from base64 data"""
    # Decode base64
    file_bytes = base64.b64decode(file_data.split(',')[1])
    
    if file_type == 'application/pdf':
        # Parse PDF
        pdf_file = io.BytesIO(file_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    
    elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        # Parse DOCX
        docx_file = io.BytesIO(file_bytes)
        doc = docx.Document(docx_file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    
    elif file_type == 'text/plain':
        # Parse TXT
        return file_bytes.decode('utf-8')
    
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
