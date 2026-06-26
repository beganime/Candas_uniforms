document.addEventListener('DOMContentLoaded', () => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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
        '.about-size-guide',
        '.request-info',
        '.request-form',
        '.text-card',
        '.contact-card'
    ];

    const nodes = Array.from(document.querySelectorAll(revealTargets.join(',')));

    nodes.forEach((node, index) => {
        if (!node.classList.contains('scroll-reveal')) {
            node.classList.add('scroll-reveal');
        }
        node.style.setProperty('--reveal-delay', `${Math.min(index % 8, 7) * 55}ms`);
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
        }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });

        nodes.forEach((node) => observer.observe(node));
    }

    const visualHosts = document.querySelectorAll('.hero-media, .catalog-hero-visual, .catalog-poster');
    visualHosts.forEach((host, index) => {
        if (host.querySelector('.uniform-orb')) return;

        const orb = document.createElement('span');
        orb.className = 'uniform-orb';
        orb.style.right = index % 2 ? '8%' : '12%';
        orb.style.top = index % 2 ? '18%' : '10%';

        const cube = document.createElement('span');
        cube.className = 'uniform-cube';
        cube.style.left = index % 2 ? '12%' : '8%';
        cube.style.bottom = index % 2 ? '16%' : '20%';

        const ring = document.createElement('span');
        ring.className = 'uniform-ring';
        ring.style.right = index % 2 ? 'auto' : '-42px';
        ring.style.left = index % 2 ? '-48px' : 'auto';
        ring.style.bottom = '-46px';

        host.append(orb, cube, ring);
    });

    if (!reduceMotion) {
        document.querySelectorAll('.product-card, .category-card, .promo-card, .mini-promo, .catalog-poster, .about-feature-card').forEach((card) => {
            card.classList.add('tilt-card');

            card.addEventListener('mousemove', (event) => {
                const rect = card.getBoundingClientRect();
                const x = (event.clientX - rect.left) / rect.width - 0.5;
                const y = (event.clientY - rect.top) / rect.height - 0.5;
                card.style.transform = `perspective(900px) rotateX(${(-y * 5).toFixed(2)}deg) rotateY(${(x * 5).toFixed(2)}deg) translateY(-6px)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }
});
