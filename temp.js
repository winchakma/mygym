
    function openMediaModal(url, type) {
        const modal = document.getElementById('mediaModal');
        const container = document.getElementById('mediaModalContentContainer');
        if (!modal || !container) return;
        
        container.innerHTML = '';
        if (type === 'image') {
            container.innerHTML = `<img src="${url}" class="max-w-full rounded-lg shadow-lg" style="max-height: 70vh;">`;
        } else if (type === 'video') {
            container.innerHTML = `<video src="${url}" controls autoplay class="w-full rounded-lg shadow-lg" style="max-height: 70vh;"></video>`;
        }
        modal.classList.remove('hidden');
    }
    
    function closeMediaModal(event) {
        if (event && event.target.id !== 'mediaModal' && event.target.tagName !== 'BUTTON' && !event.target.classList.contains('modal-close')) return;
        const modal = document.getElementById('mediaModal');
        const container = document.getElementById('mediaModalContentContainer');
        if (modal) modal.classList.add('hidden');
        if (container) container.innerHTML = ''; // Stop video playback
    }
  