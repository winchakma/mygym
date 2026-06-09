import os, glob

frontend_dir = r'c:\Users\user\Desktop\mygym\frontend'
forgot_link = '''        <div style="text-align:right;margin-top:-6px;">
          <a href="#" onclick="forgotPassword(event)" style="font-size:12px;color:var(--muted);font-family:var(--font-sub);letter-spacing:1px;">Forgot Password?</a>
        </div>
'''

count = 0
for filepath in glob.glob(os.path.join(frontend_dir, '*.html')):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    idx_login_modal = content.find('id="loginFormModal"')
    if idx_login_modal != -1:
        end_idx = content.find('id="registerFormModal"', idx_login_modal)
        modal_content = content[idx_login_modal:end_idx] if end_idx != -1 else content[idx_login_modal:]
        
        if 'forgotPassword(event)' not in modal_content:
            pwd_end = content.find('</div>\n        </div>', idx_login_modal)
            if pwd_end != -1 and pwd_end < (end_idx if end_idx != -1 else len(content)):
                insert_pos = pwd_end + len('</div>\n        </div>')
                new_content = content[:insert_pos] + '\n' + forgot_link + content[insert_pos:]
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
                print(f'Updated {os.path.basename(filepath)}')

print(f'Total files updated: {count}')
