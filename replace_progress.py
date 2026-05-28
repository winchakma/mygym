import re

with open('frontend/admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

new_progress_section = """        <!-- Performance Hub (Detail View) -->
        <div id="section-progress" class="admin-section hidden">
            <div class="flex items-center gap-4 mb-10">
                <button onclick="showSection('users')" class="btn btn-outline-white text-[10px]">← BACK</button>
                <h2 class="text-4xl font-bold italic">Performance <span class="text-yellow-400">Hub</span></h2>
            </div>
            
            <style>
            .bento-container-admin {
              display: grid;
              grid-template-columns: repeat(4, 1fr);
              gap: 20px;
              grid-template-areas:
                "hero hero stats activity"
                "neural neural activity activity"
                "nutrition nutrition nutrition nutrition";
              margin-bottom: 60px;
            }
            @media (max-width: 1200px) {
              .bento-container-admin {
                grid-template-columns: repeat(2, 1fr);
                grid-template-areas: "hero hero" "stats activity" "neural neural" "nutrition nutrition";
              }
            }
            @media (max-width: 768px) {
              .bento-container-admin {
                grid-template-columns: 1fr;
                grid-template-areas: "hero" "stats" "activity" "neural" "nutrition";
              }
            }
            .area-hero { grid-area: hero; background: linear-gradient(135deg, #1a1a1a 0%, #080808 100%); }
            .area-stats { grid-area: stats; }
            .area-activity { grid-area: activity; }
            .area-neural { grid-area: neural; background: radial-gradient(circle at center, #1a1a1a, #080808); }
            .area-nutrition { grid-area: nutrition; background: linear-gradient(135deg, #0d1a0d 0%, #080808 100%); }
            
            .bento-card-admin {
              background: rgba(18, 18, 18, 0.8);
              backdrop-filter: blur(20px);
              border: 1px solid rgba(255, 255, 255, 0.05);
              border-radius: 24px;
              padding: 30px;
              position: relative;
              overflow: hidden;
              transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
            }
            .bento-card-admin:hover { border-color: var(--yellow); transform: translateY(-5px) scale(1.01); box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6); }
            </style>

            <div class="bento-container-admin">
                <!-- HERO CARD -->
                <div class="bento-card-admin area-hero">
                    <div class="flex items-start justify-between mb-8">
                        <img id="progress-avatar" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" alt="User" class="w-20 h-20 rounded-full border-2 border-yellow-400 p-1">
                        <div class="text-right">
                            <div class="flex items-center justify-end">
                                <span class="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_10px_#4caf50] inline-block mr-2"></span>
                                <span class="text-[10px] uppercase tracking-widest text-[#555] font-bold">System Online</span>
                            </div>
                            <div class="text-xs font-bold text-yellow-400 mt-2" id="progress-role">MEMBER</div>
                        </div>
                    </div>
                    <h2 id="progress-member-name" class="text-4xl font-bold mb-2">Member Name</h2>
                    <p id="progress-member-email" class="text-[#888] text-sm leading-relaxed max-w-[300px]">Member Email</p>
                    <div id="progress-member-goal" class="mt-4 px-3 py-1 bg-yellow-400/10 border border-yellow-400/20 rounded-full inline-block text-[10px] font-bold text-yellow-400 uppercase tracking-widest">
                        Goal: ---
                    </div>
                </div>

                <!-- STATS CARD: CALORIES BURNED -->
                <div class="bento-card-admin area-stats">
                    <div class="flex flex-col h-full justify-between">
                        <div>
                            <h3 class="text-[11px] uppercase tracking-[2px] text-[#555] font-bold">Daily burn</h3>
                            <div class="text-3xl font-bold text-white mt-2" id="progress-daily-burn">-- <span class="text-sm font-normal text-[#555]">KCAL</span></div>
                        </div>
                        <div class="mt-8">
                            <span class="text-[11px] uppercase tracking-[2px] text-[#555] font-bold">Current Weight</span>
                            <div class="flex items-end gap-2 mt-2">
                                <span class="text-3xl font-bold text-white" id="progress-current-weight">--</span>
                                <span class="text-xs text-[#555] pb-2">KG</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ACTIVITY CARD: RECENT WORKOUTS -->
                <div class="bento-card-admin area-activity">
                    <h3 class="text-[11px] uppercase tracking-[2px] text-[#555] font-bold mb-6">Recent Workouts</h3>
                    <div id="progress-workout-list" class="flex flex-col gap-4 max-h-[300px] overflow-y-auto no-scrollbar">
                        <!-- Workouts injected here -->
                    </div>
                </div>

                <!-- NEURAL SCAN: PHYSIQUE ANALYSIS -->
                <div class="bento-card-admin area-neural">
                    <div class="flex justify-between items-start relative z-10">
                        <div>
                            <span class="text-[10px] font-bold uppercase tracking-widest text-[#888]">Neural scan</span>
                            <h3 class="text-xl font-bold mt-2 italic">Physique <span class="text-yellow-400">Analysis</span></h3>
                        </div>
                        <div class="text-right">
                            <div class="text-[10px] uppercase text-[#555] font-bold tracking-widest">Target Weight</div>
                            <div class="text-lg font-bold text-green-400" id="progress-target-weight">-- kg</div>
                        </div>
                    </div>
                    <div class="mt-8">
                        <div class="relative h-[200px] w-full">
                            <canvas id="weightJourneyChart"></canvas>
                        </div>
                    </div>
                </div>

                <!-- AI NUTRITION HUD -->
                <div class="bento-card-admin area-nutrition">
                    <span class="text-[10px] font-bold uppercase tracking-widest text-[#888]">Ai nutrition</span>
                    <h3 class="text-xl font-bold mt-2 italic">Fueling <span class="text-yellow-400">Status</span></h3>
                    <div class="mt-8 flex flex-col md:flex-row gap-6">
                        <div class="flex-1">
                            <div class="flex justify-between text-[10px] uppercase font-bold mb-2 tracking-widest">
                                <span>Protein intake</span> <span id="progress-protein-label">--/--g</span>
                            </div>
                            <div class="h-1.5 bg-white/5 rounded-full overflow-hidden">
                                <div id="progress-protein-bar" class="h-full bg-yellow-400 shadow-[0_0_10px_rgba(245,230,66,0.5)] transition-all duration-1000" style="width: 0%;"></div>
                            </div>
                        </div>
                        <div class="flex-1">
                            <div class="flex justify-between text-[10px] uppercase font-bold mb-2 tracking-widest">
                                <span>Active energy</span> <span id="progress-energy-label">--/-- kcal</span>
                            </div>
                            <div class="h-1.5 bg-white/5 rounded-full overflow-hidden">
                                <div id="progress-energy-bar" class="h-full bg-green-500 shadow-[0_0_10px_rgba(76,175,80,0.5)] transition-all duration-1000" style="width: 0%;"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>"""

pattern = re.compile(r'<!-- Performance Hub \(Detail View\) -->.*?</div>\s*</main>', re.DOTALL)
new_html = pattern.sub(new_progress_section + '\n    </main>', admin_html)

with open('frontend/admin.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('Admin HTML replaced successfully.')
