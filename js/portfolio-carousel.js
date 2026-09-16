/**
 * Keystone Possibilities - 2026 Master Portfolio 9-Residence Carousel Controller
 * Enforces hardware-accelerated CSS scroll-snap, real-time counter badges, touch swipe,
 * and smooth Prev/Next button controls across all 9 luxury residences.
 * 
 * @package KeystonePossibilitiesChild
 * @version 2.6.0
 */

document.addEventListener('DOMContentLoaded', () => {
    initPortfolioCarousels();
});

function initPortfolioCarousels() {
    const sections = document.querySelectorAll('.residence-section');
    if (!sections.length) return;

    sections.forEach((section, index) => {
        const track = section.querySelector('.residence-carousel-track');
        if (!track) return;

        const cards = track.querySelectorAll('.residence-card');
        const total = cards.length;
        if (total <= 1) return; // Single image doesn't need carousel controls

        // Find or create header controls
        let headerBar = section.querySelector('.residence-carousel-header-bar');
        if (!headerBar) {
            const titleHeading = section.querySelector('.residence-title-heading');
            if (titleHeading) {
                headerBar = document.createElement('div');
                headerBar.className = 'residence-carousel-header-bar';
                
                // Move title heading inside header bar
                titleHeading.parentNode.insertBefore(headerBar, titleHeading);
                headerBar.appendChild(titleHeading);
            }
        }

        if (headerBar && !headerBar.querySelector('.residence-carousel-controls')) {
            const controls = document.createElement('div');
            controls.className = 'residence-carousel-controls';
            
            const badge = document.createElement('span');
            badge.className = 'residence-counter-badge';
            badge.textContent = `01 / ${String(total).padStart(2, '0')}`;

            const prevBtn = document.createElement('button');
            prevBtn.className = 'residence-nav-btn prev';
            prevBtn.setAttribute('aria-label', 'Previous photo');
            prevBtn.innerHTML = '&#8249;';

            const nextBtn = document.createElement('button');
            nextBtn.className = 'residence-nav-btn next';
            nextBtn.setAttribute('aria-label', 'Next photo');
            nextBtn.innerHTML = '&#8250;';

            controls.appendChild(badge);
            controls.appendChild(prevBtn);
            controls.appendChild(nextBtn);
            headerBar.appendChild(controls);

            // Button click handlers
            prevBtn.addEventListener('click', (e) => {
                e.preventDefault();
                const cardWidth = cards[0].getBoundingClientRect().width + 20;
                track.scrollBy({ left: -cardWidth, behavior: 'smooth' });
            });

            nextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                const cardWidth = cards[0].getBoundingClientRect().width + 20;
                track.scrollBy({ left: cardWidth, behavior: 'smooth' });
            });

            // Update counter badge on scroll via IntersectionObserver
            if ('IntersectionObserver' in window) {
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const cardIndex = Array.from(cards).indexOf(entry.target);
                            if (cardIndex !== -1) {
                                badge.textContent = `${String(cardIndex + 1).padStart(2, '0')} / ${String(total).padStart(2, '0')}`;
                            }
                        }
                    });
                }, {
                    root: track,
                    threshold: 0.6
                });

                cards.forEach(card => observer.observe(card));
            } else {
                // Fallback scroll listener
                track.addEventListener('scroll', () => {
                    const scrollLeft = track.scrollLeft;
                    const cardWidth = cards[0].getBoundingClientRect().width + 20;
                    const activeIndex = Math.min(Math.round(scrollLeft / cardWidth), total - 1);
                    badge.textContent = `${String(activeIndex + 1).padStart(2, '0')} / ${String(total).padStart(2, '0')}`;
                }, { passive: true });
            }
        }
    });

    console.log(`[Keystone Carousel] Initialized 2026 scroll-snap controls across ${sections.length} residences.`);
}
