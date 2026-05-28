import os
import re

frontend_dir = r'c:\Users\user\Desktop\mygym\frontend'

# Canonical Auth Modal HTML
GOOD_AUTH_MODAL = """  <!-- GLOBAL AUTH MODAL -->
  <div id="authModal" class="modal-overlay hidden">
    <div class="modal-content glass auth-modal-inner">
      <button class="modal-close" id="closeAuthModal">&times;</button>
      
      <div class="auth-tabs">
        <button class="auth-tab active" onclick="switchTab('login')">Sign In</button>
        <button class="auth-tab" onclick="switchTab('register')">Register</button>
      </div>

      <!-- Login Form -->
      <form id="loginFormModal" class="auth-form active ajax-form" action="/api/auth/login" method="POST">
        <h2 class="modal-title">WELCOME <span>BACK</span></h2>
        <p class="modal-subtitle">Enter your elite credentials to continue.</p>
        
        <div class="form-group">
          <label class="form-label">Email or Phone Number</label>
          <input type="text" name="email" class="form-input" placeholder="you@example.com or +880..." required>
        </div>
        <div class="form-group">
          <label class="form-label">Password</label>
          <div class="relative">
            <input type="password" name="password" class="form-input pr-10" placeholder="••••••••" required>
            <button type="button" onclick="togglePassword(this)" class="absolute right-3 top-1/2 -translate-y-1/2 bg-transparent border-none cursor-pointer text-[#444] hover:text-yellow-400">👁️</button>
          </div>
        </div>
        <button type="submit" class="btn btn-yellow w-full justify-center mt-4">Sign In</button>
        <p class="auth-switch-text">Don't have an account? <a href="#" onclick="switchTab('register')">Join the Elite</a></p>
      </form>

      <!-- Register Form -->
      <form id="registerFormModal" class="auth-form ajax-form" action="/api/auth/register" method="POST">
        <input type="hidden" name="membershipType" value="FREE GUEST">
        <h2 class="modal-title">START <span>A TRIAL</span></h2>
        <p class="modal-subtitle">Join the East Blue community today.</p>
        
        <div class="grid grid-cols-2 gap-4">
          <div class="form-group">
            <label class="form-label">First Name</label>
            <input type="text" name="firstName" class="form-input" placeholder="John" required>
          </div>
          <div class="form-group">
            <label class="form-label">Last Name</label>
            <input type="text" name="lastName" class="form-input" placeholder="Doe" required>
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Phone Number</label>
          <input type="tel" name="phoneNumber" class="form-input" placeholder="+880 1XXX-XXXXXX" required>
        </div>
        <div class="form-group">
          <label class="form-label">Email Address</label>
          <input type="email" name="email" class="form-input" placeholder="you@example.com" required>
        </div>
        <div class="form-group">
          <label class="form-label">Password</label>
          <div class="relative">
            <input type="password" name="password" class="form-input pr-10" placeholder="••••••••" required>
            <button type="button" onclick="togglePassword(this)" class="absolute right-3 top-1/2 -translate-y-1/2 bg-transparent border-none cursor-pointer text-[#444] hover:text-yellow-400">👁️</button>
          </div>
        </div>
        <button type="submit" class="btn btn-yellow w-full justify-center mt-4">Create Account</button>
        <p class="auth-switch-text">Already a member? <a href="#" onclick="switchTab('login')">Sign In</a></p>
      </form>
    </div>
  </div>"""

def fix_html_files():
    for filename in os.listdir(frontend_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(frontend_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            has_auth = 'id="authModal"' in content
            has_register = 'id="registerFormModal"' in content
            
            if has_auth and not has_register:
                print(f"Fixing corrupted authModal in {filename}...")
                
                start_idx = content.find('<div id="authModal"')
                # Also try to catch the comment if it exists just before
                comment_marker = '<!-- GLOBAL AUTH MODAL -->'
                comment_idx = content.rfind(comment_marker, 0, start_idx)
                if comment_idx != -1 and (start_idx - comment_idx) < 50:
                    start_idx = comment_idx

                # Find where the broken modal should end (before the next modal or body end)
                end_idx = content.find('<div id="contactModal"', start_idx)
                if end_idx == -1:
                    end_idx = content.find('<!-- CONTACT MODAL -->', start_idx)
                if end_idx == -1:
                    end_idx = content.find('</body>', start_idx)
                
                if start_idx != -1 and end_idx != -1:
                     content = content[:start_idx] + GOOD_AUTH_MODAL + "\n\n  " + content[end_idx:]
                else:
                    print(f"Could not find boundaries for modal in {filename}")

            # Also fix forms that have class ajax-form but NO action or method
            # (Keeping this from original script but making it safer)
            def fix_form_tags(match):
                tag = match.group(0)
                if 'action=' not in tag:
                    if 'login' in tag.lower():
                        tag = tag.replace('>', ' action="/api/auth/login" method="POST">')
                    elif 'register' in tag.lower():
                        tag = tag.replace('>', ' action="/api/auth/register" method="POST">')
                    elif 'contact' in tag.lower():
                        tag = tag.replace('>', ' action="/api/contact" method="POST">')
                return tag

            content = re.sub(r'<form[^>]*?class="[^"]*?ajax-form[^"]*?"[^>]*?>', fix_form_tags, content)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    fix_html_files()
    print("HTML files fixed.")
