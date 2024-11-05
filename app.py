from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import re

app = Flask(__name__)
CORS(app)  


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  

def extract_document_info(image):
    text = pytesseract.image_to_string(image)
    # Extract Name
    name = re.search(r'Name:\s*(.*)', text)
    name = name.group(1) if name else 'Not found'
    # Extract Document Number
    doc_number = re.search(r'Document No\.\s*:\s*(\w+)', text)
    doc_number = doc_number.group(1) if doc_number else 'Not found'
    # Extract Expiration Date
    expiration_date = re.search(r'Expiration Date\s*:\s*(\d{2}/\d{2}/\d{4})', text)
    expiration_date = expiration_date.group(1) if expiration_date else 'Not found'
    
    return {
        'Name': name,
        'Document Number': doc_number,
        'Expiration Date': expiration_date
    }

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        image = Image.open(file.stream)
        info = extract_document_info(image)
        return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True)
