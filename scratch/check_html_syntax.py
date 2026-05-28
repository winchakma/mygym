import sys
import re

def check_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Remove script and style tags content for pure HTML tag matching
    clean_html = re.sub(r'<script\b[^>]*>([\s\S]*?)<\/script>', '<script></script>', html)
    clean_html = re.sub(r'<style\b[^>]*>([\s\S]*?)<\/style>', '<style></style>', clean_html)

    # Simple tag parser
    tag_pattern = re.compile(r'<(\/?[a-zA-Z0-9:-]+)(?:\s+[^>]*)?>')
    stack = []
    errors = []
    
    # Void/self-closing tags in HTML5
    void_tags = {'img', 'input', 'br', 'hr', 'meta', 'link', 'source', 'area', 'base', 'col', 'embed', 'param', 'track', 'wbr'}

    for match in tag_pattern.finditer(clean_html):
        tag_name = match.group(1)
        # Get line number of match
        pos = match.start()
        line = html.count('\n', 0, pos) + 1
        
        if tag_name.startswith('/'):
            # Closing tag
            tag_name = tag_name[1:].lower()
            if tag_name in void_tags:
                continue
            if not stack:
                errors.append(f"Unexpected closing tag </{tag_name}> at line {line}")
            else:
                last_tag, last_line = stack.pop()
                if last_tag != tag_name:
                    errors.append(f"Mismatched closing tag </{tag_name}> at line {line}. Expected </{last_tag}> (opened at line {last_line})")
        else:
            # Opening tag
            tag_name = tag_name.lower()
            if tag_name in void_tags or tag_name.endswith('/'):
                continue
            stack.append((tag_name, line))

    if stack:
        print("\n🚨 Unclosed tags left in stack:")
        for tag, line in reversed(stack):
            print(f"  - <{tag}> opened at line {line}")
            
    if errors:
        print("\n🚨 Mismatched tag errors:")
        for err in errors:
            print(f"  - {err}")
            
    if not stack and not errors:
        print("\n✅ HTML Tag nesting is 100% clean and perfect!")

if __name__ == '__main__':
    check_html(r"c:\Users\user\Desktop\mygym\frontend\community.html")
