document.addEventListener('DOMContentLoaded', () => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!document.querySelector('link[href*="identity-fix.css"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/static/css/identity-fix.css';
        document.head.appendChild(link);
    }

    document.querySelectorAll('.uniform-orb, .uniform-cube, .uniform-ring').forEach((item) => item.remove());

    const poster = document.querySelector('.catalog-poster');
    const catalogHeroImage = document.querySelector('.catalog-hero-visual > img');

    if (poster && catalogHeroImage) {
        poster.classList.add('has-admin-image');
        poster.style.backgroundImage = `linear-gradient(90deg, rgba(7,24,70,.82), rgba(7,24,70,.32)), url('${catalogHeroImage.currentSrc || catalogHeroImage.src}')`;
    }

    const posterText = poster ? poster.querySelector('p') : null;
    if (posterText && /1920|WebP|JPG|размер/i.test(posterText.textContent || '')) {
        posterText.textContent = 'Покажите здесь акцию, событие, новую коллекцию или важное объявление для клиентов.';
    }

    const guide = document.querySelector('.about-size-guide');
    if (guide) {
        const section = guide.closest('section');
        if (section) section.remove();
    }

    const iconTemplates = [
        '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 17V7a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2Z" stroke="currentColor" stroke-width="1.8"/><path d="M8 9h8M8 13h5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
        '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 7h12l-1 13H7L6 7Z" stroke="currentColor" stroke-width="1.8"/><path d="M9 7a3 3 0 0 1 6 0" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
        '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 12h14M12 5v14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="1.8"/></svg>'
    ];

    document.querySelectorAll('.about-feature-card').forEach((card, index) => {
        if (!card.querySelector('svg')) {
            card.insertAdjacentHTML('afterbegin', iconTemplates[index % iconTemplates.length]);
        }
    });

    const revealTargets = [
        '.section',
        '.hero-slide.active .hero-copy',
        '.hero-slide.active .hero-media',
        '.catalog-hero-copy',
        '.catalog-hero-visual',
        '.catalog-poster',
        '.product-card',
        '.category-card',
        '.promo-card',
        '.mini-promo',
        '.about-feature-card',
        '.about-process-card',
        '.request-info',
        '.request-form',
        '.text-card',
        '.contact-card'
    ];

    const nodes = Array.from(document.querySelectorAll(revealTargets.join(',')));

    nodes.forEach((node, index) => {
        node.classList.add('scroll-reveal');
        node.style.setProperty('--reveal-delay', `${Math.min(index % 8, 7) * 45}ms`);
    });

    if (reduceMotion || !('IntersectionObserver' in window)) {
        nodes.forEach((node) => node.classList.add('is-visible'));
    } else {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });

        nodes.forEach((node) => observer.observe(node));
    }

    if (!reduceMotion) {
        document.querySelectorAll('.product-card, .category-card, .promo-card, .mini-promo, .catalog-poster, .about-feature-card').forEach((card) => {
            card.classList.add('tilt-card');

            card.addEventListener('mousemove', (event) => {
                const rect = card.getBoundingClientRect();
                const x = (event.clientX - rect.left) / rect.width - 0.5;
                const y = (event.clientY - rect.top) / rect.height - 0.5;
                card.style.transform = `perspective(900px) rotateX(${(-y * 3).toFixed(2)}deg) rotateY(${(x * 3).toFixed(2)}deg) translateY(-4px)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }
});
