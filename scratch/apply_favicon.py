import os
import re

favicon_tag = '  <link rel="icon" type="image/png" href="img/favicon.png"/>\n'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'rel="icon"' in content:
        print(f"Skipping {filepath} (favicon already exists)")
        return

    # Insert before </head> or after a common meta/link tag
    if '</head>' in content:
        new_content = content.replace('</head>', f'{favicon_tag}</head>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        print(f"Warning: No </head> tag found in {filepath}")

frontend_dir = 'frontend'
for filename in os.listdir(frontend_dir):
    if filename.endswith('.html'):
        process_file(os.path.join(frontend_dir, filename))
