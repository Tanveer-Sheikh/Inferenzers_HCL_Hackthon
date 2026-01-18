# Information Extraction from Scanned User-Filled Forms

A Django REST Framework application that extracts structured data from scanned user-filled forms using OCR (Tesseract) and AI-powered text enhancement (OpenAI GPT-4o-mini). This system automates the digitization of paper forms, reducing manual data entry and enabling searchable document management.

## 👥 Team Members

- **Tanveer** - 24CSM2R20
- **Vikranth Tej** - 22BTB0A44
- **Pradyumna** - 22CEB0A26
- **Anvesh** - 22CEB0A15

## 🎯 Project Overview

This hackathon project demonstrates an end-to-end solution for digitizing paper forms. The system accepts scanned images or PDF documents of filled forms, extracts text using OCR, enhances the data using AI, and stores structured information in a database. Users can search, view, chat with documents, and export data in multiple formats.

### Key Capabilities
- Automatic text extraction from scanned forms (PDF/Images)
- AI-powered data cleaning and field extraction
- Interactive chat interface to query document contents
- Self-service document browser with search
- Export functionality (JSON/TXT formats)
- Admin dashboard for complete data management

## 📁 Project Structure

```
HCL_Hackthon/
├── ocr.ipynb                   # Jupyter notebook for OCR testing & development
├── LLM.ipynb                   # Jupyter notebook for LLM integration testing
├── LLM_google.ipynb            # Alternative LLM testing notebook
├── README.md                   # This file
├── backend/                    # Initial backend exploration
└── myproject/                  # Main Django REST Framework application
    ├── manage.py              # Django management script
    ├── myproject/             # Project configuration
    │   ├── settings.py        # Django settings
    │   ├── urls.py            # Root URL configuration
    │   └── wsgi.py            # WSGI configuration
    ├── myapp/                 # Main application
    │   ├── models.py          # Database models (Document, ChatMessage)
    │   ├── views.py           # API endpoints (8 views)
    │   ├── urls.py            # App URL routing
    │   ├── admin.py           # Admin panel configuration
    │   ├── ocr_utils.py       # Tesseract OCR processing utilities
    │   ├── llm_utils.py       # OpenAI GPT integration utilities
    │   └── migrations/        # Database migrations
    ├── templates/
    │   └── index.html         # Frontend web interface
    ├── media/uploads/         # Uploaded documents storage
    └── db.sqlite3             # SQLite database
```

## 📓 Jupyter Notebooks (Testing & Development)

The project includes separate Jupyter notebooks used for testing and development of core features:

### 1. ocr.ipynb
- **Purpose**: OCR testing and image preprocessing
- **Contains**: 
  - Tesseract OCR implementation
  - Image preprocessing pipeline (grayscale, denoising, thresholding)
  - PDF to image conversion
  - Text extraction experiments
- **Status**: Successfully integrated into `myapp/ocr_utils.py`

### 2. LLM.ipynb
- **Purpose**: OpenAI GPT integration testing
- **Contains**: 
  - Text enhancement logic
  - Field extraction prompts
  - JSON parsing and validation
  - Chat functionality experiments
- **Status**: Successfully integrated into `myapp/llm_utils.py`

### 3. LLM_google.ipynb
- **Purpose**: Alternative LLM testing (Google AI)
- **Contains**: 
  - Google AI API experiments
  - Comparative testing with OpenAI
- **Status**: Research/testing notebook (not integrated)

**Note**: These notebooks were used during development to test OCR and LLM features independently before integrating them into the Django application.

## 🚀 Step-by-Step Project Implementation

### Step 1: Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install django djangorestframework
pip install pytesseract opencv-python pillow pdf2image numpy
pip install openai
```

### Step 2: Create Django Project
```bash
# Create project and app
django-admin startproject myproject
cd myproject
python manage.py startapp myapp

# Configure settings.py
# - Add 'rest_framework' and 'myapp' to INSTALLED_APPS
# - Configure MEDIA_ROOT and MEDIA_URL for file uploads
# - Set TEMPLATES dirs to include templates folder
```

### Step 3: Define Database Models
**File**: `myapp/models.py`
- **Document Model**: Stores uploaded files and extracted data (9 fields)
- **ChatMessage Model**: Stores chat Q&A for each document

```bash
# Create migrations
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Implement OCR Utilities
**File**: `myapp/ocr_utils.py`
- Port code from `ocr.ipynb`
- Functions: `load_document_pages()`, `preprocess_image()`, `run_ocr_on_image()`, `extract_text_document()`
- Configure Tesseract and Poppler paths

### Step 5: Implement LLM Utilities
**File**: `myapp/llm_utils.py`
- Port code from `LLM.ipynb`
- Functions: `enhance_text()`, `extract_fields()`, `process_ocr_text()`, `answer_query()`
- Configure OpenAI API key

### Step 6: Create API Views
**File**: `myapp/views.py`
- 8 function-based views:
  1. `index()` - Home page
  2. `upload_document()` - Upload & process files
  3. `get_document()` - Retrieve document details
  4. `chat_with_document()` - Ask questions about document
  5. `get_chat_history()` - Get all chat messages
  6. `list_documents()` - List/search documents
  7. `download_json_report()` - Export JSON
  8. `download_text_report()` - Export TXT

### Step 7: Configure URL Routing
**File**: `myapp/urls.py`
- Define RESTful API endpoints
- Map URLs to views

**File**: `myproject/urls.py`
- Include app URLs
- Configure media file serving

### Step 8: Build Frontend Interface
**File**: `templates/index.html`
- Upload interface with drag-and-drop
- Extracted data display with grid layout
- Chat interface for document queries
- Document browser with search functionality
- Download buttons for JSON/TXT exports

### Step 9: Configure Admin Panel
**File**: `myapp/admin.py`
- Custom `DocumentAdmin` with search and filters
- Custom `ChatMessageAdmin` for viewing conversations
- Create superuser for admin access

```bash
python manage.py createsuperuser
# Username: admin
```

### Step 10: Run Development Server
```bash
python manage.py runserver
# Access at: http://127.0.0.1:8000/
# Admin at: http://127.0.0.1:8000/admin/
```

### Backend Framework
- **Django 5.2.10** - Web framework
- **Django REST Framework 3.16.1** - RESTful API development

### OCR & Image Processing
- **Pytesseract** - Python wrapper for Tesseract OCR engine
- **OpenCV (opencv-python)** - Image preprocessing and manipulation
- **Pillow** - Image handling and conversion
- **pdf2image** - PDF to image conversion
- **NumPy** - Numerical operations for image processing

### AI/LLM Integration
- **OpenAI 2.15.0** - GPT-4o-mini for text enhancement and field extraction

### Database
- **SQLite** - Default Django database (for development)

## 🤖 Models & Engines Used

### OCR Engine
- **Tesseract OCR Engine**
  - Version: 5.x
  - Language: English (eng)
  - PSM (Page Segmentation Mode): 6 (Uniform block of text)
  - OEM (OCR Engine Mode): 3 (Default, based on what is available)

### AI Model
- **OpenAI GPT-4o-mini**
  - Used for: Text enhancement, field extraction, data normalization
  - Temperature: 0 (deterministic output)
  - Max Tokens: 196-400 depending on task

### Image Processing Pipeline
1. **Grayscale Conversion** - Convert BGR to grayscale
2. **Denoising** - Fast Non-Local Means Denoising (h=15)
3. **Adaptive Thresholding** - Gaussian adaptive threshold (block size: 31, C: 15)
4. **Morphological Operations** - Dilation with 2x2 kernel (1 iteration)

## 📋 Features

### Core Functionality
- **Document Upload** - Support for PDF, JPG, PNG, BMP, TIFF formats
- **OCR Processing** - Automatic text extraction from images and PDFs
- **AI Enhancement** - LLM-powered text cleaning and normalization
- **Field Extraction** - Automatic extraction of structured fields:
  - Name
  - Date of Birth
  - Address
  - City
  - State
  - Phone
  - Email
  - Gender
  - Date

### Data Management
- **Database Storage** - All extracted data stored in SQLite
- **Document Browser** - Self-service document viewing interface
- **Search Functionality** - Search by name, email, or phone
- **Admin Panel** - Full database management through Django admin

### Export Options
- **JSON Download** - Structured JSON format with all fields
- **TXT Download** - Human-readable text report
- **Direct Browser Access** - View documents from table interface

## 🏗️ Project Structure

### Main Application Files

**Backend (Django REST Framework)**
```
myproject/myapp/
├── models.py           # Document & ChatMessage database models
├── views.py            # 8 API endpoint functions
├── urls.py             # RESTful URL routing
├── admin.py            # Admin panel customization
├── ocr_utils.py        # Tesseract OCR processing (from ocr.ipynb)
└── llm_utils.py        # OpenAI GPT integration (from LLM.ipynb)
```

**Frontend**
```
myproject/templates/
└── index.html          # Complete web interface (upload, chat, browser)
```

**Database & Media**
```
myproject/
├── db.sqlite3          # SQLite database with all extracted data
└── media/uploads/      # Uploaded PDF/image files
```

**Testing & Development Notebooks**
```
├── ocr.ipynb           # OCR testing (integrated into ocr_utils.py)
├── LLM.ipynb           # LLM testing (integrated into llm_utils.py)
└── LLM_google.ipynb    # Alternative LLM experiments
```

## 🗄️ Database Schema

### Document Model
Stores uploaded documents and all extracted information.

| Field | Type | Description |
|-------|------|-------------|
| id | Primary Key | Auto-increment unique identifier |
| uploaded_file | FileField | Path to uploaded PDF/image |
| file_type | CharField | 'image' or 'pdf' |
| raw_ocr_text | TextField | Raw text from Tesseract OCR |
| enhanced_text | TextField | AI-cleaned and normalized text |
| name | CharField | Extracted person name |
| dob | CharField | Date of birth |
| address | CharField | Complete address |
| city | CharField | City name |
| state | CharField | State/province |
| phone | CharField | Phone number |
| email | EmailField | Email address |
| gender | CharField | Gender |
| date | CharField | Document date |

### ChatMessage Model
Stores chat conversations for each document.

| Field | Type | Description |
|-------|------|-------------|
| id | Primary Key | Auto-increment unique identifier |
| document | ForeignKey | Link to Document model |
| question | TextField | User's question |
| answer | TextField | AI-generated answer |
| created_at | DateTimeField | Timestamp of conversation |

## 🔌 API Endpoints

The Django REST Framework provides the following RESTful endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main web interface with upload, chat & browser |
| POST | `/api/upload/` | Upload and process document (OCR + AI) |
| GET | `/api/documents/` | List all documents with search functionality |
| GET | `/api/documents/<id>/` | Get specific document details |
| POST | `/api/documents/<id>/chat/` | Ask questions about document content |
| GET | `/api/documents/<id>/chat/history/` | Get all chat messages for document |
| GET | `/api/documents/<id>/download/json/` | Download document data as JSON |
| GET | `/api/documents/<id>/download/txt/` | Download document data as TXT |
| GET | `/admin/` | Django admin panel (requires login) |

### Example API Usage

**Upload Document**
```bash
curl -X POST http://127.0.0.1:8000/api/upload/ \
  -F "file=@form.pdf"
```

**Search Documents**
```bash
curl "http://127.0.0.1:8000/api/documents/?search=john"
```

**Chat with Document**
```bash
curl -X POST http://127.0.0.1:8000/api/documents/1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the person'\''s name?"}'
```

## ⚙️ Configuration Notes

### Required External Dependencies
These tools must be installed separately on the system:

1. **Tesseract OCR Engine**
   - Download from: https://github.com/tesseract-ocr/tesseract
   - Windows installer available
   - After installation, update path in `myapp/ocr_utils.py`:
     ```python
     TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
     ```

2. **Poppler (for PDF processing)**
   - Download from: https://github.com/oschwartz10612/poppler-windows/releases
   - Extract and update path in `myapp/ocr_utils.py`:
     ```python
     POPPLER_PATH = r"C:\path\to\poppler\Library\bin"
     ```

3. **OpenAI API Key**
   - Get from: https://platform.openai.com/api-keys
   - Update in `myapp/llm_utils.py`:
     ```python
     OPENAI_API_KEY = "your-openai-api-key-here"
     ```

### Django Configuration

**Media Files** (`settings.py`)
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/uploads/'
```

**Templates** (`settings.py`)
```python
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],
        ...
    }
]
```

**Installed Apps** (`settings.py`)
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST Framework
    'myapp',           # Our application
]
```

## 🔍 Field Extraction Logic

### LLM-Based Extraction
The system uses OpenAI GPT-4o-mini to extract structured fields from cleaned OCR text:
1. **Prompt Engineering** - Specific field schema provided to LLM
2. **JSON Response** - LLM returns structured JSON
3. **Validation** - Format enforcement (dates, phones, emails)
4. **Fallback** - Regex-based heuristic extraction if LLM fails

### Field Formatting Rules
- **Names**: Letters, spaces, periods, hyphens, apostrophes only
- **Dates**: Format validation for DOB and date fields
- **Phone**: Digits and + symbols only
- **Email**: Standard email regex validation
- **ZIP**: Digits only

## 🖥️ Frontend Features

### Upload Interface
- Drag-and-drop file upload
- File type validation
- Progress indicator
- Success/error messaging

### Document Browser
- Table view of all documents
- Search by name, email, or phone
- View button for full document details
- Download buttons for JSON and TXT reports
- Responsive design

### Data Display
- Grid layout for extracted fields
- Enhanced text preview
- Clean, modern UI with gradient colors

## 🔐 Security Features

- CSRF protection on all POST requests
- File type validation
- Media file isolation
- Admin authentication required
- API endpoint protection

## 📊 Admin Panel Features

### Document Management
- List view with key fields (ID, name, email, phone)
- Search functionality
- Filter by file type and gender
- Collapsible OCR text sections
- Field grouping (File Info, Extracted Fields, OCR Processing)

### Chat Message Management
- View all chat interactions
- Search by questions/answers
- Filter by date
- Readonly fields for data integrity

## 🎨 UI Components

### Color Scheme
- Primary Gradient: `#667eea` to `#764ba2`
- Success: `#48bb78`
- Info: `#4299e1`
- Gray: `#718096`

### Design Features
- Card-based layout
- Responsive grid system
- Smooth animations
- Modern button styles
- Clean typography (Segoe UI font family)

## 📝 Use Cases

1. **Form Digitization** - Convert paper forms to digital structured data automatically
2. **Data Entry Automation** - Eliminate manual typing from scanned documents
3. **Document Management** - Searchable database of all processed forms
4. **Intelligent Search** - Find documents by name, email, or phone instantly
5. **Document Intelligence** - Chat interface to query extracted information
6. **Data Export** - Download structured data in JSON or human-readable TXT
7. **Compliance & Audit** - Track all documents with timestamps in admin panel
8. **Self-Service Portal** - Users can upload, search, and download their data

## 🔄 Processing Workflow

```
1. User uploads PDF/Image of filled form
         ↓
2. System validates file type and saves to media/uploads/
         ↓
3. OCR Engine (Tesseract) extracts raw text
   • Image preprocessing (grayscale, denoise, threshold)
   • Text extraction with PSM mode 6
         ↓
4. AI Enhancement (GPT-4o-mini) processes text
   • Cleans and normalizes extracted text
   • Extracts structured fields using LLM
   • Validates and formats data
         ↓
5. Database Storage (SQLite)
   • Saves all fields to Document model
   • Stores raw OCR and enhanced text
         ↓
6. User Interface displays results
   • Shows extracted fields in grid
   • Enables chat with document
   • Provides download options
         ↓
7. Optional: User asks questions via chat
   • LLM answers based on document context
   • Chat history saved to database
```

## 🎨 Frontend Features

### Upload Interface
- **Drag-and-drop** file upload area
- **File validation** (PDF, JPG, PNG, BMP, TIFF)
- **Visual feedback** with icons and colors
- **Progress indicators** during processing
- **Success/error messages** with clear feedback

### Extracted Data Display
- **Grid layout** showing all extracted fields
- **Enhanced text preview** in formatted box
- **Download buttons** for JSON and TXT exports
- **View button** to see full document details

### Chat Interface
- **Question input** with Enter key support
- **Chat history** showing all Q&A pairs
- **Timestamp** for each conversation
- **Auto-scroll** to latest message
- **Loading indicator** while AI processes

### Document Browser
- **Table view** of all documents with key fields
- **Search bar** to filter by name, email, phone
- **Reset button** to clear search
- **Action buttons** for each document:
  - View: Open document details with chat
  - JSON: Download structured data
  - TXT: Download readable report

## 📊 Admin Panel Features

### Access
- URL: `http://127.0.0.1:8000/admin/`
- Login: admin credentials created via `createsuperuser`

### Document Management
- **List View**: ID, name, email, phone, file type
- **Search**: By name, email, phone, address
- **Filters**: File type (PDF/Image), gender
- **Field Groups**: 
  - File Information (uploaded file, type)
  - Extracted Fields (all 9 fields)
  - OCR Processing (raw text, enhanced text)
- **Collapsible sections** for large text fields

### Chat Message Management
- **View conversations** linked to documents
- **Search** questions and answers
- **Filter by date** range
- **Readonly fields** to preserve data integrity

## 🔐 Security Features

- **CSRF Protection**: All POST requests require CSRF token
- **File Type Validation**: Only allowed formats accepted
- **Media File Isolation**: Uploads stored in dedicated directory
- **Admin Authentication**: Password-protected admin panel
- **Input Sanitization**: Escaping HTML in chat display
- **API Endpoint Protection**: Django REST Framework security

## 📚 Libraries Used

### Backend Framework
- **Django 5.2.10** - Web framework
- **Django REST Framework 3.16.1** - RESTful API development

### OCR & Image Processing
- **Pytesseract** - Python wrapper for Tesseract OCR engine
- **OpenCV (opencv-python)** - Image preprocessing and manipulation
- **Pillow** - Image handling and conversion
- **pdf2image** - PDF to image conversion
- **NumPy** - Numerical operations for image processing

### AI/LLM Integration
- **OpenAI 2.15.0** - GPT-4o-mini for text enhancement and field extraction

### Database
- **SQLite** - Default Django database (for development)

## 🤖 Models & Engines Used

### OCR Engine: Tesseract 5.x
- **Language**: English (eng)
- **PSM (Page Segmentation Mode)**: 6 - Uniform block of text
- **OEM (OCR Engine Mode)**: 3 - Default, based on what is available
- **Preprocessing**: Grayscale → Denoising → Thresholding → Dilation

### AI Model: OpenAI GPT-4o-mini
- **Purpose**: Text enhancement, field extraction, data normalization
- **Temperature**: 0 (deterministic, consistent output)
- **Max Tokens**: 196-400 depending on task
- **Approach**: Prompt engineering with structured JSON output

### Image Processing Pipeline
1. **Grayscale Conversion** - Convert BGR to grayscale for better OCR
2. **Denoising** - Fast Non-Local Means Denoising (h=15)
3. **Adaptive Thresholding** - Gaussian adaptive threshold (block size: 31, C: 15)
4. **Morphological Operations** - Dilation with 2x2 kernel (1 iteration)

## ⚙️ Configuration Notes

### Media Files
- Upload directory: `media/uploads/`
- Configured in `settings.py`: `MEDIA_ROOT` and `MEDIA_URL`

### Templates
- Template directory: `templates/`
- Configured in `settings.py`: `DIRS = [BASE_DIR / 'templates']`

### REST Framework
- No authentication required (development mode)
- JSON responses by default
- Function-based API views

## 🎓 Technical Highlights

- **No Forms.py** - Direct model interaction in views
- **Function-Based Views** - Simple, straightforward API endpoints
- **Clean URL Routing** - RESTful endpoint structure
- **Modular Design** - Separate utilities for OCR and LLM
- **Error Handling** - Comprehensive try-catch blocks
- **Code Reusability** - Shared functions for common tasks

## 📌 Important Notes

- Tesseract OCR engine must be installed separately
- Poppler is required for PDF processing
- Valid OpenAI API key needed for LLM features
- Paths must be updated based on local installation
- Development server not suitable for production

## 🚀 Quick Start

1. Update configuration paths in `ocr_utils.py`
2. Add OpenAI API key in `llm_utils.py`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Start server: `python manage.py runserver`
6. Access at: `http://127.0.0.1:8000/`

## 👤 Admin Access

- URL: `http://127.0.0.1:8000/admin/`
- Default username: `admin`
- Manage documents, view chat history, search data

---

**Built with Django REST Framework for HCL Hackathon 2026**
