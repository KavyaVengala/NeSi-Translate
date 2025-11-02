from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import logging
from utils.ocr_engine import OCREngine
from utils.file_processor import FileProcessor
from models.nepali_translator import NepaliTranslator
from models.sinhalese_translator import SinhaleseTranslator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
ocr_engine = OCREngine()
file_processor = FileProcessor()
nepali_translator = NepaliTranslator()
sinhalese_translator = SinhaleseTranslator()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_document():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        language = request.form.get('language', 'nepali')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the file
            logger.info(f"Processing file: {filename} for {language} language")
            
            # Extract text based on file type
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                extracted_text = ocr_engine.extract_text_from_image(filepath, language=language)
            elif filename.lower().endswith('.pdf'):
                extracted_text = file_processor.extract_text_from_pdf(filepath)
            else:
                return jsonify({'error': 'Unsupported file format'}), 400

            # Log extraction info to help debugging
            logger.info(f"Extracted text length: {len(extracted_text) if extracted_text is not None else 0}")

            # Ensure we have text to translate
            if not extracted_text or not extracted_text.strip():
                logger.warning("No text extracted from the uploaded file")
                return jsonify({'error': 'No text could be extracted from the file'}), 400
            
            # Translate text based on language
            if language == 'nepali':
                translated_text = nepali_translator.translate(extracted_text)
            elif language == 'sinhalese':
                translated_text = sinhalese_translator.translate(extracted_text)
            else:
                return jsonify({'error': 'Unsupported language'}), 400
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'original_text': extracted_text,
                'translated_text': translated_text,
                'language': language
            })
            
    except Exception as e:
        logger.error(f"Error during translation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/translate-text', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        language = data.get('language', 'nepali')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if language == 'nepali':
            translated_text = nepali_translator.translate(text)
        elif language == 'sinhalese':
            translated_text = sinhalese_translator.translate(text)
        else:
            return jsonify({'error': 'Unsupported language'}), 400
        
        return jsonify({
            'success': True,
            'original_text': text,
            'translated_text': translated_text,
            'language': language
        })
        
    except Exception as e:
        logger.error(f"Error in text translation: {str(e)}")
        return jsonify({'error': str(e)}), 500

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'pdf'}

if __name__ == '__main__':
    # For production use: waitress.serve(app, host='0.0.0.0', port=5000)
    app.run(debug=True, host='0.0.0.0', port=5000)
    