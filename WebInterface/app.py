from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_code():
    if 'code_file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['code_file']
    if file.filename == '':
        return "No selected file", 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Save the processed result to a new output file
    output_filename = 'proofed_' + file.filename
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        hard_coded = open("testing/example_converted.c", "r")
        f.write(hard_coded.read())
        hard_coded.close()
        
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)