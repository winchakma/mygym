import os
import re

frontend_dir = r"c:\Users\user\Desktop\mygym\frontend"
html_files = [f for f in os.listdir(frontend_dir) if f.endswith(".html")]

skip_files = {"admin.html", "trainer.html", "community.html", "admission.html"}

standard_nav_links = """    <div class="nav-links">
      <a href="index.html">Home</a>
      <a href="workouts.html">Workouts</a>
      <a href="community.html" class="nav-dashboard-link hidden">Community</a>
      <a href="studio.html">Studio</a>
      <a href="shop.html">Shop</a>
      <a href="dashboard.html" class="nav-dashboard-link hidden">Dashboard</a>
      <a href="admin.html" class="nav-admin-only hidden text-yellow-400 font-bold border border-yellow-400/30 px-3 py-1 rounded">Manage Elite</a>
      <a href="trainer.html" class="nav-trainer-only hidden text-yellow-400 font-bold border border-yellow-400/30 px-3 py-1 rounded">Trainer HUD</a>
      <a href="membership.html">Membership</a>
      <a href="about.html">About</a>
    </div>"""

standard_dropdown = """        <div id="navDropdown" class="nav-dropdown">
            <a href="dashboard.html">Dashboard</a>
            <a href="community.html" class="nav-dashboard-link hidden">Community</a>
            <a href="admin.html" class="nav-admin-only hidden text-yellow-400 font-bold">Manage Elite</a>
            <a href="trainer.html" class="nav-trainer-only hidden text-yellow-400 font-bold">Trainer HUD</a>
            <a href="profile.html">Settings</a>
            <hr style="border: 0; border-top: 1px solid var(--border); margin: 8px 0;">
            <a href="#" onclick="logout()">Logout</a>
        </div>"""

standard_mobile_menu = """  <div class="mobile-menu" id="mobile-menu">
    <a href="index.html">Home</a>
    <a href="workouts.html">Workouts</a>
    <a href="community.html" class="nav-dashboard-link hidden">Community</a>
    <a href="studio.html">Studio</a>
    <a href="shop.html">Shop</a>
    <a href="dashboard.html" class="nav-dashboard-link hidden">Dashboard</a>
    <a href="profile.html" class="nav-dashboard-link hidden">Settings</a>
    <a href="admin.html" class="nav-admin-only hidden text-yellow-400 font-bold">Manage Elite</a>
    <a href="trainer.html" class="nav-trainer-only hidden text-yellow-400 font-bold">Trainer HUD</a>
    <hr class="nav-dashboard-link hidden" style="border: 0; border-top: 1px solid var(--border); margin: 8px 0; opacity: 0.2;">
    <a href="#" onclick="logout()" class="nav-dashboard-link hidden text-red-500">Logout</a>
    <a href="membership.html">Membership</a>
    <a href="about.html">About</a>
  </div>"""

for filename in html_files:
    if filename in skip_files:
        continue
        
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
    
    # 1. Replace nav-links container
    nav_links_pattern = r'[ \t]*<div class="nav-links">.*?</div>'
    if re.search(nav_links_pattern, content, re.DOTALL):
        content = re.sub(nav_links_pattern, standard_nav_links, content, flags=re.DOTALL)
        modified = True
        
    # 2. Replace dropdown container
    dropdown_pattern = r'[ \t]*<div id="navDropdown" class="nav-dropdown">.*?</div>'
    if re.search(dropdown_pattern, content, re.DOTALL):
        content = re.sub(dropdown_pattern, standard_dropdown, content, flags=re.DOTALL)
        modified = True
        
    # 3. Replace mobile menu container
    mobile_menu_pattern = r'[ \t]*<div class="mobile-menu" id="mobile-menu">.*?</div>'
    if re.search(mobile_menu_pattern, content, re.DOTALL):
        content = re.sub(mobile_menu_pattern, standard_mobile_menu, content, flags=re.DOTALL)
        modified = True
        
    if modified:
        with open(file_path, "w", encoding=used_encoding) as file:
            file.write(content)
        print(f"Normalized navigation in: {filename} ({used_encoding})")
    else:
        print(f"No navigation matches found in: {filename}")
