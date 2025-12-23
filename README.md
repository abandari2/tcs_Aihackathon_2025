# Ti Tans Bank - KYC Portal System

A comprehensive, production-ready Know Your Customer (KYC) verification system with AI-powered document validation, progressive onboarding, and administrative management.

## 🎯 System Overview

Ti Tans Bank KYC Portal is a modern banking application that streamlines customer onboarding through a two-stage progressive KYC process:

1. **Registration**: Customers provide personal, employment, and address information
2. **KYC Verification**: Post-login identity verification with document upload and AI validation

### Key Features

- ✅ **Progressive KYC Flow**: Two-stage onboarding (Registration → KYC Portal)
- ✅ **AI-Powered Validation**: Face detection, liveness detection, image quality analysis
- ✅ **OCR Document Processing**: Automated text extraction from Aadhar, PAN, Passport
- ✅ **Admin Dashboard**: Comprehensive customer management and KYC review
- ✅ **Real-time Status Tracking**: 5-state application status system
- ✅ **Audit & Reporting**: Complete audit trail with Excel/CSV export
- ✅ **Modern UI**: Glassmorphism design with page-specific color schemes

## 📋 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Tesseract OCR (optional, for real OCR)

### Installation

1. **Clone/Download Project**
   ```bash
   cd AIDEMO
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .virtualenv
   .virtualenv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Database**
   ```bash
   # Create database
   psql -U postgres -c "CREATE DATABASE horizon_bank_kyc;"
   
   # Initialize schema
   python database_init.py
   ```

5. **Configure Environment**
   Create `.env` file:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=horizon_bank_kyc
   DB_USER=postgres
   DB_PASSWORD=test
   ```

6. **Run Application**
   ```bash
   streamlit run app_main.py
   ```

**Access**: `http://localhost:8501`

📖 **For detailed setup instructions, see [SETUP.md](SETUP.md)**

## 📁 Project Structure

### Active Production Files (14 Essential Files)

**Python Application Modules (11 files)**:
```
AIDEMO/
├── app_main.py                 # Main Streamlit application (ACTIVE)
├── database_config.py          # PostgreSQL connection management (ACTIVE)
├── database_init.py            # Database initialization script (ACTIVE)
├── db_helpers.py              # Database helper functions (ACTIVE)
├── styling.py                 # UI styling and CSS (ACTIVE)
├── ocr_engine.py              # OCR text extraction (ACTIVE)
├── kyc_validator.py           # Basic KYC validation (ACTIVE)
├── ai_kyc_validator.py        # Advanced AI validation (ACTIVE)
├── admin_dashboard.py         # Admin panel (ACTIVE)
├── audit_reports.py           # Audit reporting (ACTIVE)
└── notifications.py           # Toast notifications (ACTIVE)
```

**Database & Configuration (3 files)**:
```
├── database_schema.sql         # Database schema definition (ACTIVE)
├── requirements.txt           # Python dependencies (ACTIVE)
└── .env                       # Environment variables (ACTIVE)
```

**Total: 11 Python modules + 1 SQL schema + 2 config files = 14 files**

### Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Complete system architecture, data flow, and technical deep dive
- **[SETUP.md](SETUP.md)**: Detailed installation and integration guide
- **[USER_MANUAL.md](USER_MANUAL.md)**: End-user guide
- **[ADMIN_GUIDE.md](ADMIN_GUIDE.md)**: Administrator guide

## 🔧 Core Components

### 1. Application Entry Point
- **File**: `app_main.py`
- **Purpose**: Main Streamlit application with routing, session management, and UI
- **Key Views**: Landing, Login, Register, KYC Portal, Dashboard, Status Check, Admin

### 2. Database Layer
- **Files**: `database_config.py`, `database_schema.sql`, `db_helpers.py`
- **Purpose**: PostgreSQL integration with connection pooling, schema management, and CRUD operations
- **Connection**: Threaded connection pool (1-10 connections)

### 3. KYC Validation Engine
- **Files**: `kyc_validator.py`, `ai_kyc_validator.py`, `ocr_engine.py`
- **Purpose**: Multi-stage validation with OCR, face detection, liveness, and quality analysis
- **Scoring**: Weighted scoring system (Photo 30-40%, Address 15-20%, Documents 50-30%)

### 4. Admin & Audit
- **Files**: `admin_dashboard.py`, `audit_reports.py`
- **Purpose**: Customer management, KYC review, audit logging, and report generation

## 🎨 UI Design

- **Framework**: Streamlit with custom CSS
- **Design**: Glassmorphism with Deep Navy (#0f172a), Slate (#1e293b), Cyan (#06b6d4)
- **Page-Specific Backgrounds**: Different color schemes for Landing, Login, Admin, Status pages
- **Responsive**: Works on desktop and tablet

## 🔐 Security Features

- Password hashing (SHA-256)
- SQL injection prevention (parameterized queries)
- Session-based authentication
- Audit logging for all actions
- File upload validation

## 📊 KYC Validation Process

### Validation Stages

1. **Photo Validation**
   - Face detection (OpenCV Haar Cascade)
   - Liveness detection (sharpness, color depth, resolution)
   - Image quality analysis (brightness, contrast, noise)

2. **Address Validation**
   - Completeness check
   - OCR cross-reference
   - Fuzzy matching with document data

3. **Document Validation**
   - OCR text extraction
   - Document type detection
   - Verification status check

### Scoring Formula

**Basic Validation** (`kyc_validator.py`):
```
overall_score = (photo_score × 0.3) + (address_score × 0.2) + (document_score × 0.5)
```

**Advanced Validation** (`ai_kyc_validator.py`):
```
overall_score = (photo_score × 0.40) + (address_score × 0.15) + 
                (identity_doc_score × 0.30) + (photo_doc_score × 0.15)
```

**Approval Threshold**: Score ≥ 50-70% (configurable)

## 🗄️ Database Schema

### Core Tables

- **users**: Authentication and user accounts
- **customers**: Customer profile with progressive KYC fields
- **kyc_applications**: KYC application records with validation scores
- **documents**: Uploaded documents with OCR data
- **audit_logs**: System audit trail
- **notifications**: User notifications

**See [ARCHITECTURE.md](ARCHITECTURE.md) for complete schema details**

## 📦 Dependencies

| Library | Purpose |
|---------|---------|
| `streamlit` | Web framework |
| `psycopg2-binary` | PostgreSQL adapter |
| `Pillow` | Image processing |
| `opencv-python` | Face detection, image analysis |
| `pytesseract` | OCR text extraction |
| `pandas` | Data manipulation, Excel export |
| `openpyxl` | Excel file generation |

**Full list**: See `requirements.txt`

## 🚀 Deployment

### Development
```bash
streamlit run app_main.py
```

### Production Considerations
- Use environment variables for sensitive data
- Enable PostgreSQL SSL
- Implement proper logging
- Set up monitoring
- Use reverse proxy (nginx)
- Enable HTTPS

## 📝 Project Audit Status

### Active Files (Production)
✅ All files in "Active Production Files" section above

### Legacy Files (Safe to Archive)
- `main.py` (replaced by `app_main.py`)
- `Sample.py` (UI reference, merged)
- `migrate_*.py` and `migrate_*.sql` (one-time migrations)
- `verify_syntax.py`, `generate_test_data.py` (utilities)

**See [ARCHITECTURE.md](ARCHITECTURE.md) for complete file manifest**

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check PostgreSQL is running
   - Verify credentials in `.env`
   - Ensure database exists

2. **Tesseract Not Found**
   - Install Tesseract OCR
   - System works without it (uses mock OCR)

3. **Port Already in Use**
   - Use different port: `--server.port 8502`
   - Kill existing process

**See [SETUP.md](SETUP.md) for detailed troubleshooting**

## 📚 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: System architecture, data flow, validation logic
- **[SETUP.md](SETUP.md)**: Installation, PyCharm, DBeaver setup
- **[USER_MANUAL.md](USER_MANUAL.md)**: User workflows and features
- **[ADMIN_GUIDE.md](ADMIN_GUIDE.md)**: Admin operations and management

## 🔄 Version History

- **v1.0**: Initial release with progressive KYC flow
- **v1.1**: Added AI-powered validation
- **v1.2**: Enhanced admin dashboard and audit reports
- **v1.3**: Modern UI redesign with glassmorphism

## 📄 License

Proprietary - Ti Tans Bank

## 👥 Support

For technical support or questions:
1. Review documentation files
2. Check troubleshooting section
3. Review application logs
4. Check database audit logs

---

**Built with ❤️ for Ti Tans Bank**
