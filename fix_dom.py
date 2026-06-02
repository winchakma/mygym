import os

html_files = [
    "about.html", "admin.html", "admission.html", "checkout.html", "community.html",
    "contact.html", "dashboard.html", "index.html", "membership.html",
    "profile.html", "shop.html", "studio.html", "support.html",
    "trainer.html", "vault.html", "workouts.html"
]

base_dir = r"c:\Users\user\Desktop\mygym\frontend"

for f in html_files:
    filepath = os.path.join(base_dir, f)
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
        except UnicodeDecodeError:
            try:
                with open(filepath, "r", encoding="utf-16") as file:
                    content = file.read()
            except Exception:
                with open(filepath, "r", errors="ignore") as file:
                    content = file.read()
            
        # Add remixicon in head if not present
        if "remixicon.css" not in content:
            head_idx = content.find("</head>")
            if head_idx != -1:
                content = content[:head_idx] + '  <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">\n' + content[head_idx:]

        # Add support_widget.js in body if not present
        if "support_widget.js" not in content:
            body_idx = content.find("</body>")
            if body_idx != -1:
                content = content[:body_idx] + '  <script src="js/support_widget.js"></script>\n' + content[body_idx:]

        # Try to save in UTF-8
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
            
print("Done fixing HTML files.")
