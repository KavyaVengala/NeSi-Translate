from transformers import MarianMTModel, MarianTokenizer
from huggingface_hub import login as hf_login
from transformers import pipeline
import torch
import logging
import os

logger = logging.getLogger(__name__)

# Optional: login using the environment variable
token = os.environ.get("HUGGINGFACE_TOKEN")#this contains the huggingface token


class NepaliTranslator:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        self.load_model()
    
    def load_model(self):
        """Load the translation model"""
        try:
            # Using Helsinki-NLP's multilingual model that supports Nepali
            model_name = "Helsinki-NLP/opus-mt-mul-en"  # This model supports multiple languages including Nepali
            
            logger.info(f"Loading multilingual translation model {model_name}...")
            # Download model anonymously - this is a public model
            self.tokenizer = MarianTokenizer.from_pretrained(model_name)
            self.model = MarianMTModel.from_pretrained(model_name)
            
            self.model_loaded = True
            logger.info("Nepali translation model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading translation model: {str(e)}")
            self.model_loaded = False
    
    def translate(self, text, max_length=512):
        """Translate Nepali text to English"""
        # If there's no input text, return empty string
        if not text or not text.strip():
            return ""

        # If the model failed to load, return an explicit error message so the UI shows the problem
        if not self.model_loaded:
            logger.error("Nepali translation model is not loaded")
            return "[Error: Nepali translation model not loaded - check server logs]"
        
        try:
            # Split long text into chunks
            chunks = self._split_text(text, max_length)
            translated_chunks = []
            
            for chunk in chunks:
                # Tokenize
                inputs = self.tokenizer(
                    chunk, 
                    return_tensors="pt", 
                    padding=True, 
                    truncation=True,
                    max_length=max_length
                )
                
                # Generate translation
                with torch.no_grad():
                    translated = self.model.generate(
                        **inputs,
                        max_length=max_length,
                        num_beams=4,
                        early_stopping=True
                    )
                
                # Decode
                translated_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)
                translated_chunks.append(translated_text)
            
            return " ".join(translated_chunks)
            
        except Exception as e:
            logger.error(f"Error in translation: {str(e)}")
            return f"Translation error: {str(e)}"
    
    def _split_text(self, text, max_length):
        """Split text into chunks for translation"""
        sentences = text.split('.')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_length:
                current_chunk += sentence + "."
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence + "."
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def fine_tune(self, training_data):
        """Fine-tune the model with new data (basic implementation)"""
        # This would be implemented for continuous learning
        # Requires substantial training data and computational resources
        logger.info("Fine-tuning functionality would be implemented here")
        pass