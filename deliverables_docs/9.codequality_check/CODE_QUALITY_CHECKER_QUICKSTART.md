# 🚀 Code Quality Checker - Quick Start Guide

## Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install streamlit openai python-dotenv
```

### 2. Set API Key (Optional - for AI analysis)
Add to `.env` file:
```env
OPENAI_API_KEY=your_key_here
```

### 3. Run the Tool
```bash
streamlit run code_quality_checker.py
```

### 4. Open Browser
Navigate to: `http://localhost:8501`

---

## Quick Usage

### Step 1: Paste Your Code
```
def my_function():
    password = "hardcoded123"  # BAD!
    return password
```

### Step 2: Click "Analyze Code Quality"

### Step 3: Review Results
- ✅ Green = Pass
- ⚠️ Yellow = Partial (needs improvement)
- ❌ Red = Fail (needs fixing)

### Step 4: Read Suggestions
Each failed item shows:
- What's wrong
- Why it's wrong
- How to fix it

---

## Example: Analyzing KYC Project Code

### Analyze `app_main.py`:
1. Open `code_quality_checker.py` in Streamlit
2. Click "Upload File"
3. Select `app_main.py`
4. Click "Analyze Code Quality"
5. Review results for security, structure, and quality issues

### Analyze `ai_kyc_validator.py`:
1. Upload or paste the file
2. Review AI validation code quality
3. Check for:
   - Proper error handling
   - Function documentation
   - Code organization

---

## Checklist Categories

| Category | Items | Focus |
|----------|-------|-------|
| Code Structure | 4 | Formatting, naming, organization |
| Error Handling | 2 | Try-except, error messages |
| Security | 3 | Credentials, SQL injection, validation |
| Performance | 2 | Algorithms, database connections |
| Code Quality | 5 | DRY, naming, PEP 8, unused code |
| Maintainability | 3 | Comments, function length, modularity |
| Testing | 1 | Testable structure |

**Total: 20 Quality Checks**

---

## Tips

✅ **Use AI Analysis** for best results (requires API key)  
✅ **Start with Critical Items** - Security and error handling first  
✅ **Export Results** - Save JSON reports for tracking  
✅ **Customize Checklist** - Add project-specific checks  

---

## Common Issues Found

### Security Issues
- ❌ Hardcoded passwords → Use environment variables
- ❌ SQL injection → Use parameterized queries
- ❌ Missing input validation → Validate all inputs

### Code Quality Issues
- ❌ No docstrings → Add function documentation
- ❌ Unused imports → Remove unused code
- ❌ Magic numbers → Use named constants

### Structure Issues
- ❌ Mixed indentation → Use consistent spacing
- ❌ Long functions → Break into smaller functions
- ❌ No error handling → Add try-except blocks

---

## Next Steps

1. ✅ Run analysis on your code
2. ✅ Fix critical issues (security, errors)
3. ✅ Review suggestions
4. ✅ Re-analyze after fixes
5. ✅ Export and track improvements

---

**Ready to improve your code quality! 🔍✨**

