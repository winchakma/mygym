import re

filepath = r"c:\Users\user\Desktop\mygym\frontend\css\style.css"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Fix support widget position
content = re.sub(r'#support-widget\s*{\s*position:\s*fixed;\s*bottom:\s*20px;\s*right:\s*20px;', r'#support-widget {\n  position: fixed;\n  bottom: 20px;\n  left: 20px;', content)

# Fix support toggle btn position
content = re.sub(r'\.support-toggle-btn\s*{\s*position:\s*fixed;\s*bottom:\s*20px;\s*right:\s*20px;', r'.support-toggle-btn {\n  position: fixed;\n  bottom: 20px;\n  left: 20px;', content)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Done fixing CSS.")
