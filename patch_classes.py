import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new grid HTML
new_grid = """
      <div class="flex flex-wrap justify-center gap-6 w-full mt-10">
        
        <!-- Card 1: Pilates -->
        <div class="w-full sm:w-[calc(50%-12px)] lg:w-[calc(25%-18px)] max-w-[380px] group relative overflow-hidden rounded-[24px] cursor-pointer bg-[#0a0a0a] border border-white/5 aspect-[3/4] flex flex-col shadow-2xl">
          <img src="img/pilates.jpg" loading="lazy" class="absolute inset-0 w-full h-full object-cover z-0 transition-transform duration-1000 group-hover:scale-110 filter grayscale brightness-50 group-hover:grayscale-0 group-hover:brightness-75 transform-gpu" style="will-change: transform, filter;" />
          <div class="absolute inset-0 bg-gradient-to-b from-[#050505]/90 via-[#050505]/40 to-[#050505] z-10 transition-opacity duration-500 group-hover:opacity-80"></div>
          <div class="relative z-20 p-6 flex flex-col h-full justify-between">
            <div class="flex justify-between items-start">
              <div>
                <div class="text-[#9b5de5] font-black text-3xl tracking-tighter drop-shadow-lg">3 PM</div>
                <div class="text-[9px] text-white/50 uppercase font-black tracking-[3px] mt-1">High Intensity</div>
              </div>
              <div class="w-10 h-10 rounded-full bg-white/10 backdrop-blur-md flex items-center justify-center text-sm group-hover:bg-[#9b5de5] transition-colors duration-300">
                <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m14.31 8 5.74 9.94M9.69 8h11.48M7.38 12l5.74-9.94M9.69 16 3.95 6.06M14.31 16H2.83M16.62 12l-5.74 9.94"/></svg>
              </div>
            </div>
            <div class="mt-auto transform transition-transform duration-500 group-hover:-translate-y-2">
              <div class="text-[10px] text-[#9b5de5] font-bold uppercase tracking-[4px] mb-2">Pilates</div>
              <h3 class="text-4xl font-black italic text-white leading-[1] uppercase mb-2 drop-shadow-md">PILATES</h3>
              <p class="text-[12px] text-white/60 font-medium mb-8">Led by <span class="text-white">mia</span></p>
              <a href="workouts.html" class="block text-center w-full py-4 px-4 bg-white/10 backdrop-blur-md rounded-xl text-[10px] text-white font-black uppercase tracking-[3px] transition-all duration-300 border border-white/10 shadow-lg group-hover:bg-[#9b5de5] group-hover:text-black group-hover:border-transparent">Book Session</a>
            </div>
          </div>
        </div>

        <!-- Card 2: Recovery -->
        <div class="w-full sm:w-[calc(50%-12px)] lg:w-[calc(25%-18px)] max-w-[380px] group relative overflow-hidden rounded-[24px] cursor-pointer bg-[#0a0a0a] border border-white/5 aspect-[3/4] flex flex-col shadow-2xl">
          <img src="img/recovery.jpg" loading="lazy" class="absolute inset-0 w-full h-full object-cover z-0 transition-transform duration-1000 group-hover:scale-110 filter grayscale brightness-50 group-hover:grayscale-0 group-hover:brightness-75 transform-gpu" style="will-change: transform, filter;" />
          <div class="absolute inset-0 bg-gradient-to-b from-[#050505]/90 via-[#050505]/40 to-[#050505] z-10 transition-opacity duration-500 group-hover:opacity-80"></div>
          <div class="relative z-20 p-6 flex flex-col h-full justify-between">
            <div class="flex justify-between items-start">
              <div>
                <div class="text-[#2a9d8f] font-black text-3xl tracking-tighter drop-shadow-lg">7 PM</div>
                <div class="text-[9px] text-white/50 uppercase font-black tracking-[3px] mt-1">High Intensity</div>
              </div>
              <div class="w-10 h-10 rounded-full bg-white/10 backdrop-blur-md flex items-center justify-center text-sm group-hover:bg-[#2a9d8f] transition-colors duration-300">
                <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>
              </div>
            </div>
            <div class="mt-auto transform transition-transform duration-500 group-hover:-translate-y-2">
              <div class="text-[10px] text-[#2a9d8f] font-bold uppercase tracking-[4px] mb-2">Recovery</div>
              <h3 class="text-4xl font-black italic text-white leading-[1] uppercase mb-2 drop-shadow-md">RECOVERY</h3>
              <p class="text-[12px] text-white/60 font-medium mb-8">Led by <span class="text-white">manson</span></p>
              <a href="workouts.html" class="block text-center w-full py-4 px-4 bg-white/10 backdrop-blur-md rounded-xl text-[10px] text-white font-black uppercase tracking-[3px] transition-all duration-300 border border-white/10 shadow-lg group-hover:bg-[#2a9d8f] group-hover:text-black group-hover:border-transparent">Book Session</a>
            </div>
          </div>
        </div>

        <!-- Card 3: Yoga -->
        <div class="w-full sm:w-[calc(50%-12px)] lg:w-[calc(25%-18px)] max-w-[380px] group relative overflow-hidden rounded-[24px] cursor-pointer bg-[#0a0a0a] border border-white/5 aspect-[3/4] flex flex-col shadow-2xl">
          <img src="img/yoga.jpg" loading="lazy" class="absolute inset-0 w-full h-full object-cover z-0 transition-transform duration-1000 group-hover:scale-110 filter grayscale brightness-50 group-hover:grayscale-0 group-hover:brightness-75 transform-gpu" style="will-change: transform, filter;" />
          <div class="absolute inset-0 bg-gradient-to-b from-[#050505]/90 via-[#050505]/40 to-[#050505] z-10 transition-opacity duration-500 group-hover:opacity-80"></div>
          <div class="relative z-20 p-6 flex flex-col h-full justify-between">
            <div class="flex justify-between items-start">
              <div>
                <div class="text-[#f4a261] font-black text-3xl tracking-tighter drop-shadow-lg">8 AM</div>
                <div class="text-[9px] text-white/50 uppercase font-black tracking-[3px] mt-1">High Intensity</div>
              </div>
              <div class="w-10 h-10 rounded-full bg-white/10 backdrop-blur-md flex items-center justify-center text-sm group-hover:bg-[#f4a261] transition-colors duration-300">
                <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
              </div>
            </div>
            <div class="mt-auto transform transition-transform duration-500 group-hover:-translate-y-2">
              <div class="text-[10px] text-[#f4a261] font-bold uppercase tracking-[4px] mb-2">Yoga</div>
              <h3 class="text-4xl font-black italic text-white leading-[1] uppercase mb-2 drop-shadow-md">YOGA</h3>
              <p class="text-[12px] text-white/60 font-medium mb-8">Led by <span class="text-white">sarah</span></p>
              <a href="workouts.html" class="block text-center w-full py-4 px-4 bg-white/10 backdrop-blur-md rounded-xl text-[10px] text-white font-black uppercase tracking-[3px] transition-all duration-300 border border-white/10 shadow-lg group-hover:bg-[#f4a261] group-hover:text-black group-hover:border-transparent">Book Session</a>
            </div>
          </div>
        </div>

        <!-- Card 4: Boxing -->
        <div class="w-full sm:w-[calc(50%-12px)] lg:w-[calc(25%-18px)] max-w-[380px] group relative overflow-hidden rounded-[24px] cursor-pointer bg-[#0a0a0a] border border-white/5 aspect-[3/4] flex flex-col shadow-2xl">
          <img src="img/boxing.jpg" loading="lazy" class="absolute inset-0 w-full h-full object-cover z-0 transition-transform duration-1000 group-hover:scale-110 filter grayscale brightness-50 group-hover:grayscale-0 group-hover:brightness-75 transform-gpu" style="will-change: transform, filter;" />
          <div class="absolute inset-0 bg-gradient-to-b from-[#050505]/90 via-[#050505]/40 to-[#050505] z-10 transition-opacity duration-500 group-hover:opacity-80"></div>
          <div class="relative z-20 p-6 flex flex-col h-full justify-between">
            <div class="flex justify-between items-start">
              <div>
                <div class="text-[#e63946] font-black text-3xl tracking-tighter drop-shadow-lg">12 PM</div>
                <div class="text-[9px] text-white/50 uppercase font-black tracking-[3px] mt-1">High Intensity</div>
              </div>
              <div class="w-10 h-10 rounded-full bg-white/10 backdrop-blur-md flex items-center justify-center text-sm group-hover:bg-[#e63946] transition-colors duration-300">
                <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
              </div>
            </div>
            <div class="mt-auto transform transition-transform duration-500 group-hover:-translate-y-2">
              <div class="text-[10px] text-[#e63946] font-bold uppercase tracking-[4px] mb-2">Boxing</div>
              <h3 class="text-4xl font-black italic text-white leading-[1] uppercase mb-2 drop-shadow-md">BOXING</h3>
              <p class="text-[12px] text-white/60 font-medium mb-8">Led by <span class="text-white">alex</span></p>
              <a href="workouts.html" class="block text-center w-full py-4 px-4 bg-white/10 backdrop-blur-md rounded-xl text-[10px] text-white font-black uppercase tracking-[3px] transition-all duration-300 border border-white/10 shadow-lg group-hover:bg-[#e63946] group-hover:text-black group-hover:border-transparent">Book Session</a>
            </div>
          </div>
        </div>

        <!-- Card 5: Cycling -->
        <div class="w-full sm:w-[calc(50%-12px)] lg:w-[calc(25%-18px)] max-w-[380px] group relative overflow-hidden rounded-[24px] cursor-pointer bg-[#0a0a0a] border border-white/5 aspect-[3/4] flex flex-col shadow-2xl">
          <img src="img/cycling.jpg" loading="lazy" class="absolute inset-0 w-full h-full object-cover z-0 transition-transform duration-1000 group-hover:scale-110 filter grayscale brightness-50 group-hover:grayscale-0 group-hover:brightness-75 transform-gpu" style="will-change: transform, filter;" />
          <div class="absolute inset-0 bg-gradient-to-b from-[#050505]/90 via-[#050505]/40 to-[#050505] z-10 transition-opacity duration-500 group-hover:opacity-80"></div>
          <div class="relative z-20 p-6 flex flex-col h-full justify-between">
            <div class="flex justify-between items-start">
              <div>
                <div class="text-[#457b9d] font-black text-3xl tracking-tighter drop-shadow-lg">10 AM</div>
                <div class="text-[9px] text-white/50 uppercase font-black tracking-[3px] mt-1">High Intensity</div>
              </div>
              <div class="w-10 h-10 rounded-full bg-white/10 backdrop-blur-md flex items-center justify-center text-sm group-hover:bg-[#457b9d] transition-colors duration-300">
                <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.14 12a7.14 7.14 0 0 0-7.14-7.14"/><path d="M4.86 12a7.14 7.14 0 0 0 7.14 7.14"/><path d="m17.05 17.05-5.05-5.05"/><path d="m6.95 6.95 5.05 5.05"/></svg>
              </div>
            </div>
            <div class="mt-auto transform transition-transform duration-500 group-hover:-translate-y-2">
              <div class="text-[10px] text-[#457b9d] font-bold uppercase tracking-[4px] mb-2">Cycling</div>
              <h3 class="text-4xl font-black italic text-white leading-[1] uppercase mb-2 drop-shadow-md">CYCLING</h3>
              <p class="text-[12px] text-white/60 font-medium mb-8">Led by <span class="text-white">david</span></p>
              <a href="workouts.html" class="block text-center w-full py-4 px-4 bg-white/10 backdrop-blur-md rounded-xl text-[10px] text-white font-black uppercase tracking-[3px] transition-all duration-300 border border-white/10 shadow-lg group-hover:bg-[#457b9d] group-hover:text-black group-hover:border-transparent">Book Session</a>
            </div>
          </div>
        </div>

      </div>
"""

# Extract the part we want to replace
start_idx = content.find('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">')
end_idx = content.find('</div>\\n    </div>\\n  </div>\\n\\n  <section class="section-full bmi-section')

if start_idx != -1 and end_idx != -1:
    # the end_idx will be the closing div of the old grid container and section
    # Let's be more precise
    old_grid_end = content.find('</div>\\n      </div>\\n    </div>\\n  </div>\\n\\n  <section class="section-full bmi-section')
    # Actually, let's just find the closing </div> of the <div class="grid..."> element.
    # The grid has 4 cards. We can use a simpler replacement strategy.
    
    # We will replace from <div class="grid grid-cols-1... "> down to the </div> that closes it.
    
    # Find start
    grid_start = content.find('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">')
    
    # Find end: The grid ends right before:
    #       </div>
    #     </div>
    #   </div>
    #
    #   <section class="section-full bmi-section
    
    bmi_start = content.find('<section class="section-full bmi-section')
    
    # Let's replace the whole chunk between grid_start and the closing divs before bmi_start.
    # We just need to replace the grid block itself. 
    
    # Regex approach for replacing the grid
    pattern = re.compile(r'<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">.*?</div>\s*</div>\s*</div>\s*<section class="section-full bmi-section', re.DOTALL)
    
    new_content = content[:grid_start] + new_grid + "\\n    </div>\\n  </div>\\n\\n  <section class=\"section-full bmi-section" + content[bmi_start + len('<section class="section-full bmi-section'):]
    
    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Replaced old classes grid with new glassmorphism cards!")
else:
    print("Could not find the target grid block in index.html")
