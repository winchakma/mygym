import os
import re

frontend_dir = r"c:\Users\user\Desktop\mygym\frontend"

tubes_html_pattern = re.compile(r'\s*<!-- TUBES INTERACTIVE BACKGROUND -->\s*<div class="tubes-bg-container">\s*<canvas id="tubesCanvas" class="tubes-canvas"></canvas>\s*<div class="tubes-bg-overlay"></div>\s*</div>\s*', re.IGNORECASE)

tubes_script_pattern = re.compile(r'\s*<script type="module">\s*import TubesCursor from \'https://cdn\.jsdelivr\.net/npm/threejs-components@0\.0\.19/build/cursors/tubes1\.min\.js\';.*?</script>\s*', re.IGNORECASE | re.DOTALL)

for filename in os.listdir(frontend_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(frontend_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                enc = 'utf-8'
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='utf-16') as f:
                content = f.read()
                enc = 'utf-16'

        changed = False
        
        if tubes_html_pattern.search(content):
            content = tubes_html_pattern.sub('\n', content)
            changed = True
            
        if tubes_script_pattern.search(content):
            content = tubes_script_pattern.sub('\n', content)
            changed = True
            
        if changed:
            with open(filepath, 'w', encoding=enc) as f:
                f.write(content)
            print(f"Removed tubes from {filename}")
