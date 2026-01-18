# Quick Start Guide

## ✅ Setup Complete!

Your Django REST backend is now running at: **http://127.0.0.1:8000/**

## 📋 What's Been Created

### Backend Structure:
```
myproject/
├── myapp/
│   ├── models.py          # Document & ChatMessage models
│   ├── views.py           # Function-based API views
│   ├── urls.py            # Clean URL routing
│   ├── ocr_utils.py       # OCR processing (from ocr.ipynb)
│   └── llm_utils.py       # LLM enhancement (from LLM.ipynb)
├── templates/
│   └── index.html         # User-friendly frontend
└── media/uploads/         # Uploaded files storage
```

### API Endpoints:
- `POST /api/upload/` - Upload & process document
- `GET /api/documents/` - List all documents
- `GET /api/documents/<id>/` - Get document details
- `POST /api/documents/<id>/chat/` - Ask questions
- `GET /api/documents/<id>/chat/history/` - Chat history

## 🚀 How to Use

1. **Open the application**: http://127.0.0.1:8000/

2. **Upload a form**:
   - Click the upload area or drag-and-drop
   - Supported: PDF, JPG, PNG, BMP, TIFF
   - The app will automatically:
     - Extract text using OCR
     - Enhance text with LLM
     - Extract structured fields (name, DOB, address, etc.)

3. **View extracted data**:
   - All fields displayed in a clean grid
   - See enhanced text below

4. **Chat with your document**:
   - Ask questions like:
     - "What is the customer's name?"
     - "What is the phone number?"
     - "What is the date of birth?"
   - AI will answer based on extracted data

## ⚙️ Configuration

### Before uploading files, update these paths:

**1. Tesseract OCR Path**
- File: `myapp/ocr_utils.py`
- Line: `TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"`
- Update to your Tesseract installation path

**2. Poppler Path (for PDFs)**
- File: `myapp/ocr_utils.py`
- Line: `POPPLER_PATH = r"C:\Users\tsheikh\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"`
- Update to your Poppler bin folder

**3. OpenAI API Key**
- File: `myapp/llm_utils.py`
- Line: `OPENAI_API_KEY = "your-key-here"`
- Replace with your actual OpenAI API key

## 🎯 Features

✅ **Function-based views** (no forms.py)
✅ **Clean URL routing**
✅ **OCR code from ocr.ipynb** (working as-is)
✅ **LLM code from LLM.ipynb** (working as-is)
✅ **User-friendly interface**
✅ **Real-time chat functionality**
✅ **Structured field extraction**
✅ **Support for images and PDFs**

## 🛠️ Troubleshooting

**If OCR fails:**
- Ensure Tesseract is installed and path is correct
- For PDFs, ensure Poppler is installed and path is correct

**If LLM fails:**
- Check your OpenAI API key is valid
- Ensure you have API credits available

**If upload fails:**
- Check file format is supported
- Ensure media folder has write permissions

## 🏗️ Project Highlights for Hackathon

1. **Simple & Clean**: No complex forms, just function-based views
2. **Working Code**: Uses proven OCR and LLM code from notebooks
3. **User-Friendly**: Beautiful interface with drag-and-drop
4. **Complete Workflow**: Upload → OCR → LLM Enhancement → Chat
5. **Production-Ready**: Proper models, error handling, and API structure

## 📦 Dependencies Installed

- django==5.2.10
- djangorestframework==3.16.1
- pytesseract (OCR)
- opencv-python (Image processing)
- pillow (Image handling)
- pdf2image (PDF conversion)
- openai (LLM)
- numpy (Data processing)

## 🎉 Ready to Demo!

Your form reading app is ready for the hackathon. Just:
1. Update the three configuration paths above
2. Open http://127.0.0.1:8000/
3. Upload a form and start chatting!
