# 📖 Detailed Code Explanation - Line by Line

## Table of Contents
1. [Main Application (app_main.py)](#main-application-app_mainpy)
2. [AI KYC Validator (ai_kyc_validator.py)](#ai-kyc-validator-ai_kyc_validatorpy)
3. [OCR Engine (ocr_engine.py)](#ocr-engine-ocr_enginepy)
4. [Database Helpers (db_helpers.py)](#database-helpers-db_helperspy)
5. [AI Helper (ai_helper.py)](#ai-helper-ai_helperpy)

---

## Main Application (app_main.py)

### Lines 1-50: Imports and Setup

```python
import streamlit as st
import os
import shutil
from datetime import date, datetime
from pathlib import Path
import uuid
import json
import ai_helper
import cv2
import time
from collections import deque
from streamlit_webrtc import webrtc_streamer, WebRtcMode
```

**Explanation**:
- `streamlit`: Web framework for building the UI
- `os`, `shutil`: File system operations
- `datetime`: Date/time handling
- `pathlib.Path`: Modern path handling
- `uuid`: Unique ID generation
- `json`: JSON data handling
- `ai_helper`: Custom AI helper functions
- `cv2` (OpenCV): Computer vision for image processing
- `streamlit_webrtc`: WebRTC for camera access (future feature)

```python
from database_config import db
from db_helpers import (
    create_user, authenticate_user, create_customer, create_kyc_application,
    save_document, get_customer_kyc_status, get_customer_documents,
    get_customer_by_user_id, create_notification, log_audit,
    update_customer_kyc, get_customer_by_email_or_phone, check_application_status
)
```

**Explanation**:
- Imports database connection object
- Imports all database helper functions for user/customer/KYC operations

```python
from styling import get_banking_css
from ocr_engine import ocr_engine
from notifications import notifications
from admin_dashboard import AdminDashboard
from audit_reports import AuditReports
from kyc_validator import perform_kyc_validation
from ai_kyc_validator import perform_advanced_kyc_validation
```

**Explanation**:
- `get_banking_css()`: Returns CSS styling
- `ocr_engine`: OCR processing instance
- `notifications`: Toast notification system
- `AdminDashboard`: Admin panel class
- `AuditReports`: Audit report generation
- `perform_kyc_validation()`: Basic validation function
- `perform_advanced_kyc_validation()`: AI-powered validation function

### Lines 42-48: Page Configuration

```python
st.set_page_config(
    page_title="Ti Tans Bank | Professional Banking", 
    page_icon="🏦", 
    layout="wide",
    initial_sidebar_state="expanded"
)
```

**Explanation**:
- Sets browser tab title
- Sets favicon (bank emoji)
- Uses wide layout (more horizontal space)
- Sidebar starts expanded

### Lines 50-52: Document Storage Setup

```python
DOCUMENTS_DIR = Path("submitted_data/documents")
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
```

**Explanation**:
- Creates directory path for uploaded documents
- `mkdir(parents=True, exist_ok=True)`: Creates directory and parent directories if they don't exist

### Lines 54-61: Session State Initialization

```python
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.customer = None
    st.session_state.view = "Landing"
    st.session_state.first_login = False
    st.session_state.admin_mode = False
```

**Explanation**:
- `authenticated`: Whether user is logged in
- `user`: Current user data dictionary
- `customer`: Current customer profile data
- `view`: Current page/view name
- `first_login`: Flag for first-time login (triggers KYC portal)
- `admin_mode`: Whether admin mode is enabled

### Lines 63-64: Apply CSS Styling

```python
st.markdown(f"<style>{get_banking_css()}</style>", unsafe_allow_html=True)
```

**Explanation**:
- Injects custom CSS into the page
- `unsafe_allow_html=True`: Allows HTML/CSS injection (required for styling)

### Lines 66-85: Page Background Function

```python
def set_page_background(view_name):
    """Set page-specific background styling"""
    page_map = {
        "Landing": "landing",
        "Login": "login",
        "Register": "register",
        "Admin": "admin",
        "AdminLogin": "admin",
        "CustomerManagement": "admin",
        "StatusCheck": "status",
        "Dashboard": "dashboard",
        "KYC Portal": "kyc"
    }
    page_class = page_map.get(view_name, "landing")
    st.markdown(f"""
        <script>
            document.querySelector('.stApp').setAttribute('data-page', '{page_class}');
        </script>
    """, unsafe_allow_html=True)
```

**Explanation**:
- Maps view names to CSS classes
- Sets `data-page` attribute on main app element
- CSS uses this attribute to apply different backgrounds per page

### Lines 87-96: Database Initialization

```python
@st.cache_resource
def init_database():
    """Initialize database connection"""
    try:
        db.create_connection_pool()
        return db.test_connection()
    except Exception as e:
        return False

db_connected = init_database()
```

**Explanation**:
- `@st.cache_resource`: Caches the database connection (runs once)
- Creates connection pool
- Tests connection
- Stores result in `db_connected` variable

### Lines 99-102: Navigation Helper

```python
def change_view(v):
    st.session_state.view = v
    st.rerun()
```

**Explanation**:
- Changes current view/page
- `st.rerun()`: Refreshes the page to show new view

### Lines 104-118: Webcam Helper

```python
def handle_webcam_capture():
    """Handle webcam capture with fallback"""
    try:
        camera_photo = st.camera_input(
            "Take a live photo*",
            help="Position your face in the frame...",
            key="camera_capture"
        )
        return camera_photo
    except Exception as e:
        st.warning(f"⚠️ Camera not available: {str(e)}")
        st.info("💡 Please use the 'Upload Photo' option instead.")
        return None
```

**Explanation**:
- Tries to use Streamlit's camera input
- If camera fails, shows warning and suggests file upload
- Returns photo file object or None

### Lines 120-327: Application Details Display Helper

```python
def _display_application_details(result):
    """Helper function to display application details"""
    # Shows application ID, customer name, email, phone
    # Shows KYC status, validation score, application status
    # Shows document verification status for each document
    # Groups documents by type and shows latest status
```

**Key Logic**:
1. Extracts KYC score from notes field
2. Queries documents for the application
3. Groups documents by type (identity_proof, photo, etc.)
4. Prioritizes rejected documents (shows them first)
5. Displays verification status with color coding (✅ verified, ❌ rejected, ⏳ pending)

---

## AI KYC Validator (ai_kyc_validator.py)

### Lines 14-90: Face Detection Function

```python
def detect_face_in_image(image_path: str) -> Dict[str, Any]:
    """AI Feature: Detect face in image using advanced algorithms"""
    try:
        from PIL import Image
        import cv2
        
        # Load image
        img = Image.open(image_path)
        img_array = np.array(img)
```

**Explanation**:
- Opens image using PIL
- Converts to NumPy array for OpenCV processing

```python
        # Convert to RGB if needed
        if len(img_array.shape) == 3 and img_array.shape[2] == 4:
            img_array = img_array[:, :, :3]
```

**Explanation**:
- Removes alpha channel if present (RGBA → RGB)
- OpenCV expects RGB format

```python
        # Convert PIL to OpenCV format
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Load face cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
```

**Explanation**:
- Converts RGB to BGR (OpenCV uses BGR)
- Loads pre-trained Haar Cascade classifier for face detection
- Converts to grayscale (face detection works on grayscale)
- `detectMultiScale()`: Detects faces with scale factor 1.1, minimum neighbors 4

```python
        if len(faces) > 0:
            # Get largest face
            largest_face = max(faces, key=lambda x: x[2] * x[3])
            x, y, w, h = largest_face
            
            # Calculate face position and size
            face_area = w * h
            image_area = img_array.shape[0] * img_array.shape[1]
            face_ratio = face_area / image_area
```

**Explanation**:
- If faces detected, selects largest face (by area)
- `x, y, w, h`: Face bounding box coordinates
- Calculates face size as percentage of image

```python
            # Check if face is centered
            center_x = img_array.shape[1] / 2
            center_y = img_array.shape[0] / 2
            face_center_x = x + w / 2
            face_center_y = y + h / 2
            offset_x = abs(face_center_x - center_x) / img_array.shape[1]
            offset_y = abs(face_center_y - center_y) / img_array.shape[0]
```

**Explanation**:
- Calculates image center
- Calculates face center
- Calculates offset as percentage (0.0 = centered, 1.0 = at edge)
- If offset < 0.3, face is considered centered

```python
            return {
                'face_detected': True,
                'confidence': 95.0,
                'face_count': len(faces),
                'face_ratio': round(face_ratio * 100, 2),
                'is_centered': offset_x < 0.3 and offset_y < 0.3,
                'face_size': {'width': int(w), 'height': int(h)},
                'face_position': {'x': int(x), 'y': int(y)},
                'issues': []
            }
```

**Explanation**:
- Returns comprehensive face detection results
- Includes confidence, count, size, position, centering status

### Lines 142-227: Liveness Detection Function

```python
def detect_liveness(image_path: str) -> Dict[str, Any]:
    """AI Feature: Detect if photo is live (not a printed photo or screen)"""
    liveness_score = 100
    issues = []
```

**Explanation**:
- Starts with perfect score (100)
- Deducts points for issues

```python
    # Check 1: Image sharpness (live photos are usually sharper)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    if laplacian_var < 100:
        issues.append('Image appears blurry (possible printed photo)')
        liveness_score -= 20
    elif laplacian_var > 500:
        liveness_score += 10  # Very sharp = likely live
```

**Explanation**:
- **Laplacian Operator**: Detects edges (sharpness indicator)
- **Variance**: Higher variance = sharper image
- < 100: Blurry (printed photo)
- > 500: Very sharp (likely live)

```python
    # Check 2: Color depth and quality
    color_variance = np.var(img_array)
    if color_variance < 500:
        issues.append('Low color variance (possible printed photo)')
        liveness_score -= 15
```

**Explanation**:
- **Color Variance**: Measures color richness
- Printed photos often have lower color variance
- Live photos have richer colors

```python
    # Check 3: Image resolution
    total_pixels = height * width
    if total_pixels < 50000:  # Less than ~224x224
        issues.append('Low resolution (possible screenshot)')
        liveness_score -= 10
```

**Explanation**:
- Screenshots often have lower resolution
- Live camera captures usually higher resolution

```python
    # Check 4: EXIF data
    exif = img._getexif()
    if exif:
        liveness_score += 5
```

**Explanation**:
- EXIF metadata present = likely from camera
- Printed photos/screenshots often lack EXIF

```python
    # Check 5: Compression artifacts
    if file_size < 10000 and total_pixels > 100000:
        issues.append('High compression ratio (possible printed photo)')
        liveness_score -= 10
```

**Explanation**:
- High compression = small file size for large image
- Indicates possible printed photo (re-compressed)

### Lines 229-326: Face Comparison Function

```python
def compare_faces(image1_path: str, image2_path: str) -> Dict[str, Any]:
    """AI Feature: Compare faces between two images"""
    # Load both images
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)
```

**Explanation**:
- Loads customer photo and ID document photo

```python
    # Detect faces in both images
    faces1 = face_cascade.detectMultiScale(gray1, 1.1, 4)
    faces2 = face_cascade.detectMultiScale(gray2, 1.1, 4)
```

**Explanation**:
- Detects faces in both images separately

```python
    # Get largest face from each image
    face1 = max(faces1, key=lambda x: x[2] * x[3])
    face2 = max(faces2, key=lambda x: x[2] * x[3])
    
    # Extract face regions
    x1, y1, w1, h1 = face1
    x2, y2, w2, h2 = face2
    face_roi1 = gray1[y1:y1+h1, x1:x1+w1]
    face_roi2 = gray2[y2:y2+h2, x2:x2+w2]
```

**Explanation**:
- Selects largest face from each image
- Extracts face region (ROI = Region of Interest)

```python
    # Resize faces to same size for comparison
    face_roi1 = cv2.resize(face_roi1, (100, 100))
    face_roi2 = cv2.resize(face_roi2, (100, 100))
```

**Explanation**:
- Normalizes face sizes for comparison
- Both faces now 100x100 pixels

```python
    # Calculate similarity using template matching
    result = cv2.matchTemplate(face_roi1, face_roi2, cv2.TM_CCOEFF_NORMED)
    similarity = float(result[0][0])
```

**Explanation**:
- **Template Matching**: Compares face patterns
- `TM_CCOEFF_NORMED`: Normalized correlation coefficient
- Returns value between -1 and 1 (higher = more similar)

```python
    # Calculate histogram correlation
    hist1 = cv2.calcHist([face_roi1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([face_roi2], [0], None, [256], [0, 256])
    hist_corr = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
```

**Explanation**:
- **Histogram**: Distribution of pixel intensities
- Compares histograms to measure structural similarity
- Returns correlation value (0-1)

```python
    # Combined similarity score
    combined_similarity = (similarity * 0.7) + (hist_corr * 0.3)
    
    # Threshold for match: 0.6 (60% similarity)
    faces_match = combined_similarity >= 0.6
```

**Explanation**:
- Combines template matching (70%) and histogram (30%)
- If combined score >= 60%, faces match

### Lines 375-493: Image Quality Analysis

```python
def analyze_image_quality(image_path: str) -> Dict[str, Any]:
    """AI Feature: Advanced image quality analysis"""
    quality_score = 100
    issues = []
    metrics = {}
```

**Explanation**:
- Starts with perfect score
- Tracks issues and metrics

```python
    # 1. Brightness analysis
    brightness = np.mean(gray)
    metrics['brightness'] = round(brightness, 2)
```

**Explanation**:
- **Brightness**: Mean pixel value (0-255)
- 0 = black, 255 = white
- Optimal: 80-180

```python
    # Enhanced blur detection using Laplacian variance
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    metrics['sharpness'] = round(laplacian_var, 2)
    
    if laplacian_var < 100:
        quality_score -= 30
        issues.append(f'Image is blurry (sharpness: {round(laplacian_var, 2)})')
```

**Explanation**:
- **Laplacian Variance**: Sharpness measure
- < 100: Very blurry
- 100-200: Slightly blurry
- > 200: Sharp

```python
    # Edge detection
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / (gray.shape[0] * gray.shape[1])
```

**Explanation**:
- **Canny Edge Detection**: Finds edges in image
- **Edge Density**: Percentage of pixels that are edges
- Low density = blurry or lacks detail

```python
    # 2. Contrast analysis
    contrast = np.std(gray)
    metrics['contrast'] = round(contrast, 2)
    if contrast < 20:
        issues.append('Low contrast')
        quality_score -= 15
```

**Explanation**:
- **Contrast**: Standard deviation of pixel values
- Low contrast = image looks flat
- High contrast = clear distinction between light/dark

```python
    # 3. Noise analysis
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    noise_level = np.var(laplacian)
    if noise_level > 1000:
        issues.append('High noise level')
        quality_score -= 10
```

**Explanation**:
- **Noise**: Random variations in pixel values
- High noise = grainy image
- Measured as variance of Laplacian

### Lines 831-1187: Advanced KYC Validation

```python
def perform_advanced_kyc_validation(application_id, customer_id) -> Dict[str, Any]:
    """Perform advanced AI-powered KYC validation"""
    validation_start_time = datetime.now()
```

**Explanation**:
- Main validation orchestrator
- Tracks validation duration

```python
    # Get customer data
    customer_query = "SELECT * FROM customers WHERE customer_id = %s"
    customer = db.execute_one(customer_query, (customer_id,))
```

**Explanation**:
- Fetches customer profile from database
- Uses parameterized query (prevents SQL injection)

```python
    # Advanced photo validation with AI
    photo_validation = validate_photo_advanced(photo_path, is_live_capture=True)
```

**Explanation**:
- Runs comprehensive photo validation
- Includes face detection, liveness, quality analysis

```python
    # Get document OCR data
    doc_query = """
        SELECT ocr_extracted_data, created_at
        FROM documents 
        WHERE application_id = %s AND document_type = 'identity_proof'
        ORDER BY created_at DESC
        LIMIT 1
    """
    doc_result = db.execute_one(doc_query, (application_id,))
    ocr_data = doc_result.get('ocr_extracted_data') if doc_result else None
```

**Explanation**:
- Fetches OCR extracted data from identity document
- Used for address validation and document type detection

```python
    # Validate address
    from kyc_validator import validate_address
    address_validation = validate_address(customer, ocr_data)
```

**Explanation**:
- Validates address completeness
- Cross-references with document OCR

```python
    # Advanced document validation
    identity_doc_validation = validate_document_advanced(application_id, 'identity_proof')
    photo_doc_validation = validate_document_advanced(application_id, 'photo')
```

**Explanation**:
- Validates identity document (PAN/Aadhar)
- Validates photo document separately

```python
    # Face Matching
    face_match_result = None
    if photo_path and doc_result:
        id_doc = db.execute_one(id_doc_query, (application_id,))
        if id_doc and id_doc.get('file_path'):
            face_match_result = compare_faces(photo_path, id_doc.get('file_path'))
            if not face_match_result.get('faces_match', False):
                # Critical issue: Faces don't match
                photo_validation['issues'].append('Face does not match ID document photo')
                photo_validation['score'] = max(0, photo_validation.get('score', 100) - 50)
```

**Explanation**:
- Compares customer photo with ID document photo
- If faces don't match, deducts 50 points (critical issue)
- Prevents identity fraud

```python
    # Document Type Detection
    customer_selected_doc_type = None
    if customer.get('pan_card'):
        customer_selected_doc_type = 'pan'
    elif customer.get('aadhar_no'):
        customer_selected_doc_type = 'aadhar'
    
    detected_doc_type = detect_document_type_from_ocr(ocr_data_for_detection)
    
    if customer_selected_doc_type != detected_doc_type:
        # Critical: Document type mismatch
        critical_issue = f'Document type mismatch: Selected {customer_selected_doc_type.upper()} but uploaded {detected_doc_type.upper()}'
        identity_doc_validation['issues'].append(critical_issue)
        identity_doc_validation['score'] = 0
        identity_doc_validation['is_valid'] = False
```

**Explanation**:
- Detects actual document type from OCR
- Compares with user's selection
- If mismatch, sets score to 0 (auto-rejection)

```python
    # Calculate overall score with weights
    photo_weight = 0.4
    address_weight = 0.15
    identity_doc_weight = 0.3
    photo_doc_weight = 0.15
    
    overall_score = (
        photo_validation['score'] * photo_weight +
        address_validation['score'] * address_weight +
        identity_doc_validation['score'] * identity_doc_weight +
        photo_doc_validation['score'] * photo_doc_weight
    )
```

**Explanation**:
- Weighted scoring formula
- Photo has highest weight (40%)
- Identity document second (30%)
- Address and photo document lower (15% each)

```python
    # Determine status - STRICT VALIDATION
    has_critical_issues = (
        (face_match_result and not face_match_result.get('faces_match', True)) or
        (customer_selected_doc_type and detected_doc_type != 'unknown' and customer_selected_doc_type != detected_doc_type) or
        len(identity_doc_validation.get('critical_issues', [])) > 0
    )
    
    if has_critical_issues:
        status = 'rejected'
    elif overall_score >= 70:
        status = 'approved'
    else:
        status = 'rejected'
```

**Explanation**:
- Checks for critical issues first
- If critical issues exist → auto-reject
- Otherwise, approves if score >= 70%

```python
    # Update application status
    update_query = """
        UPDATE kyc_applications 
        SET application_status = %s,
            verification_date = %s,
            notes = %s
        WHERE application_id = %s
    """
    db.execute_query(update_query, (status, validation_end_time, notes, application_id), fetch=False)
```

**Explanation**:
- Updates application status in database
- Stores detailed validation notes
- Records verification timestamp

```python
    # Update document verification status INDIVIDUALLY
    for doc in all_documents:
        doc_type = doc.get('document_type')
        if doc_type == 'photo':
            doc_validation = photo_doc_validation
        elif doc_type == 'identity_proof':
            doc_validation = identity_doc_validation
        
        if doc_validation.get('is_valid', False) and doc_validation.get('score', 0) >= 60:
            doc_status = 'verified'
        else:
            doc_status = 'rejected'
        
        doc_update_query = """
            UPDATE documents 
            SET verification_status = %s,
                verification_notes = %s,
                verified_at = %s
            WHERE document_id = %s
        """
        db.execute_query(doc_update_query, (doc_status, doc_notes, validation_end_time, doc_id), fetch=False)
```

**Explanation**:
- Updates each document's status individually
- Documents can be verified or rejected independently
- Stores verification notes per document

---

## OCR Engine (ocr_engine.py)

### Lines 24-38: OCR Engine Initialization

```python
class OCREngine:
    def __init__(self):
        self.tesseract_available = TESSERACT_AVAILABLE
        if TESSERACT_AVAILABLE:
            if os.name == 'nt':  # Windows
                possible_paths = [
                    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        break
```

**Explanation**:
- Checks if Tesseract is available
- On Windows, searches common installation paths
- Sets Tesseract executable path if found

### Lines 40-48: Text Extraction

```python
def extract_text_from_image(self, image_path: str) -> str:
    """Extract text from an image file"""
    try:
        if not self.tesseract_available:
            return self._mock_ocr_extraction(image_path)
        
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='eng')
        return text.strip()
    except Exception as e:
        return self._mock_ocr_extraction(image_path)
```

**Explanation**:
- Opens image using PIL
- Runs Tesseract OCR with English language
- Returns extracted text
- Falls back to mock OCR if Tesseract fails

### Lines 69-138: PAN Card Validation

```python
def validate_pan(self, extracted_text: str) -> Dict[str, any]:
    results = {
        'is_valid': False,
        'pan_number': None,
        'name': None,
        'father_name': None,
        'dob': None,
        'completeness_score': 0,
        'missing_fields': [],
        'confidence': 0
    }
```

**Explanation**:
- Initializes result dictionary
- All fields start as None/False/0

```python
    # PAN format: 5 letters + 4 digits + 1 letter (e.g., ABCDE1234F)
    pan_pattern = r'\b([A-Z]{5})[\s\-]?(\d{4})[\s\-]?([A-Z]{1})\b'
    pan_match = re.search(pan_pattern, extracted_text.upper())
    if pan_match:
        pan_number = pan_match.group(1) + pan_match.group(2) + pan_match.group(3)
        results['pan_number'] = pan_number
        results['completeness_score'] += 35
```

**Explanation**:
- **Regex Pattern**: Matches PAN format
  - `[A-Z]{5}`: 5 uppercase letters
  - `[\s\-]?`: Optional space or hyphen
  - `\d{4}`: 4 digits
  - `[A-Z]{1}`: 1 uppercase letter
- If found, adds 35 points to completeness score

```python
    # Extract name
    name_patterns = [
        r'(?:Name|NAME)[\s:]+([A-Z][A-Z\s]{5,40})',
        r'(?:Name|NAME)[\s:]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        r'INCOME TAX DEPARTMENT\s+([A-Z][A-Z\s]{5,40})',
    ]
    for pattern in name_patterns:
        name_match = re.search(pattern, extracted_text)
        if name_match:
            results['name'] = name_match.group(1).strip()
            results['completeness_score'] += 25
            break
```

**Explanation**:
- Multiple regex patterns for name extraction
- Tries different formats (all caps, mixed case, after "INCOME TAX DEPARTMENT")
- If found, adds 25 points

```python
    if results['completeness_score'] >= 60:  # PAN number + Name is minimum
        results['is_valid'] = True
        results['confidence'] = min(100, results['completeness_score'])
```

**Explanation**:
- Minimum 60 points required (PAN + Name)
- Sets `is_valid` to True
- Confidence = completeness score (capped at 100)

### Lines 140-180: Aadhar Card Validation

```python
def validate_aadhar(self, extracted_text: str) -> Dict[str, any]:
    # Aadhar format: 12 digits, can be space-separated
    aadhar_pattern = r'\b\d{4}\s?\d{4}\s?\d{4}\b'
    aadhar_match = re.search(aadhar_pattern, extracted_text)
    if aadhar_match:
        results['aadhar_number'] = re.sub(r'\s', '', aadhar_match.group())
        results['completeness_score'] += 30
```

**Explanation**:
- **Aadhar Pattern**: 4 digits, optional space, 4 digits, optional space, 4 digits
- Removes spaces from extracted number
- Adds 30 points for Aadhar number

```python
    if results['completeness_score'] >= 70:
        results['is_valid'] = True
        results['confidence'] = min(100, results['completeness_score'])
```

**Explanation**:
- Aadhar requires 70 points (higher threshold than PAN)
- Name + Aadhar number = 55 points minimum
- Additional fields needed to reach 70

---

## Database Helpers (db_helpers.py)

### Lines 13-19: Password Hashing

```python
def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == password_hash
```

**Explanation**:
- `hash_password()`: Converts password to SHA-256 hash
- `verify_password()`: Hashes input password and compares with stored hash
- Never stores plain text passwords

### Lines 21-68: Duplicate Checking Functions

```python
def check_username_exists(username: str) -> bool:
    """Check if username already exists"""
    try:
        query = "SELECT user_id FROM users WHERE username = %s"
        result = db.execute_one(query, (username,))
        return result is not None
    except:
        return False
```

**Explanation**:
- Parameterized query prevents SQL injection
- Returns True if username exists, False otherwise
- Similar functions for email, phone, PAN, Aadhar

### Lines 70-106: User Creation

```python
def create_user(username: str, email: str, password: str, role: str = 'customer') -> Optional[uuid.UUID]:
    """Create a new user"""
    # Check if username already exists
    if check_username_exists(username):
        st.error(f"❌ Username '{username}' already exists.")
        return None
    
    # Check if email already exists
    if check_email_exists(email):
        st.error(f"❌ Email '{email}' is already registered.")
        return None
    
    password_hash = hash_password(password)
    query = """
        INSERT INTO users (username, email, password_hash, role)
        VALUES (%s, %s, %s, %s)
        RETURNING user_id
    """
    result = db.execute_one(query, (username, email, password_hash, role))
    if result:
        log_audit(result['user_id'], 'login', 'user', result['user_id'], 
                 f"New user registered: {username}")
        return result['user_id']
    return None
```

**Explanation**:
- Checks for duplicates before insertion
- Hashes password before storing
- `RETURNING user_id`: PostgreSQL returns generated UUID
- Logs audit trail
- Returns user_id on success, None on failure

### Lines 108-139: Authentication

```python
def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate user and return user data"""
    query = """
        SELECT user_id, username, email, password_hash, role, is_active
        FROM users
        WHERE username = %s OR email = %s
    """
    user = db.execute_one(query, (username, username))
    
    if user and verify_password(password, user['password_hash']):
        if not user['is_active']:
            return None
        
        # Update last login
        update_query = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = %s"
        db.execute_query(update_query, (user['user_id'],), fetch=False)
        
        # Log audit
        log_audit(user['user_id'], 'login', 'user', user['user_id'], 
                 f"User logged in: {username}")
        
        return {
            'user_id': user['user_id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role']
        }
    return None
```

**Explanation**:
- Allows login with username OR email
- Verifies password hash
- Checks if account is active
- Updates last_login timestamp
- Logs audit trail
- Returns user data dictionary (without password_hash)

### Lines 141-175: Customer Creation

```python
def create_customer(user_id: uuid.UUID, customer_data: Dict[str, Any]) -> Optional[uuid.UUID]:
    """Create customer profile"""
    query = """
        INSERT INTO customers (user_id, first_name, last_name, full_name, date_of_birth, gender, 
                             marital_status, age, address, city_town, pincode, pan_card, aadhar_no,
                             phone_number, salary, annual_income, occupation, photo_path, kyc_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING customer_id
    """
    result = db.execute_one(query, (
        user_id,
        customer_data.get('first_name'),
        customer_data.get('last_name'),
        # ... all other fields
        customer_data.get('kyc_status', 'Not Submitted')
    ))
    return result['customer_id'] if result else None
```

**Explanation**:
- Creates customer record linked to user account
- Uses `.get()` with defaults for optional fields
- Sets default KYC status to 'Not Submitted'
- Returns customer_id on success

### Lines 349-370: KYC Application Creation

```python
def create_kyc_application(customer_id: uuid.UUID) -> Optional[uuid.UUID]:
    """Create a new KYC application"""
    query = """
        INSERT INTO kyc_applications (customer_id, application_status)
        VALUES (%s, 'submitted')
        RETURNING application_id
    """
    result = db.execute_one(query, (customer_id,))
    if result:
        # Update customer KYC status
        update_query = "UPDATE customers SET kyc_status = 'Submitted' WHERE customer_id = %s"
        db.execute_query(update_query, (customer_id,), fetch=False)
        
        log_audit(None, 'application_submit', 'application', result['application_id'],
                 f"New KYC application submitted")
        return result['application_id']
    return None
```

**Explanation**:
- Creates KYC application record
- Sets status to 'submitted'
- Updates customer's KYC status
- Logs audit trail
- Returns application_id

### Lines 372-398: Document Saving

```python
def save_document(application_id: uuid.UUID, document_type: str, 
                 document_name: str, file_path: str, file_size: int, 
                 mime_type: str, ocr_data: Dict = None) -> Optional[uuid.UUID]:
    """Save document information to database"""
    import json
    ocr_json = json.dumps(ocr_data) if ocr_data else None
    
    query = """
        INSERT INTO documents (application_id, document_type, document_name, 
                             file_path, file_size, mime_type, ocr_extracted_data, verification_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
        RETURNING document_id
    """
    result = db.execute_one(query, (
        application_id, document_type, document_name, 
        file_path, file_size, mime_type, ocr_json
    ))
    if result:
        log_audit(None, 'document_upload', 'document', result['document_id'],
                 f"Document uploaded: {document_name}")
        return result['document_id']
    return None
```

**Explanation**:
- Converts OCR data dictionary to JSON string
- Stores document metadata in database
- Sets verification_status to 'pending'
- Stores file path (actual file stored on disk)
- Logs audit trail

---

## AI Helper (ai_helper.py)

### Lines 13-17: OpenAI Client Setup

```python
client = OpenAI(
    api_key=os.environ["GENAILAB_API_KEY"],
    base_url="https://genailab.tcs.in",
    http_client=httpx.Client(verify=False)  # GenAILab needs this
)
```

**Explanation**:
- Uses TCS GenAILab endpoint (not standard OpenAI)
- Requires API key from environment variable
- `verify=False`: Disables SSL verification (for GenAILab)

### Lines 22-37: JSON Parsing Helper

```python
def parse_json_safe(content: str) -> dict:
    """Extract the first valid JSON object from the string"""
    # Remove ```json or ``` from the string
    content = re.sub(r'```(json)?', '', content, flags=re.IGNORECASE).strip()
    
    # Find the first {...} JSON object
    match = re.search(r'\{.*\}', content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return {"is_live": False, "reason": "AI response could not be parsed"}
```

**Explanation**:
- Removes Markdown code blocks
- Finds JSON object in response
- Safely parses JSON
- Returns default dict if parsing fails

### Lines 43-95: Photo Liveness Check

```python
def openai_photo_liveness_check(base64_image: str) -> dict:
    """Returns: { "is_live": bool, "reason": str }"""
    
    response = client.chat.completions.create(
        model="azure/genailab-maas-gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a bank-grade KYC liveness detection system. "
                    "Determine if the image is a REAL LIVE PERSON "
                    "or a PHOTO / SCREEN / PRINT / REPLAY ATTACK. "
                    "Always reply strictly in JSON."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze the image and decide if it was captured live "
                            "by a webcam. Return JSON ONLY:\n"
                            "{ \"is_live\": true/false, \"reason\": \"short explanation\" }"
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0,
        max_tokens=100
    )
```

**Explanation**:
- Uses GPT-4 Vision model via GenAILab
- System prompt defines role as liveness detector
- User prompt requests JSON response
- Image sent as base64-encoded data URL
- `temperature=0`: Deterministic responses
- `max_tokens=100`: Short response

```python
    try:
        content = response.choices[0].message.content
        return parse_json_safe(content)
    except Exception:
        return {
            "is_live": False,
            "reason": "AI response could not be parsed"
        }
```

**Explanation**:
- Extracts response content
- Parses JSON safely
- Returns default dict on error

### Lines 99-113: Face Detection Helper

```python
def has_face(image_file) -> bool:
    """Returns True if a face is detected in the uploaded image."""
    img = np.array(Image.open(image_file).convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    return len(faces) > 0
```

**Explanation**:
- Simple face detection function
- Returns boolean (face found or not)
- Used for quick checks

---

## Summary

This document provides detailed line-by-line explanations of the key functions in your KYC system. Each function is broken down to explain:

1. **Purpose**: What the function does
2. **Parameters**: Input parameters and their types
3. **Logic**: Step-by-step explanation of the code
4. **Return Values**: What the function returns
5. **Error Handling**: How errors are handled

Use this document alongside `DEMO_PRESENTATION_GUIDE.md` to prepare for your presentation. The combination gives you both high-level understanding and detailed technical knowledge.


