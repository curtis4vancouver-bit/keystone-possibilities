// content.js - Injected into Google Flow to bridge the extension sidepanel and the page context.

console.log("[Flow Commander Content] Script injected.");

// Inject inject.js into the main page context to access the React store
const script = document.createElement('script');
script.src = chrome.runtime.getURL('inject.js');
script.onload = function() {
  this.remove(); // Clean up after injection
};
(document.head || document.documentElement).appendChild(script);

// Registry for pending requests sent to page context
const pendingRequests = new Map();
let messageIdSeq = 0;

// Relay a message to the page context (inject.js) and wait for response
function sendToPage(action, payload = {}) {
  return new Promise((resolve) => {
    const messageId = ++messageIdSeq;
    pendingRequests.set(messageId, resolve);
    
    window.postMessage({
      source: 'flow-commander-content',
      action: action,
      payload: payload,
      messageId: messageId
    }, '*');

    // Timeout fallback (5 seconds)
    setTimeout(() => {
      if (pendingRequests.has(messageId)) {
        pendingRequests.delete(messageId);
        resolve({ success: false, error: `Timeout waiting for page response to '${action}'` });
      }
    }, 5000);
  });
}

// Listen for responses from the page context
window.addEventListener('message', (event) => {
  if (event.data && event.data.source === 'flow-commander-page') {
    const { action, payload, messageId } = event.data;
    if (action === "WRITE_STORAGE") {
      chrome.storage.local.set(payload, () => {
        console.log("[Flow Commander Content] Saved storage from page:", payload);
      });
      return;
    }
    if (action === "READ_STORAGE") {
      chrome.storage.local.get(null, (data) => {
        window.postMessage({
          source: 'flow-commander-page',
          action: 'READ_STORAGE_RESPONSE',
          payload: data,
          messageId: messageId
        }, '*');
      });
      return;
    }
    if (action === "START_QUEUE") {
      chrome.runtime.sendMessage({ action: "START_QUEUE" });
      return;
    }
    if (action === "OPEN_SIDEPANEL") {
      chrome.runtime.sendMessage({ action: "OPEN_SIDEPANEL" });
      return;
    }
    if (action === "RELOAD_EXTENSION") {
      chrome.runtime.sendMessage({ action: "RELOAD_EXTENSION" });
      return;
    }
    if (pendingRequests.has(messageId)) {
      const resolve = pendingRequests.get(messageId);
      pendingRequests.delete(messageId);
      resolve(payload);
    }
  }
});

// Helper for waiting
const sleep = (ms) => new Promise(res => setTimeout(res, ms));

// Helper to scan gallery cards in the UI
function scanGalleryCards() {
  const cards = document.querySelectorAll('[aria-roledescription="draggable"]');
  const results = [];
  
  cards.forEach((card, index) => {
    const text = (card.innerText || '').trim();
    const links = card.querySelectorAll('a[href]');
    const href = links.length > 0 ? links[0].href : '';
    const imgEl = card.querySelector('img');
    const thumbnailUrl = imgEl ? imgEl.src : '';

    let type = 'unknown';
    let mediaId = '';
    let status = 'unknown';
    let percent = 0;

    // Identify card type and media/character ID
    if (href.includes('/character/')) {
      type = 'character';
      mediaId = href.split('/character/')[1];
      status = 'done';
    } else if (href.includes('/edit/')) {
      mediaId = href.split('/edit/')[1];
      
      // Determine generation status
      if (text.includes('play_circle')) {
        type = 'video';
        status = 'done';
      } else if (text.includes('Failed') || text.includes('failed') || text.includes('violated') || text.includes('violate')) {
        type = 'video';
        status = 'failed';
      } else if (/\d+%/.test(text)) {
        type = 'video';
        status = 'rendering';
        const match = text.match(/(\d+)%/);
        if (match) percent = parseInt(match[1]);
      } else {
        // No video play button or rendering percentage means it is an image card
        type = 'image';
        status = 'done';
      }
    }

    results.push({
      index,
      type,
      mediaId,
      status,
      percent,
      thumbnailUrl,
      name: text.includes('accessibility_new') 
        ? text.replace(/accessibility_new/g, '').trim().split('\n')[0].trim()
        : (text.split('\n')[0] || text.substring(0, 30))
    });
  });

  return results;
}

// Ensure the All Media (Gallery) tab is selected in the sidebar
async function ensureAllMediaTabActive() {
  const buttons = document.querySelectorAll('button');
  for (const btn of buttons) {
    if (btn.textContent.includes('All Media')) {
      btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
      btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
      btn.click();
      await sleep(500); // Wait for the transition to complete
      return true;
    }
  }
  return false;
}

// Find and click the Submit (Create) button
function clickSubmitButton() {
  return new Promise((resolve) => {
    setTimeout(() => {
      // Find button by icon name or button title
      const buttons = document.querySelectorAll('button');
      let submitBtn = null;
      
      for (const btn of buttons) {
        if (btn.textContent.includes('arrow_forward') && !btn.disabled) {
          submitBtn = btn;
          break;
        }
      }

      if (submitBtn) {
        submitBtn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
        submitBtn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
        submitBtn.click();
        resolve(true);
      } else {
        console.warn("[Flow Commander Content] Submit button not found or disabled.");
        resolve(false);
      }
    }, 300);
  });
}

// Trigger click-by-click download menu on the card
// Helper to dispatch a full trusted-like mouse click sequence
function dispatchClickSequence(el) {
  if (!el) return;
  const rect = el.getBoundingClientRect();
  const clientX = rect.left + rect.width / 2;
  const clientY = rect.top + rect.height / 2;

  const eventOpts = { bubbles: true, cancelable: true, view: window, clientX, clientY };
  
  el.dispatchEvent(new PointerEvent('pointerdown', { ...eventOpts, pointerType: 'mouse' }));
  el.dispatchEvent(new MouseEvent('mousedown', eventOpts));
  
  el.focus();
  
  el.dispatchEvent(new PointerEvent('pointerup', { ...eventOpts, pointerType: 'mouse' }));
  el.dispatchEvent(new MouseEvent('mouseup', eventOpts));
  el.dispatchEvent(new MouseEvent('click', eventOpts));
}

// Trigger click-by-click download menu on the card
async function triggerDownloadMenu(mediaId, resolution) {
  // 1. Locate the card
  const cards = scanGalleryCards();
  const targetCardInfo = cards.find(c => c.mediaId === mediaId);
  if (!targetCardInfo) {
    return { success: false, error: `Card with media ID ${mediaId} not found in gallery.` };
  }

  const domCards = document.querySelectorAll('[aria-roledescription="draggable"]');
  const targetCard = domCards[targetCardInfo.index];
  if (!targetCard) {
    return { success: false, error: "DOM element for card not found." };
  }

  // 2. Right-click the card target to open context menu directly
  const target = targetCard.querySelector("video") || targetCard.querySelector("img") || targetCard.querySelector("a") || targetCard;
  console.log("[Flow Commander Content] Dispatching right-click contextmenu event on target");
  target.dispatchEvent(new MouseEvent('contextmenu', {
    bubbles: true,
    cancelable: true,
    view: window,
    button: 2,
    buttons: 2
  }));
  await sleep(800);

  // 4. Find the context menu items and click "Download"
  const menuItems = document.querySelectorAll('[role="menuitem"], .mat-mdc-menu-item');
  let downloadItem = null;
  for (const item of menuItems) {
    const text = item.textContent || "";
    if (text.includes("Download") || text.includes("download")) {
      downloadItem = item;
      break;
    }
  }

  if (!downloadItem) {
    return { success: false, error: "Could not find 'Download' item in context menu." };
  }
  
  console.log("[Flow Commander Content] Clicking Download item via full event sequence");
  dispatchClickSequence(downloadItem);
  await sleep(800);

  // 5. Select resolution option from submenu
  const subMenuItems = document.querySelectorAll('[role="menuitem"], .mat-mdc-menu-item');
  let resolutionItem = null;

  // Resolution display names on Flow
  const resMap = {
    "1080p": "1080p Upscaled",
    "720p": "720p Original",
    "2K": "2K Upscaled",
    "1K": "1K Original"
  };
  const targetLabel = resMap[resolution] || resolution;

  for (const item of subMenuItems) {
    const text = item.textContent || "";
    if (text.includes(targetLabel)) {
      resolutionItem = item;
      break;
    }
  }

  if (!resolutionItem) {
    // If specific option not found, try a looser match
    for (const item of subMenuItems) {
      if (item.textContent.toLowerCase().includes(resolution.toLowerCase())) {
        resolutionItem = item;
        break;
      }
    }
  }

  if (!resolutionItem) {
    return { success: false, error: `Quality option '${targetLabel}' not found in submenu.` };
  }

  console.log(`[Flow Commander Content] Clicking resolution option '${targetLabel}' via full event sequence`);
  dispatchClickSequence(resolutionItem);
  
  // Close menu if still open by clicking somewhere safe
  await sleep(400);
  document.body.click();
  return { success: true };
}

// Handle runtime messages from the extension sidepanel
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  console.log(`[Flow Commander Content] Received tab message: ${msg.action}`);

  switch (msg.action) {
    case "PING": {
      sendToPage("PING").then(res => {
        sendResponse({ success: true, connected: res.storeFound });
      });
      break;
    }

    case "GET_PROJECT_INFO": {
      Promise.all([
        scanGalleryCards(),
        sendToPage("GET_STORE_STATE")
      ]).then(([cards, storeState]) => {
        const workflowNames = (storeState && storeState.workflowNames) || {};
        
        // Enrich card names using the React workflow display names if available
        cards.forEach(card => {
          if (card.mediaId && workflowNames[card.mediaId]) {
            card.name = workflowNames[card.mediaId];
          }
        });

        // Filter character info from scanned cards
        const characters = cards
          .filter(c => c.type === 'character')
          .map(c => ({ name: c.name.replace('accessibility_new', '').trim(), serverId: c.mediaId }));
        
        // Find Wayne's likeness (Avatar) card if present in store context or cards
        // Typically Wayne uses likenessMediaId
        sendResponse({
          success: true,
          characters: characters,
          cards: cards.filter(c => c.type !== 'character'),
          storeState: storeState
        });
      }).catch(err => {
        sendResponse({ success: false, error: err.message });
      });
      break;
    }

    case "SET_SETTINGS": {
      sendToPage("SET_SETTINGS", msg.payload).then(res => {
        sendResponse(res);
      });
      break;
    }

    case "SUBMIT_PROMPT": {
      (async () => {
        try {
          // Force switch to the All Media tab so we can scan and see the rendering card
          await ensureAllMediaTabActive();
          
          const beforeCards = scanGalleryCards();

          // 1. Prepare store inputs (which triggers the React submit click natively)
          const prepRes = await sendToPage("PREPARE_PROMPT", msg.payload);
          if (!prepRes.success) {
            sendResponse({ success: false, error: prepRes.error });
            return;
          }

          // 2. Poll for the newly generated card to grab its media ID
          let attempts = 0;
          const maxAttempts = 50;
          const checkInterval = setInterval(() => {
            attempts++;
            const currentCards = scanGalleryCards();
            
            // Find card present now that wasn't there before
            const newCard = currentCards.find(ac => 
              ac.type !== 'character' && 
              !beforeCards.some(bc => bc.mediaId === ac.mediaId)
            );

            if (newCard && newCard.mediaId) {
              clearInterval(checkInterval);
              console.log(`[Flow Commander Content] Detected new card spawned: ${newCard.mediaId}`);
              sendResponse({ success: true, mediaId: newCard.mediaId });
            } else if (attempts >= maxAttempts) {
              clearInterval(checkInterval);
              // Fallback: search for first rendering card
              const renderingCard = currentCards.find(c => c.status === 'rendering');
              if (renderingCard) {
                sendResponse({ success: true, mediaId: renderingCard.mediaId });
              } else {
                sendResponse({ success: false, error: "Timed out waiting for new generation card to spawn." });
              }
            }
          }, 400);
        } catch (err) {
          sendResponse({ success: false, error: err.message });
        }
      })();
      break;
    }

    case "GET_CARD_STATUS": {
      const currentCards = scanGalleryCards();
      const statuses = currentCards
        .filter(c => c.type !== 'character')
        .map(c => ({ mediaId: c.mediaId, status: c.status, percent: c.percent }));
      sendResponse({ success: true, cards: statuses });
      break;
    }

    case "TRIGGER_DOWNLOAD": {
      triggerDownloadMenu(msg.payload.mediaId, msg.payload.resolution).then(res => {
        sendResponse(res);
      }).catch(err => {
        sendResponse({ success: false, error: err.message });
      });
      break;
    }

    case "REMOTE_LOAD_QUEUE": {
      // AI agent pushes queue items + settings into storage → sidepanel picks them up
      const { queue: newQueue, settings: newSettings, autoStart } = msg.payload;
      const storageUpdate = {};
      if (newQueue) storageUpdate.queue = newQueue;
      if (newSettings) storageUpdate.settings = newSettings;
      
      chrome.storage.local.set(storageUpdate, () => {
        console.log(`[Flow Commander Content] Remote loaded ${newQueue ? newQueue.length : 0} queue items`);
        
        if (autoStart) {
          // Give sidepanel 500ms to pick up the storage change, then trigger start
          setTimeout(() => {
            chrome.runtime.sendMessage({ action: "START_QUEUE" }, (res) => {
              console.log("[Flow Commander Content] START_QUEUE sent:", res);
            });
          }, 500);
        }
        
        sendResponse({ success: true, queued: newQueue ? newQueue.length : 0 });
      });
      break;
    }

    default:
      sendResponse({ success: false, error: `Action '${msg.action}' not recognized.` });
  }

  return true; // Keep response channel open for asynchronous calls
});
