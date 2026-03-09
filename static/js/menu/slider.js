// slider.js — Hero şəkil slayderi.
// initSlider() çağıranda avtomatik başlayır və düymələri dinləyir.

export function initSlider() {
    const slides    = document.querySelectorAll('.hero-slide');
    const dots      = document.querySelectorAll('.hero-dot');
    const prevBtn   = document.getElementById('hero-prev');
    const nextBtn   = document.getElementById('hero-next');

    if (!slides.length) return; // HTML-də slider yoxdursa çıx

    let current  = 0;
    let autoPlay = setInterval(() => goTo(current + 1), 5000);

    function goTo(n) {
        slides[current].classList.remove('active');
        dots[current].classList.remove('active');

        current = (n + slides.length) % slides.length;

        slides[current].classList.add('active');
        dots[current].classList.add('active');
    }

    function resetTimer() {
        clearInterval(autoPlay);
        autoPlay = setInterval(() => goTo(current + 1), 5000);
    }

    prevBtn?.addEventListener('click', () => { goTo(current - 1); resetTimer(); });
    nextBtn?.addEventListener('click', () => { goTo(current + 1); resetTimer(); });

    dots.forEach(dot =>
        dot.addEventListener('click', () => { goTo(+dot.dataset.i); resetTimer(); })
    );
}
