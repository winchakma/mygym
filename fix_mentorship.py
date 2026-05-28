import glob

# 1. Fix 'primary goal' required attribute in all trainer html files
for f in glob.glob('frontend/trainer-*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = content.replace('"What is your primary goal for this session?" required></textarea>', '"What is your primary goal for this session?"></textarea>')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

# 2. Inject fetchMentorships into frontend/js/script.js
with open('frontend/js/script.js', 'r', encoding='utf-8') as file:
    js_content = file.read()

mentorship_js = '''
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
'''

if 'fetchMentorships' not in js_content:
    js_content = js_content.replace('window.fetchAdminUsers();', f'window.fetchAdminUsers();\n{mentorship_js}\n    window.fetchMentorships();')
    with open('frontend/js/script.js', 'w', encoding='utf-8') as file:
        file.write(js_content)
