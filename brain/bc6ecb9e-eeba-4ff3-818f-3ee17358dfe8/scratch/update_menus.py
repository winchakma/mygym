import os
import re

new_menu = """  <div class="mobile-menu" id="mobile-menu">
    <a href="index.html">Home</a>
    <a href="classes.html">Classes</a>
    <a href="activity.html">Activity</a>
    <a href="studio.html">Studio</a>
    <a href="shop.html">Shop</a>
    <a href="demo.html" class="text-yellow-400 font-bold">Demo HUD</a>
    <a href="dashboard.html" class="nav-dashboard-link hidden">Dashboard</a>
    <a href="profile.html" class="nav-dashboard-link hidden">Settings</a>
    <a href="admin.html" class="nav-admin-only hidden text-yellow-400 font-bold">Manage Elite</a>
    <hr class="nav-dashboard-link hidden" style="border: 0; border-top: 1px solid var(--border); margin: 8px 0; opacity: 0.2;">
    <a href="#" onclick="logout()" class="nav-dashboard-link hidden text-red-500">Logout</a>
    <a href="membership.html">Membership</a>
    <a href="about.html">About</a>
  </div>"""

frontend_dir = r"c:\Users\user\Desktop\mygym\frontend"

# Regex to find the mobile-menu div block
# It usually starts with <div class="mobile-menu" id="mobile-menu"> and ends with </div>
menu_regex = re.compile(r'    <div class="mobile-menu" id="mobile-menu">.*?  </div>', re.DOTALL)

for filename in os.listdir(frontend_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(frontend_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "mobile-menu" in content:
            new_content = menu_regex.sub(new_menu, content)
            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {filename}")
            else:
                print(f"No match for regex in {filename}")
        else:
            print(f"Skipped {filename} (no mobile-menu div)")
