import os

frontend_dir = r"c:\Users\user\Desktop\mygym\frontend"

html_files = [f for f in os.listdir(frontend_dir) if f.endswith(".html")]

print(f"Found HTML files: {html_files}")

for filename in html_files:
    file_path = os.path.join(frontend_dir, filename)
    
    content = None
    encodings = ["utf-8", "utf-16", "latin1"]
    used_encoding = None
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as file:
                content = file.read()
            used_encoding = enc
            break
        except Exception:
            continue
            
    if content is None:
        print(f"ERROR: Could not read {filename}")
        continue
    
    modified = False
    
    # 1. Button type with classes
    target1 = '<a href="admin.html" class="nav-admin-only hidden text-yellow-400 font-bold border border-yellow-400/30 px-3 py-1 rounded">Manage Elite</a>'
    replacement1 = '<a href="admin.html" class="nav-admin-only hidden text-yellow-400 font-bold border border-yellow-400/30 px-3 py-1 rounded">Manage Elite</a>\n      <a href="trainer.html" class="nav-trainer-only hidden text-yellow-400 font-bold border border-yellow-400/30 px-3 py-1 rounded">Trainer HUD</a>'
    
    if target1 in content and "nav-trainer-only" not in content:
        content = content.replace(target1, replacement1)
        modified = True
        
    # 2. Dropdown item / mobile menu item type
    target2 = '<a href="admin.html" class="nav-admin-only hidden text-yellow-400 font-bold">Manage Elite</a>'
    replacement2 = '<a href="admin.html" class="nav-admin-only hidden text-yellow-400 font-bold">Manage Elite</a>\n            <a href="trainer.html" class="nav-trainer-only hidden text-yellow-400 font-bold">Trainer HUD</a>'
    
    if target2 in content:
        occurrences = content.count(target2)
        already_done = content.count('trainer.html" class="nav-trainer-only')
        if occurrences > already_done:
            content = content.replace(target2, replacement2)
            modified = True
            
    if modified:
        with open(file_path, "w", encoding=used_encoding) as file:
            file.write(content)
        print(f"Successfully updated: {filename} using {used_encoding}")
    else:
        print(f"No changes needed or already updated: {filename}")
