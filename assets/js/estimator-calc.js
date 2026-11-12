/**
 * Keystone Possibilities v3.0 — 9-Corridor Lot & Cost Engine, BC Geocoder Autocomplete,
 * Open-Book CCDC 5B Savings Slider & BCFSA Rule 5-11 Brokerage Referral Calculator
 */
(function () {
  'use strict';

  var CORRIDOR_PRESETS = {
    'west-vancouver': {
      name: 'West Vancouver',
      minSf: 650,
      maxSf: 980,
      civilRange: [85000, 185000],
      ssmuhUnits: '3–4 Units (or Luxury Estate + Coach House)',
      bylaw: 'DWV Bylaw 4662 · Watercourse Bylaw 4364 (15m setback) · Steep-Slope Granite Micropiles'
    },
    'whistler': {
      name: 'Whistler',
      minSf: 680,
      maxSf: 1050,
      civilRange: [90000, 195000],
      ssmuhUnits: 'Alpine Estate + Employee / Auxiliary Suite',
      bylaw: 'RMOW Bylaw 303 · BCBC Part 4 Snow Load Sg = 6.2–8.1 kPa · Wildfire DPA Class A'
    },
    'squamish': {
      name: 'Squamish (HQ)',
      minSf: 450,
      maxSf: 680,
      civilRange: [48000, 125000],
      ssmuhUnits: '3–4 Units SSMUH (R-1 / R-2 Serviced Lots)',
      bylaw: 'District of Squamish Bylaw 2200 · Flood Construction Level (FCL) · Step Code 4/5'
    },
    'north-vancouver': {
      name: 'North Vancouver',
      minSf: 475,
      maxSf: 720,
      civilRange: [58000, 145000],
      ssmuhUnits: '4–6 Units SSMUH (DNV / CNV Transit Tier)',
      bylaw: 'DNV & CNV SSMUH Bylaws · High-Rainfall Dual-Membrane Drainage · Part 4 Shear Frames'
    },
    'vancouver-r1-1': {
      name: 'Vancouver R1-1',
      minSf: 430,
      maxSf: 620,
      civilRange: [65000, 165000],
      ssmuhUnits: '3–6 Strata Units or up to 8 Rental Units (1.0 FSR)',
      bylaw: 'Vancouver R1-1 District Schedule · VBBL 2025 · NFPA 13D Sprinklers & BC Hydro PMT Check'
    },
    'coquitlam': {
      name: 'Coquitlam / Tri-Cities',
      minSf: 420,
      maxSf: 610,
      civilRange: [52000, 130000],
      ssmuhUnits: '4–6 Units SSMUH (Zero Parking Min within 400m FTN)',
      bylaw: 'Coquitlam SSMUH RS Amendments · Burke Mountain Slope DPA · On-Site Storm Detention'
    },
    'sunshine-coast': {
      name: 'Sunshine Coast',
      minSf: 440,
      maxSf: 660,
      civilRange: [50000, 135000],
      ssmuhUnits: '3–4 Units (Sechelt / Gibsons Serviced Urban Lots)',
      bylaw: 'Sechelt Bylaw 580 · Wind Pressure q100 = 0.55 kPa · ES54 Underground DB2 Conduit'
    },
    'pemberton': {
      name: 'Pemberton',
      minSf: 480,
      maxSf: 740,
      civilRange: [75000, 190000],
      ssmuhUnits: 'Village SSMUH or ALR Primary + Secondary Ranch Compound',
      bylaw: 'Pemberton Bylaw 832 / SLRD Area C ALR · Long-Run ES54 Ducting & Solar/BESS Microgrids'
    },
    'vancouver-island': {
      name: 'Vancouver Island',
      minSf: 460,
      maxSf: 760,
      civilRange: [55000, 150000],
      ssmuhUnits: '4–6 Units Missing Middle (Victoria / Saanich / Nanaimo)',
      bylaw: 'Peak Cascadia Seismic Zone (Sa > 1.1g) · Coastal Bluff Anchors & Marine Rainscreens'
    }
  };

  function fmtCAD(num) {
    return '$' + Math.round(num).toLocaleString('en-CA');
  }

  function initSampleAddressChips() {
    document.querySelectorAll('[data-kp-sample-address], .sample-chip, .kp-sample-chip').forEach(function (chip) {
      chip.addEventListener('click', function () {
        var addr = chip.getAttribute('data-kp-sample-address') || chip.textContent.trim();
        var container = chip.closest('form, section, .kp-quick-intake-card, .hero-intake-card') || document;
        var input = container.querySelector('input[name="address"], input[name="project_address"], [data-kp-address-input]');
        if (input) {
          input.value = addr;
          input.focus();
          input.dispatchEvent(new Event('input', { bubbles: true }));
        }
      });
    });
  }

  function initAddressGeocoder() {
    var geocodeUrl = (window.keystoneData && window.keystoneData.geocodeRestUrl)
      ? window.keystoneData.geocodeRestUrl
      : '/wp-json/keystone/v1/geocode';

    document.querySelectorAll('[data-kp-address-input]').forEach(function (input) {
      var listId = input.getAttribute('list');
      var datalist = listId ? document.getElementById(listId) : null;
      if (!datalist) {
        datalist = document.createElement('datalist');
        datalist.id = 'kp-bc-geocode-' + Math.random().toString(36).slice(2, 8);
        input.setAttribute('list', datalist.id);
        input.parentNode.appendChild(datalist);
      }

      var timer = null;
      input.addEventListener('input', function () {
        var q = (input.value || '').trim();
        if (q.length < 4) {
          return;
        }
        clearTimeout(timer);
        timer = setTimeout(function () {
          fetch(geocodeUrl + '?q=' + encodeURIComponent(q))
            .then(function (r) { return r.ok ? r.json() : null; })
            .then(function (data) {
              if (!data || !Array.isArray(data.results)) {
                return;
              }
              datalist.innerHTML = '';
              data.results.slice(0, 5).forEach(function (item) {
                var opt = document.createElement('option');
                opt.value = item.fullAddress || item.address || '';
                datalist.appendChild(opt);
              });
            })
            .catch(function () { /* graceful silent fallback */ });
        }, 280);
      });
    });
  }

  function initFeasibilityEstimator() {
    document.querySelectorAll('[data-kp-estimator]').forEach(function (root) {
      var state = {
        corridor: root.getAttribute('data-default-corridor') || 'west-vancouver',
        buildType: 'custom-estate', // 'custom-estate' | 'bill44-multiplex' | 'steep-slope-alpine'
        sqft: 4200,
        transit: false,
        includeCivil: true
      };

      var sqftSlider = root.querySelector('[data-kp-est-sqft]');
      var sqftReadout = root.querySelector('[data-kp-est-sqft-val]');
      var transitToggle = root.querySelector('[data-kp-est-transit]');
      var civilToggle = root.querySelector('[data-kp-est-civil]');

      var outCorridor = root.querySelector('[data-kp-out-corridor]');
      var outHeadline = root.querySelector('[data-kp-out-headline]');
      var outBylaw = root.querySelector('[data-kp-out-bylaw]');
      var outRate = root.querySelector('[data-kp-out-rate]');
      var outCivil = root.querySelector('[data-kp-out-civil]');
      var outUnits = root.querySelector('[data-kp-out-units]');
      var outSavings = root.querySelector('[data-kp-out-savings]');

      function recalculate() {
        var preset = CORRIDOR_PRESETS[state.corridor] || CORRIDOR_PRESETS['west-vancouver'];
        var minRate = preset.minSf;
        var maxRate = preset.maxSf;

        if (state.buildType === 'bill44-multiplex') {
          minRate = Math.round(minRate * 0.92);
          maxRate = Math.round(maxRate * 0.94);
        } else if (state.buildType === 'steep-slope-alpine') {
          minRate = Math.round(minRate * 1.12);
          maxRate = Math.round(maxRate * 1.16);
        }

        var civilLow = state.includeCivil ? preset.civilRange[0] : 0;
        var civilHigh = state.includeCivil ? preset.civilRange[1] : 0;

        var lowTotal = state.sqft * minRate + civilLow;
        var highTotal = state.sqft * maxRate + civilHigh;
        var midTotal = (lowTotal + highTotal) / 2;
        var ccdcSavings = midTotal * 0.09; // ~9% net fee delta vs 18%+ opaque fixed-markup GCs

        if (sqftReadout) {
          sqftReadout.textContent = state.sqft.toLocaleString('en-CA') + ' sq. ft.';
        }
        if (outCorridor) {
          outCorridor.textContent = preset.name.toUpperCase();
        }
        if (outHeadline) {
          outHeadline.textContent = fmtCAD(lowTotal) + ' – ' + fmtCAD(highTotal);
        }
        if (outBylaw) {
          outBylaw.textContent = preset.bylaw;
        }
        if (outRate) {
          outRate.textContent = '$' + minRate + ' – $' + maxRate + ' / sq. ft.';
        }
        if (outCivil) {
          outCivil.textContent = state.includeCivil
            ? (fmtCAD(civilLow) + ' – ' + fmtCAD(civilHigh))
            : 'Excluded (Site Pre-Serviced)';
        }
        if (outUnits) {
          outUnits.textContent = state.transit
            ? 'Up to 6 Units (FTN 400m Transit Tier)'
            : preset.ssmuhUnits;
        }
        if (outSavings) {
          outSavings.textContent = fmtCAD(ccdcSavings);
        }
      }

      root.querySelectorAll('[data-kp-est-corridor]').forEach(function (el) {
        if (el.tagName === 'SELECT') {
          el.addEventListener('change', function () {
            state.corridor = el.value;
            recalculate();
          });
        } else {
          el.addEventListener('click', function () {
            state.corridor = el.getAttribute('data-kp-est-corridor') || 'west-vancouver';
            root.querySelectorAll('[data-kp-est-corridor]').forEach(function (btn) {
              btn.classList.toggle('is-selected', btn === el);
              btn.classList.toggle('is-active', btn === el);
            });
            recalculate();
          });
        }
      });

      root.querySelectorAll('[data-kp-est-type]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          state.buildType = btn.getAttribute('data-kp-est-type') || 'custom-estate';
          root.querySelectorAll('[data-kp-est-type]').forEach(function (b) {
            b.classList.toggle('is-selected', b === btn);
            b.classList.toggle('is-active', b === btn);
          });
          recalculate();
        });
      });

      if (sqftSlider) {
        state.sqft = parseInt(sqftSlider.value, 10) || 4200;
        sqftSlider.addEventListener('input', function () {
          state.sqft = parseInt(sqftSlider.value, 10) || 4200;
          recalculate();
        });
      }

      if (transitToggle) {
        transitToggle.addEventListener('click', function () {
          if (transitToggle.type === 'checkbox') {
            state.transit = transitToggle.checked;
          } else {
            state.transit = transitToggle.getAttribute('aria-checked') !== 'true';
            transitToggle.setAttribute('aria-checked', state.transit ? 'true' : 'false');
          }
          recalculate();
        });
      }

      if (civilToggle) {
        civilToggle.addEventListener('change', function () {
          state.includeCivil = civilToggle.checked;
          recalculate();
        });
      }

      recalculate();
    });
  }

  function initCcdcSavingsSlider() {
    document.querySelectorAll('[data-kp-ccdc-calc]').forEach(function (wrap) {
      var slider = wrap.querySelector('[data-kp-ccdc-slider]');
      var budgetOut = wrap.querySelector('[data-kp-ccdc-budget]');
      var tradOut = wrap.querySelector('[data-kp-ccdc-traditional]');
      var openOut = wrap.querySelector('[data-kp-ccdc-openbook]');
      var deltaOut = wrap.querySelector('[data-kp-ccdc-delta]');

      if (!slider) {
        return;
      }

      function update() {
        var hardCost = parseFloat(slider.value) || 3000000;
        var traditionalFee = hardCost * 0.19; // Typical 18%–22% fixed-price GC contingency + sub-trade margin
        var openBookFee = hardCost * 0.10;    // Transparent CCDC 5B management fee
        var retained = traditionalFee - openBookFee;

        if (budgetOut) budgetOut.textContent = fmtCAD(hardCost);
        if (tradOut) tradOut.textContent = fmtCAD(traditionalFee);
        if (openOut) openOut.textContent = fmtCAD(openBookFee);
        if (deltaOut) deltaOut.textContent = fmtCAD(retained);
      }

      slider.addEventListener('input', update);
      update();
    });
  }

  function initBcfsaReferralCalculator() {
    document.querySelectorAll('[data-kp-bcfsa-calc]').forEach(function (wrap) {
      var slider = wrap.querySelector('[data-kp-bcfsa-slider]');
      var contractOut = wrap.querySelector('[data-kp-bcfsa-contract]');
      var feeOut = wrap.querySelector('[data-kp-bcfsa-fee]');

      if (!slider) {
        return;
      }

      function update() {
        var contractVal = parseFloat(slider.value) || 3200000;
        var brokerageFee = contractVal * 0.005; // 0.50% BCFSA Rule 5-11 Managing Brokerage referral fee
        if (contractOut) contractOut.textContent = fmtCAD(contractVal);
        if (feeOut) feeOut.textContent = fmtCAD(brokerageFee);
      }

      slider.addEventListener('input', update);
      update();
    });
  }

  function boot() {
    initSampleAddressChips();
    initAddressGeocoder();
    initFeasibilityEstimator();
    initCcdcSavingsSlider();
    initBcfsaReferralCalculator();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
