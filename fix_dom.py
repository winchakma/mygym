import re

with open('frontend/js/script.js', 'r', encoding='utf-8') as f:
    script_content = f.read()

# Replace document.addEventListener("DOMContentLoaded", () => {
# with function initSupportWidget() {
pattern = r'document\.addEventListener\("DOMContentLoaded", \(\) => \{'
replacement = '''function initSupportWidget() {'''

script_content = re.sub(pattern, replacement, script_content, count=1)

# At the bottom, replace the closing '});' with:
# if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', initSupportWidget); } else { initSupportWidget(); }

pattern_end = r'\}\);\s*\n*window\.loadSupportHistory'
replacement_end = '''}

if (document.readyState === 'loading') {
    document.addEventListener("DOMContentLoaded", initSupportWidget);
} else {
    initSupportWidget();
}

window.loadSupportHistory'''

script_content = re.sub(pattern_end, replacement_end, script_content)

with open('frontend/js/script.js', 'w', encoding='utf-8') as f:
    f.write(script_content)

print("Updated script.js successfully!")
