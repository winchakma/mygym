import sys
from html.parser import HTMLParser

class HTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.ignore_tags = {'img', 'input', 'br', 'hr', 'meta', 'link', 'source', 'area', 'base', 'col', 'embed', 'param', 'track', 'wbr'}

    def handle_starttag(self, tag, attrs):
        if tag not in self.ignore_tags:
            line, col = self.getpos()
            self.stack.append((tag, line, col))

    def handle_endtag(self, tag):
        if tag in self.ignore_tags:
            return
        if not self.stack:
            line, col = self.getpos()
            self.errors.append(f"Unexpected closing tag </{tag}> at line {line}, col {col} (no open tags in stack)")
            return
        
        last_tag, line, col = self.stack.pop()
        if last_tag != tag:
            curr_line, curr_col = self.getpos()
            self.errors.append(f"Mismatched closing tag </{tag}> at line {curr_line}, col {curr_col}. Expected </{last_tag}> (opened at line {line}, col {col})")

def validate_file(filepath):
    validator = HTMLValidator()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        validator.feed(content)
        
        # Check for unclosed tags
        if validator.stack:
            print("\n🚨 Unclosed tags found in hierarchy stack:")
            for tag, line, col in reversed(validator.stack):
                print(f"  - <{tag}> opened at line {line}, col {col}")
        
        if validator.errors:
            print("\n🚨 Syntax and Tag Mismatch Errors:")
            for err in validator.errors:
                print(f"  - {err}")
                
        if not validator.stack and not validator.errors:
            print("\n✅ HTML Tag Structure is 100% syntactically perfect! No unclosed or mismatched tags.")
            
    except Exception as e:
        print(f"Error reading or parsing file: {e}")

if __name__ == '__main__':
    validate_file(r"c:\Users\user\Desktop\mygym\frontend\community.html")
