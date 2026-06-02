/* ============================================
   EAST BLUE GYM — MAIN SCRIPT
   ============================================ */

console.log("EAST BLUE SCRIPT LOADED v2026");
const API_URL = window.ELITE_API_URL || '';

// Force mobile browsers to respect :active pseudo-classes instantly on tap
if ('ontouchstart' in document.documentElement) {
  document.body.addEventListener('touchstart', function() {}, {passive: true});
}

/* ---- GLOBAL UTILITIES ---- */
window.showToast = function (message, type = 'success') {
  // Extract string from complex objects (FastAPI detail arrays or error objects)
  let displayMessage = message;
  if (typeof message === 'object' && message !== null) {
    if (Array.isArray(message)) {
      displayMessage = message.map(m => typeof m === 'object' ? (m.msg || JSON.stringify(m)) : m).join(', ');
    } else {
      displayMessage = message.detail || message.message || message.msg || JSON.stringify(message);
    }
  }

  // Final safeguard against stringified objects
  if (String(displayMessage).includes('[object Object]')) {
    displayMessage = 'Request failed. Please check inputs.';
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type} flex items-center gap-3`;
  toast.innerHTML = `
    <span class="flex-1">${displayMessage}</span>
    <button onclick="this.parentElement.remove()" class="bg-transparent border-none text-current opacity-50 hover:opacity-100 cursor-pointer text-xs">✕</button>
  `;
  document.body.appendChild(toast);
  setTimeout(() => toast.classList.add('show'), 10);
  setTimeout(() => {
    if (toast.parentElement) {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 400);
    }
  }, 4000);
};

/* ---- SESSION SECURITY ---- */
window.checkSession = function (response) {
  if (response.status === 401) {
    localStorage.removeItem('token');
    localStorage.removeItem('elite_profile');
    window.location.href = 'index.html?session=expired';
  }
  return response;
};

/* ---- NEURAL ACTIVITY LOGGING ---- */
window.logActivity = async function (action) {
  const token = localStorage.getItem('token');
  const profile = JSON.parse(localStorage.getItem('elite_profile') || '{}');
  if (!token || !profile.email) return;

  try {
    await fetch(`${API_URL}/api/user/activity`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        userEmail: profile.email,
        action: action,
        details: 'Neural sync successful'
      })
    });
  } catch (err) { console.warn('Activity sync offline.'); }
};

/* ---- NEURAL MOUSE TRACKING ---- */
window.initNeuralTracking = function () {
  if ('ontouchstart' in window || navigator.maxTouchPoints > 0) return; // Disable on Mobile to prevent crashes
  document.querySelectorAll('.bento-card, .product-card, .class-card, .glass, .studio-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    });
  });
};

window.updateDashboardUI = function (user, isFresh = false) {
  if (!user || user.error) return;
  document.querySelectorAll('#nav-avatar, #sidebar-avatar, #dashboard-avatar, #modal-avatar, #modal-avatar-preview').forEach(img => {
    let pic = user.profilePicture || 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png';
    if (pic.startsWith('/uploads/')) {
      pic = `${API_URL}${pic}`;
    }
    img.src = pic;
  });

  // Role-based navigation
  if (user.role === 'admin' || user.role === 'super_admin' || user.role === 'superadmin') {
    document.querySelectorAll('.nav-admin-only').forEach(el => el.classList.remove('hidden'));
    document.querySelectorAll('.nav-trainer-only').forEach(el => el.classList.add('hidden'));
    
    // Hide support chat for admins
    const fab = document.getElementById('aiSupportFab');
    if (fab) fab.style.display = 'none';
    const panel = document.getElementById('aiSupportPanel');
    if (panel) panel.style.display = 'none';
  } else if (user.role === 'trainer') {
    document.querySelectorAll('.nav-admin-only').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.nav-trainer-only').forEach(el => el.classList.remove('hidden'));
  } else {
    document.querySelectorAll('.nav-admin-only, .nav-trainer-only').forEach(el => el.classList.add('hidden'));
  }

  const fullName = user.username || `${user.firstName || ''} ${user.lastName || ''}`.trim() || 'Elite Member';
  const firstName = user.nickname || (user.firstName) || (user.username ? user.username.split(' ')[0] : 'Member');

  const elements = {
    'member-nickname': user.nickname || fullName,
    'member-bio': user.bio || 'No bio set. Customize your profile in settings!',
    'member-email': user.email,
    'user-greeting': 'Hello, ' + firstName + '!',
    'nav-greeting': user.nickname || fullName,
    'membership-type': user.membershipType || 'Free Trial',
    'profile-name-display': fullName,
    'profile-email-display': user.email,
    'display-membership-tier': user.membershipType || 'ELITE ANNUAL',
    'member-since': user.date ? new Date(user.date).toLocaleDateString('en-US', { month: 'short', year: 'numeric' }) : 'Jan 2026'
  };
  Object.entries(elements).forEach(([id, val]) => {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  });

  // Calculate and sync physical metrics to dashboard UI
  const dashboardWeight = parseFloat(user.weight) || 75.0;
  const dashboardHeight = parseFloat(user.height) || 170.0;
  const dashboardGoal = user.goal || 'Fat Loss';
  
  // Use Scientific Database for calculations
  let activeBurnTarget = 250; // Fallback
  if (typeof ScientificMetabolics !== 'undefined') {
    const metrics = ScientificMetabolics.calculateTargets(dashboardWeight, dashboardHeight, 25, dashboardGoal);
    activeBurnTarget = metrics.activeBurnTarget;
  }

  const dashboardBurnEl = document.getElementById('dashboard-daily-burn');
  if (dashboardBurnEl) dashboardBurnEl.innerHTML = `${activeBurnTarget.toLocaleString()} <span class="text-sm font-normal text-[#555]">KCAL</span>`;

  const dashboardFocusEl = document.getElementById('dashboard-target-focus');
  if (dashboardFocusEl) dashboardFocusEl.textContent = `Target focus: ${dashboardGoal.toUpperCase()} 99.8%`;

  const dashboardEnergyLabel = document.getElementById('energy-label');
  const dashboardEnergyBar = document.getElementById('energy-bar');
  if (dashboardEnergyLabel && dashboardEnergyBar) {
    dashboardEnergyLabel.textContent = `1.2k/${(dashboardCalorieTarget / 1000).toFixed(1)}k kcal`;
    dashboardEnergyBar.style.width = `${Math.min(100, Math.round((1200 / dashboardCalorieTarget) * 100))}%`;
  }

  // Fetch Live Notifications
  const syncNotifications = async () => {
    try {
      const res = await fetch(`${API_URL}/api/user/notifications?token=${localStorage.getItem('token')}`);
      const notes = await res.json();
      const container = document.getElementById('notification-list');
      if (container && notes.length > 0) {
        container.innerHTML = notes.map(n => `
          <div class="flex items-start gap-4 p-4 bg-[#111] border border-[#222] rounded-2xl hover:border-yellow-400/30 transition-all">
            <div class="w-10 h-10 rounded-full bg-yellow-400/10 flex items-center justify-center text-yellow-400">⚡</div>
            <div>
              <h4 class="text-xs font-bold uppercase tracking-widest italic">${n.title}</h4>
              <p class="text-[10px] text-[#555] mt-1 font-bold">${n.message}</p>
            </div>
          </div>
        `).join('');
      }
    } catch (err) { console.warn('Notification sync slow.'); }
  };

  // Fetch Unread Community Messages
  window.syncUnreadMessages = async () => {
    try {
      const res = await fetch(`${API_URL}/api/community/unread?token=${localStorage.getItem('token')}`);
      const { unread } = await res.json();
      const navLink = document.querySelector('a[href="community.html"]');
      if (navLink) {
        let badge = navLink.querySelector('.nav-badge');
        if (unread > 0) {
          if (!badge) {
            badge = document.createElement('span');
            badge.className = 'nav-badge absolute -top-1 -right-2 w-3 h-3 bg-yellow-400 rounded-full flex items-center justify-center text-[7px] text-black font-black animate-pulse';
            navLink.style.position = 'relative';
            navLink.appendChild(badge);
          }
          badge.textContent = unread;
        } else if (badge) {
          badge.remove();
        }
      }
    } catch (err) { console.warn('Unread sync slow.'); }
  };

  const path = window.location.pathname.toLowerCase();
  const requiresAdmission = path.includes('dashboard') || path.includes('workouts') || path.includes('activity');
  const isStaff = user.role === 'admin' || user.role === 'super_admin' || user.role === 'trainer';
  if (user.admissionStatus === 'pending' && requiresAdmission && !isStaff && isFresh) {
    window.location.href = 'admission.html';
    return;
  }

  const admissionStatusEl = document.getElementById('display-admission-status');
  if (admissionStatusEl) {
    admissionStatusEl.textContent = user.admissionStatus.toUpperCase();
    admissionStatusEl.className = `text-[9px] font-bold px-2 py-1 rounded ${user.admissionStatus === 'approved' ? 'bg-green-500/10 text-green-500' : 'bg-yellow-400/10 text-yellow-400'}`;
  }

  syncNotifications();
  syncUnreadMessages();

  // Fetch Upcoming Sessions
  window.syncUpcomingSessions = async () => {
    try {
      const res = await fetch(`${API_URL}/api/user/activities?token=${localStorage.getItem('token')}`);
      if (!res.ok) return;
      const data = await res.json();
      const bookings = data.filter(item => item.type === 'booking').slice(0, 3); // Get top 3 bookings
      
      const container = document.getElementById('upcoming-sessions-list');
      if (container) {
        if (bookings.length === 0) {
          container.innerHTML = `<div class="p-4 bg-white/5 rounded-2xl border border-white/5 opacity-60 text-center text-[10px] text-[#888]">No upcoming sessions booked.</div>`;
        } else {
          container.innerHTML = bookings.map((b, index) => `
            <div class="p-4 bg-white/5 rounded-2xl border border-white/5 ${index === 0 ? 'hover:border-yellow-400/30 transition-all cursor-pointer' : 'opacity-60'}">
              <div class="text-[10px] font-bold ${index === 0 ? 'text-yellow-400' : 'text-[#888]'} mb-1">${b.date}</div>
              <div class="text-sm font-bold">${b.activity}</div>
              <div class="text-[10px] text-[#555] mt-1">Trainer: ${b.location}</div>
            </div>
          `).join('');
        }
      }
    } catch (err) {
      console.warn('Failed to sync sessions:', err);
    }
  };
  syncUpcomingSessions();

  // Set intervals only once
  if (!window.eliteSyncIntervalsSet) {
    setInterval(syncUnreadMessages, 5000);
    window.eliteSyncIntervalsSet = true;
  }
  // --- HUD DATA SYNCHRONIZATION (Dashboard Only) ---
  // 1. Physique Analysis Focus
  const focusEl = document.querySelector('.area-neural-delay-2 .text-\\[\\#555\\]');
  if (focusEl) {
    focusEl.textContent = `TARGET FOCUS: ${user.goal ? user.goal.toUpperCase() : 'OPTIMIZATION'}`;
  }

  // 2. AI Nutrition Synchronization
  const weight = parseFloat(user.weight) || 75;
  const height = parseFloat(user.height) || 170;
  const age = 25; // Default age
  const goal = user.goal || 'Maintenance';

  // Use Scientific Database for Nutrition Math
  let metrics = { calorieTarget: 2500, proteinTarget: 150, fatTarget: 70, carbTarget: 300 };
  if (typeof ScientificMetabolics !== 'undefined') {
    metrics = ScientificMetabolics.calculateTargets(weight, height, age, goal);
  }

  let calorieTarget = metrics.calorieTarget;
  const proteinTarget = metrics.proteinTarget;
  const fatTarget = metrics.fatTarget;
  const carbTarget = metrics.carbTarget;
  const proteinCalories = proteinTarget * 4;
  const fatCalories = fatTarget * 9;

  // Current values (mock progress based on a fixed ratio for UI display)
  const progressRatio = 0.45;
  const calorieCurrent = Math.round(calorieTarget * progressRatio);
  const proteinCurrent = Math.round(proteinTarget * progressRatio);
  const carbCurrent = Math.round(carbTarget * progressRatio);
  const fatCurrent = Math.round(fatTarget * progressRatio);

  // Update UI Calorie
  const cLabel = document.getElementById('calorie-label');
  const cBar = document.getElementById('calorie-bar');
  if (cLabel) cLabel.textContent = `${(calorieCurrent / 1000).toFixed(1)}k/${(calorieTarget / 1000).toFixed(1)}k kcal`;
  if (cBar) cBar.style.width = `${(calorieCurrent / calorieTarget * 100).toFixed(0)}%`;

  // Update UI Protein
  const pLabel = document.getElementById('protein-label');
  const pBar = document.getElementById('protein-bar');
  if (pLabel) pLabel.textContent = `${proteinCurrent}/${proteinTarget}g`;
  if (pBar) pBar.style.width = `${(proteinCurrent / proteinTarget * 100).toFixed(0)}%`;

  // Update UI Carbs
  const cbLabel = document.getElementById('carbs-label');
  const cbBar = document.getElementById('carbs-bar');
  if (cbLabel) cbLabel.textContent = `${carbCurrent}/${carbTarget}g`;
  if (cbBar) cbBar.style.width = `${(carbCurrent / carbTarget * 100).toFixed(0)}%`;

  // Update UI Fats
  const fLabel = document.getElementById('fats-label');
  const fBar = document.getElementById('fats-bar');
  if (fLabel) fLabel.textContent = `${fatCurrent}/${fatTarget}g`;
  if (fBar) fBar.style.width = `${(fatCurrent / fatTarget * 100).toFixed(0)}%`;

  // Update Physique Fatigue & Recovery (Synchronized with Database)
  if (typeof metrics !== 'undefined') {
    // Make the Scanning live badge static to show it's synced
    const scanningBadge = document.querySelector('.animate-bounce');
    if (scanningBadge && scanningBadge.textContent.includes('Scanning live')) {
        scanningBadge.textContent = 'SYNCED: SCIENTIFIC DB';
        scanningBadge.classList.remove('animate-bounce');
        scanningBadge.classList.add('bg-green-400', 'text-black');
    }
  }

  // Neural Recommendations
  const nutritionCard = document.querySelector('.area-nutrition-delay-3');
  if (nutritionCard) {
    const recTitle = nutritionCard.querySelector('.text-sm');
    const recSub = nutritionCard.querySelector('.italic');
    if (recTitle && recSub) {
      const recommendations = {
        'Fat Loss': { title: 'Post-workout: White fish & steamed greens', sub: '+ L-Carnitine & Green Tea extract' },
        'Bulking': { title: 'Post-workout: Double beef bowl with eggs', sub: '+ Creatine Monohydrate & 50g Dextrose' },
        'Hypertrophy': { title: 'Post-workout: Grilled chicken & sweet potato', sub: '+ BCAAs & Electrolyte balance' },
        'Endurance': { title: 'Post-workout: Pasta with lean turkey', sub: '+ Complex Carb load & Vitamin B complex' },
        'Recovery': { title: 'Rest day: Bone broth & berry smoothie', sub: '+ Magnesium & Omega-3 recovery pack' },
        'Maintenance': { title: 'Balanced: Grilled salmon & quinoa bowl', sub: '+ Daily Multi-vitamin & Zinc' }
      };
      const rec = recommendations[goal] || recommendations['Maintenance'];
      recTitle.textContent = rec.title;
      recSub.textContent = rec.sub;
    }
  }

  // 3. Elite Leaderboard Sync
  const syncLeaderboard = async () => {
    try {
      const res = await fetch(`${API_URL}/api/user/leaderboard`);
      const leaders = await res.json();
      const list = document.getElementById('leaderboard-list');
      if (list && leaders.length > 0) {
        list.innerHTML = leaders.map((u, i) => `
                    <div class="leader-item shrink-0 w-32 p-3 bg-white/5 rounded-xl border border-white/5 hover:border-yellow-400/20 transition-all">
                        <div class="rank-circle ${i === 0 ? 'rank-1' : ''} mb-2">${i + 1}</div>
                        <div class="text-[10px] font-bold uppercase truncate">${u.name}</div>
                        <div class="text-[8px] text-[#555]">${(u.points / 1000).toFixed(1)}k PTS</div>
                    </div>
                `).join('');
      }
    } catch (err) { console.warn('Leaderboard sync failed.'); }
  };

  // 4. Elite Pulse (Live Activity) Sync
  const syncElitePulse = async () => {
    try {
      const res = await fetch(`${API_URL}/api/user/pulse`);
      const pulse = await res.json();
      const feed = document.getElementById('live-activity-feed');
      if (feed && pulse.length > 0) {
        feed.innerHTML = pulse.map(a => {
          const time = new Date(a.time);
          const diff = Math.floor((new Date() - time) / 60000); // mins
          const timeStr = diff < 1 ? 'Just now' : diff < 60 ? `${diff}m ago` : `${Math.floor(diff / 60)}h ago`;

          return `
                        <div class="flex items-center gap-2 text-[10px] border-l-2 border-yellow-400/20 pl-2 py-1">
                            <span class="text-yellow-400 font-bold">${a.user}</span>
                            <span class="text-[#888]">${a.action}</span>
                            <span class="ml-auto text-[8px] text-[#444]">${timeStr}</span>
                        </div>
                    `;
        }).join('');
      }
    } catch (err) { console.warn('Pulse sync failed.'); }
  };

  syncLeaderboard();
  syncElitePulse();
};

window.logout = function () {
  localStorage.removeItem('token');
  localStorage.removeItem('cart');
  localStorage.removeItem('elite_profile');
  window.location.href = 'index.html';
};

window.switchTab = function (tabName) {
  const normalizedTab = tabName.toLowerCase();

  // Auth Tabs (Login/Register)
  const authTabs = document.querySelectorAll('.auth-tab');
  const authForms = document.querySelectorAll('.auth-form');

  if (authTabs.length) {
    authTabs.forEach(btn => {
      const text = btn.textContent.toLowerCase();
      const isActive = text.includes(normalizedTab) ||
        (normalizedTab === 'login' && text.includes('sign')) ||
        (normalizedTab === 'register' && text.includes('start'));
      btn.classList.toggle('active', isActive);
    });
  }

  if (authForms.length) {
    authForms.forEach(form => {
      const id = form.id.toLowerCase();
      const isActive = id.includes(normalizedTab) ||
        (normalizedTab === 'login' && id.includes('sign'));
      form.classList.toggle('active', isActive);
    });
  }

  // General Tabs
  const controlBtns = document.querySelectorAll('.tab-btn');
  const controlContents = document.querySelectorAll('.tab-content');
  if (controlBtns.length && controlContents.length) {
    controlBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.tab === normalizedTab));
    controlContents.forEach(content => content.classList.toggle('active', content.dataset.tab === normalizedTab));
  }
};

/* ---- MAIN INITIALIZATION ---- */
/* ---- ELITE GLOBAL CONFIG ---- */

/* ---- GLOBAL MOBILE MENU TOGGLE ---- */
window.toggleMobileMenu = function (e) {
  if (e) {
    if (typeof e.preventDefault === 'function') e.preventDefault();
    if (typeof e.stopPropagation === 'function') e.stopPropagation();
  }
  const hamburger = document.querySelectorAll('.hamburger');
  const mobileMenu = document.getElementById('mobile-menu');
  const adminSidebar = document.querySelector('.admin-sidebar');

  hamburger.forEach(h => h.classList.toggle('active'));
  if (mobileMenu) mobileMenu.classList.toggle('active');
  if (adminSidebar) adminSidebar.classList.toggle('active');

  const isActive = mobileMenu ? mobileMenu.classList.contains('active') : false;
  hamburger.forEach(h => h.setAttribute('aria-expanded', isActive ? 'true' : 'false'));
  if (document.body) document.body.style.overflow = isActive ? 'hidden' : 'auto';
};

window.togglePassword = function (btn) {
  const input = btn.previousElementSibling;
  if (input.type === 'password') {
    input.type = 'text';
    btn.textContent = '🔒';
  } else {
    input.type = 'password';
    btn.textContent = '👁️';
  }
};

// Safety Polyfills for older Mobile Browsers (ES5 Compatible)
if (!window.AbortController) {
  window.AbortController = function () {
    this.signal = { aborted: false, addEventListener: function () { } };
    this.abort = function () { this.signal.aborted = true; };
  };
}
if (!window.IntersectionObserver) {
  window.IntersectionObserver = function (cb) {
    this.observe = function (el) { el.classList.add('visible'); };
    this.unobserve = function () { };
  };
}

// Emergency White-Screen Killswitch
setTimeout(function () {
  if (document.body) document.body.style.opacity = '1';
  document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('visible'); });
}, 3000);

document.addEventListener('DOMContentLoaded', () => {

  window.initNeuralTracking();

  /* ---- NAVBAR & NAV LOGIC ---- */
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 40);
    });
  }

  // Attach to all hamburgers found in the DOM
  document.querySelectorAll('.hamburger').forEach(h => {
    h.onclick = window.toggleMobileMenu;
  });

  // Close menu when clicking outside or on a link
  document.addEventListener('click', (e) => {
    const isHamburger = e.target.closest('.hamburger');
    const isMenu = e.target.closest('.mobile-menu');
    const isAdminSidebar = e.target.closest('.admin-sidebar');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenu && mobileMenu.classList.contains('active')) {
      if (!isMenu && !isHamburger && !isAdminSidebar) {
        window.toggleMobileMenu();
      }
    }

    // Close menu when a link inside mobile menu is clicked
    if (e.target.closest('.mobile-menu a') || e.target.closest('.admin-sidebar .sidebar-link')) {
      if (mobileMenu && mobileMenu.classList.contains('active')) {
        window.toggleMobileMenu();
      }
    }
  });

  /* ---- REVEAL ON SCROLL ---- */
  try {
    const revealCallback = (entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    };
    const revealObserver = new IntersectionObserver(revealCallback, { threshold: 0.1 });
    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));
    // Fallback
    setTimeout(() => { document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible')); }, 2000);
  } catch (err) { console.error('Reveal error:', err); }

  /* ---- ACTIVE LINK HIGHLIGHTING ---- */
  try {
    let currentPath = window.location.pathname.split('/').pop().replace('.html', '').toLowerCase();
    if (!currentPath || currentPath === '') currentPath = 'index';
    
    document.querySelectorAll('.nav-links a, .mobile-menu a').forEach(link => {
      const linkPath = (link.getAttribute('href') || '').replace('.html', '').toLowerCase();
      if (linkPath === currentPath) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  } catch (err) { console.error('Link highlighting error:', err); }

  let token = null;
  try {
    token = localStorage.getItem('token');
  } catch (err) { console.error('LocalStorage access error:', err); }

  const profileDataStr = localStorage.getItem('elite_profile');
  if (token || (profileDataStr && profileDataStr !== 'undefined')) {
    document.querySelectorAll('.nav-dashboard-link').forEach(el => el.classList.remove('hidden'));
    document.querySelectorAll('.nav-auth-only').forEach(el => el.classList.add('hidden'));

    try {
      if (profileDataStr && profileDataStr !== 'undefined') {
        const localData = JSON.parse(profileDataStr);
        if (localData && localData.email) window.updateDashboardUI(localData);
      }
    } catch (err) { localStorage.removeItem('elite_profile'); }

    // Fetch with timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);

    fetch(`${API_URL}/api/user/me?token=${token}`, {
      signal: controller.signal
    })
      .then(res => res.json())
      .then(user => {
        clearTimeout(timeoutId);
        if (user && !user.detail && !user.error) {
          window.updateDashboardUI(user, true);
          localStorage.setItem('elite_profile', JSON.stringify(user));
        }
      })
      .catch(err => {
        console.warn('Backend link slow or offline.');
      });
  }

  /* ---- NAV PROFILE DROPDOWN ---- */
  const navProfileBtn = document.getElementById('navProfileBtn');
  const navDropdown = document.getElementById('navDropdown');
  if (navProfileBtn && navDropdown) {
    navProfileBtn.onclick = (e) => {
      const isLink = e.target.closest('a');
      if (!isLink) {
        e.preventDefault();
        e.stopPropagation();
        navDropdown.classList.toggle('active');
      }
    };
    document.addEventListener('click', (e) => {
      if (!navProfileBtn.contains(e.target)) navDropdown.classList.remove('active');
    });
  }

  /* ---- GLOBAL MODAL LOGIC ---- */
  const authModal = document.getElementById('authModal');
  const closeAuthModal = document.getElementById('closeAuthModal');

  window.openAuthModal = function (tab = 'login') {
    if (authModal) {
      authModal.classList.remove('hidden');
      window.switchTab(tab);
    }
  };

  if (closeAuthModal) {
    closeAuthModal.addEventListener('click', () => authModal.classList.add('hidden'));
    authModal.addEventListener('click', (e) => {
      if (e.target === authModal) authModal.classList.add('hidden');
    });
  }

  // Global Modal Trigger Detection
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('button, a');
    if (!btn) return;

    const txt = btn.textContent.toLowerCase();
    const isAuthTrigger = txt.includes('sign in') || txt.includes('login') || txt.includes('register') || txt.includes('trial') || txt.includes('join now');

    if (isAuthTrigger && !btn.classList.contains('no-modal') && btn.type !== 'submit') {
      // If user is already logged in, let the link work normally (e.g. going to dashboard)
      if (localStorage.getItem('token') && btn.tagName === 'A' && btn.getAttribute('href') !== '#') return;

      e.preventDefault();
      const isRegister = txt.includes('trial') || txt.includes('register') || txt.includes('join');
      window.openAuthModal(isRegister ? 'register' : 'login');
    }
  });

  /* ---- COUNTER ANIMATION (THE HEARTBEAT) ---- */
  function animateCounter(el) {
    const target = parseFloat(el.dataset.target);
    const suffix = el.dataset.suffix || '';
    const prefix = el.dataset.prefix || '';
    const duration = 2000;
    const start = performance.now();

    function update(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = eased * target;
      el.textContent = prefix + (Number.isInteger(target) ? Math.floor(current) : current.toFixed(1)) + suffix;
      if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
  }

  const counterEls = document.querySelectorAll('.stat-num[data-target]');
  if (counterEls.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    counterEls.forEach(el => observer.observe(el));
  }

  /* ---- SCROLL REVEAL ---- */
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    const revObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    revealEls.forEach(el => revObserver.observe(el));
  }

  /* ---- HASH NAVIGATION ---- */
  const hash = window.location.hash.substring(1);
  if (hash === 'register' || hash === 'signin' || hash === 'login') {
    setTimeout(() => {
      window.switchTab(hash === 'signin' ? 'login' : hash);
      const target = document.getElementById(hash === 'register' || hash === 'signin' ? 'signin' : hash);
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  }

  /* ---- FORMS (AJAX) ---- */
  const attachFormHandler = (form) => {
    console.log("Attaching handler to form:", form.id);
    if (form.dataset.neuralAttached) return;
    form.dataset.neuralAttached = "true";

    form.addEventListener('submit', async (e) => {
      console.log("Form submitted:", form.id);
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      const originalText = btn.textContent;
      btn.disabled = true; btn.textContent = 'Sending...';
      try {
        const formData = Object.fromEntries(new FormData(form));
        const action = form.getAttribute('action') || '/api/auth/login';
        const route = action.startsWith('/') ? action : `/${action}`;
        const actionUrl = action.startsWith('http') ? action : `${API_URL}${route}`;

        const res = await fetch(actionUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(formData)
        });
        const data = await res.json();
        if (res.ok) {
          window.showToast(data.message || 'Success!', 'success');
          if (data.token) {
            localStorage.setItem('token', data.token);
            if (data.user) {
              localStorage.setItem('elite_profile', JSON.stringify(data.user));
              const isRegister = form.id.toLowerCase().includes('register');
              window.logActivity(isRegister ? 'Signed Up' : 'Logged In');
            }
            setTimeout(() => {
              if (data.user && (data.user.role === 'admin' || data.user.role === 'super_admin')) {
                window.location.href = 'admin.html';
              } else if (data.user && data.user.role === 'trainer') {
                window.location.href = 'trainer.html';
              } else {
                window.location.href = 'dashboard.html';
              }
            }, 1000);
          } else { 
            form.reset(); 
            const parentModal = form.closest('.modal-overlay');
            if (parentModal) parentModal.classList.add('hidden');
          }
        } else { window.showToast(data.detail || data.error || 'Error', 'error'); }
      } catch (err) {
        console.error('AJAX Error:', err);
        const apiHint = API_URL ? '' : ' API URL missing — check js/config.js.';
        window.showToast(`Connection failed.${apiHint} Is the backend online?`, 'error');
      } finally { btn.disabled = false; btn.textContent = originalText; }
    });
  };

  document.querySelectorAll('.ajax-form').forEach(attachFormHandler);

  /* ---- PLACEHOLDER HANDLERS ---- */
  document.addEventListener('click', (e) => {
    const el = e.target.closest('a, button');
    if (!el) return;

    if (el.classList.contains('btn-contact-trigger')) {
      e.preventDefault();
      const modal = document.getElementById('contactModal');
      if (modal) modal.classList.remove('hidden');
      return;
    }

    if (el.id === 'closeContactModal' || el.classList.contains('modal-overlay')) {
      const modal = el.id === 'closeContactModal' ? document.getElementById('contactModal') : el;
      if (modal) {
        modal.classList.add('hidden');
        if (el.id === 'closeContactModal') e.preventDefault();
      }
      if (el.id === 'closeContactModal') return;
    }

    if (el.getAttribute('href') === '#') {
      if (el.id === 'btnOpenSettings' || el.id === 'navProfileBtn' || el.classList.contains('hamburger') || el.id === 'btnCheckIn' || el.id === 'btnClaimPerk' || el.id === 'closeChat') return;
      if (el.textContent.toLowerCase().includes('forgot') || el.classList.contains('footer-social-btn') || el.textContent.toLowerCase().includes('app store') || el.textContent.toLowerCase().includes('google play')) {
        e.preventDefault();
        if (!el.textContent.toLowerCase().includes('forgot')) {
          window.showToast('This feature is currently in development for the Elite version.', 'info');
        }
      }
    }
  });

  window.forgotPassword = async function (e) {
    if (e) e.preventDefault();
    const email = prompt("Enter your registered Email Address to receive a temporary password:");
    if (!email) return;

    window.showToast("Synchronizing with Elite Recovery...", "info");

    try {
      const res = await fetch(`${API_URL}/api/auth/forgot-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email })
      });
      const data = await res.json();
      if (res.ok) {
        window.showToast(data.message, "success");
      } else {
        window.showToast(data.detail || "Recovery failed.", "error");
      }
    } catch (err) {
      window.showToast("Neural Link Error. Try again later.", "error");
    }
  };

  // CheckInBtn listener removed for correct form flow
  const cancelBtn = document.getElementById('btnCancel');
  if (cancelBtn) {
    cancelBtn.addEventListener('click', () => {
      cancelBtn.closest('.flex.items-center').style.opacity = '0.3';
      cancelBtn.textContent = 'CANCELLED'; cancelBtn.disabled = true;
      window.showToast('Booking cancelled successfully.', 'info');
      window.logActivity('Cancelled Booking');
    });
  }
  const claimBtn = document.getElementById('btnClaimPerk');
  if (claimBtn) {
    claimBtn.addEventListener('click', () => {
      claimBtn.textContent = 'CLAIMED'; claimBtn.disabled = true; claimBtn.style.opacity = '0.5';
      window.showToast('Perk added to your Elite account!', 'success');
      window.logActivity('Claimed Perk');
    });
  }
  const keepPushingBtn = document.getElementById('btnKeepPushing');
  if (keepPushingBtn) {
    keepPushingBtn.addEventListener('click', () => {
      window.showToast('You are 65% there! Complete 1 more session today to hit your goal.', 'info');
    });
  }
  const streakBtn = document.getElementById('btnStreak');
  if (streakBtn) {
    streakBtn.addEventListener('click', () => {
      window.showToast('You are on a 24-day streak! Only 6 days left to unlock your reward.', 'success');
    });
  }
  const bmrValueEl = document.getElementById('bmr-value');
  if (bmrValueEl) {
    bmrValueEl.addEventListener('click', () => {
      window.showToast('Talk to our AI Gym Assistant (bottom right) to recalculate your BMR!', 'info');
    });
  }

  /* ---- FAQ ACCORDION LOGIC ---- */
  document.querySelectorAll('.faq-item, .faq-question').forEach(item => {
    item.addEventListener('click', () => {
      const parent = item.closest('.faq-item') || item;
      const wasActive = parent.classList.contains('active');

      // Close others
      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('active'));

      // Toggle current
      if (!wasActive) parent.classList.add('active');
    });
  });

  /* ---- MODAL LOGIC ---- */
  const profileModal = document.getElementById('profileModal');
  const btnOpenSettings = document.getElementById('btnOpenSettings');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const profileUpdateForm = document.getElementById('profileUpdateForm');

  if (btnOpenSettings) {
    btnOpenSettings.addEventListener('click', () => {
      profileModal.classList.remove('hidden');
      const saved = JSON.parse(localStorage.getItem('elite_profile') || '{}');
      if (saved.nickname) document.getElementById('edit-nickname').value = saved.nickname;
      if (saved.firstName || saved.lastName) {
        const fullName = `${saved.firstName || ''} ${saved.lastName || ''}`.trim();
        const fullNameEl = document.getElementById('edit-fullname');
        if (fullNameEl) fullNameEl.value = fullName;
      }
      if (saved.goal) document.getElementById('edit-goal').value = saved.goal;
      if (saved.weight) document.getElementById('edit-weight').value = saved.weight;
      if (saved.weightGoal) document.getElementById('edit-weightGoal').value = saved.weightGoal;
      if (saved.height) document.getElementById('edit-height').value = saved.height;
      if (saved.bio) document.getElementById('edit-bio').value = saved.bio;

      const avatar = document.getElementById('modal-avatar') || document.getElementById('modal-avatar-preview');
      if (avatar) avatar.src = saved.profilePicture || 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png';

      const phoneEl = document.getElementById('edit-phone');
      if (phoneEl) phoneEl.value = saved.phoneNumber || '';
    });
  }

  if (btnCloseModal) btnCloseModal.addEventListener('click', () => profileModal.classList.add('hidden'));

  window.previewProfilePicture = function (input) {
    if (input.files && input.files[0]) {
      const reader = new FileReader();
      reader.onload = function (e) {
        const avatars = [
          document.getElementById('modal-avatar'),
          document.getElementById('modal-avatar-preview'),
          document.getElementById('dashboard-avatar'),
          document.getElementById('nav-avatar')
        ];
        avatars.forEach(avatar => {
          if (avatar) avatar.src = e.target.result;
        });
      }
      reader.readAsDataURL(input.files[0]);
    }
  };

  window.setSentiment = function (sentiment, btn) {
    document.querySelectorAll('.sentiment-btn').forEach(b => {
      b.classList.remove('active', 'border-yellow-400/50', 'bg-yellow-400/10');
    });
    btn.classList.add('active', 'border-yellow-400/50', 'bg-yellow-400/10');
    const input = document.getElementById('feedbackSentiment');
    if (input) input.value = sentiment;
  };



  if (profileUpdateForm) {
    profileUpdateForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = profileUpdateForm.querySelector('button[type="submit"]');
      const originalText = btn.textContent;
      const token = localStorage.getItem('token');

      if (!token) {
        window.showToast('Login required to save changes', 'error');
        return;
      }

      btn.disabled = true;
      btn.textContent = 'SYNCING ELITE HUD...';

      try {
        const formData = new FormData(profileUpdateForm);
        formData.append('token', token); // Essential: Backend expects token in form data
        const response = await fetch(`${API_URL}/api/user/update`, {
          method: 'POST',
          body: formData
        });

        const result = await response.json();

        if (response.ok && result.user) {
          localStorage.setItem('elite_profile', JSON.stringify(result.user));
          window.updateDashboardUI(result.user);
          window.updateEliteUI(result.user);
          window.showToast('Elite Profile Synchronized!', 'success');

          const modal = document.getElementById('profileModal');
          if (modal) modal.classList.add('hidden');

          if (typeof fetchActivities === 'function') fetchActivities();

          // 8. INDEX/MEMBERSHIP MODULE SYNC (index.html, membership.html)
          const path = window.location.pathname.split('/').pop();
          if (path === 'index.html' || path === 'membership.html') {
            // Sync Hero Stats (Members worldwide, etc.)
            const syncHeroStats = async () => {
              try {
                const res = await fetch(`${API_URL}/api/admin/stats`);
                const stats = await res.json();
                const memberCountEl = document.querySelector('[data-target="3.4"]');
                if (memberCountEl && stats.totalUsers) {
                  memberCountEl.dataset.target = (stats.totalUsers / 1000000).toFixed(1);
                  // Trigger re-animation
                  if (typeof animateCounter === 'function') animateCounter(memberCountEl);
                }
              } catch (err) { }
            };
            syncHeroStats();

            // Membership Plan Bridge
            const planBtns = document.querySelectorAll('.btn-yellow, .btn-outline-yellow');
            planBtns.forEach(btn => {
              const txt = btn.textContent.toLowerCase();
              if (txt.includes('join') || txt.includes('get started') || txt.includes('start trial')) {
                btn.onclick = (e) => {
                  e.preventDefault();
                  // Detect plan from context (header of card)
                  const card = btn.closest('.membership-card, .price-card');
                  let plan = 'FREE GUEST';
                  if (card) {
                    const h3 = card.querySelector('h3');
                    if (h3) plan = h3.textContent.toUpperCase();
                  }

                  // Inject into hidden registration field
                  const planInput = document.querySelector('input[name="membershipType"]');
                  if (planInput) planInput.value = plan;

                  window.openAuthModal('register');
                };
              }
            });
          }
        } else {
          window.showToast(result.detail || 'Update failed', 'error');
        }
      } catch (err) {
        console.error('Profile Sync Error:', err);
        window.showToast('Neural Sync Interrupted. Check connection.', 'error');
      } finally {
        btn.disabled = false;
        btn.textContent = originalText;
      }
    });
  }


  window.updateEliteUI = function (profile) {
    if (!profile) return;

    // 1. Core Profile Identity
    const nick = profile.nickname || profile.firstName || 'Elite Member';
    const fullName = `${profile.firstName || ''} ${profile.lastName || ''}`.trim() || nick;

    const textUpdates = {
      'member-nickname': nick,
      'user-greeting': `Hello, ${nick}!`,
      'nav-greeting': nick,
      'member-bio': profile.bio || 'Neural performance trending high.',
      'user-goal': profile.goal ? `Goal: ${profile.goal}` : 'Goal: Maintenance',
      'display-membership-tier': profile.membershipType || 'ELITE ANNUAL',
      'display-target-weight': profile.weightGoal ? `${profile.weightGoal} kg` : '80 kg',
      'profile-phone-display': profile.phoneNumber || '+880 ---'
    };

    Object.entries(textUpdates).forEach(([id, val]) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    });

    // HUD sync logic has been centralized to the dashboard initialization block.
    // 4. Neural Scan Metadata
    const focusEl = document.querySelector('.area-neural-delay-2 h3 + div') || document.querySelector('.area-neural-delay-2 .text-center span');
    if (focusEl) {
      focusEl.textContent = `Target Focus: ${profile.goal || 'General Fitness'}`;
    }

    // 5. Visual HUD Refresh (Heatmap & Charts)
    if (typeof window.renderPerformanceHeatmap === 'function') window.renderPerformanceHeatmap();
    if (typeof Chart !== 'undefined') {
      if (typeof window.initEliteCharts === 'function') window.initEliteCharts(profile);
    }
  };

  // HELPER: Performance Heatmap (Last 14 Days)
  window.renderPerformanceHeatmap = function () {
    const grid = document.getElementById('heatmap-grid');
    if (!grid) return;
    grid.innerHTML = '';
    const container = document.createElement('div');
    container.className = 'flex flex-wrap gap-2';

    for (let i = 0; i < 14; i++) {
      const block = document.createElement('div');
      const opacity = Math.random() * 0.9 + 0.1;
      block.className = 'w-6 h-6 rounded-sm bg-yellow-400';
      block.style.opacity = opacity > 0.4 ? opacity : 0.1;
      container.appendChild(block);
    }
    grid.appendChild(container);
  };

  // HELPER: Elite Analytics Charts (Chart.js)
  window.initEliteCharts = function (profile) {
    if (typeof Chart === 'undefined') return;

    // Destroy existing charts to prevent memory leaks/overlap
    const charts = ['intensityChart', 'fuelChart', 'synergyChart'];
    charts.forEach(id => {
      const chartInstance = Chart.getChart(id);
      if (chartInstance) chartInstance.destroy();
    });

    const weight = parseFloat(profile.weight || 75);
    const height = parseFloat(profile.height || 170);
    const goal = profile.goal || 'Maintenance';
    
    // Fetch precise database metrics
    let dbMetrics = { intensityData: [65, 82, 45, 90, 75, 95, 60], synergyData: [85, 92, 65, 88, 70], calorieTarget: 2500, activeBurnTarget: 400 };
    if (typeof ScientificMetabolics !== 'undefined') {
        dbMetrics = ScientificMetabolics.calculateTargets(weight, height, 25, goal);
    }

    // 1. Intensity Pulse
    const ctxInt = document.getElementById('intensityChart');
    if (ctxInt) {
      new Chart(ctxInt, {
        type: 'line',
        data: {
          labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          datasets: [{
            data: dbMetrics.intensityData,
            borderColor: '#f5e62a',
            backgroundColor: 'rgba(245, 230, 42, 0.1)',
            fill: true, tension: 0.4, borderWidth: 3, pointRadius: 4
          }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
      });
    }

    // 2. Fuel Burned
    const ctxFuel = document.getElementById('fuelChart');
    if (ctxFuel) {
      // Simulate real variance around the exact clinical daily target
      const dailyTarget = dbMetrics.calorieTarget + dbMetrics.activeBurnTarget;
      new Chart(ctxFuel, {
        type: 'bar',
        data: {
          labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          datasets: [{
            data: [
              dailyTarget * 0.9, 
              dailyTarget * 1.1, 
              dailyTarget * 0.85, 
              dailyTarget * 1.05, 
              dailyTarget * 0.95, 
              dailyTarget * 1.15, 
              dailyTarget * 0.8
            ],
            backgroundColor: '#f5e62a', borderRadius: 8, barThickness: 15
          }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
      });
    }

    // 3. Training Synergy
    const ctxSyn = document.getElementById('synergyChart');
    if (ctxSyn) {
      new Chart(ctxSyn, {
        type: 'radar',
        data: {
          labels: ['Strength', 'Cardio', 'Mobility', 'Endurance', 'Recovery'],
          datasets: [{
            label: 'Your Synergy',
            data: dbMetrics.synergyData,
            borderColor: '#f5e62a', backgroundColor: 'rgba(245, 230, 42, 0.2)', pointBackgroundColor: '#f5e62a', borderWidth: 2
          }]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: { r: { grid: { color: 'rgba(255,255,255,0.05)' }, pointLabels: { color: '#888' }, ticks: { display: false }, suggestedMin: 0, suggestedMax: 100 } }
        }
      });
    }
  };

  // Load profile on start
  const savedProfile = JSON.parse(localStorage.getItem('elite_profile') || '{}');
  window.updateEliteUI(savedProfile);

  /* ---- SECURITY TAB HANDLERS ---- */
  const changeEmailForm = document.getElementById('changeEmailForm');
  const changePasswordForm = document.getElementById('changePasswordForm');

  if (changeEmailForm) {
    changeEmailForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = changeEmailForm.querySelector('button[type="submit"]');
      const newEmailInput = changeEmailForm.querySelector('input[name="newEmail"]');
      if (!newEmailInput) return;
      const newEmail = newEmailInput.value;
      btn.disabled = true;
      const token = localStorage.getItem('token');
      if (!token) { window.showToast('Please sign in first.', 'error'); btn.disabled = false; return; }
      try {
        const res = await fetch(`${API_URL}/api/user/change-email?token=${encodeURIComponent(token)}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ newEmail })
        });
        const data = await res.json();
        if (res.ok) {
          window.showToast(data.message || 'Email updated.', 'success');
          changeEmailForm.reset();
          fetch(`${API_URL}/api/user/me?token=${token}`).then(r => r.json()).then(u => window.updateDashboardUI(u));
        } else { window.showToast(data.detail || data.error || 'Update failed', 'error'); }
      } catch (err) { window.showToast('Network error', 'error'); } finally { btn.disabled = false; }
    });
  }

  if (changePasswordForm) {
    changePasswordForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = changePasswordForm.querySelector('button[type="submit"]');
      const newPasswordInput = changePasswordForm.querySelector('input[name="newPassword"]');
      if (!newPasswordInput) return;
      const oldPasswordInput = changePasswordForm.querySelector('input[name="oldPassword"]');
      const newPassword = newPasswordInput.value;
      const oldPassword = oldPasswordInput ? oldPasswordInput.value : '';
      const token = localStorage.getItem('token');
      if (!token) { window.showToast('Please sign in first.', 'error'); btn.disabled = false; return; }
      if (!oldPassword) { window.showToast('Enter your current password.', 'error'); btn.disabled = false; return; }
      btn.disabled = true;
      try {
        const res = await fetch(`${API_URL}/api/user/change-password?token=${encodeURIComponent(token)}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ oldPassword, newPassword })
        });
        const data = await res.json();
        if (res.ok) {
          window.showToast(data.message, 'success');
          changePasswordForm.reset();
        } else { window.showToast(data.detail || data.error || 'Update failed', 'error'); }
      } catch (err) { window.showToast('Network error', 'error'); } finally { btn.disabled = false; }
    });
  }

  /* ---- TESTIMONIAL SLIDER LOGIC ---- */
  const testiTrack = document.getElementById('testiTrack');
  if (testiTrack) {
    let index = 0;
    const cards = testiTrack.children;
    const updateSlider = () => {
      if (cards.length === 0) return;
      const cardWidth = cards[0].offsetWidth;
      const gap = 32;
      const offset = index * -(cardWidth + gap);
      testiTrack.style.transition = 'transform 0.8s cubic-bezier(0.16, 1, 0.3, 1)';
      testiTrack.style.transform = `translateX(${offset}px)`;
    };

    const nextSlide = () => {
      if (cards.length > 1) {
        const cardWidth = cards[0].offsetWidth;
        const gap = 32;
        const visibleWidth = testiTrack.parentElement.offsetWidth;
        const visibleCards = Math.floor((visibleWidth + gap) / (cardWidth + gap));
        const maxIndex = Math.max(0, cards.length - visibleCards);
        
        if (maxIndex > 0) {
          index = (index + 1) % (maxIndex + 1);
          updateSlider();
        } else if (index !== 0) {
          index = 0;
          updateSlider();
        }
      }
    };

    let testiInterval = setInterval(nextSlide, 5000);

    // Pause on hover
    testiTrack.parentElement.addEventListener('mouseenter', () => clearInterval(testiInterval));
    testiTrack.parentElement.addEventListener('mouseleave', () => {
      testiInterval = setInterval(nextSlide, 5000);
    });

    // Handle resize
    window.addEventListener('resize', () => {
      index = 0;
      updateSlider();
    });
  }




  // --- MULTI-MODAL ELITE PROOF VERIFICATION ---
  window.submitTextProof = async function() {
    const textInput = document.getElementById('textProofInput');
    if (!textInput.value.trim()) {
      window.showToast('Please enter your text log.', 'error');
      return;
    }
    await processEliteProof(null, textInput.value.trim());
    textInput.value = '';
    const container = document.getElementById('textProofContainer');
    if (container) container.classList.add('hidden');
  };

  window.selectedMediaFile = null;

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      window.selectedMediaFile = file;
      const textContainer = document.getElementById('textProofContainer');
      if (textContainer) textContainer.classList.add('hidden');
      
      const mediaContainer = document.getElementById('mediaProofContainer');
      if (mediaContainer) {
        document.getElementById('mediaProofLabel').textContent = `Selected: ${file.name}`;
        mediaContainer.classList.remove('hidden');
      }
      
      // Clear the input so the 'change' event fires again even for the same file
      event.target.value = '';
    }
  };

  window.submitMediaProof = async function() {
    if (!window.selectedMediaFile) return;
    const captionInput = document.getElementById('mediaProofCaption');
    const caption = captionInput ? captionInput.value.trim() : null;
    
    await processEliteProof(window.selectedMediaFile, caption || null);
    
    window.selectedMediaFile = null;
    if (captionInput) captionInput.value = '';
    document.getElementById('mediaProofContainer').classList.add('hidden');
  };

  const videoUpload = document.getElementById('videoUpload');
  if (videoUpload) videoUpload.addEventListener('change', handleFileUpload);
  
  const photoUpload = document.getElementById('photoUpload');
  if (photoUpload) photoUpload.addEventListener('change', handleFileUpload);

  async function processEliteProof(file, textProof) {
    const token = localStorage.getItem('token');
    if (!token) {
      window.showToast('Please sign in to verify workout proof.', 'error');
      return;
    }

    window.showToast('Verifying Elite Proof...', 'info');

    const formData = new FormData();
    if (file) formData.append('file', file);
    if (textProof) formData.append('text_proof', textProof);

    try {
      const res = await fetch(`${API_URL}/api/workouts/verify?token=${encodeURIComponent(token)}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });
      const data = await res.json();

      if (res.ok) {
        window.showToast('Neural Analysis Complete!', 'success');

          // 1. UPDATE CUMULATIVE STATS
          const burnEl = document.querySelector('.area-stats div:nth-child(1) .stat-value');
          if (burnEl) {
            const current = parseInt(burnEl.textContent.replace(',', ''));
            burnEl.innerHTML = `${(current + data.calories).toLocaleString()} <span class="text-sm font-normal text-[#555]">KCAL</span>`;
          }

          // 2. UPDATE PHYSIQUE FATIGUE
          const fatigueEl = document.getElementById('live-fatigue');
          const recoveryEl = document.getElementById('live-recovery');
          if (fatigueEl) {
            const current = parseFloat(fatigueEl.textContent.match(/[\d.]+/)[0]);
            fatigueEl.textContent = `CORE: ${(current + 5.2).toFixed(1)}% FATIGUE`;
          }
          if (recoveryEl) {
            const current = parseFloat(recoveryEl.textContent.match(/[\d.]+/)[0]);
            recoveryEl.textContent = `RECOVERY: ${(current - 4.5).toFixed(1)}%`;
          }

          // 3. IMPROVE RANK
          const rankEl = document.getElementById('user-rank');
          if (rankEl) {
            rankEl.textContent = '#13';
            window.showToast('You climbed to #13 in the community!', 'success');
          }
          
          // --- AI BRAIN LIVE REACTION ---
          const chatWindow = document.getElementById('chatbotWindow');
          if (chatWindow) {
              const messagesContainer = document.getElementById('chatMessages');
              if (messagesContainer) {
                  const msgDiv = document.createElement('div');
                  msgDiv.className = `message bot`;
                  msgDiv.innerHTML = `<span class="text-green-400 font-bold">VERIFIED:</span><br>WORLD LIBRARY SCANNED: ${data.exercise} verified! Neural sync complete.`;
                  msgDiv.classList.remove('hidden');
                  messagesContainer.appendChild(msgDiv);
                  messagesContainer.scrollTop = messagesContainer.scrollHeight;
              }
          }
          
          if (typeof window.updateNeuralCoach === 'function') {
              window.updateNeuralCoach();
          }

          // 4. SHOW VERIFICATION IN FEED
          const feed = document.getElementById('live-activity-feed');
          if (feed) {
            const item = document.createElement('div');
            item.className = 'text-[9px] flex flex-col gap-1 p-2 bg-yellow-400/10 border border-yellow-400/20 rounded-lg mt-2';
            item.innerHTML = `
                <div class="flex justify-between items-start">
                  <div>
                    <div class="text-[10px] font-bold uppercase tracking-widest text-yellow-400">${data.exercise || 'Workout'}</div>
                    <div class="text-[8px] text-[#555] font-bold mt-0.5">Just now &bull; ${data.formScore}% Form</div>
                  </div>
                  <div class="text-right flex flex-col items-end">
                    <span class="text-[10px] font-bold px-1.5 py-0.5 bg-green-500/10 text-green-500 rounded">SYNCED</span>
                    <span class="text-[8px] text-[#888] font-bold mt-1 flex items-center gap-1">
                      <span>Verified</span>
                    </span>
                  </div>
                </div>
              `;
            feed.prepend(item);
          }

          // 5. UPDATE HEATMAP (ADD NEW SESSION)
          if (typeof generateHeatmap === 'function') generateHeatmap(true);

          // 6. UPDATE GRAPHS (ADD DATA POINT)
          updateDataHUD(data.calories);

          // 7. UPDATE DASHBOARD LATEST VAULT
          if (typeof fetchLatestVerification === 'function') {
            fetchLatestVerification();
          }
        } else {
          window.showToast(data.detail || 'Analysis failed.', 'error');
        }
      } catch (err) {
        window.showToast('Cloud analysis server connecting...', 'info');
      }
    }

  // --- VAULT SYNC ---
  window.fetchLatestVerification = async function() {
    const box = document.getElementById('latest-verification-box');
    if (!box) return;

    const token = localStorage.getItem('token') || localStorage.getItem('elite_token');
    if (!token) return;

    try {
        const apiBase = window.ELITE_API_URL || 'https://mygym-p9rd.onrender.com';
        const res = await fetch(`${apiBase}/api/workouts/?token=${encodeURIComponent(token)}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (res.ok) {
            const workouts = await res.json();
            if (workouts.length > 0) {
                const w = workouts.sort((a,b) => new Date(b.date) - new Date(a.date))[0];
                const utcDate = w.date.endsWith('Z') ? w.date : w.date + 'Z';
                const d = new Date(utcDate).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
                
                document.getElementById('latest-verification-time').textContent = `Latest: ${d}`;
                document.getElementById('latest-verification-title').textContent = `${w.exercise}`;
                
                const mediaDiv = document.getElementById('latest-verification-media');
                if (w.videoUrl) {
                    const isVideo = w.videoUrl.match(/\.(mp4|webm|mov)$/i);
                    if (isVideo) {
                        mediaDiv.innerHTML = `<video src="${w.videoUrl}" class="w-full h-full object-cover rounded-lg" muted></video>`;
                    } else {
                        mediaDiv.innerHTML = `<img src="${w.videoUrl}" class="w-full h-full object-cover rounded-lg">`;
                    }
                    mediaDiv.style.backgroundImage = 'none';
                } else {
                    const proofText = w.text_proof ? w.text_proof : 'Text Verification';
                    mediaDiv.innerHTML = `<div class="w-full h-full flex flex-col items-center justify-center p-1"><span class="text-[6px] text-white font-bold leading-none italic uppercase tracking-widest text-center" style="word-break: break-word;">${proofText.substring(0, 15)}...</span></div>`;
                    mediaDiv.style.backgroundImage = 'none';
                }
                
                box.classList.remove('hidden');
            }
        }
    } catch (e) {
        console.error("Vault sync failed", e);
    }
  };

  // --- GRAPHS UPDATE LOGIC ---
  function updateDataHUD(newBurn) {
    // Logic to simulate adding a point to Chart.js
    if (window.intensityChartInstance) {
      window.intensityChartInstance.data.datasets[0].data.push(85);
      window.intensityChartInstance.data.labels.push('Now');
      window.intensityChartInstance.update();
    }
  }

  // Update Macro Logic in updateEliteUI
  const originalUpdateEliteUI = window.updateEliteUI;
  window.updateEliteUI = function (profile) {
    originalUpdateEliteUI(profile);
    if (!profile) return;

    const weight = parseFloat(profile.weight || 75);
    const proteinEl = document.getElementById('diet-protein');
    const carbsEl = document.getElementById('diet-carbs');
    const fatsEl = document.getElementById('diet-fats');
    const recEl = document.getElementById('diet-rec');

    let p = 180, c = 250, f = 70, rec = "Maintenance Phase";

    if (profile.goal === 'Bulking') {
      p = Math.round(weight * 2.2);
      c = Math.round(weight * 5);
      f = Math.round(weight * 1);
      rec = "Anabolic Loading Phase";
    } else if (profile.goal === 'Fat Loss') {
      p = Math.round(weight * 2.5);
      c = Math.round(weight * 2);
      f = Math.round(weight * 0.8);
      rec = "Thermogenic Cutting Phase";
    } else if (profile.goal === 'Endurance') {
      p = Math.round(weight * 1.6);
      c = Math.round(weight * 6);
      f = Math.round(weight * 1.2);
      rec = "Glycogen Replenishment";
    }

    if (proteinEl) proteinEl.textContent = `${p}g`;
    if (carbsEl) carbsEl.textContent = `${c}g`;
    if (fatsEl) fatsEl.textContent = `${f}g`;
    if (recEl) recEl.textContent = rec;
  };


  // --- HEATMAP GENERATION ---
  async function generateHeatmap(isVerification = false) {
    const grid = document.getElementById('heatmap-grid');
    if (!grid) return;
    
    const token = localStorage.getItem('token') || localStorage.getItem('elite_token');
    let workoutCounts = Array(14).fill(0);
    
    if (token) {
        try {
            const apiBase = window.ELITE_API_URL || 'https://mygym-p9rd.onrender.com';
            const res = await fetch(`${apiBase}/api/workouts/?token=${encodeURIComponent(token)}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const workouts = await res.json();
                
                // --- NEURAL COACH FIX: Call it here directly so it shares the fetched data ---
                if (typeof window.updateNeuralCoach === 'function') {
                    window.updateNeuralCoach(workouts);
                }
                
                const today = new Date();
                today.setHours(23, 59, 59, 999);
                
                let todayCalories = 0;

                workouts.forEach(w => {
                    const utcDate = w.date.endsWith('Z') ? w.date : w.date + 'Z';
                    const wDate = new Date(utcDate);
                    const diffTime = Math.abs(today - wDate);
                    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
                    if (diffDays === 0) {
                        todayCalories += (w.calories || 0);
                    }
                    if (diffDays >= 0 && diffDays < 14) {
                        // We want chronological order in the grid, so array index 0 = 13 days ago, index 13 = today
                        workoutCounts[13 - diffDays]++;
                    }
                });

                // Dynamically update UI with today's calories
                const profile = JSON.parse(localStorage.getItem('elite_profile')) || {};
                const weight = parseFloat(profile.weight || 75);
                const height = parseFloat(profile.height || 180);
                const bmr = Math.round(10 * weight + 6.25 * height - 5 * 25 + 5);
            }
        } catch (e) {
            console.error("Failed to fetch workouts for heatmap", e);
        }
    }
    
    grid.innerHTML = '';
    
    // Create the 14 grid cells
    for (let i = 0; i < 2; i++) {
      const row = document.createElement('div');
      row.className = 'grid grid-cols-7 gap-2' + (i === 1 ? ' opacity-50' : '');
      for (let j = 0; j < 7; j++) {
        const cell = document.createElement('div');
        const dayIndex = (i * 7) + j;
        const count = workoutCounts[dayIndex];
        
        let colorClass = 'bg-[#111]';
        if (count === 1) colorClass = 'bg-yellow-900';
        else if (count === 2) colorClass = 'bg-yellow-700';
        else if (count >= 3) colorClass = 'bg-yellow-500';
        
        cell.className = `w-full aspect-square ${colorClass} rounded-sm transition-colors duration-1000`;
        row.appendChild(cell);
      }
      grid.appendChild(row);
    }
    
    // Calculate Daily Performance instead of 14-day consistency
    const profile = JSON.parse(localStorage.getItem('elite_profile')) || {};
    const weight = parseFloat(profile.weight || 75);
    const height = parseFloat(profile.height || 180);
    const bmr = Math.round(10 * weight + 6.25 * height - 5 * 25 + 5);
    let energyGoal = Math.round(bmr * 1.2);
    if (profile.goal === 'Bulking' || profile.goal === 'Hypertrophy') energyGoal = Math.round(bmr * 1.4);
    else if (profile.goal === 'Fat Loss') energyGoal = Math.round(bmr * 0.9);
    
    // We need to fetch todayCalories again since it's out of scope here, or we can just calculate it from workoutCounts? 
    // Wait, workoutCounts only has counts, not calories. Let's extract todayCalories globally or just fetch from the energy-label!
    let pct = 0;
    const eBar = document.getElementById('energy-bar');
    if (eBar && eBar.style.width) {
        pct = parseInt(eBar.style.width) || 0;
    }
    
    const valEl = document.getElementById('consistency-val');
    const barEl = document.getElementById('consistency-bar');
    if (valEl) valEl.innerText = `${pct}%`;
    if (barEl) barEl.style.width = `${pct}%`;
  }

  // --- LIVE ACTIVITY FEED ---
  async function initActivityFeed() {
    const feed = document.getElementById('live-activity-feed');
    const leaderList = document.getElementById('leaderboard-list');
    if (!feed && !leaderList) return;
    
    async function fetchLiveHUD() {
        const token = localStorage.getItem('token') || localStorage.getItem('elite_token');
        if (!token) return;
        
        try {
            const apiBase = window.ELITE_API_URL || 'https://mygym-p9rd.onrender.com';
            const res = await fetch(`${apiBase}/api/user/live-feed`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                
                // Update Leaderboard
                if (leaderList) {
                    leaderList.innerHTML = '';
                    data.leaderboard.forEach((user, index) => {
                        const rankHtml = index === 0 ? `<div class="rank-circle rank-1 mb-2">1</div>` : `<div class="rank-circle mb-2">${index + 1}</div>`;
                        leaderList.innerHTML += `
                            <div class="leader-item shrink-0 w-32 p-3 bg-white/5 rounded-xl border border-white/5">
                                ${rankHtml}
                                <div class="text-[10px] font-bold uppercase">${user.name}</div>
                                <div class="text-[8px] text-[#555]">${user.points} PTS</div>
                            </div>
                        `;
                    });
                }
                
                // Update Live Activity Feed
                if (feed) {
                    feed.innerHTML = '';
                    data.activities.forEach(act => {
                        const d = new Date(act.timestamp);
                        const timeStr = d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                        
                        feed.innerHTML += `
                            <div class="text-[9px] flex flex-col gap-1 p-2 bg-white/5 rounded-lg border border-white/5 mb-2">
                               <div class="flex justify-between">
                                 <span class="font-bold text-yellow-400">UPDATE</span>
                                 <span class="text-[#555]">${timeStr}</span>
                               </div>
                               <span class="text-[#888]"><span class="font-bold text-white">${act.userName}</span> ${act.text}</span>
                            </div>
                        `;
                    });
                }
            }
        } catch (e) {
            console.error("Failed to fetch live HUD", e);
        }
    }
    
    fetchLiveHUD();
    setInterval(fetchLiveHUD, 60000); // Refresh every 60 seconds
  }

  window.updateNeuralCoach = async function(workoutsArray) {
    const msgEl = document.getElementById('neural-coach-msg');
    const recEl = document.getElementById('neural-coach-recovery');
    const sleepEl = document.getElementById('neural-coach-sleep');
    if (!msgEl) return;
    
    try {
        const token = localStorage.getItem('token') || localStorage.getItem('elite_token');
        if (!token) return;
        
        const apiBase = window.ELITE_API_URL || 'https://mygym-p9rd.onrender.com';
        const res = await fetch(`${apiBase}/api/user/ai-insights?token=${encodeURIComponent(token)}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (res.ok) {
            const aiData = await res.json();
            
            // Set the dynamic AI insight
            msgEl.innerText = `"${aiData.insight}"`;
            
            // Display the exact Macros
            if (recEl && aiData.macros) {
                recEl.innerText = `GOAL MACROS: ${aiData.macros.protein}g P | ${aiData.macros.carbs}g C | ${aiData.macros.fats}g F`;
            }
            if (sleepEl && aiData.macros) {
                sleepEl.innerText = `CALORIES: ${aiData.macros.calories} KCAL`;
            }
        } else {
            msgEl.innerText = `"Your vault is currently empty. Upload your first workout proof to receive personalized, AI-driven biometric insights."`;
        }
    } catch(e) {
        console.error("Neural Coach Error:", e);
    }
  };

  generateHeatmap();
  initActivityFeed();
  
  const progressBars = document.querySelectorAll('.progress-bar');
  if (progressBars.length) {
    const progObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const bar = entry.target;
          const width = bar.style.width;
          bar.style.width = '0';
          setTimeout(() => { bar.style.width = width; }, 100);
          progObserver.unobserve(bar);
        }
      });
    }, { threshold: 0.5 });
    progressBars.forEach(bar => progObserver.observe(bar));
  }



  /* ---- ELITE FEEDBACK HANDLER ---- */
  const eliteFeedbackForm = document.getElementById('eliteFeedbackForm');
  if (eliteFeedbackForm) {
    eliteFeedbackForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const token = localStorage.getItem('token');
      if (!token) {
        window.showToast('Please sign in to submit feedback.', 'error');
        return;
      }

      const categoryEl = document.getElementById('feedbackCategory');
      const messageEl = document.getElementById('feedbackMessage');
      const sentimentEl = document.getElementById('feedbackSentiment');

      const category = categoryEl ? categoryEl.value : 'General';
      const message = messageEl ? messageEl.value : '';
      const sentiment = sentimentEl ? sentimentEl.value : 'neutral';

      if (!message) {
        window.showToast('Feedback message is required.', 'error');
        return;
      }

      const submitBtn = eliteFeedbackForm.querySelector('button[type="submit"]');
      const originalBtnText = submitBtn.textContent;
      submitBtn.disabled = true;
      submitBtn.textContent = 'TRANSMITTING...';

      try {
        const payload = {
          token: token,
          category: category,
          message: message,
          sentiment: sentiment
        };

        const targetUrl = window.ELITE_API_URL ? `${window.ELITE_API_URL}/api/user/feedback` : `${API_URL}/api/user/feedback`;

        const res = await fetch(targetUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (res.ok) {
          window.showToast('Elite Feedback Synchronized!', 'success');
          eliteFeedbackForm.reset();
          const formContainer = document.getElementById('feedbackFormContainer');
          const successState = document.getElementById('feedbackSuccessState');
          if (formContainer && successState) {
            formContainer.classList.add('hidden');
            successState.classList.remove('hidden');
          }
        } else {
          window.showToast(data.detail || 'Feedback sync failed.', 'error');
          submitBtn.disabled = false;
          submitBtn.textContent = originalBtnText;
        }
      } catch (err) {
        console.error('Feedback submission error:', err);
        window.showToast('Neural connection unstable. Try again.', 'error');
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = originalBtnText;
        }
      }
    });
  }

  /* ---- BMI CALCULATOR LOGIC ---- */
  const bmiForm = document.getElementById('bmiForm');
  const bmiResultBox = document.getElementById('bmiResultBox');
  const bmiPlaceholder = document.getElementById('bmiPlaceholder');
  const bmiValueDisplay = document.getElementById('bmiValue');
  const bmiStatusDisplay = document.getElementById('bmiStatus');
  const bmiAdviceDisplay = document.getElementById('bmiAdvice');
  const bmiCircle = document.getElementById('bmiCircle');
  const scaleItems = document.querySelectorAll('.scale-item');

  window.resetBmi = function () {
    if (bmiForm) bmiForm.reset();
    if (bmiPlaceholder) bmiPlaceholder.classList.remove('hidden');
    if (bmiResultBox) bmiResultBox.classList.add('hidden');
    if (bmiCircle) bmiCircle.style.strokeDashoffset = '283';
    scaleItems.forEach(item => item.classList.remove('active'));
  };

  if (bmiForm) {
    bmiForm.addEventListener('submit', function (e) {
      e.preventDefault();

      const height = parseFloat(document.getElementById('bmiHeight').value) / 100;
      const weight = parseFloat(document.getElementById('bmiWeight').value);

      if (height > 0 && weight > 0) {
        const bmi = (weight / (height * height)).toFixed(1);

        // Hide placeholder, show result
        if (bmiPlaceholder) bmiPlaceholder.classList.add('hidden');
        if (bmiResultBox) bmiResultBox.classList.remove('hidden');

        // Animate score
        let startValue = 0;
        const duration = 1500;
        const startTime = performance.now();

        function animate(currentTime) {
          const elapsed = currentTime - startTime;
          const progress = Math.min(elapsed / duration, 1);
          const currentBmi = (progress * bmi).toFixed(1);
          if (bmiValueDisplay) bmiValueDisplay.textContent = currentBmi;

          if (progress < 1) {
            requestAnimationFrame(animate);
          }
        }
        requestAnimationFrame(animate);

        // Animate Gauge
        const maxBmi = 40;
        const circumference = 283; // 2 * Math.PI * 45
        const offset = circumference - (Math.min(bmi, maxBmi) / maxBmi) * circumference;
        if (bmiCircle) bmiCircle.style.strokeDashoffset = offset;

        // Determine Status
        let status = '';
        let advice = '';
        let statusClass = '';

        if (bmi < 18.5) {
          status = 'Underweight';
          advice = 'Boost your nutrient intake. Consult our nutritionists for a custom plan.';
          statusClass = 'underweight';
        } else if (bmi < 25) {
          status = 'Healthy';
          advice = 'Perfect balance! Maintain your elite training and clean eating habits.';
          statusClass = 'healthy';
        } else if (bmi < 30) {
          status = 'Overweight';
          advice = 'Time to ramp up the cardio. Our HIIT classes will help you trim down fast.';
          statusClass = 'overweight';
        } else {
          status = 'Obese';
          advice = 'Your health is priority #1. Join our transformation program today.';
          statusClass = 'obese';
        }

        if (bmiStatusDisplay) bmiStatusDisplay.textContent = status;
        if (bmiAdviceDisplay) bmiAdviceDisplay.textContent = advice;

        // Update Scale
        scaleItems.forEach(item => {
          item.classList.remove('active');
          if (item.getAttribute('data-status') === statusClass) {
            item.classList.add('active');
          }
        });


        window.showToast('BMI Calculated Successfully!', 'success');
      }
    });
  }



  // window.bookClass is defined globally at the end of the file for maximum compatibility


  // --- IMAGE COMPARISON SLIDER ---
  function initComparisonSlider() {
    const containers = document.querySelectorAll('.comparison-container');

    containers.forEach(container => {
      const handle = container.querySelector('.comparison-handle');
      const afterImg = container.querySelector('.comparison-after');
      let isDragging = false;

      const moveSlider = (e) => {
        if (!isDragging) return;

        const rect = container.getBoundingClientRect();
        const clientX = e.type.includes('touch') ? e.touches[0].pageX : e.pageX;
        let x = clientX - rect.left - window.scrollX;

        // Boundaries
        if (x < 0) x = 0;
        if (x > rect.width) x = rect.width;

        const percent = (x / rect.width) * 100;

        handle.style.left = `${percent}%`;
        afterImg.style.clipPath = `inset(0 0 0 ${percent}%)`;
      };

      const startDragging = (e) => {
        isDragging = true;
        e.preventDefault();
      };
      const stopDragging = () => isDragging = false;

      handle.addEventListener('mousedown', startDragging);
      window.addEventListener('mouseup', stopDragging);
      window.addEventListener('mousemove', moveSlider);

      handle.addEventListener('touchstart', startDragging);
      window.addEventListener('touchend', stopDragging);
      window.addEventListener('touchmove', moveSlider);
    });
  }

  renderSchedule(scheduleGrid, currentDay, currentFilter);
  renderSchedule(homeScheduleGrid, currentDay, 'all');
  initComparisonSlider();

  /* ---- NEURAL PAGE ROUTER (BACKEND SYNC) ---- */
  let path = window.location.pathname.split('/').pop() || 'index.html';
  if (path && !path.endsWith('.html') && !path.includes('?')) {
      path += '.html';
  }
  // Remove any query params for clean matching
  path = path.split('?')[0];

  // 1. ADMIN MODULE SYNC (admin.html)
  if (path === 'admin.html') {
    const adminToken = localStorage.getItem('token');

    window.fetchAdminStats = async function () {
      try {
        const res = await fetch(`${API_URL}/api/admin/stats?token=${adminToken}`);
        const stats = await res.json();
        const mappings = {
          'stat-users': stats.totalUsers,
          'stat-bookings': stats.totalBookings,
          'stat-revenue': `$${(stats.estimatedRevenue || 0).toLocaleString()}`,
          'stat-active': stats.recentActivities ? stats.recentActivities.length : 0
        };
        Object.entries(mappings).forEach(([id, val]) => {
          const el = document.getElementById(id);
          if (el) el.textContent = val || 0;
        });
      } catch (err) { console.error('Admin telemetry sync failed.'); }
    };

    window.fetchAdminUsers = async function () {
      try {
        const res = await fetch(`${API_URL}/api/admin/users?token=${adminToken}`);
        const users = await res.json();
        const list = document.getElementById('admin-user-list');
        if (list) {
          list.innerHTML = users.map(u => `
            <tr class="border-b border-[#111]">
              <td class="py-4 font-bold uppercase italic text-xs">${u.firstName} ${u.lastName}</td>
              <td class="text-[#555] text-[10px] font-bold">${u.email}</td>
              <td><span class="px-2 py-1 bg-yellow-400/10 text-yellow-400 rounded text-[9px] font-bold uppercase">${u.membershipType}</span></td>
            </tr>
          `).join('') || '<tr><td colspan="3" class="text-center py-4 text-[#444] uppercase font-bold text-[10px]">No members found</td></tr>';
        }
      } catch (err) { console.error('User base sync failed.'); }
    };

    // Neural Bridge: Connect buttons by label (no HTML changes needed)
    const adminButtons = document.querySelectorAll('button, .btn');
    adminButtons.forEach(btn => {
      const txt = btn.textContent.toLowerCase();
      if (txt.includes('add video')) {
        btn.onclick = (e) => {
          e.preventDefault();
          const form = document.getElementById('addVideoForm');
          if (form) form.dispatchEvent(new Event('submit'));
        };
      }
      if (txt.includes('create session')) {
        btn.onclick = (e) => {
          e.preventDefault();
          const form = document.getElementById('add-class-form');
          if (form) form.dispatchEvent(new Event('submit'));
        };
      }
      if (txt.includes('broadcast')) {
        btn.onclick = (e) => {
          e.preventDefault();
          if (typeof window.sendBroadcast === 'function') window.sendBroadcast();
        };
      }
    });

    window.fetchAdminStats();
    window.fetchAdminUsers();

    window.fetchMentorships = async function () {
        try {
            const res = await fetch(`${API_URL}/api/admin/mentorships?token=${adminToken}`);
            const data = await res.json();
            const tbody = document.getElementById('mentorshipTable');
            if(tbody) {
                tbody.innerHTML = data.map(m => `
                    <tr class="border-b border-[#111]">
                        <td class="py-4">
                            <div class="font-bold text-xs uppercase italic">${m.name}</div>
                            <div class="text-[10px] text-gray-400 font-bold">${m.email}</div>
                        </td>
                        <td class="text-[#555] text-[10px] font-bold">${m.preferred_date}</td>
                        <td><span class="px-2 py-1 bg-white/5 rounded text-[9px] font-bold uppercase">${m.fitness_level}</span></td>
                        <td style="max-width: 250px; white-space: normal; font-size: 10px; color: #bbb;">${m.message || ''}</td>
                        <td><span class="px-2 py-1 ${m.status === 'pending' ? 'bg-yellow-400/20 text-yellow-400' : 'bg-green-500/20 text-green-500'} rounded text-[9px] font-bold uppercase">${m.status.toUpperCase()}</span></td>
                        <td>
                            ${m.status === 'pending' 
                                ? `<button onclick="updateMentorship('${m._id}', 'approved')" class="btn-yellow px-3 py-1 rounded text-[9px] font-bold">Approve</button>`
                                : `<span class="text-green-500 text-[10px] font-bold">✔ Done</span>`
                            }
                        </td>
                    </tr>
                `).join('') || '<tr><td colspan="6" class="text-center py-4 text-[#444] uppercase font-bold text-[10px]">No requests found</td></tr>';
            }
        } catch (err) { console.error('Mentorship sync failed.', err); }
    };
    
    window.updateMentorship = async function(id, status) {
        if(!confirm('Approve this mentorship request?')) return;
        try {
            const res = await fetch(`${API_URL}/api/admin/mentorships/${id}/status?token=${adminToken}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({status: status})
            });
            if(res.ok) {
                window.showToast('Request approved!', 'success');
                window.fetchMentorships();
            } else {
                window.showToast('Failed to approve', 'error');
            }
        } catch (e) { console.error(e); window.showToast('Error', 'error'); }
    };

    window.fetchMentorships();


    setInterval(window.fetchAdminStats, 15000);
  }

  // 2. ACTIVITY MODULE SYNC (activity.html)
  if (path === 'activity.html') {
    window.fetchVideoVault = async function () {
      try {
        const res = await fetch(`${API_URL}/api/user/videos`);
        const videos = await res.json();

        const renderCategory = (catName, items) => {
          const containers = document.querySelectorAll('.mb-16');
          containers.forEach(container => {
            const h2 = container.querySelector('h2');
            if (h2 && h2.textContent.toLowerCase().includes(catName.toLowerCase())) {
              const grid = container.querySelector('.grid');
              if (grid && items.length > 0) {
                grid.innerHTML = items.map(v => `
                  <div class="video-card" onclick="playVideo('${v.url}')">
                    <div class="video-thumb">
                      <img src="${v.thumbnail}" alt="${v.title}">
                      <div class="play-btn-overlay"><div class="play-icon">▶</div></div>
                    </div>
                    <div class="video-info">
                      <span class="video-tag">${v.category}</span>
                      <h4 class="video-title">${v.title}</h4>
                      <div class="video-meta"><span>${v.duration}</span> <span>·</span> <span>${v.trainer}</span></div>
                    </div>
                  </div>
                `).join('');
              }
            }
          });
        };

        renderCategory('HIIT', videos.filter(v => v.category === 'HIIT'));
        renderCategory('Strength', videos.filter(v => v.category === 'Strength'));
        renderCategory('Recovery', videos.filter(v => v.category === 'Recovery'));
      } catch (err) { console.error('Video vault sync failed.'); }
    };
    window.fetchVideoVault();
  }

  // 3. ABOUT/CONTACT MODULE SYNC
  if (path === 'about.html' || path === 'contact.html') {
    const newsBtn = document.getElementById('newsletter-subscribe');
    if (newsBtn) {
      newsBtn.onclick = async () => {
        const email = document.getElementById('newsletter-email').value;
        if (!email) return window.showToast('Please enter an email', 'error');
        try {
          const res = await fetch(`${API_URL}/api/user/activity`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userEmail: email, action: 'Newsletter Signup', details: `${path} lead` })
          });
          if (res.ok) {
            window.showToast('Welcome to the movement', 'success');
            document.getElementById('newsletter-email').value = '';
          }
        } catch (err) { console.error('Lead sync failed.'); }
      };
    }
  }

  // 4. CLASSES MODULE SYNC (classes.html)
  if (path === 'classes.html') {
    window.fetchLiveClasses = async function () {
      try {
        const res = await fetch(`${API_URL}/api/user/classes`);
        const classes = await res.json();
        const listWrap = document.getElementById('list-view-wrap');
        if (listWrap) {
          const grid = listWrap.querySelector('.grid');
          if (grid && classes.length > 0) {
            grid.innerHTML = classes.map(c => `
               <div class="class-card reveal visible">
                 <div class="class-card-img" style="height: 180px;">
                   <img src="${c.img || 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=500&h=300&fit=crop'}" alt="${c.className}">
                   ${c.category === 'HIIT' ? '<div class="live-tag"><div class="live-dot"></div> LIVE HUD</div>' : ''}
                 </div>
                 <div class="class-info">
                   <div class="class-meta">
                     <span class="intensity-badge intensity-high">${c.category}</span>
                     <span class="time">${c.time}</span>
                   </div>
                   <h3>${c.className}</h3>
                   <p>Elite instruction by ${c.trainerName}. Master your performance with real-time biometric tracking.</p>
                   <button class="btn btn-yellow w-full justify-center py-4 text-[10px] font-black italic tracking-widest" onclick="bookClass('${c.className}', '${c.time}', '${c.trainerName}')">Book Session</button>
                 </div>
               </div>
             `).join('');
          }
        }
      } catch (err) { console.error('Class schedule sync failed.'); }
    };
    window.fetchLiveClasses();
  }

  // 5. CHECKOUT MODULE SYNC (checkout.html)
  if (path === 'checkout.html') {
    const checkoutForm = document.querySelector('.checkout-grid');
    if (checkoutForm) {
      const payBtn = checkoutForm.querySelector('.btn-yellow');
      if (payBtn) {
        payBtn.onclick = async (e) => {
          e.preventDefault();
          const token = localStorage.getItem('token');
          const cart = JSON.parse(localStorage.getItem('cart') || '[]');
          if (!cart.length) return window.showToast('Your bag is empty', 'error');

          try {
            const res = await fetch(`${API_URL}/api/store/checkout?token=${token}`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                items: cart,
                total: cart.reduce((acc, item) => acc + (item.price * item.quantity), 0)
              })
            });
            if (res.ok) {
              localStorage.removeItem('cart');
              window.showToast('Order Fulfilled. Welcome to the Elite.', 'success');
              setTimeout(() => { window.location.href = 'dashboard.html'; }, 2000);
            }
          } catch (err) { console.error('Checkout sync failed.'); }
        };
      }
    }
  }



  // 9. PROFILE MODULE SYNC (profile.html)
  if (path === 'profile.html') {
    const profileForm = document.getElementById('profileUpdateForm');
    if (profileForm) {
      profileForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = profileForm.querySelector('button[type="submit"]');
        const originalText = btn.textContent;
        const token = localStorage.getItem('token');
        if (!token) return window.showToast('Login required', 'error');

        btn.disabled = true;
        btn.textContent = 'SYNCING ELITE HUD...';

        try {
          const formData = new FormData(profileForm);
          formData.append('token', token);
          const response = await fetch(`${API_URL}/api/user/update`, {
            method: 'POST',
            body: formData
          });
          const result = await response.json();
          if (response.ok && result.user) {
            localStorage.setItem('elite_profile', JSON.stringify(result.user));
            window.updateDashboardUI(result.user);
            window.showToast('Elite Profile Synchronized!', 'success');
          } else {
            window.showToast(result.detail || 'Update failed', 'error');
          }
        } catch (err) {
          console.error('Profile Sync Error:', err);
          window.showToast('Neural Sync Interrupted.', 'error');
        } finally {
          btn.disabled = false;
          btn.textContent = originalText;
        }
      });
    }
  }

  // 11. STUDIO MODULE SYNC (studio.html)
  if (path === 'studio.html') {
    if (typeof window.fetchVideoVault === 'function') window.fetchVideoVault();
  }

  // 12. TRAINER PROFILES SYNC (trainer-alex.html, trainer-kai.html, etc.)
  if (path.startsWith('trainer-')) {
    const bookBtn = document.querySelectorAll('.btn-yellow');
    bookBtn.forEach(btn => {
      if (btn.textContent.toLowerCase().includes('book')) {
        btn.onclick = (e) => {
          e.preventDefault();
          const trainerName = document.querySelector('h1')?.textContent || 'Elite Coach';
          window.showToast(`Syncing schedule for ${trainerName}...`, 'info');
          setTimeout(() => { window.location.href = 'workouts.html'; }, 1000);
        };
      }
    });
  }

  // 13. SUPPORT MODULE SYNC (support.html)
  if (path === 'support.html') {
    const contactTrigger = document.querySelector('.btn-contact-trigger');
    if (contactTrigger) {
      contactTrigger.onclick = () => {
        window.logActivity('Viewed Help Center');
      };
    }
  }

});

/* ---- STYLES INJECTION ---- */
const styles = `
  .toast { 
    position: fixed; bottom: 20px; right: 20px; 
    background: #111; color: #eee; 
    font-family: 'Inter', sans-serif; font-size: 12px; 
    padding: 12px 20px; border-radius: 12px; 
    border-left: 4px solid var(--yellow); 
    box-shadow: 0 10px 40px rgba(0,0,0,0.5); 
    z-index: 10000; opacity: 0; 
    transform: translateY(20px); transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1); 
    max-width: 90vw;
  } 
  .toast.show { opacity: 1; transform: translateY(0); } 
  .toast-error { border-left-color: #ff4d4d; } 
  .toast-success { border-left-color: #f5e642; } 
  .toast-info { border-left-color: #3498db; }
  @media (max-width: 640px) {
    .toast { bottom: 10px; right: 10px; left: 10px; font-size: 11px; padding: 10px 16px; border-radius: 10px; }
  }
  .hidden { display: none !important; }
`;
const sTag = document.createElement('style');
sTag.textContent = styles;
document.head.appendChild(sTag);

window.bookClass = async function (id, name, time, trainer) {
  // Handle different argument patterns for backward compatibility
  let className = name;
  let classTime = time;

  if (id !== 'static_class' && !time) {
    // Called with (name, time)
    className = id;
    classTime = name;
  }

  const token = localStorage.getItem('token');
  if (!token) {
    if (window.openAuthModal) window.openAuthModal('login');
    else window.showToast('Login required to book', 'error');
    return;
  }

  // Find the button to show loading state
  const event = window.event;
  let btn = null;
  if (event && event.target) {
    btn = event.target.closest('button');
  }
  if (btn) {
    btn.disabled = true;
    btn.textContent = 'SYNCING...';
  }

  const classId = id === 'static_class' ? className.toLowerCase().replace(/\s+/g, '_') : id;

  try {
    const res = await fetch(`${API_URL}/api/user/book?class_id=${encodeURIComponent(classId)}&token=${token}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await res.json();

    if (res.ok) {
      window.showToast('Neural Slot Secured: ' + className, 'success');
      if (btn) {
        btn.textContent = 'BOOKED';
        btn.classList.add('opacity-50');
      }
      window.logActivity(`Booked ${className}`);
      if (typeof fetchActivities === 'function') fetchActivities();
    } else {
      window.showToast(data.detail || 'Neural link failed', 'error');
      if (btn) {
        btn.disabled = false;
        btn.textContent = 'RETRY';
      }
    }
  } catch (err) {
    window.showToast('Connection interrupted', 'error');
    if (btn) {
      btn.disabled = false;
      btn.textContent = 'RETRY';
    }
  }
};

/* ============================================
   AI SUPPORT CHAT WIDGET
   ============================================ */

window.parseJwt = function(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) {
        return null;
    }
};

window.allSupportMessages = [];
window.activeSupportEmail = null;
window.adminSupportChatInterval = null;

window.fetchSupportMessages = async function() {
    const token = localStorage.getItem('token');
    if (!token) return;
    const payload = window.parseJwt(token);
    const role = payload ? payload.role : 'user';
    const endpoint = role === 'superadmin' ? 'owner' : 'trainer';
    const activeAPI = window.ELITE_API_URL || 'https://mygym-p9rd.onrender.com';
    
    try {
        const res = await fetch(`${activeAPI}/api/support/${endpoint}?token=${encodeURIComponent(token)}`);
        if (res.ok) {
            window.allSupportMessages = await res.json();
            window.renderSupportUsersList();
            if (window.activeSupportEmail) window.selectSupportUser(window.activeSupportEmail);
        } else {
            window.renderSupportUsersList();
        }
    } catch (err) { 
        console.error(err); 
        window.renderSupportUsersList();
    }
};

window.renderSupportUsersList = function() {
    const container = document.getElementById('support-users-list');
    if(!container) return;
    const users = {};
    
    window.allSupportMessages.forEach(m => {
        if (!users[m.senderEmail]) {
            users[m.senderEmail] = { name: m.senderName, email: m.senderEmail, messages: [], hasOpen: false };
        }
        users[m.senderEmail].messages.push(m);
        if (m.status === 'open') users[m.senderEmail].hasOpen = true;
    });
    
    const userListHTML = Object.values(users).map(u => `
        <div onclick="window.selectSupportUser('${u.email}')" class="admin-support-item ${u.hasOpen ? 'unread' : ''}">
            <div>
                <div class="admin-support-name">${u.name}</div>
                <div class="admin-support-email">${u.email}</div>
            </div>
            ${u.hasOpen ? '<div class="unread-dot"></div>' : ''}
        </div>
    `).join('') || '<div style="padding: 20px; text-align: center; color: #888; font-size: 12px; font-style: italic;">No conversations found.</div>';
    
    container.innerHTML = userListHTML;
    
    
};

window.selectSupportUser = function(email) {
    window.activeSupportEmail = email;
    
    const userMsgs = window.allSupportMessages.filter(m => m.senderEmail === email).reverse();
    const userName = userMsgs.length > 0 ? userMsgs[userMsgs.length - 1].senderName : email;
    
    const headerTitle = document.getElementById('support-active-header-title');
    if(headerTitle) headerTitle.textContent = userName;
    
    const msgsContainer = document.getElementById('support-active-messages');
    if(msgsContainer) {
        msgsContainer.innerHTML = userMsgs.map(m => `
            <div style="display: flex; flex-direction: column; width: 100%;">
                <div class="msg-bubble msg-user">
                    ${m.message}
                </div>
                ${m.reply ? `
                    <div class="msg-bubble msg-admin">
                        ${m.reply}
                    </div>
                ` : ''}
            </div>
        `).join('');
        msgsContainer.scrollTop = msgsContainer.scrollHeight;
    }
    
    const replyMsgId = userMsgs.length > 0 ? userMsgs[userMsgs.length - 1]._id : null;
    const replyArea = document.getElementById('support-reply-area');
    if (replyArea && replyMsgId) {
        replyArea.setAttribute('data-reply-id', replyMsgId);
    }
    
    const replyInput = document.getElementById('support-reply-input');
    if(replyInput) replyInput.focus();
};
window.backToSupportList = function() {
    window.activeSupportEmail = null;
    document.getElementById('adminSupportListView').style.display = 'flex';
    document.getElementById('adminSupportChatView').style.display = 'none';
    window.renderSupportUsersList();
};

window.sendActiveSupportReply = async function() {
    const token = localStorage.getItem('token');
    const replyArea = document.getElementById('support-reply-area');
    const id = replyArea.getAttribute('data-reply-id');
    const input = document.getElementById('support-reply-input');
    const reply = input.value;
    const activeAPI = window.ELITE_API_URL || 'https://mygym-p9rd.onrender.com';
    
    if (!reply || !id || !token) return;
    
    try {
        const res = await fetch(`${activeAPI}/api/support/${id}/reply?token=${encodeURIComponent(token)}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reply })
        });
        if (res.ok) {
            input.value = '';
            window.fetchSupportMessages();
        } else {
            window.showToast("Failed to reply", "error");
        }
    } catch (err) { console.error(err); }
};

function initSupportWidget() {
    const token = localStorage.getItem("token");
    if(!token) return;
    
    // Do not inject any floating widget on admin or trainer panels
    const pathName = window.location.pathname;
    if (pathName.includes('admin') || pathName.includes('trainer')) return;
    
    // Inject user widget for everyone on the normal frontend pages
    initUserSupportWidget();
}

