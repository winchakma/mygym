import re

with open("logos.txt", "r") as f:
    lines = f.read().split("\n")
    bkash_b64 = lines[0].strip()
    nagad_b64 = lines[2].strip() if len(lines) > 2 else lines[1].strip()

html_file = "frontend/checkout.html"
with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

# Replace bKash
bkash_regex = r'<div class="px-3 py-1 rounded bg-\[#E2136E\]">\s*<span class="text-white font-black italic tracking-wider text-xs">bKash</span>\s*</div>'
bkash_img = f'<img src="{bkash_b64}" class="h-8 object-contain" alt="bKash">'
html = re.sub(bkash_regex, bkash_img, html)

# Replace Nagad
nagad_regex = r'<div class="px-3 py-1 rounded bg-\[#ED1C24\]">\s*<span class="text-white font-black italic tracking-wider text-xs">Nagad</span>\s*</div>'
nagad_img = f'<img src="{nagad_b64}" class="h-8 object-contain" alt="Nagad">'
html = re.sub(nagad_regex, nagad_img, html)

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

print("checkout.html patched with base64 logos successfully.")
