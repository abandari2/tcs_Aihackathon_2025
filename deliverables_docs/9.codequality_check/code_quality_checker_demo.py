"""
Demo script showing how to use CodeQualityChecker programmatically
"""

from code_quality_checker import CodeQualityChecker

# Sample code to analyze
sample_code = """
import os
import psycopg2

# Hardcoded password - BAD
password = "mypassword123"

def get_user_data(user_id):
    # SQL injection vulnerability - BAD
    query = f"SELECT * FROM users WHERE id = {user_id}"
    conn = psycopg2.connect(host="localhost", password=password)
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total
"""

def demo():
    """Demo the code quality checker"""
    print("=" * 60)
    print("AI Code Quality Checker - Demo")
    print("=" * 60)
    
    checker = CodeQualityChecker()
    
    print(f"\nDefault checklist has {len(checker.default_checklist)} items")
    print("\nAnalyzing sample code...")
    print("-" * 60)
    
    # Analyze with basic mode (no AI required)
    results = checker.check_code_quality(
        sample_code, 
        checker.default_checklist[:5],  # Analyze first 5 items
        use_ai=False
    )
    
    print("\nAnalysis Results:")
    print("-" * 60)
    
    for result in results:
        item = result['checklist_item']
        analysis = result['result']
        
        status = analysis.get('status', 'unknown')
        status_icon = "✅" if status == "pass" else "❌" if status == "fail" else "⚠️"
        
        print(f"\n{status_icon} {item['id']} - {item['item']}")
        print(f"   Status: {status.upper()}")
        print(f"   Observation: {analysis.get('observation', 'N/A')}")
        
        suggestions = analysis.get('suggestions', [])
        if suggestions:
            print(f"   Suggestions:")
            for suggestion in suggestions:
                print(f"     - {suggestion}")
    
    print("\n" + "=" * 60)
    print("Demo complete! Run 'streamlit run code_quality_checker.py' for full UI")
    print("=" * 60)

if __name__ == "__main__":
    demo()

