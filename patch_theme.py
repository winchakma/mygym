import os
import re

css_file = "frontend/css/style.css"
with open(css_file, "r", encoding="utf-8") as f:
    css = f.read()

# 1. Update CSS Variables
if "--teal:" not in css:
    css = css.replace("--red:   #e8392a;", """--red:   #e63946;
  --teal:  #2a9d8f;
  --purple: #9b5de5;
  --blue:  #457b9d;
  --orange: #f4a261;""")

# 2. Add colored tag variants in CSS if missing
if ".card-tag-teal" not in css:
    tags_css = """
.card-tag-teal { background: rgba(42, 157, 143, 0.15); color: var(--teal); border: 1px solid rgba(42, 157, 143, 0.3); }
.card-tag-purple { background: rgba(155, 93, 229, 0.15); color: var(--purple); border: 1px solid rgba(155, 93, 229, 0.3); }
.card-tag-orange { background: rgba(244, 162, 97, 0.15); color: var(--orange); border: 1px solid rgba(244, 162, 97, 0.3); }
.card-tag-blue { background: rgba(69, 123, 157, 0.15); color: var(--blue); border: 1px solid rgba(69, 123, 157, 0.3); }
"""
    css = css.replace(".card-tag-red {", tags_css + "\n.card-tag-red {")

with open(css_file, "w", encoding="utf-8") as f:
    f.write(css)


def patch_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    original = html

    # Replace basic cards with premium dark glass
    html = html.replace('background:var(--card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:22px;', 'class="glass-panel" style="background: rgba(255,255,255,0.03); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05); border-radius: 24px; padding: 32px; box-shadow: 0 20px 40px rgba(0,0,0,0.4); transition: transform 0.3s;" onmouseover="this.style.transform=\'translateY(-5px)\'; this.style.borderColor=\'rgba(255,255,255,0.15)\'" onmouseout="this.style.transform=\'translateY(0)\'; this.style.borderColor=\'rgba(255,255,255,0.05)\'"')
    
    html = html.replace('class="card"', 'class="card glass-premium"')
    html = html.replace('class="card card-delay-1"', 'class="card card-delay-1 glass-premium"')
    html = html.replace('class="card card-delay-2"', 'class="card card-delay-2 glass-premium"')
    
    # Dashboard / Admin / Trainer generic panel replacements
    # E.g. bg-[#111] -> bg-white/5 backdrop-blur-md
    html = html.replace('bg-[#111]', 'bg-white/5 backdrop-blur-md border border-white/5 shadow-2xl')
    html = html.replace('bg-[#1a1a1a]', 'bg-white/10 backdrop-blur-md border border-white/10 shadow-2xl')
    html = html.replace('bg-black', 'bg-[#050505]')
    
    # Inject varied colors for tags and highlights instead of just yellow
    # Replace some specific instances to introduce variety
    
    # Write back if changed
    if html != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Patched {filepath}")

# Update index.html specific sections
with open("frontend/index.html", "r", encoding="utf-8") as f:
    index = f.read()

# Replace the 4 boring divs with modality cards
old_cards = r'<div class="grid grid-cols-1 sm:grid-cols-2 gap-5 mt-9">.*?</div>\s*</div>\s*<div class="mt-40">'
new_cards = """<div class="modality-grid mt-9">
        <!-- Cardio -->
        <div class="modality-card" onclick="window.location.href='workouts.html'">
          <img src="img/cardio-bg.jpg" alt="Cardio & HIIT" class="modality-bg" onerror="this.src='https://images.unsplash.com/photo-1518611012118-696072aa579a?w=800&q=80'">
          <div class="modality-overlay"></div>
          <div class="modality-content">
            <div class="modality-icon" style="color: var(--orange)">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"/></svg>
            </div>
            <h3 class="modality-title">Cardio</h3>
            <p class="modality-desc">Intense cardiovascular conditioning to maximize calorie burn and endurance.</p>
            <span class="modality-btn" style="color: var(--orange)">Explore</span>
          </div>
        </div>

        <!-- Strength -->
        <div class="modality-card" onclick="window.location.href='workouts.html'">
          <img src="img/strength-bg.jpg" alt="Strength & Power" class="modality-bg" onerror="this.src='https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800&q=80'">
          <div class="modality-overlay"></div>
          <div class="modality-content">
            <div class="modality-icon" style="color: var(--teal)">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.4 14.4 9.6 9.6"/><path d="M18.65 21.35a2 2 0 0 1-2.83 0l-5.66-5.66a2 2 0 0 1 0-2.83l.06-.06a2 2 0 0 1 2.83 0l5.66 5.66a2 2 0 0 1 0 2.83Z"/><path d="m2 2 2.83 2.83"/><path d="m22 22-2.83-2.83"/><path d="M5.35 2.65a2 2 0 0 1 2.83 0l5.66 5.66a2 2 0 0 1 0 2.83l-.06.06a2 2 0 0 1-2.83 0L5.35 5.48a2 2 0 0 1 0-2.83Z"/></svg>
            </div>
            <h3 class="modality-title">Full Body</h3>
            <p class="modality-desc">Comprehensive strength and mobility movements to build full-body power.</p>
            <span class="modality-btn" style="color: var(--teal)">Explore</span>
          </div>
        </div>

        <!-- Combat -->
        <div class="modality-card" onclick="window.location.href='workouts.html'">
          <img src="img/combat-bg.jpg" alt="Combat" class="modality-bg" onerror="this.src='https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?w=800&q=80'">
          <div class="modality-overlay"></div>
          <div class="modality-content">
            <div class="modality-icon" style="color: var(--red)">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
            </div>
            <h3 class="modality-title">Boxing</h3>
            <p class="modality-desc">High-intensity boxing and striking for speed, agility, and elite conditioning.</p>
            <span class="modality-btn" style="color: var(--red)">Explore</span>
          </div>
        </div>

        <!-- Recovery -->
        <div class="modality-card" onclick="window.location.href='workouts.html'">
          <img src="img/recovery-bg.jpg" alt="Recovery" class="modality-bg" onerror="this.src='https://images.unsplash.com/photo-1552286450-4a669f80e0ae?w=800&q=80'">
          <div class="modality-overlay"></div>
          <div class="modality-content">
            <div class="modality-icon" style="color: var(--purple)">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
            </div>
            <h3 class="modality-title">Recovery</h3>
            <p class="modality-desc">Dedicated recovery sessions to restore and rebuild.</p>
            <span class="modality-btn" style="color: var(--purple)">Explore</span>
          </div>
        </div>
      </div>
      <div class="mt-40">"""
import re
index = re.sub(old_cards, new_cards, index, flags=re.DOTALL)

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(index)
print("Patched index.html specific layout")

for f in os.listdir("frontend"):
    if f.endswith(".html"):
        patch_file(os.path.join("frontend", f))

print("All files patched successfully.")
