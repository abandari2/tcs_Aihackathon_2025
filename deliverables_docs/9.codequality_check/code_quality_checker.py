"""
AI Agent - Code Quality Checker
Built with AI framework and Streamlit
Takes code and checklist as input and provides observations against each checklist item
"""

import streamlit as st
import os
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
import json
import re

load_dotenv()

# Initialize OpenAI client (using GenAILab or standard OpenAI)
try:
    client = OpenAI(
        api_key=os.environ.get("GENAILAB_API_KEY") or os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("GENAILAB_BASE_URL", "https://api.openai.com/v1")
    )
except:
    client = None

class CodeQualityChecker:
    """AI-powered code quality checker"""
    
    def __init__(self):
        self.default_checklist = self._get_default_checklist()
    
    def _get_default_checklist(self) -> List[Dict[str, Any]]:
        """Get default code quality checklist"""
        return [
            {
                "id": "CQ001",
                "category": "Code Structure",
                "item": "Code follows proper indentation and formatting",
                "description": "Check if code has consistent indentation (4 spaces or tabs) and proper formatting"
            },
            {
                "id": "CQ002",
                "category": "Code Structure",
                "item": "Functions and classes have clear, descriptive names",
                "description": "Function and class names should be descriptive and follow naming conventions"
            },
            {
                "id": "CQ003",
                "category": "Code Structure",
                "item": "Functions have docstrings explaining their purpose",
                "description": "All functions should have docstrings describing what they do, parameters, and return values"
            },
            {
                "id": "CQ004",
                "category": "Code Structure",
                "item": "Code is properly organized into modules/classes",
                "description": "Code should be organized into logical modules, classes, or functions"
            },
            {
                "id": "CQ005",
                "category": "Error Handling",
                "item": "Proper error handling with try-except blocks",
                "description": "Code should handle exceptions gracefully with appropriate error messages"
            },
            {
                "id": "CQ006",
                "category": "Error Handling",
                "item": "Error messages are clear and informative",
                "description": "Error messages should help users understand what went wrong"
            },
            {
                "id": "CQ007",
                "category": "Security",
                "item": "No hardcoded passwords or sensitive data",
                "description": "Sensitive data like passwords, API keys should not be hardcoded"
            },
            {
                "id": "CQ008",
                "category": "Security",
                "item": "SQL queries use parameterized inputs (prevent SQL injection)",
                "description": "Database queries should use parameterized inputs to prevent SQL injection"
            },
            {
                "id": "CQ009",
                "category": "Security",
                "item": "Input validation is performed",
                "description": "User inputs should be validated before processing"
            },
            {
                "id": "CQ010",
                "category": "Performance",
                "item": "No unnecessary loops or inefficient algorithms",
                "description": "Code should use efficient algorithms and avoid unnecessary iterations"
            },
            {
                "id": "CQ011",
                "category": "Performance",
                "item": "Database connections are properly managed (pooling, closing)",
                "description": "Database connections should be managed efficiently with pooling and proper cleanup"
            },
            {
                "id": "CQ012",
                "category": "Code Quality",
                "item": "No duplicate code (DRY principle)",
                "description": "Code should follow DRY (Don't Repeat Yourself) principle"
            },
            {
                "id": "CQ013",
                "category": "Code Quality",
                "item": "Variables have meaningful names",
                "description": "Variable names should be descriptive and follow naming conventions"
            },
            {
                "id": "CQ014",
                "category": "Code Quality",
                "item": "Code follows PEP 8 style guide (for Python)",
                "description": "Python code should follow PEP 8 style guidelines"
            },
            {
                "id": "CQ015",
                "category": "Code Quality",
                "item": "No unused imports or variables",
                "description": "Remove unused imports and variables to keep code clean"
            },
            {
                "id": "CQ016",
                "category": "Code Quality",
                "item": "Magic numbers are replaced with named constants",
                "description": "Numeric literals should be replaced with named constants for better readability"
            },
            {
                "id": "CQ017",
                "category": "Maintainability",
                "item": "Code has appropriate comments for complex logic",
                "description": "Complex logic should have comments explaining the approach"
            },
            {
                "id": "CQ018",
                "category": "Maintainability",
                "item": "Functions are not too long (single responsibility)",
                "description": "Functions should be focused and not exceed reasonable length (typically < 50 lines)"
            },
            {
                "id": "CQ019",
                "category": "Maintainability",
                "item": "Code is modular and reusable",
                "description": "Code should be organized into reusable modules and functions"
            },
            {
                "id": "CQ020",
                "category": "Testing",
                "item": "Code structure allows for easy testing",
                "description": "Code should be structured to facilitate unit testing"
            }
        ]
    
    def analyze_code_with_ai(self, code: str, checklist_item: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to analyze code against a checklist item"""
        if not client:
            return {
                "status": "error",
                "observation": "AI client not configured. Please set OPENAI_API_KEY or GENAILAB_API_KEY in environment.",
                "suggestion": "Configure API key in .env file"
            }
        
        try:
            prompt = f"""You are a code quality expert. Analyze the following code against this checklist item:

Checklist Item: {checklist_item['item']}
Description: {checklist_item['description']}
Category: {checklist_item['category']}

Code to analyze:
```python
{code}
```

Provide:
1. Observation: Does the code meet this checklist item? (Yes/No/Partial)
2. Specific findings: What did you find in the code related to this item?
3. Suggestions: If improvements are needed, provide specific suggestions with examples.

Respond in JSON format:
{{
    "status": "pass" | "fail" | "partial",
    "observation": "detailed observation",
    "findings": ["finding1", "finding2"],
    "suggestions": ["suggestion1", "suggestion2"],
    "confidence": 0.0-1.0
}}"""

            response = client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "You are an expert code quality analyst. Always respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
                return result
            else:
                return {
                    "status": "error",
                    "observation": "Could not parse AI response",
                    "suggestions": []
                }
        except Exception as e:
            return {
                "status": "error",
                "observation": f"AI analysis error: {str(e)}",
                "suggestions": []
            }
    
    def analyze_code_basic(self, code: str, checklist_item: Dict[str, Any]) -> Dict[str, Any]:
        """Basic code analysis without AI (fallback)"""
        item_id = checklist_item['id']
        category = checklist_item['category']
        item = checklist_item['item']
        
        observations = []
        suggestions = []
        status = "pass"
        
        # Basic pattern-based checks
        if "indentation" in item.lower() or "formatting" in item.lower():
            # Check for mixed indentation
            lines = code.split('\n')
            has_tabs = any('\t' in line for line in lines if line.strip())
            has_spaces = any(line.startswith(' ') for line in lines if line.strip())
            if has_tabs and has_spaces:
                status = "fail"
                observations.append("Mixed indentation detected (tabs and spaces)")
                suggestions.append("Use consistent indentation (preferably 4 spaces)")
        
        if "docstring" in item.lower():
            # Check for function docstrings
            functions = re.findall(r'def\s+\w+\s*\([^)]*\):', code)
            docstrings = re.findall(r'def\s+\w+\s*\([^)]*\):\s*""".*?"""', code, re.DOTALL)
            if len(functions) > len(docstrings):
                status = "partial"
                observations.append(f"Found {len(functions)} functions but only {len(docstrings)} have docstrings")
                suggestions.append("Add docstrings to all functions explaining their purpose, parameters, and return values")
        
        if "try-except" in item.lower() or "error handling" in item.lower():
            # Check for error handling
            has_try_except = 'try:' in code and 'except' in code
            if not has_try_except and ('open(' in code or 'db.' in code or 'execute' in code):
                status = "partial"
                observations.append("File or database operations found without try-except blocks")
                suggestions.append("Add try-except blocks around file I/O and database operations")
        
        if "hardcoded" in item.lower() or "password" in item.lower():
            # Check for hardcoded secrets
            patterns = [
                r'password\s*=\s*["\'][^"\']+["\']',
                r'api_key\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']'
            ]
            for pattern in patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    status = "fail"
                    observations.append("Potential hardcoded credentials detected")
                    suggestions.append("Move sensitive data to environment variables or config files")
                    break
        
        if "parameterized" in item.lower() or "SQL injection" in item.lower():
            # Check for SQL injection vulnerabilities
            if re.search(r'execute\s*\([^)]*\+', code) or re.search(r'execute\s*\([^)]*%', code):
                status = "fail"
                observations.append("Potential SQL injection vulnerability: string concatenation in SQL queries")
                suggestions.append("Use parameterized queries: db.execute_query(query, (param1, param2))")
        
        if "unused" in item.lower():
            # Check for unused imports (basic check)
            imports = re.findall(r'^import\s+(\w+)|^from\s+(\w+)', code, re.MULTILINE)
            # This is a basic check - full analysis would need AST parsing
        
        return {
            "status": status,
            "observation": "; ".join(observations) if observations else "Basic check passed",
            "findings": observations,
            "suggestions": suggestions,
            "confidence": 0.6
        }
    
    def check_code_quality(self, code: str, checklist: List[Dict[str, Any]], use_ai: bool = True) -> List[Dict[str, Any]]:
        """Check code quality against checklist"""
        results = []
        
        for item in checklist:
            if use_ai and client:
                result = self.analyze_code_with_ai(code, item)
            else:
                result = self.analyze_code_basic(code, item)
            
            results.append({
                "checklist_item": item,
                "result": result
            })
        
        return results

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="AI Code Quality Checker",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🤖 AI Agent - Code Quality Checker")
    st.markdown("---")
    st.markdown("""
    **Analyze your code against quality standards and get AI-powered suggestions for improvements.**
    
    This tool helps ensure your code follows best practices, security guidelines, and maintainability standards.
    """)
    
    checker = CodeQualityChecker()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        use_ai = st.checkbox("Use AI Analysis", value=True, help="Enable AI-powered analysis (requires API key)")
        if use_ai:
            api_key_status = "✅ Configured" if client else "❌ Not Configured"
            st.info(f"AI Status: {api_key_status}")
            if not client:
                st.warning("Set OPENAI_API_KEY or GENAILAB_API_KEY in .env file")
        
        st.markdown("---")
        st.header("📋 Checklist Options")
        use_default = st.checkbox("Use Default Checklist", value=True)
        
        if not use_default:
            st.info("You can customize the checklist in the main area")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Code Input")
        code_input_method = st.radio(
            "Input Method",
            ["Type/Paste Code", "Upload File"],
            horizontal=True
        )
        
        if code_input_method == "Type/Paste Code":
            code = st.text_area(
                "Enter your code here:",
                height=400,
                placeholder="""# Example code
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total
"""
            )
        else:
            uploaded_file = st.file_uploader("Upload Python file", type=['py'])
            if uploaded_file:
                code = uploaded_file.read().decode('utf-8')
                st.code(code[:500] + "..." if len(code) > 500 else code)
            else:
                code = ""
    
    with col2:
        st.subheader("📋 Quality Checklist")
        
        if use_default:
            checklist = checker.default_checklist
            st.info(f"Using default checklist ({len(checklist)} items)")
            
            # Show checklist items
            with st.expander("View Checklist Items", expanded=False):
                for item in checklist:
                    st.markdown(f"**{item['id']}** - {item['item']}")
                    st.caption(f"Category: {item['category']}")
        else:
            st.info("Custom checklist editor")
            # Allow custom checklist input
            checklist_json = st.text_area(
                "Enter checklist as JSON:",
                height=300,
                value=json.dumps(checker.default_checklist, indent=2)
            )
            try:
                checklist = json.loads(checklist_json)
            except:
                st.error("Invalid JSON format")
                checklist = checker.default_checklist
    
    st.markdown("---")
    
    # Analyze button
    if st.button("🔍 Analyze Code Quality", type="primary", use_container_width=True):
        if not code.strip():
            st.error("Please enter or upload code to analyze")
        else:
            with st.spinner("Analyzing code quality..."):
                results = checker.check_code_quality(code, checklist, use_ai=use_ai)
                
                # Display results
                st.subheader("📊 Analysis Results")
                
                # Summary statistics
                pass_count = sum(1 for r in results if r['result'].get('status') == 'pass')
                fail_count = sum(1 for r in results if r['result'].get('status') == 'fail')
                partial_count = sum(1 for r in results if r['result'].get('status') == 'partial')
                error_count = sum(1 for r in results if r['result'].get('status') == 'error')
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("✅ Passed", pass_count)
                with col2:
                    st.metric("⚠️ Partial", partial_count)
                with col3:
                    st.metric("❌ Failed", fail_count)
                with col4:
                    st.metric("🔴 Errors", error_count)
                
                st.markdown("---")
                
                # Detailed results
                for result in results:
                    item = result['checklist_item']
                    analysis = result['result']
                    
                    status = analysis.get('status', 'unknown')
                    
                    # Color code based on status
                    if status == 'pass':
                        status_icon = "✅"
                        status_color = "green"
                    elif status == 'fail':
                        status_icon = "❌"
                        status_color = "red"
                    elif status == 'partial':
                        status_icon = "⚠️"
                        status_color = "orange"
                    else:
                        status_icon = "🔴"
                        status_color = "red"
                    
                    with st.expander(f"{status_icon} {item['id']} - {item['item']}", expanded=(status != 'pass')):
                        st.markdown(f"**Category:** {item['category']}")
                        st.markdown(f"**Description:** {item['description']}")
                        
                        st.markdown("---")
                        st.markdown(f"**Status:** :{status_color}[{status.upper()}]")
                        
                        observation = analysis.get('observation', 'No observation provided')
                        st.markdown(f"**Observation:** {observation}")
                        
                        findings = analysis.get('findings', [])
                        if findings:
                            st.markdown("**Findings:**")
                            for finding in findings:
                                st.markdown(f"- {finding}")
                        
                        suggestions = analysis.get('suggestions', [])
                        if suggestions:
                            st.markdown("**💡 Suggestions for Improvement:**")
                            for i, suggestion in enumerate(suggestions, 1):
                                st.markdown(f"{i}. {suggestion}")
                        elif status == 'pass':
                            st.success("✅ This checklist item is satisfied. No improvements needed.")
                        
                        confidence = analysis.get('confidence', 0)
                        if confidence > 0:
                            st.caption(f"Confidence: {confidence*100:.1f}%")
                
                # Export results
                st.markdown("---")
                st.subheader("📥 Export Results")
                
                results_json = json.dumps(results, indent=2, default=str)
                st.download_button(
                    label="Download Results as JSON",
                    data=results_json,
                    file_name="code_quality_report.json",
                    mime="application/json"
                )
                
                # Generate summary report
                summary = f"""Code Quality Analysis Report
========================

Total Checklist Items: {len(checklist)}
Passed: {pass_count}
Partial: {partial_count}
Failed: {fail_count}
Errors: {error_count}

Pass Rate: {(pass_count/len(checklist)*100):.1f}%

Detailed Results:
"""
                for result in results:
                    item = result['checklist_item']
                    analysis = result['result']
                    summary += f"\n{item['id']} - {item['item']}: {analysis.get('status', 'unknown').upper()}\n"
                    if analysis.get('suggestions'):
                        summary += f"  Suggestions: {', '.join(analysis['suggestions'])}\n"
                
                st.download_button(
                    label="Download Summary Report",
                    data=summary,
                    file_name="code_quality_summary.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()

