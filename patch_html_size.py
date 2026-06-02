import re

html_file = "frontend/checkout.html"
with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

# Replace bKash
bkash_regex = r'<img src="(data:image/png;base64,[A-Za-z0-9+/=]+)" class="h-8 object-contain" alt="bKash">'
html = re.sub(bkash_regex, r'<div class="flex gap-3">\n                <img src="\1" class="h-10 object-contain" alt="bKash">\n              </div>', html)

# Replace Nagad
nagad_regex = r'<img src="(data:image/png;base64,[A-Za-z0-9+/=]+)" class="h-8 object-contain" alt="Nagad">'
html = re.sub(nagad_regex, r'<div class="flex gap-3">\n                <img src="\1" class="h-10 object-contain" alt="Nagad">\n              </div>', html)

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

print("checkout.html patched sizing successfully.")
