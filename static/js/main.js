document.addEventListener('DOMContentLoaded', () => {
    // 1. Year handler
    const yearEl = document.querySelector('#year');
    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }

    // 1.5 Splash overlay handler
    const splash = document.getElementById('splash-overlay');
    const enterBtn = document.getElementById('enter-site-btn');

    if (splash && enterBtn) {
        if (sessionStorage.getItem('entered_site') === 'true') {
            splash.style.display = 'none';
        } else {
            splash.classList.remove('hidden');
            enterBtn.addEventListener('click', () => {
                sessionStorage.setItem('entered_site', 'true');
                splash.classList.add('hidden');
                setTimeout(() => {
                    splash.style.display = 'none';
                }, 800); // Remove display after transition
                
                // Play music on click!
                isPlaying = true;
                localStorage.setItem('bg_music_playing', 'true');
                playAudio();
            });
        }
    }

    // 2. Global background music player
    const audio = document.getElementById('global-bg-audio');
    const toggleBtn = document.getElementById('music-toggle-btn');
    const musicIcon = document.getElementById('music-icon');
    const heartPulse = document.getElementById('heart-pulse');
    const pillTitle = document.getElementById('player-song-title');
    const pillStatus = document.getElementById('player-status-icon');

    if (!audio || !toggleBtn) return;

    // Load state from localStorage
    const defaultSong = audio.getAttribute('data-default-song') || 'tum_se_hi.mp3';
    const defaultTitle = audio.getAttribute('data-default-title') || 'Tum Se Hi 🌸';

    const lastDefaultSong = localStorage.getItem('last_default_song');
    if (lastDefaultSong !== defaultSong) {
        localStorage.setItem('bg_music_file', defaultSong);
        localStorage.setItem('bg_music_title', defaultTitle);
        localStorage.setItem('last_default_song', defaultSong);
        localStorage.setItem('bg_music_time', '0');
    }

    let songFile = localStorage.getItem('bg_music_file') || defaultSong;
    let songTitle = localStorage.getItem('bg_music_title') || defaultTitle;
    let isPlaying = localStorage.getItem('bg_music_playing') !== 'false';
    let savedTime = parseFloat(localStorage.getItem('bg_music_time')) || 0;

    // Build correct source URL
    audio.src = `/media/music/${songFile}`;

    // Set initial playback position once metadata is loaded
    if (audio.readyState >= 1) {
        if (savedTime > 0) {
            audio.currentTime = savedTime;
        }
    } else {
        audio.addEventListener('loadedmetadata', () => {
            if (savedTime > 0) {
                audio.currentTime = savedTime;
            }
        });
    }

    // Save playback position in real-time, but only when playing and time is valid
    audio.addEventListener('timeupdate', () => {
        if (!audio.paused && audio.currentTime > 0) {
            localStorage.setItem('bg_music_time', audio.currentTime);
        }
    });

    // Auto-advance to NEXT SONG in playlist when current song ends
    audio.addEventListener('ended', () => {
        fetch('/music/api/playlist')
            .then(res => res.json())
            .then(playlist => {
                if (!playlist || playlist.length === 0) return;
                const currentFile = localStorage.getItem('bg_music_file') || defaultSong;
                let currentIndex = playlist.findIndex(t => t.file === currentFile);
                let nextIndex = (currentIndex + 1) % playlist.length;
                let nextTrack = playlist[nextIndex];
                if (nextTrack) {
                    window.setGlobalBgMusic(nextTrack.file, nextTrack.title);
                }
            })
            .catch(err => console.log('Playlist auto-advance error:', err));
    });

    function updateUI() {
        if (pillTitle) pillTitle.textContent = songTitle;
        if (audio.paused) {
            musicIcon.style.animation = 'none';
            heartPulse.style.animation = 'none';
            if (pillStatus) pillStatus.textContent = '▶️';
        } else {
            musicIcon.style.animation = 'musicRotate 3s linear infinite';
            heartPulse.style.animation = 'privateHeartbeat 1.2s infinite';
            if (pillStatus) pillStatus.textContent = '⏸️';
        }
    }

    let isPlayPending = false;

    function playAudio() {
        if (isPlayPending) return;

        const checkTime = parseFloat(localStorage.getItem('bg_music_time')) || 0;
        if (audio.currentTime === 0 && checkTime > 0) {
            audio.currentTime = checkTime;
        }

        isPlayPending = true;
        audio.play().then(() => {
            isPlayPending = false;
            isPlaying = true;
            localStorage.setItem('bg_music_playing', 'true');
            updateUI();
            removeInteractionListeners();
        }).catch(err => {
            isPlayPending = false;
            console.log("Autoplay blocked by browser. Music will play on click. ❤️", err);
        });
    }

    function pauseAudio() {
        audio.pause();
        isPlaying = false;
        localStorage.setItem('bg_music_playing', 'false');
        updateUI();
        removeInteractionListeners();
    }

    // Toggle click handler
    toggleBtn.addEventListener('click', () => {
        if (audio.paused) {
            playAudio();
        } else {
            pauseAudio();
        }
    });


    // 3. User interaction autoplay triggers (scroll, touch, swipe, click)
    const playOnInteract = (e) => {
        // DO NOT play if user explicitly paused music!
        if (localStorage.getItem('bg_music_playing') === 'false') {
            removeInteractionListeners();
            return;
        }

        // DO NOT play music if Welcome Splash Screen is still active!
        const splashEl = document.getElementById('splash-overlay');
        if (splashEl && splashEl.style.display !== 'none' && !splashEl.classList.contains('hidden')) {
            return;
        }

        if (audio.paused) {
            playAudio();
        }
    };

    function removeInteractionListeners() {
        document.removeEventListener('click', playOnInteract);
        document.removeEventListener('touchstart', playOnInteract);
        document.removeEventListener('scroll', playOnInteract);
        document.removeEventListener('wheel', playOnInteract);
        document.removeEventListener('keydown', playOnInteract);
    }

    // Only add interaction listeners if user has NOT explicitly paused the music!
    if (localStorage.getItem('bg_music_playing') !== 'false') {
        document.addEventListener('click', playOnInteract);
        document.addEventListener('touchstart', playOnInteract);
        document.addEventListener('scroll', playOnInteract);
        document.addEventListener('wheel', playOnInteract);
        document.addEventListener('keydown', playOnInteract);
    }

    // Attempt autoplay immediately ONLY IF splash screen is already dismissed!
    const activeSplash = document.getElementById('splash-overlay');
    const isSplashVisible = activeSplash && activeSplash.style.display !== 'none' && !activeSplash.classList.contains('hidden');

    if (isPlaying && !isSplashVisible) {
        playAudio();
    } else {
        removeInteractionListeners();
    }
    updateUI();

    // 4. Auto-pause background music when a video plays, and resume when video pauses/ends
    let wasMusicPausedByVideo = false;

    document.addEventListener('play', function(e) {
        if (e.target && e.target.tagName === 'VIDEO') {
            if (!audio.paused) {
                wasMusicPausedByVideo = true;
                pauseAudio();
            }
        }
    }, true);

    document.addEventListener('pause', function(e) {
        if (e.target && e.target.tagName === 'VIDEO') {
            if (wasMusicPausedByVideo) {
                wasMusicPausedByVideo = false;
                playAudio();
            }
        }
    }, true);

    document.addEventListener('ended', function(e) {
        if (e.target && e.target.tagName === 'VIDEO') {
            if (wasMusicPausedByVideo) {
                wasMusicPausedByVideo = false;
                playAudio();
            }
        }
    }, true);



    // Expose global function to change background music from the playlist page
    window.setGlobalBgMusic = function(file, title, btnEl) {
        try {
            localStorage.setItem('bg_music_file', file);
            localStorage.setItem('bg_music_title', title);
            localStorage.setItem('bg_music_playing', 'true');
            localStorage.setItem('bg_music_time', '0');
        } catch(e) {}

        songFile = file;
        songTitle = title;
        savedTime = 0;

        // Reset all playlist buttons UI
        document.querySelectorAll('.music-play-btn').forEach(function(b) {
            b.style.background = '';
            var txt = b.querySelector('.play-text');
            var icn = b.querySelector('.play-icon');
            if (txt) txt.textContent = 'Play Song';
            if (icn) icn.textContent = '▶️';
        });

        // Update active button UI
        if (btnEl) {
            btnEl.style.background = 'linear-gradient(135deg, #2b8a3e 0%, #1b5e20 100%)';
            var txt = btnEl.querySelector('.play-text');
            var icn = btnEl.querySelector('.play-icon');
            if (txt) txt.textContent = 'Playing 🎶';
            if (icn) icn.textContent = '🔊';
        }

        if (audio) {
            audio.pause();
            audio.muted = false;
            audio.volume = 1.0;
            audio.src = `/media/music/${encodeURIComponent(file)}`;
            audio.currentTime = 0;
            playAudio();
        }
    };

});
