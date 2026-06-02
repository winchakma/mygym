import os

html_files = [
    "admin.html", "community.html", "trainer.html"
]

base_dir = r"c:\Users\user\Desktop\mygym\frontend"

for f in html_files:
    filepath = os.path.join(base_dir, f)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
            
        content = content.replace('  <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">\n', "")
        content = content.replace('  <script src="js/support_widget.js"></script>\n', "")
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
            
print("Done reverting unneeded files.")
