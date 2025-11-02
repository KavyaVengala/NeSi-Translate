import PyPDF2
from pdf2image import convert_from_path
import os
import logging
from .ocr_engine import OCREngine

logger = logging.getLogger(__name__)

class FileProcessor:
    def __init__(self):
        self.ocr_engine = OCREngine()
    
    def extract_text_from_pdf(self, pdf_path, use_ocr=True):
        """Extract text from PDF file"""
        try:
            text = ""
            
            # First try to extract text directly
            if not use_ocr:
                try:
                    with open(pdf_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        for page in pdf_reader.pages:
                            text += page.extract_text() + "\n"
                    
                    if text.strip():
                        return text.strip()
                except Exception as e:
                    logger.warning(f"Direct PDF text extraction failed: {str(e)}")
            
            # Fallback to OCR
            logger.info("Using OCR for PDF text extraction")
            images = convert_from_path(pdf_path)
            
            for i, image in enumerate(images):
                image_path = f"temp_page_{i}.png"
                image.save(image_path, 'PNG')
                
                page_text = self.ocr_engine.extract_text_from_image(image_path)
                text += page_text + "\n"
                
                # Clean up temporary image
                os.remove(image_path)
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error in PDF processing: {str(e)}")
            raise Exception(f"PDF processing failed: {str(e)}")