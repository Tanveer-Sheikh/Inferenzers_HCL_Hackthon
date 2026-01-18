# Form OCR & Document Management System

A Django REST Framework application for extracting data from filled forms using OCR and AI-powered text enhancement.

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

```
myproject/
├── myapp/
│   ├── models.py           # Document & ChatMessage models
│   ├── views.py            # API endpoints (function-based views)
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin panel configuration
│   ├── ocr_utils.py        # Tesseract OCR processing
│   └── llm_utils.py        # OpenAI GPT integration
├── templates/
│   └── index.html          # Frontend interface
├── media/uploads/          # Uploaded files storage
├── db.sqlite3             # SQLite database
└── manage.py              # Django management script
```

## 🗄️ Database Schema

### Document Model
```
- id (Primary Key)
- uploaded_file (FileField)
- file_type (CharField: 'image' or 'pdf')
- raw_ocr_text (TextField)
- enhanced_text (TextField)
- name (CharField)
- dob (CharField)
- address (CharField)
- city (CharField)
- state (CharField)
- phone (CharField)
- email (EmailField)
- gender (CharField)
- date (CharField)
```

### ChatMessage Model
```
- id (Primary Key)
- document (ForeignKey to Document)
- question (TextField)
- answer (TextField)
- created_at (DateTimeField)
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main web interface |
| POST | `/api/upload/` | Upload and process document |
| GET | `/api/documents/` | List/search all documents |
| GET | `/api/documents/<id>/` | Get specific document details |
| POST | `/api/documents/<id>/chat/` | Ask questions about document |
| GET | `/api/documents/<id>/chat/history/` | Get chat history |
| GET | `/api/documents/<id>/download/json/` | Download JSON report |
| GET | `/api/documents/<id>/download/txt/` | Download TXT report |
| GET | `/admin/` | Admin panel |

## 🎯 OCR Configuration

### Tesseract Path Configuration
Located in `myapp/ocr_utils.py`:
```python
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### Poppler Path Configuration (for PDF processing)
Located in `myapp/ocr_utils.py`:
```python
POPPLER_PATH = r"C:\Users\tsheikh\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"
```

### OpenAI API Key Configuration
Located in `myapp/llm_utils.py`:
```python
OPENAI_API_KEY = "your-api-key-here"
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

1. **Form Processing** - Digitize paper forms automatically
2. **Data Entry Automation** - Reduce manual data entry
3. **Document Archive** - Searchable database of processed forms
4. **Compliance** - Track and store form data with timestamps
5. **Self-Service Portal** - Users can search and download their data

## 🔄 Processing Workflow

1. **Upload** → File validation
2. **OCR** → Text extraction (Tesseract)
3. **Enhancement** → AI cleaning (GPT-4o-mini)
4. **Extraction** → Structured field parsing
5. **Storage** → Save to database
6. **Display** → Show results to user
7. **Export** → Download as JSON/TXT

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
