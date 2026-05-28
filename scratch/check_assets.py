import os
import re

def check_local_assets(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all src="..." and href="..."
    links = re.findall(r'(?:src|href)="([^"]+)"', content)
    
    frontend_dir = 'frontend'
    broken = []
    
    for link in links:
        # Skip external links and data URIs
        if link.startswith('http') or link.startswith('//') or link.startswith('data:'):
            continue
        
        # Skip hashes and mailto/tel
        if link.startswith('#') or link.startswith('mailto:') or link.startswith('tel:'):
            continue
            
        # Clean query params and hashes
        path = link.split('?')[0].split('#')[0]
        
        # Skip template literals and empty paths
        if not path or '${' in path:
            continue
        full_path = os.path.join(frontend_dir, path)
        if not os.path.exists(full_path):
            broken.append(link)
            
    return broken

frontend_dir = 'frontend'
all_broken = {}
for filename in os.listdir(frontend_dir):
    if filename.endswith('.html'):
        broken = check_local_assets(os.path.join(frontend_dir, filename))
        if broken:
            all_broken[filename] = list(set(broken))

if all_broken:
    print("Found broken local assets:")
    for file, assets in all_broken.items():
        print(f"  {file}:")
        for asset in assets:
            print(f"    - {asset}")
else:
    print("No broken local assets found!")
