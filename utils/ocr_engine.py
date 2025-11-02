import pytesseract
from PIL import Image
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

class OCREngine:
    def __init__(self):
        # Configure tesseract path if needed
        # pytesseract.pytesseract.tesseract_cmd = r'<path_to_tesseract_executable>'
        self.supported_languages = {
            'nepali': 'nep',
            'sinhalese': 'sin'
        }
    
    def preprocess_image(self, image_path):
        """Preprocess image for better OCR results"""
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Could not read image")
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply noise reduction
            denoised = cv2.medianBlur(gray, 3)
            
            # Apply thresholding
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            return thresh
            
        except Exception as e:
            logger.error(f"Error in image preprocessing: {str(e)}")
            return None
    
    def extract_text_from_image(self, image_path, language='nepali'):
        """Extract text from image using OCR"""
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_path)
            
            if processed_image is None:
                # Fallback to direct OCR
                processed_image = Image.open(image_path)
            else:
                processed_image = Image.fromarray(processed_image)
            
            # Get tesseract language code
            lang_code = self.supported_languages.get(language, 'nep')
            
            # Configure tesseract
            custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'
            
            # Extract text
            extracted_text = pytesseract.image_to_string(
                processed_image, 
                lang=lang_code,
                config=custom_config
            )
            
            logger.info(f"Successfully extracted text from image: {len(extracted_text)} characters")
            return extracted_text.strip()
            
        except Exception as e:
            logger.error(f"Error in OCR extraction: {str(e)}")
            raise Exception(f"OCR extraction failed: {str(e)}")
    
    def detect_language(self, image_path):
        """Detect language of the text in image"""
        try:
            # Simple language detection based on OCR confidence for different languages
            image = Image.open(image_path)
            
            nepali_text = pytesseract.image_to_string(image, lang='nep')
            sinhalese_text = pytesseract.image_to_string(image, lang='sin')
            
            # Return the language with more non-empty characters
            if len(nepali_text.strip()) > len(sinhalese_text.strip()):
                return 'nepali'
            else:
                return 'sinhalese'
                
        except Exception as e:
            logger.error(f"Error in language detection: {str(e)}")
            return 'nepali'  # Default fallback