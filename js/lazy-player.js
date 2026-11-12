/**
 * Keystone Possibilities v3.0 — Zero-CLS Click-to-Play YouTube-Nocookie Facade & Chapter Seeker
 * Supports [keystone_video] shortcodes, .keystone-lazy-video facades, and Cinema Chapter Players.
 */
(function () {
  'use strict';

  function buildEmbedIframe(videoId, title, startSec) {
    var cleanId = String(videoId || '').replace(/[^a-zA-Z0-9_-]/g, '');
    if (!cleanId) {
      return null;
    }
    var params = 'autoplay=1&rel=0&modestbranding=1&playsinline=1';
    if (startSec && Number(startSec) > 0) {
      params += '&start=' + Math.floor(Number(startSec));
    }
    var iframe = document.createElement('iframe');
    iframe.src = 'https://www.youtube-nocookie.com/embed/' + cleanId + '?' + params;
    iframe.title = title || 'Keystone Possibilities Engineering Briefing';
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    iframe.allowFullscreen = true;
    iframe.style.position = 'absolute';
    iframe.style.inset = '0';
    iframe.style.width = '100%';
    iframe.style.height = '100%';
    iframe.style.border = '0';
    return iframe;
  }

  function mountVideo(container, startSec) {
    var videoId = container.getAttribute('data-video-id') || container.getAttribute('data-kp-youtube-id');
    var videoType = container.getAttribute('data-video-type') || 'youtube';
    var title = container.getAttribute('data-video-title') || 'Keystone Possibilities Engineering Briefing';

    if (videoType === 'mp4') {
      var src = container.getAttribute('data-video-src') || videoId;
      if (!src) {
        return;
      }
      var video = document.createElement('video');
      video.src = src;
      video.controls = true;
      video.autoplay = true;
      video.playsInline = true;
      video.style.width = '100%';
      video.style.height = '100%';
      container.innerHTML = '';
      container.appendChild(video);
      return;
    }

    var targetStage = container.querySelector('.keystone-lazy-video__ratio, .luxury-video-theater__ratio') || container;
    var iframe = buildEmbedIframe(videoId, title, startSec || 0);
    if (!iframe) {
      return;
    }
    targetStage.innerHTML = '';
    targetStage.appendChild(iframe);
    container.classList.add('is-playing');
  }

  function initLazyPlayers() {
    document.querySelectorAll('.keystone-lazy-video, [data-kp-youtube-id]').forEach(function (facade) {
      if (facade.dataset.kpLazyBound === '1') {
        return;
      }
      facade.dataset.kpLazyBound = '1';

      var playTrigger = facade.querySelector('.keystone-lazy-video__play, .kp-cinema-play-btn, .cinema-center-play') || facade;
      playTrigger.addEventListener('click', function (e) {
        e.preventDefault();
        mountVideo(facade, 0);
      });
    });

    // Clickable clip chapters ([data-kp-seek="42"] targeting #hero-cinema-frame or closest cinema block)
    document.querySelectorAll('[data-kp-seek]').forEach(function (chapterBtn) {
      chapterBtn.addEventListener('click', function () {
        var sec = parseInt(chapterBtn.getAttribute('data-kp-seek'), 10) || 0;
        var targetId = chapterBtn.getAttribute('data-kp-player');
        var player = targetId
          ? document.getElementById(targetId)
          : (chapterBtn.closest('section, .kp-hero-cinema-col, .hero-watch-col') &&
             chapterBtn.closest('section, .kp-hero-cinema-col, .hero-watch-col').querySelector('[data-kp-youtube-id], .keystone-lazy-video'));
        if (!player) {
          return;
        }
        var group = chapterBtn.parentElement ? chapterBtn.parentElement.querySelectorAll('[data-kp-seek]') : [];
        group.forEach(function (b) {
          b.classList.toggle('is-active', b === chapterBtn);
          b.classList.toggle('active', b === chapterBtn);
        });
        mountVideo(player, sec);
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLazyPlayers);
  } else {
    initLazyPlayers();
  }
})();
