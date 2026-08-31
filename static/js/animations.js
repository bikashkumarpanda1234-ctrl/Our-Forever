/* =========================================================
   OUR FOREVER ❤️ - FLOWER SHOWER (FULA JHARIBA) & ANIMATIONS
========================================================= */

(function() {
    // Flower Petal Shower Trigger
    function triggerPetalShower(count = 40) {
        const petals = ['🌸', '🌹', '✨', '💮', '🌺', '💖', '🌷', '💕', '💗'];
        const container = document.body;

        for (let i = 0; i < count; i++) {
            setTimeout(() => {
                const petal = document.createElement('div');
                petal.className = 'petal-shower-leaf';
                petal.textContent = petals[Math.floor(Math.random() * petals.length)];
                
                const leftPos = Math.random() * 100; // 0 to 100vw
                const duration = 4.5 + Math.random() * 3.5; // 4.5s to 8s
                const size = 16 + Math.random() * 22; // 16px to 38px
                const delay = Math.random() * 1.5; // 0s to 1.5s delay

                petal.style.left = leftPos + 'vw';
                petal.style.fontSize = size + 'px';
                petal.style.animationDuration = duration + 's, ' + (2 + Math.random() * 2) + 's';
                petal.style.animationDelay = delay + 's, ' + delay + 's';
                
                container.appendChild(petal);

                setTimeout(() => {
                    petal.remove();
                }, (duration + delay + 0.5) * 1000);
            }, i * 75);
        }
    }

    // Run flower shower on page load
    document.addEventListener("DOMContentLoaded", function() {
        triggerPetalShower(45);

        // Add subtle petal shower on clicking navigation links
        document.querySelectorAll("a").forEach(link => {
            link.addEventListener("click", function(e) {
                const href = this.getAttribute("href");
                if (href && !href.startsWith("#") && !href.startsWith("javascript")) {
                    triggerPetalShower(15);
                }
            });
        });
    });

    // Continuous ambient floating hearts
    setInterval(() => {
        const h = document.createElement('span');
        h.className = 'heart';
        const icons = ['♥', '♡', '💖', '🌸', '💕'];
        h.textContent = icons[Math.floor(Math.random() * icons.length)];
        h.style.left = Math.random() * 98 + 'vw';
        h.style.fontSize = (14 + Math.random() * 18) + 'px';
        h.style.zIndex = '1';
        document.body.appendChild(h);
        setTimeout(() => h.remove(), 7500);
    }, 1100);

    window.triggerPetalShower = triggerPetalShower;
})();