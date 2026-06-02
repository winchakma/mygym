import re

html_file = "frontend/workouts.html"
with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

# Fix Monday hidden issue: replace justify-center with justify-start md:justify-center
html = html.replace('class="flex items-center justify-center gap-3 overflow-x-auto pb-4 hide-scrollbar w-full"', 'class="flex items-center justify-start md:justify-center gap-3 overflow-x-auto pb-4 hide-scrollbar w-full"')

# Fix card onclick issue: remove card.onclick and add to button
html = re.sub(r'card\.onclick = \(\) => bookClass\(c\.id, c\.name, c\.time, c\.trainer\);', '', html)

# Add onclick to button
button_search = r'<button class="w-full py-4 px-4 bg-white/10 backdrop-blur-md rounded-xl text-\[10px\] text-white font-black uppercase tracking-\[3px\] group-hover:bg-\$\{accentColor\} group-hover:text-black transition-all duration-300 border border-white/10 group-hover:border-transparent shadow-lg">'
button_replace = r'<button onclick="bookClass(\'${c.id}\', \'${c.name}\', \'${c.time}\', \'${c.trainer}\')" class="w-full py-4 px-4 bg-white/10 backdrop-blur-md rounded-xl text-[10px] text-white font-black uppercase tracking-[3px] group-hover:bg-${accentColor} group-[.is-active]:bg-${accentColor} group-hover:text-black group-[.is-active]:text-black transition-all duration-300 border border-white/10 group-hover:border-transparent group-[.is-active]:border-transparent shadow-lg">'
html = html.replace(button_search, button_replace)

# Add group-[.is-active]: equivalents for all group-hover
html = html.replace('group-hover:scale-110', 'group-hover:scale-110 group-[.is-active]:scale-110')
html = html.replace('group-hover:grayscale-0', 'group-hover:grayscale-0 group-[.is-active]:grayscale-0')
html = html.replace('group-hover:brightness-75', 'group-hover:brightness-75 group-[.is-active]:brightness-75')
html = html.replace('group-hover:opacity-80', 'group-hover:opacity-80 group-[.is-active]:opacity-80')
html = html.replace('group-hover:bg-${accentColor}', 'group-hover:bg-${accentColor} group-[.is-active]:bg-${accentColor}')
html = html.replace('group-hover:-translate-y-2', 'group-hover:-translate-y-2 group-[.is-active]:-translate-y-2')

# Add IntersectionObserver
observer_script = """
      // Intersection Observer for mobile scroll highlighting
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (window.innerWidth < 1024) {
            if (entry.isIntersecting) {
              entry.target.classList.add('is-active');
            } else {
              entry.target.classList.remove('is-active');
            }
          }
        });
      }, { threshold: 0.6 });

      // After rendering schedule, observe cards
      const originalRender = renderSchedule;
      renderSchedule = function() {
        originalRender();
        document.querySelectorAll('.group.relative.overflow-hidden').forEach(card => observer.observe(card));
      };
"""

# Inject observer script before fetchClasses()
html = html.replace('fetchClasses();', observer_script + '\n      fetchClasses();')

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

print("workouts.html patched successfully.")
