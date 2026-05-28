import os
import re

frontend_dir = r'c:\Users\user\Desktop\mygym\frontend'

def clean_html_attributes():
    for filename in os.listdir(frontend_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(frontend_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Fix duplicate action and method attributes in <form> tags
            # Replace multiple occurrences of action="..." with just one
            content = re.sub(r'(action="/api/auth/login"\s*){2,}', r'action="/api/auth/login" ', content)
            content = re.sub(r'(method="POST"\s*){2,}', r'method="POST" ', content)
            
            # General cleanup for any duplicated attributes in form
            def cleanup_form(match):
                tag = match.group(0)
                # Split by space but preserve quoted strings
                attrs = re.findall(r'[a-zA-Z-]+="[^"]*"', tag)
                unique_attrs = []
                seen_keys = set()
                for attr in attrs:
                    key = attr.split('=')[0]
                    if key not in seen_keys:
                        unique_attrs.append(attr)
                        seen_keys.add(key)
                
                # Reconstruct the tag
                base_tag = re.search(r'<form[^>]*?id="([^"]*)"[^>]*?class="([^"]*)"', tag)
                if base_tag:
                    id_val = base_tag.group(1)
                    class_val = base_tag.group(2)
                    other_attrs = " ".join([a for a in unique_attrs if 'id=' not in a and 'class=' not in a])
                    return f'<form id="{id_val}" class="{class_val}" {other_attrs}>'
                return tag

            content = re.sub(r'<form[^>]*?>', cleanup_form, content)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    clean_html_attributes()
    print("HTML attributes cleaned.")
