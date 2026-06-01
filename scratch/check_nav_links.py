import os
import re

frontend_dir = r"c:\Users\user\Desktop\mygym\frontend"
html_files = [f for f in os.listdir(frontend_dir) if f.endswith(".html")]

for filename in html_files:
    file_path = os.path.join(frontend_dir, filename)
    
    content = None
    encodings = ["utf-8", "utf-16", "latin1"]
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as file:
                content = file.read()
            break
        except Exception:
            continue
            
    if content is None:
        continue
        
    # Extract nav-links container
    match = re.search(r'<div class="nav-links">(.*?)</div>', content, re.DOTALL)
    if match:
        nav_html = match.group(1).strip()
        # Extract href and text for each link
        links = re.findall(r'href="([^"]+)"[^>]*>(.*?)</a>', nav_html)
        print(f"{filename}: {[f'{text.strip()} ({href})' for href, text in links]}")
    else:
        print(f"{filename}: No nav-links found")
