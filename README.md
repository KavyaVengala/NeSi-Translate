🧠 AI/ML Based Translation System

A web-based translation application that leverages Artificial Intelligence (AI) and Machine Learning (ML) technologies to translate Nepali and Sinhalese text or documents into English.
Designed for accuracy, security, and offline deployment.


🚀 Features

Document Translation — Upload and translate files in PDF, PNG, JPG, or JPEG formats.

Text Translation — Instantly translate typed or pasted text directly in the interface.

Optical Character Recognition (OCR) — Extract and translate text from scanned documents and images using Tesseract OCR.

Offline Capability — Operates fully within local or internal networks without internet access.

Machine Learning Integration — Uses Transformer-based models for adaptive, high-quality translations.

Security-Oriented Design — Implements robust security practices for data handling and storage.


🌐 Supported Languages

Nepali ➜ English

Sinhalese ➜ English

⚙️ Installation Guide
🔧 Prerequisites

Ensure the following are installed on your system:

Python 3.8+

Tesseract OCR

Download Tesseract OCR

🧩 Setup Instructions
# 1️⃣ Clone the repository
git clone https://github.com/<your-username>/ai-ml-translation-system.git
cd ai-ml-translation-system

# 2️⃣ Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
# or
source venv/bin/activate  # On macOS/Linux

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run the application
python app.py


Then open your browser and visit:

http://localhost:5000


🧭 Usage Example
🔹 Text Translation

Open the web interface.

Select Text Translation from the main menu.

Choose the source language (Nepali or Sinhalese).

Enter or paste text into the input box.

Click Translate to generate the English translation.

Copy or download the translated output as needed.

🔹 Document Translation

Navigate to Document Translation.

Upload a supported file (.pdf, .jpg, .jpeg, .png).

The system applies OCR automatically for scanned files.

View the translated content and download the result.


🔒 Security Features

Environment-based Configuration — Secure key and credential management using .env.

Secure File Uploads — Enforces file validation and sandboxing.

Input Validation & Sanitization — Prevents code injection or data corruption.

Security Headers — Includes CSP, HSTS, and X-Frame-Options.

Session Security — Encrypted and time-limited user sessions.

File Type Validation — Ensures only permitted file types are processed.


🤖 Machine Learning Models
Language Pair	Model Used
Nepali → English	Helsinki-NLP/opus-mt-ne-en
Sinhalese → English	Helsinki-NLP/opus-mt-si-en

These MarianMT Transformer models from Helsinki-NLP provide high-quality, context-aware translation performance and can be fine-tuned for future improvements.


 Project Structure:

translation_app/

translation_app/
├── app.py
├── requirements.txt
├── models/
│   ├── __init__.py
│   ├── nepali_translator.py
│   └── sinhalese_translator.py
├── utils/
│   ├── __init__.py
│   ├── ocr_engine.py
│   └── file_processor.py
├── templates/
│   ├── index.html
│   └── result.html
├── static/
│   ├── css/
│   └── js/
├── data/
│   └── training/
└── README.md



📦 Technologies Used

Python (Flask / FastAPI)

Transformers (Hugging Face)

Tesseract OCR

OpenCV / Pillow

HTML5, CSS3, JavaScript


🧰 Future Enhancements

Expand translation support to Hindi, Tamil, and other regional languages.

Add real-time translation previews.

Integrate cloud-based APIs for hybrid online/offline use.

Improve UI/UX with modern interactive design.


Enable custom model fine-tuning for domain-specific translation needs.
