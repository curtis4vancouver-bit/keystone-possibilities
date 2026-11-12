/**
 * Keystone Possibilities v3.0 — Unified Lead Intake & 48-Hr Feasibility Submission Engine
 * Submits cleanly to POST /wp-json/keystone/v1/lead with accessible inline status updates.
 */
(function () {
  'use strict';

  function getLeadEndpoint() {
    if (window.keystoneData && window.keystoneData.restUrl) {
      return window.keystoneData.restUrl;
    }
    return '/wp-json/keystone/v1/lead';
  }

  function ensureStatusNode(form) {
    var existing = form.querySelector('[data-kp-form-status], .kp-form-status');
    if (existing) {
      return existing;
    }
    var status = document.createElement('div');
    status.className = 'kp-form-status';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    form.appendChild(status);
    return status;
  }

  function serializeLeadForm(form) {
    var fd = new FormData(form);
    var getAny = function (keys) {
      for (var i = 0; i < keys.length; i += 1) {
        var val = fd.get(keys[i]);
        if (val && String(val).trim() !== '') {
          return String(val).trim();
        }
      }
      return '';
    };

    var name = getAny(['name', 'full_name', 'client_name', 'partner_name']);
    var email = getAny(['email', 'client_email', 'work_email']);
    var phone = getAny(['phone', 'tel', 'client_phone']);
    var address = getAny(['address', 'project_address', 'lot_address', 'pid']);
    var scope = getAny(['scope', 'project_scope', 'corridor', 'inquiry_type']);
    var brokerage = getAny(['brokerage', 'firm', 'managing_brokerage']);
    var notes = getAny(['notes', 'message', 'project_details']);

    var combinedAddress = address;
    if (scope && combinedAddress) {
      combinedAddress = combinedAddress + ' [' + scope + ']';
    } else if (scope) {
      combinedAddress = scope;
    }
    if (brokerage) {
      combinedAddress = (combinedAddress ? combinedAddress + ' · ' : '') + 'Firm/Brokerage: ' + brokerage;
    }
    if (notes) {
      combinedAddress = (combinedAddress ? combinedAddress + ' — ' : '') + notes;
    }

    return {
      name: name || 'Property Owner / Lot Inquiry',
      email: email,
      phone: phone,
      address: combinedAddress || 'BC Custom Home / Multiplex Feasibility Inquiry',
      source_url: window.location.href,
      form_id: form.id || form.getAttribute('data-kp-lead-form') || 'kp-v3-intake'
    };
  }

  function bindLeadForms() {
    var selector = 'form[data-kp-lead-form], form.kp-lead-form, #keystone-feasibility-form, #kp-quick-lot-form, #kp-feasibility-intake-form, #kp-partner-desk-form, #kp-contact-form';
    document.querySelectorAll(selector).forEach(function (form) {
      if (form.dataset.kpLeadBound === '1') {
        return;
      }
      form.dataset.kpLeadBound = '1';

      form.addEventListener('submit', function (e) {
        e.preventDefault();

        var statusEl = ensureStatusNode(form);
        var submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
        var originalLabel = submitBtn ? submitBtn.innerHTML : '';
        var payload = serializeLeadForm(form);

        if (!payload.email || payload.email.indexOf('@') === -1) {
          statusEl.className = 'kp-form-status is-visible is-error';
          statusEl.textContent = 'Please enter a valid email address so Wayne Stevenson can deliver your Lot & Cost Feasibility Plan.';
          return;
        }

        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.innerHTML = 'Transmitting to Squamish HQ...';
        }
        statusEl.className = 'kp-form-status';
        statusEl.textContent = '';

        fetch(getLeadEndpoint(), {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
          .then(function (res) {
            return res.json().then(function (body) {
              return { ok: res.ok, body: body };
            });
          })
          .then(function (result) {
            if (result.ok && result.body && result.body.success) {
              statusEl.className = 'kp-form-status is-visible is-success';
              statusEl.textContent = result.body.message || 'Thank you — your lot feasibility brief has been logged directly with Wayne Stevenson (BC Housing #52603). Expect a response within 1 business day.';
              form.reset();
            } else {
              var msg = (result.body && result.body.message)
                ? result.body.message
                : 'Unable to submit right now. Please call Wayne Stevenson directly at (604) 848-9688.';
              statusEl.className = 'kp-form-status is-visible is-error';
              statusEl.textContent = msg;
            }
          })
          .catch(function () {
            statusEl.className = 'kp-form-status is-visible is-error';
            statusEl.textContent = 'Network interruption — please call Squamish HQ directly at (604) 848-9688 or email info@keystonepossibilities.ca.';
          })
          .finally(function () {
            if (submitBtn) {
              submitBtn.disabled = false;
              submitBtn.innerHTML = originalLabel;
            }
          });
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindLeadForms);
  } else {
    bindLeadForms();
  }
})();
