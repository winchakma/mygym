document.addEventListener('DOMContentLoaded', () => {
    const activeAPI = window.ELITE_API_URL || "https://mygym-p9rd.onrender.com";

    // 1. Fetch Stats
    fetch(`${activeAPI}/api/public/stats`)
        .then(res => res.json())
        .then(data => {
            // Update big header stats (Testimonials section)
            const memEl = document.getElementById('liveTotalMembers');
            if(memEl) memEl.innerText = formatNumber(data.totalMembers);
            
            const ratEl = document.getElementById('liveOverallRating');
            if(ratEl) ratEl.innerText = data.overallRating === 0 ? "N/A" : data.overallRating.toFixed(2);

            // Update Yellow Stat Bar

            const statActive = document.getElementById('statActiveMembers');
            if(statActive) statActive.innerText = formatNumber(data.totalMembers);
        })
        .catch(err => console.error('Error fetching stats:', err));

    // 2. Fetch Reviews (Testimonials)
    fetch(`${activeAPI}/api/public/reviews`)
        .then(res => res.json())
        .then(data => {
            const track = document.getElementById('testiTrack');
            const section = document.getElementById('testimonialsSection');
            
            if (!track) return;
            
            if (!data || data.length === 0) {
                // If there are exactly 0 reviews, completely hide the section.
                if (section) section.style.display = 'none';
                return;
            }

            track.innerHTML = ''; // clear placeholders
            
            data.forEach((review, index) => {
                const delayClass = index === 0 ? '' : `testi-card-delay-${index}`;
                const pic = review.avatarUrl.startsWith('/uploads/') ? activeAPI + review.avatarUrl : review.avatarUrl;
                const html = `
                  <div class="testi-card ${delayClass}">
                    <div class="testi-quote">"</div>
                    <p class="testi-text">${review.quote}</p>
                    <div class="testi-author">
                      <img class="testi-avatar" src="${pic}" alt="${review.userName}"/>
                      <div>
                        <div class="testi-name">${review.userName}</div>
                        <div class="testi-loc">${review.location}</div>
                      </div>
                    </div>
                  </div>
                `;
                track.innerHTML += html;
            });
        })
        .catch(err => {
            console.error('Error fetching reviews:', err);
            const section = document.getElementById('testimonialsSection');
            if (section) section.style.display = 'none'; // Hide if backend is down
        });

    // 3. Fetch Transformations
    fetch(`${activeAPI}/api/public/transformations`)
        .then(res => res.json())
        .then(data => {
            const grid = document.getElementById('transformationsGrid');
            const section = document.getElementById('transformationsSection');

            if (!grid) return;

            if (!data || data.length === 0) {
                // If exactly 0 transformations, completely hide the section.
                if (section) section.style.display = 'none';
                return;
            }

            grid.innerHTML = ''; // clear placeholders
            
            data.forEach((trans, index) => {
                const delayClass = index === 0 ? '' : `story-card-delay-${index}`;
                const html = `
                <div class="story-card ${delayClass}">
                  <div class="story-header">
                    <img src="${trans.avatarUrl}" class="story-avatar" alt="${trans.userName}">
                    <div class="story-meta">
                      <h4>${trans.userName}</h4>
                      <span>${trans.badge}</span>
                    </div>
                  </div>
                  <p class="story-content">"${trans.quote}"</p>
                  <div class="story-stats">
                    <div class="s-stat-item">
                      <div class="s-stat-val">${trans.stat1Value}</div>
                      <div class="s-stat-lab">${trans.stat1Label}</div>
                    </div>
                    <div class="s-stat-item">
                      <div class="s-stat-val">${trans.stat2Value}</div>
                      <div class="s-stat-lab">${trans.stat2Label}</div>
                    </div>
                  </div>
                </div>
                `;
                grid.innerHTML += html;
            });
        })
        .catch(err => {
            console.error('Error fetching transformations:', err);
            const section = document.getElementById('transformationsSection');
            if (section) section.style.display = 'none'; // Hide if backend is down
        });
});

function formatNumber(num) {
    if (num === 0) return "0";
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
    }
    return num.toString();
}
