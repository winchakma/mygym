import os
import re

frontend_dir = 'frontend'
html_files = [f for f in os.listdir(frontend_dir) if f.endswith('.html')]
js_files = [f for f in os.listdir(os.path.join(frontend_dir, 'js')) if f.endswith('.js')]

onclick_pattern = re.compile(r'onclick=[\'\"]([a-zA-Z0-9_]+)\(')
defined_functions = set()
missing_map = {}

for js_file in js_files:
    with open(os.path.join(frontend_dir, 'js', js_file), 'r', errors='ignore') as f:
        content = f.read()
        defined_functions.update(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', content))
        defined_functions.update(re.findall(r'const\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>', content))
        defined_functions.update(re.findall(r'let\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>', content))
        defined_functions.update(re.findall(r'var\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>', content))

for html_file in html_files:
    with open(os.path.join(frontend_dir, html_file), 'r', errors='ignore') as f:
        content = f.read()
        defined_functions.update(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', content))
        defined_functions.update(re.findall(r'const\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>', content))
        called = set(onclick_pattern.findall(content))
        for c in called:
            if c not in missing_map:
                missing_map[c] = set()
            missing_map[c].add(html_file)

print('--- Missing Function Locations ---')
count = 0
for m, files in sorted(missing_map.items()):
    if m not in defined_functions:
        count += 1
        print(f'- {m}() is missing in: {", ".join(files)}')
print(f'TOTAL BROKEN BUTTONS: {count}')
