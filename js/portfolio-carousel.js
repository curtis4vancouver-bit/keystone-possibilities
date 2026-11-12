/**
 * Keystone Possibilities v3.0 — Smooth Tactile Portfolio Carousel & Keyboard Track Controller
 * Zero vertical bounce; clean horizontal scroll-snap navigation for .residence-carousel-track & .kp-lux-reel-track.
 */
(function () {
  'use strict';

  function enhanceCarouselTracks() {
    var tracks = document.querySelectorAll('.residence-carousel-track, .kp-lux-reel-track, .horizontal-reel-track');
    tracks.forEach(function (track) {
      if (track.dataset.kpCarouselBound === '1') {
        return;
      }
      track.dataset.kpCarouselBound = '1';
      track.setAttribute('tabindex', '0');

      track.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') {
          e.preventDefault();
          track.scrollBy({ left: 360, behavior: 'smooth' });
        } else if (e.key === 'ArrowLeft') {
          e.preventDefault();
          track.scrollBy({ left: -360, behavior: 'smooth' });
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhanceCarouselTracks);
  } else {
    enhanceCarouselTracks();
  }
})();
