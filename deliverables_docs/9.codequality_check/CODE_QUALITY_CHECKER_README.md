# 🤖 AI Code Quality Checker - User Guide

## Overview

The **AI Code Quality Checker** is an intelligent code analysis tool built with Streamlit and AI frameworks. It analyzes code against a comprehensive quality checklist and provides AI-powered observations and improvement suggestions.

## Features

- ✅ **AI-Powered Analysis**: Uses GPT-4 or similar models for intelligent code analysis
- ✅ **Comprehensive Checklist**: 20 default quality checks covering structure, security, performance, and maintainability
- ✅ **Customizable Checklist**: Add or modify checklist items as needed
- ✅ **Detailed Observations**: Get specific findings for each checklist item
- ✅ **Improvement Suggestions**: Receive actionable suggestions to improve code quality
- ✅ **Export Reports**: Download analysis results as JSON or text reports
- ✅ **Fallback Mode**: Basic pattern-based analysis when AI is unavailable

## Installation

### Prerequisites
- Python 3.8+
- Streamlit
- OpenAI API key (for AI analysis) or GenAILab API key

### Setup

1. **Install Dependencies**:
   ```bash
   pip install streamlit openai python-dotenv
   ```

2. **Configure API Key**:
   Create or update `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   # OR
   GENAILAB_API_KEY=your_genailab_api_key
   GENAILAB_BASE_URL=https://genailab.tcs.in
   ```

3. **Run the Application**:
   ```bash
   streamlit run code_quality_checker.py
   ```

4. **Access the Tool**:
   Open browser to `http://localhost:8501`

## Usage

### Step 1: Input Code
- **Option A**: Type or paste code directly into the text area
- **Option B**: Upload a Python file (.py)

### Step 2: Select Checklist
- **Default Checklist**: Use the built-in 20-item quality checklist
- **Custom Checklist**: Provide your own checklist as JSON

### Step 3: Configure Analysis
- **AI Analysis**: Enable for intelligent analysis (requires API key)
- **Basic Analysis**: Fallback mode with pattern-based checks

### Step 4: Analyze
- Click "Analyze Code Quality" button
- Wait for analysis to complete (may take 30-60 seconds for AI analysis)

### Step 5: Review Results
- View summary statistics (Passed/Partial/Failed/Errors)
- Expand each checklist item to see:
  - Status (Pass/Fail/Partial)
  - Observation
  - Specific findings
  - Improvement suggestions

### Step 6: Export Results
- Download detailed results as JSON
- Download summary report as text

## Default Checklist Categories

### 1. Code Structure (4 items)
- Proper indentation and formatting
- Descriptive function/class names
- Function docstrings
- Code organization

### 2. Error Handling (2 items)
- Try-except blocks
- Clear error messages

### 3. Security (3 items)
- No hardcoded credentials
- SQL injection prevention
- Input validation

### 4. Performance (2 items)
- Efficient algorithms
- Database connection management

### 5. Code Quality (5 items)
- DRY principle
- Meaningful variable names
- PEP 8 compliance
- No unused imports
- Named constants

### 6. Maintainability (3 items)
- Appropriate comments
- Function length
- Modular design

### 7. Testing (1 item)
- Testable code structure

## Custom Checklist Format

You can provide a custom checklist as JSON:

```json
[
    {
        "id": "CQ001",
        "category": "Security",
        "item": "No hardcoded API keys",
        "description": "API keys should be stored in environment variables"
    },
    {
        "id": "CQ002",
        "category": "Performance",
        "item": "Efficient database queries",
        "description": "Queries should use indexes and avoid N+1 problems"
    }
]
```

## AI Analysis vs Basic Analysis

### AI Analysis (Recommended)
- **Pros**:
  - Intelligent understanding of code context
  - Context-aware suggestions
  - Better detection of complex issues
  - Explains why code fails/passes
  
- **Cons**:
  - Requires API key
  - Takes longer (30-60 seconds)
  - May incur API costs

### Basic Analysis (Fallback)
- **Pros**:
  - No API key required
  - Fast analysis
  - No costs
  
- **Cons**:
  - Pattern-based only
  - Limited context understanding
  - May miss complex issues

## Example Analysis Output

### For a Checklist Item:

**Status**: ❌ FAIL

**Observation**: 
The code contains hardcoded database credentials in the connection string. This is a security vulnerability.

**Findings**:
- Line 15: `password = "mypassword123"` - Hardcoded password detected
- Line 20: `api_key = "sk-1234567890"` - Hardcoded API key detected

**💡 Suggestions for Improvement**:
1. Move sensitive credentials to environment variables using `os.getenv()`
2. Use a `.env` file with `python-dotenv` package
3. Never commit credentials to version control
4. Example: `password = os.getenv('DB_PASSWORD')`

## Integration with Your Project

### Use for KYC Project Files

You can analyze any file from your KYC project:

```python
# Example: Analyze app_main.py
streamlit run code_quality_checker.py
# Then upload app_main.py or paste its contents
```

### Batch Analysis

To analyze multiple files:
1. Run the tool
2. Analyze each file separately
3. Export results for each
4. Compare results across files

## Best Practices

1. **Regular Checks**: Run code quality checks before committing code
2. **Fix Critical Issues First**: Address security and error handling issues immediately
3. **Use AI Analysis**: Enable AI analysis for comprehensive feedback
4. **Customize Checklist**: Adapt checklist to your project's specific needs
5. **Review Suggestions**: Carefully review AI suggestions before implementing

## Troubleshooting

### Issue: "AI client not configured"
**Solution**: Set `OPENAI_API_KEY` or `GENAILAB_API_KEY` in `.env` file

### Issue: "Could not parse AI response"
**Solution**: The AI response format may have changed. Try basic analysis mode or check API configuration

### Issue: Analysis takes too long
**Solution**: 
- Use basic analysis mode for faster results
- Reduce checklist items
- Check API rate limits

### Issue: API errors
**Solution**:
- Verify API key is correct
- Check API quota/limits
- Verify network connectivity
- Try basic analysis mode as fallback

## Advanced Usage

### Programmatic Usage

You can also use the checker programmatically:

```python
from code_quality_checker import CodeQualityChecker

checker = CodeQualityChecker()
code = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total
"""

results = checker.check_code_quality(code, checker.default_checklist, use_ai=True)
for result in results:
    print(f"{result['checklist_item']['id']}: {result['result']['status']}")
```

## Checklist Item Statuses

- **✅ PASS**: Code meets the checklist requirement
- **⚠️ PARTIAL**: Code partially meets the requirement, improvements needed
- **❌ FAIL**: Code does not meet the requirement, needs fixing
- **🔴 ERROR**: Analysis error occurred

## Export Formats

### JSON Export
Contains complete analysis results with all details:
- Checklist items
- Status for each item
- Observations
- Findings
- Suggestions
- Confidence scores

### Text Summary Export
Contains:
- Summary statistics
- Pass rate
- Brief results for each item
- Key suggestions

## Future Enhancements

Potential improvements:
- Support for multiple programming languages
- Integration with CI/CD pipelines
- Code diff analysis
- Historical tracking
- Team collaboration features
- Custom rule definitions
- Integration with linters

## Support

For issues or questions:
1. Check this README
2. Review error messages
3. Try basic analysis mode
4. Verify API configuration

---

**Use this tool to ensure your code meets quality standards and follows best practices! 🔍✅**

