import os
import re

def audit_pages(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    report = []
    
    for filename in html_files:
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check CSS
            has_css = 'href="css/style.css' in content or 'href="css/style.css?v=2026"' in content
            
            # Check Main Script
            has_script = 'src="js/script.js' in content
            
            # Check Config
            has_config = 'src="js/config.js"' in content
            
            # Check for Uppercase utility classes (Tailwind uppercase)
            # We want to minimize this as per user request
            uppercase_count = len(re.findall(r'uppercase', content))
            
            # Check for critical buttons/forms
            has_forms = '<form' in content
            
            report.append({
                "page": filename,
                "css": "OK" if has_css else "MISSING",
                "js": "OK" if has_script else "MISSING",
                "config": "OK" if has_config else "MISSING",
                "uppercase_instances": uppercase_count,
                "interactive": "YES" if has_forms else "NO"
            })
            
    return report

if __name__ == "__main__":
    results = audit_pages('.')
    for r in results:
        print(f"PAGE: {r['page']} | CSS: {r['css']} | JS: {r['js']} | CONFIG: {r['config']} | UPPERCASE: {r['uppercase_instances']}")
