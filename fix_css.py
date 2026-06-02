import re

with open('frontend/js/script.js', 'r', encoding='utf-8') as f:
    script_content = f.read()

style_match = re.search(r'<style>(.*?)</style>', script_content, re.DOTALL)
if style_match:
    style_css = style_match.group(0)
    
    for filename in ['frontend/admin.html', 'frontend/trainer.html']:
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()
            
        if '/* ai-support-fab styles */' not in html:
            html = html.replace('<!-- Admin Support Floating Widget -->', style_css + '\n    <!-- Admin Support Floating Widget -->\n    <style>/* ai-support-fab styles */</style>')
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'Updated {filename}')
