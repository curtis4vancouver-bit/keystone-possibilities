/**
 * Keystone Possibilities v3.0 — Navigation, Mobile Drawer, Tactile Reels & Lightbox UI
 */
(function () {
  'use strict';

  function initMobileNav() {
    var toggle = document.getElementById('kpMobileNavToggle');
    var drawer = document.getElementById('kpMobileNavDrawer');
    var backdrop = document.getElementById('kpMobileNavBackdrop');
    var closeBtn = document.getElementById('kpMobileNavClose');

    if (!toggle || !drawer) {
      return;
    }

    function setOpen(open) {
      drawer.classList.toggle('is-open', open);
      drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (backdrop) {
        backdrop.classList.toggle('is-open', open);
      }
      document.body.style.overflow = open ? 'hidden' : '';
    }

    toggle.addEventListener('click', function () {
      var isOpen = drawer.classList.contains('is-open');
      setOpen(!isOpen);
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        setOpen(false);
      });
    }

    if (backdrop) {
      backdrop.addEventListener('click', function () {
        setOpen(false);
      });
    }

    drawer.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        setOpen(false);
      });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) {
        setOpen(false);
        toggle.focus();
      }
    });
  }

  function initDesktopDropdown() {
    var dropdownItems = document.querySelectorAll('.kp-nav-item--has-dropdown');
    dropdownItems.forEach(function (item) {
      var btn = item.querySelector('[data-kp-dropdown-toggle]');
      if (!btn) {
        return;
      }
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var nextState = !item.classList.contains('is-open');
        dropdownItems.forEach(function (other) {
          other.classList.remove('is-open');
          var otherBtn = other.querySelector('[data-kp-dropdown-toggle]');
          if (otherBtn) {
            otherBtn.setAttribute('aria-expanded', 'false');
          }
        });
        item.classList.toggle('is-open', nextState);
        btn.setAttribute('aria-expanded', nextState ? 'true' : 'false');
      });
    });

    document.addEventListener('click', function (e) {
      dropdownItems.forEach(function (item) {
        if (!item.contains(e.target)) {
          item.classList.remove('is-open');
          var btn = item.querySelector('[data-kp-dropdown-toggle]');
          if (btn) {
            btn.setAttribute('aria-expanded', 'false');
          }
        }
      });
    });
  }

  function initReelControlsAndFilters() {
    // Prev / Next arrow glide buttons
    document.querySelectorAll('[data-kp-reel-prev], [data-kp-reel-next]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var targetId = btn.getAttribute('data-kp-reel-prev') || btn.getAttribute('data-kp-reel-next');
        var track = targetId
          ? document.getElementById(targetId)
          : (btn.closest('section') && btn.closest('section').querySelector('.kp-lux-reel-track, .horizontal-reel-track'));
        if (!track) {
          return;
        }
        var dir = btn.hasAttribute('data-kp-reel-prev') ? -1 : 1;
        var step = Math.max(320, Math.round(track.clientWidth * 0.78));
        track.scrollBy({ left: dir * step, behavior: 'smooth' });
      });
    });

    // Category filter pills
    document.querySelectorAll('[data-kp-filter-bar]').forEach(function (bar) {
      var targetId = bar.getAttribute('data-kp-filter-bar');
      var section = bar.closest('section') || document;
      var track = targetId
        ? document.getElementById(targetId)
        : section.querySelector('.kp-lux-reel-track, .horizontal-reel-track');
      if (!track) {
        return;
      }

      var pills = bar.querySelectorAll('[data-kp-filter]');
      var countEl = section.querySelector('[data-kp-reel-count], .kp-reel-count, .reel-count-readout');

      pills.forEach(function (pill) {
        pill.addEventListener('click', function () {
          var filterVal = pill.getAttribute('data-kp-filter') || 'all';
          pills.forEach(function (p) {
            var active = p === pill;
            p.classList.toggle('is-active', active);
            p.setAttribute('aria-pressed', active ? 'true' : 'false');
          });

          var cards = track.querySelectorAll('[data-kp-category]');
          var visibleCount = 0;
          cards.forEach(function (card) {
            var cat = card.getAttribute('data-kp-category') || '';
            var show = filterVal === 'all' || cat === filterVal;
            if (show) {
              card.removeAttribute('hidden');
              visibleCount += 1;
            } else {
              card.setAttribute('hidden', 'hidden');
            }
          });

          if (countEl) {
            var unit = countEl.getAttribute('data-kp-unit') || 'items';
            countEl.textContent = 'Showing ' + visibleCount + ' ' + unit;
          }
          track.scrollTo({ left: 0, behavior: 'smooth' });
        });
      });
    });
  }

  function initLightboxModal() {
    var modal = document.getElementById('kpLightboxModal');
    if (!modal) {
      return;
    }

    var imgEl = modal.querySelector('[data-kp-lightbox-img]');
    var titleEl = modal.querySelector('[data-kp-lightbox-title]');
    var subEl = modal.querySelector('[data-kp-lightbox-sub]');
    var thumbsWrap = modal.querySelector('[data-kp-lightbox-thumbs]');
    var closeBtn = modal.querySelector('[data-kp-lightbox-close]');
    var prevBtn = modal.querySelector('[data-kp-lightbox-prev]');
    var nextBtn = modal.querySelector('[data-kp-lightbox-next]');

    var gallery = [];
    var activeIndex = 0;
    var lastFocused = null;

    function renderSlide(index) {
      if (!gallery.length || !imgEl) {
        return;
      }
      activeIndex = (index + gallery.length) % gallery.length;
      imgEl.src = gallery[activeIndex];
      if (thumbsWrap) {
        thumbsWrap.querySelectorAll('.kp-lightbox-thumb').forEach(function (thumb, idx) {
          thumb.classList.toggle('is-active', idx === activeIndex);
        });
      }
      var hasMultiple = gallery.length > 1;
      if (prevBtn) {
        prevBtn.style.display = hasMultiple ? 'inline-flex' : 'none';
      }
      if (nextBtn) {
        nextBtn.style.display = hasMultiple ? 'inline-flex' : 'none';
      }
    }

    function openLightbox(opts) {
      if (!opts || !imgEl) {
        return;
      }
      lastFocused = document.activeElement;
      gallery = Array.isArray(opts.gallery) && opts.gallery.length ? opts.gallery : [opts.src];
      activeIndex = opts.index || 0;

      if (titleEl) {
        titleEl.textContent = opts.title || 'Keystone Possibilities — Verified Asset';
      }
      if (subEl) {
        subEl.textContent = opts.subtitle || '';
      }
      if (imgEl) {
        imgEl.alt = opts.alt || opts.title || 'Keystone Possibilities Verified Image';
      }

      if (thumbsWrap) {
        thumbsWrap.innerHTML = '';
        if (gallery.length > 1) {
          gallery.forEach(function (url, idx) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'kp-lightbox-thumb' + (idx === activeIndex ? ' is-active' : '');
            btn.setAttribute('aria-label', 'View photo ' + (idx + 1) + ' of ' + gallery.length);
            var tImg = document.createElement('img');
            tImg.src = url;
            tImg.alt = '';
            tImg.loading = 'lazy';
            btn.appendChild(tImg);
            btn.addEventListener('click', function () {
              renderSlide(idx);
            });
            thumbsWrap.appendChild(btn);
          });
          thumbsWrap.style.display = 'flex';
        } else {
          thumbsWrap.style.display = 'none';
        }
      }

      renderSlide(activeIndex);
      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      if (closeBtn) {
        closeBtn.focus();
      }
    }

    function closeLightbox() {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      if (lastFocused && typeof lastFocused.focus === 'function') {
        lastFocused.focus();
      }
    }

    if (closeBtn) {
      closeBtn.addEventListener('click', closeLightbox);
    }
    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        renderSlide(activeIndex - 1);
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        renderSlide(activeIndex + 1);
      });
    }

    modal.addEventListener('click', function (e) {
      if (e.target === modal) {
        closeLightbox();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (!modal.classList.contains('is-open')) {
        return;
      }
      if (e.key === 'Escape') {
        closeLightbox();
      } else if (e.key === 'ArrowLeft' && gallery.length > 1) {
        renderSlide(activeIndex - 1);
      } else if (e.key === 'ArrowRight' && gallery.length > 1) {
        renderSlide(activeIndex + 1);
      }
    });

    // Delegate clicks on [data-kp-lightbox] cards or buttons
    document.addEventListener('click', function (e) {
      var trigger = e.target.closest('[data-kp-lightbox]');
      if (!trigger) {
        return;
      }
      e.preventDefault();
      var src = trigger.getAttribute('data-kp-src') || trigger.getAttribute('href') || '';
      var rawGallery = trigger.getAttribute('data-kp-gallery');
      var parsedGallery = [];
      if (rawGallery) {
        try {
          parsedGallery = JSON.parse(rawGallery);
        } catch (_err) {
          parsedGallery = [];
        }
      }
      openLightbox({
        src: src || (parsedGallery[0] || ''),
        gallery: parsedGallery,
        title: trigger.getAttribute('data-kp-title') || '',
        subtitle: trigger.getAttribute('data-kp-subtitle') || '',
        alt: trigger.getAttribute('data-kp-alt') || ''
      });
    });

    window.openKeystoneLightbox = openLightbox;
    window.openResidenceLightbox = function (src, caption) {
      openLightbox({ src: src, title: caption || 'Signature Portfolio Residence' });
    };
  }

  function boot() {
    initMobileNav();
    initDesktopDropdown();
    initReelControlsAndFilters();
    initLightboxModal();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
