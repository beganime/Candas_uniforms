document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('[data-nav-toggle]');
    const nav = document.querySelector('[data-nav]');

    if (toggle && nav) {
        toggle.addEventListener('click', () => {
            nav.classList.toggle('open');
            toggle.classList.toggle('open');
        });
    }

    const mainImage = document.querySelector('.main-product-img');

    document.querySelectorAll('[data-thumb]').forEach((thumb) => {
        thumb.addEventListener('click', () => {
            if (!mainImage) return;

            const nextSrc = thumb.getAttribute('src');
            const currentSrc = mainImage.getAttribute('src');

            mainImage.setAttribute('src', nextSrc);
            thumb.setAttribute('src', currentSrc);
        });
    });

    const slider = document.querySelector('[data-hero-slider]');

    if (slider) {
        const slides = Array.from(slider.querySelectorAll('.hero-slide'));
        const prevButton = slider.querySelector('[data-hero-prev]');
        const nextButton = slider.querySelector('[data-hero-next]');
        const dots = Array.from(slider.querySelectorAll('[data-hero-dot]'));

        let currentIndex = 0;
        let timer = null;

        const showSlide = (index) => {
            if (!slides.length) return;

            currentIndex = (index + slides.length) % slides.length;

            slides.forEach((slide, slideIndex) => {
                slide.classList.toggle('active', slideIndex === currentIndex);
            });

            dots.forEach((dot, dotIndex) => {
                dot.classList.toggle('active', dotIndex === currentIndex);
            });
        };

        const nextSlide = () => {
            showSlide(currentIndex + 1);
        };

        const prevSlide = () => {
            showSlide(currentIndex - 1);
        };

        const startAutoplay = () => {
            if (slides.length <= 1) return;
            stopAutoplay();
            timer = window.setInterval(nextSlide, 5500);
        };

        const stopAutoplay = () => {
            if (timer) {
                window.clearInterval(timer);
                timer = null;
            }
        };

        if (nextButton) {
            nextButton.addEventListener('click', () => {
                nextSlide();
                startAutoplay();
            });
        }

        if (prevButton) {
            prevButton.addEventListener('click', () => {
                prevSlide();
                startAutoplay();
            });
        }

        dots.forEach((dot) => {
            dot.addEventListener('click', () => {
                const index = Number(dot.dataset.heroDot || 0);
                showSlide(index);
                startAutoplay();
            });
        });

        slider.addEventListener('mouseenter', stopAutoplay);
        slider.addEventListener('mouseleave', startAutoplay);

        showSlide(0);
        startAutoplay();
    }
});