/**
 * Keystone WebMCP Google Flow Content Script (MAIN world)
 * Provides programmatic control hooks exposed directly to the page window.
 */
(function() {
    console.log("WebMCP: Google Flow Content Script loaded in MAIN world.");

    // Store intercepted media URLs
    const interceptedUrls = [];

    // Intercept window.fetch to capture video generation URLs
    const originalFetch = window.fetch;
    window.fetch = async function(...args) {
        const response = await originalFetch(...args);
        try {
            const url = args[0];
            if (typeof url === 'string') {
                if (url.includes('getMediaUrlRedirect') || url.includes('getMedia') || url.includes('video') || url.includes('.mp4')) {
                    console.log("WebMCP: Intercepted media redirect URL:", url);
                    if (!interceptedUrls.includes(url)) {
                        interceptedUrls.push(url);
                        // Forward message to background to register download/intercept
                        sendToBackground({
                            action: 'media_url_intercepted',
                            url: url
                        });
                    }
                }
            }
        } catch (e) {
            console.log("WebMCP: Failed to intercept fetch:", e);
        }
        return response;
    };

    /**
     * Dismiss application-level overlays (changelogs, terms, modals)
     */
    function dismissOverlays() {
        console.log("WebMCP: Running overlay dismissal checks...");
        let closed = false;

        // 1. Search for changelog or notification iframe overlays
        const iframes = Array.from(document.querySelectorAll('iframe[src*="/flow/changelogs/"], iframe[src*="/changelogs/"], iframe[src*="modal"]'));
        if (iframes.length > 0) {
            console.log(`WebMCP: Found ${iframes.length} changelog/modal iframe(s). Dispatching Escape key.`);
            dispatchEscape();
            closed = true;
        }

        // 2. Search for close buttons by aria-label or internal icon text
        const closeButtons = Array.from(document.querySelectorAll('[aria-label*="close" i], button'));
        for (const btn of closeButtons) {
            const text = btn.textContent.toLowerCase();
            const icon = btn.querySelector('.google-symbols, i');
            const hasCloseIcon = icon && icon.textContent.trim().toLowerCase() === 'close';
            
            if (text.includes('close') || hasCloseIcon || btn.getAttribute('aria-label')?.toLowerCase().includes('close')) {
                console.log("WebMCP: Clicking overlay close button:", btn);
                btn.click();
                closed = true;
            }
        }

        // 3. Fallback: Dispatch Escape key down/up on body
        if (!closed) {
            dispatchEscape();
        }
    }

    function dispatchEscape() {
        const escapeEvent = new KeyboardEvent('keydown', {
            key: 'Escape',
            code: 'Escape',
            keyCode: 27,
            which: 27,
            bubbles: true,
            cancelable: true
        });
        document.body.dispatchEvent(escapeEvent);
        document.dispatchEvent(escapeEvent);
    }

    /**
     * Focuses and fills the prompt editor
     */
    function fillPrompt(text) {
        console.log("WebMCP: fillPrompt called with:", text);
        dismissOverlays();

        const editor = document.querySelector('[data-slate-editor]');
        if (!editor) {
            console.log("WebMCP: Prompt editor ([data-slate-editor]) not found.");
            return false;
        }

        editor.focus();

        // Try Zustand/React Fiber state injection first (most robust)
        try {
            const fiberKey = Object.keys(editor).find(k => k.startsWith('__reactFiber$'));
            if (fiberKey) {
                let current = editor[fiberKey];
                let promptStoreFiber = null;
                while (current) {
                    if (current.memoizedProps && current.memoizedProps.promptBoxStore) {
                        promptStoreFiber = current;
                        break;
                    }
                    current = current.return;
                }
                if (promptStoreFiber && promptStoreFiber.memoizedProps.promptBoxStore) {
                    const store = promptStoreFiber.memoizedProps.promptBoxStore;
                    if (store.getState && store.getState().actions && typeof store.getState().actions.setPrompt === 'function') {
                        console.log("WebMCP: Found promptBoxStore. Setting prompt via store actions.");
                        store.getState().actions.setPrompt(text);
                        return true;
                    }
                }
            }
        } catch (fiberErr) {
            console.log("WebMCP: React Fiber injection failed, falling back:", fiberErr);
        }

        // Fallback to standard injection if React Fiber fails
        try {
            // Select all existing content so we overwrite it
            const range = document.createRange();
            range.selectNodeContents(editor);
            const sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);

            document.execCommand('delete', false, null);
            document.execCommand('insertText', false, text);
            
            // Dispatch typical React events to force validation
            editor.dispatchEvent(new Event('input', { bubbles: true }));
            editor.dispatchEvent(new Event('change', { bubbles: true }));
            
            console.log("WebMCP: Successfully filled prompt via execCommand fallback.");
            return true;
        } catch (error) {
            console.log("WebMCP: Failed to fill prompt using execCommand fallback:", error);
            // Fallback: set textContent directly
            editor.textContent = text;
            editor.dispatchEvent(new Event('input', { bubbles: true }));
            return true;
        }
    }

    /**
     * Programmatically uploads reference image via synthetic drag-and-drop
     */
    async function uploadReference(imageDataUrl) {
        console.log("WebMCP: uploadReference called.");
        dismissOverlays();

        try {
            // Convert data URL to Blob, then to File
            const res = await fetch(imageDataUrl);
            const blob = await res.blob();
            const file = new File([blob], 'reference_image.png', { type: blob.type });

            // Search for reference dropzone or default editor zone
            const dropzone = document.querySelector('[data-slate-editor].reference-dropzone') ||
                             document.querySelector('.reference-dropzone') ||
                             document.querySelector('[data-slate-editor]') ||
                             document.querySelector('.dropzone') ||
                             document.body;

            if (!dropzone) {
                console.log("WebMCP: Dropzone target not found.");
                return false;
            }

            // Create synthetic DataTransfer
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);

            // Dispatch drag-and-drop sequence
            const eventOptions = {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer
            };

            dropzone.dispatchEvent(new DragEvent('dragenter', eventOptions));
            dropzone.dispatchEvent(new DragEvent('dragover', eventOptions));
            dropzone.dispatchEvent(new DragEvent('drop', eventOptions));

            // Also try hidden file inputs if present on page
            const fileInput = document.querySelector('input[type="file"]');
            if (fileInput) {
                fileInput.files = dataTransfer.files;
                fileInput.dispatchEvent(new Event('change', { bubbles: true }));
            }

            console.log("WebMCP: Reference image drop events successfully dispatched.");
            return true;
        } catch (error) {
            console.log("WebMCP: Failed to upload reference:", error);
            return false;
        }
    }

    /**
     * Clicks the Google Flow generate/submit button
     */
    function clickGenerate() {
        console.log("WebMCP: clickGenerate called.");
        dismissOverlays();

        // Selector based on Material Symbols icon 'arrow_forward'
        const symbols = Array.from(document.querySelectorAll('.google-symbols, i.google-symbols, i'));
        const arrowForward = symbols.find(el => el.textContent.trim() === 'arrow_forward');
        let submitBtn = arrowForward ? arrowForward.closest('button') || arrowForward : null;

        if (!submitBtn) {
            // Fallback selectors
            submitBtn = document.querySelector('button[type="submit"]') ||
                        document.querySelector('button.generate-button') ||
                        document.querySelector('button.create-button') ||
                        document.querySelector('[aria-label="Generate"]') ||
                        document.querySelector('[aria-label="Submit"]');
        }

        if (submitBtn) {
            console.log("WebMCP: Clicking generate button:", submitBtn);
            submitBtn.click();
            return true;
        }

        // Fallback: Dispatch Ctrl+Enter keypress on prompt editor
        const editor = document.querySelector('[data-slate-editor]');
        if (editor) {
            console.log("WebMCP: Submit button not found. Dispatching Ctrl+Enter fallback.");
            editor.focus();
            const enterEvent = new KeyboardEvent('keydown', {
                key: 'Enter',
                code: 'Enter',
                keyCode: 13,
                which: 13,
                ctrlKey: true,
                bubbles: true,
                cancelable: true
            });
            editor.dispatchEvent(enterEvent);
            return true;
        }

        console.log("WebMCP: Submit button and editor not found.");
        return false;
    }

    /**
     * Checks visual and DOM queue status
     */
    function getQueueStatus() {
        // Find typical gallery container or output cards
        const items = Array.from(document.querySelectorAll('.flow-output-gallery > div, [class*="gallery"] > div, [class*="output-card"]'));
        let activeCount = 0;
        let completedCount = 0;
        let failedCount = 0;
        const details = [];

        items.forEach((item, index) => {
            const text = item.innerText.toLowerCase();
            const hasSpinner = item.querySelector('.spinner, [class*="spinner"], [class*="progress"], [class*="loading"]') !== null;
            const hasVideo = item.querySelector('video') !== null;
            const hasImage = item.querySelector('img') !== null;

            let status = 'unknown';
            if (hasSpinner || text.includes('generating') || text.includes('rendering') || text.includes('processing')) {
                status = 'processing';
                activeCount++;
            } else if (text.includes('failed') || text.includes('error') || text.includes('retry')) {
                status = 'failed';
                failedCount++;
            } else if (hasVideo || hasImage) {
                status = 'completed';
                completedCount++;
            }

            details.push({
                index,
                status,
                hasVideo,
                hasImage,
                textSnippet: item.innerText.slice(0, 80)
            });
        });

        // Also check if any video element is currently active in the page
        const globalVideos = Array.from(document.querySelectorAll('video'));
        const activeGlobalVideos = globalVideos.filter(v => !v.paused).length;

        return {
            activeCount: activeCount || activeGlobalVideos,
            completedCount,
            failedCount,
            totalCount: items.length,
            items: details
        };
    }

    /**
     * Gathers all available media download links
     */
    function getDownloadLinks() {
        const links = [];

        // 1. Scan video elements
        document.querySelectorAll('video').forEach((video, idx) => {
            if (video.src) {
                links.push({
                    type: 'video_src',
                    url: video.src,
                    name: `video_${idx}.mp4`
                });
            }
        });

        // 2. Scan download buttons or anchor tags
        const downloadElements = Array.from(document.querySelectorAll('a[download], a[href*="download"], a[href*="getMedia"]'));
        downloadElements.forEach((el, idx) => {
            if (el.href) {
                links.push({
                    type: 'download_anchor',
                    url: el.href,
                    name: el.getAttribute('download') || `download_${idx}.mp4`
                });
            }
        });

        // 3. Scan for any button with a download label or icon
        const buttons = Array.from(document.querySelectorAll('button, a')).filter(el => {
            return el.textContent.toLowerCase().includes('download') || 
                   el.querySelector('.google-symbols')?.textContent.trim() === 'download';
        });
        buttons.forEach((btn, idx) => {
            const href = btn.getAttribute('href') || btn.getAttribute('src');
            if (href) {
                links.push({
                    type: 'download_button',
                    url: href,
                    name: `button_download_${idx}.mp4`
                });
            }
        });

        // 4. Incorporate intercepted URLs
        interceptedUrls.forEach((url, idx) => {
            if (!links.some(l => l.url === url)) {
                links.push({
                    type: 'intercepted_media',
                    url: url,
                    name: `intercepted_${idx}.mp4`
                });
            }
        });

        return links;
    }

    /**
     * Scrapes remaining credit count from the DOM/Profile menu
     */
    async function getCreditsRemaining() {
        const getFromDOM = () => {
            const text = document.body.innerText;
            // Matches formats like "200 credits", "50 of 50 credits", "Credits: 120", etc.
            const match = text.match(/(\d+)\s*(?:of\s*\d+\s*)?credits?\b/i) || text.match(/credits?:\s*(\d+)/i);
            if (match) {
                return parseInt(match[1], 10);
            }
            const creditEl = document.querySelector('.credit-balance, [class*="credit"], [aria-label*="credit"]');
            if (creditEl) {
                const num = creditEl.textContent.match(/\d+/);
                if (num) return parseInt(num[0], 10);
            }
            return null;
        };

        let credits = getFromDOM();
        if (credits !== null) {
            console.log(`WebMCP: Found ${credits} credits directly in DOM.`);
            // Update service worker cache
            sendToBackground({ action: 'update_credits', credits });
            return credits;
        }

        // Try to trigger profile menu click to reveal credits
        const profileBtn = document.querySelector('button[aria-label*="profile" i], button[class*="profile" i], [class*="avatar" i] button, img[src*="googleusercontent.com"]');
        if (profileBtn) {
            console.log("WebMCP: Attempting to open profile menu to read credit balance...");
            profileBtn.click();
            await new Promise(r => setTimeout(r, 600)); // wait for transitions
            credits = getFromDOM();
            profileBtn.click(); // close menu
            
            if (credits !== null) {
                console.log(`WebMCP: Found ${credits} credits in profile menu.`);
                sendToBackground({ action: 'update_credits', credits });
                return credits;
            }
        }

        console.log("WebMCP: Could not extract credits balance from page DOM.");
        return null;
    }

    /**
     * Configures generation settings (model, duration, aspect ratio, mode)
     */
    async function applySettings(config) {
        console.log("WebMCP: applySettings called with:", config);
        dismissOverlays();
        
        // Open settings panel if not already open
        const settingsBtn = document.querySelector('[aria-label*="settings" i]') || 
                            document.querySelector('[aria-label*="View Settings" i]') ||
                            Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('Settings') || el.textContent.includes('crop_'));
                            
        if (settingsBtn) {
            settingsBtn.click();
            await new Promise(r => setTimeout(r, 600)); // wait for panel transition
        }

        // Determine target mode (Image vs Video)
        const mode = config.mode || 'video'; // 'video' or 'image'
        const tabLabel = mode === 'image' ? 'Image' : 'Video';
        const tabBtn = Array.from(document.querySelectorAll('button, [role="tab"]')).find(el => el.textContent.trim().includes(tabLabel));
        if (tabBtn) {
            tabBtn.click();
            await new Promise(r => setTimeout(r, 400));
        }

        // Set Aspect Ratio
        if (config.aspectRatio) {
            const aspectLabel = config.aspectRatio === '9:16' ? '9:16' : '16:9';
            const aspectBtn = Array.from(document.querySelectorAll('button, span, div')).find(el => el.textContent.trim() === aspectLabel);
            if (aspectBtn) aspectBtn.click();
        }

        // Set Duration if video
        if (mode === 'video' && config.duration) {
            const durationBtn = Array.from(document.querySelectorAll('button, span, div')).find(el => el.textContent.trim() === config.duration);
            if (durationBtn) durationBtn.click();
        }

        // Close Settings
        const closeBtn = document.querySelector('[aria-label*="Close" i]') || document.querySelector('button:has(.google-symbols:has-text("close"))');
        if (closeBtn) {
            closeBtn.click();
        } else {
            dispatchEscape();
        }
        await new Promise(r => setTimeout(r, 300));
        return true;
    }

    /**
     * Attaches saved avatar or character to the prompt
     */
    async function attachAvatarOrCharacter(type, name) {
        console.log(`WebMCP: attachAvatarOrCharacter called: type=${type}, name=${name}`);
        dismissOverlays();
        
        // Open Create dialog
        const createBtn = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('add_2 Create') || el.textContent.includes('Create'));
        if (!createBtn) {
            console.log("WebMCP: Create button not found.");
            return false;
        }
        createBtn.click();
        await new Promise(r => setTimeout(r, 700)); // wait for modal dialog

        // Switch to target tab
        const tabLabel = type === 'avatar' ? 'Avatar' : 'Characters';
        const tabBtn = Array.from(document.querySelectorAll('button, [role="tab"]')).find(el => el.textContent.trim().includes(tabLabel));
        if (!tabBtn) {
            console.log(`WebMCP: Tab '${tabLabel}' not found in dialog.`);
            return false;
        }
        tabBtn.click();
        await new Promise(r => setTimeout(r, 600));

        // Find card with matching name
        let targetCard = null;
        if (type === 'avatar' && name === 'me') {
            targetCard = Array.from(document.querySelectorAll('div, button, span')).find(el => el.textContent.trim() === 'me' || el.textContent.includes('Wayne Stevenson'));
        } else {
            const searchInput = document.querySelector('input[placeholder*="Search" i]') || document.querySelector('input[type="text"]');
            if (searchInput) {
                searchInput.focus();
                document.execCommand('insertText', false, name);
                searchInput.dispatchEvent(new Event('input', { bubbles: true }));
                await new Promise(r => setTimeout(r, 600));
            }
            targetCard = Array.from(document.querySelectorAll('div, button, span')).find(el => el.textContent.trim().toLowerCase().includes(name.toLowerCase()));
        }

        if (!targetCard) {
            console.log(`WebMCP: Target character '${name}' card not found.`);
            return false;
        }

        const cardContainer = targetCard.closest('[class*="card" i]') || targetCard.parentElement;
        const addBtn = cardContainer ? Array.from(cardContainer.querySelectorAll('button')).find(btn => btn.textContent.includes('Add') || btn.textContent.includes('add')) : null;
        
        if (addBtn) {
            addBtn.click();
            console.log(`WebMCP: Attached character '${name}' successfully.`);
            await new Promise(r => setTimeout(r, 400));
            return true;
        }
        return false;
    }

    /**
     * Attaches a generated or uploaded card in the gallery as a reference photo by its name
     */
    async function attachCardReferenceByName(cardName) {
        console.log("WebMCP: attachCardReferenceByName called with name:", cardName);
        dismissOverlays();
        
        const cards = Array.from(document.querySelectorAll("[aria-roledescription='draggable']"));
        let targetCard = null;
        
        for (const card of cards) {
            const text = card.innerText.toLowerCase();
            if (text.includes(cardName.toLowerCase())) {
                targetCard = card;
                break;
            }
        }
        
        if (!targetCard) {
            console.log(`WebMCP: Reference card '${cardName}' not found in gallery.`);
            return false;
        }
        
        const target = targetCard.querySelector("video") || targetCard.querySelector("img") || targetCard;
        targetCard.scrollIntoView({ block: "center" });
        await new Promise(r => setTimeout(r, 200));
        
        // Right click
        target.dispatchEvent(new MouseEvent('contextmenu', {
            bubbles: true, cancelable: true, view: window, buttons: 2
        }));
        await new Promise(r => setTimeout(r, 500));
        
        const menuItems = Array.from(document.querySelectorAll("[role='menuitem']"));
        const useAsRefBtn = menuItems.find(el => el.innerText.includes("Add to prompt") || el.innerText.includes("reference"));
        
        if (useAsRefBtn) {
            useAsRefBtn.click();
            console.log(`WebMCP: Reference card '${cardName}' successfully attached.`);
            await new Promise(r => setTimeout(r, 400));
            return true;
        }
        
        // Close menu if button not found
        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
        return false;
    }

    /**
     * Downloads an asset card at a specific index to the designated resolution
     */
    async function downloadAsset(cardIndex, resolution) {
        console.log(`WebMCP: downloadAsset called for card index: ${cardIndex}, resolution: ${resolution}`);
        dismissOverlays();
        
        const notifs = document.querySelector("section[aria-label='Notifications alt+T']");
        if (notifs) notifs.style.display = 'none';

        const cards = document.querySelectorAll("[aria-roledescription='draggable']");
        const card = cards[cardIndex];
        if (!card) {
            console.log(`WebMCP: Card at index ${cardIndex} not found.`);
            return false;
        }
        
        const target = card.querySelector("video") || card.querySelector("img") || card;
        card.scrollIntoView({ block: "center" });
        await new Promise(r => setTimeout(r, 200));
        
        // Hover over card
        const hoverEvent = new MouseEvent('mouseover', { bubbles: true, cancelable: true });
        target.dispatchEvent(hoverEvent);
        await new Promise(r => setTimeout(r, 200));

        // Right-click to open context menu
        target.dispatchEvent(new MouseEvent('contextmenu', {
            bubbles: true, cancelable: true, view: window, buttons: 2
        }));
        await new Promise(r => setTimeout(r, 500));
        
        // Find menu item "Download"
        const menuItems = Array.from(document.querySelectorAll("[role='menuitem'], button, a"));
        const downloadItem = menuItems.find(el => el.innerText.includes("Download"));
        if (!downloadItem) {
            console.log("WebMCP: Download menu item not found.");
            document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
            return false;
        }
        
        downloadItem.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
        downloadItem.click();
        await new Promise(r => setTimeout(r, 500));
        
        // Find resolution item in submenu
        const submenuItems = Array.from(document.querySelectorAll("[role='menuitem'], button, a, div"));
        let resolutionItem = submenuItems.find(el => el.innerText.includes(resolution));
        
        if (!resolutionItem) {
            // Fallback checks
            if (resolution === '1080p') {
                resolutionItem = submenuItems.find(el => el.innerText.includes("1080p") || el.innerText.includes("Upscaled"));
            } else if (resolution === '720p') {
                resolutionItem = submenuItems.find(el => el.innerText.includes("720p") || el.innerText.includes("Original Size"));
            } else if (resolution === '2K') {
                resolutionItem = submenuItems.find(el => el.innerText.includes("2K") || el.innerText.includes("2K Upscaled"));
            } else if (resolution === '1K') {
                resolutionItem = submenuItems.find(el => el.innerText.includes("1K") || el.innerText.includes("Original size"));
            }
        }
        
        if (resolutionItem) {
            console.log("WebMCP: Clicking resolution button:", resolutionItem.innerText);
            resolutionItem.click();
            await new Promise(r => setTimeout(r, 300));
            document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
            return true;
        }
        
        console.log(`WebMCP: Resolution option ${resolution} not found in download submenu.`);
        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
        return false;
    }

    /**
     * Helper to send messaging through window.postMessage to the isolated world bridge
     */
    function sendToBackground(payload) {
        window.postMessage({
            source: 'WEBMCP_MAIN',
            type: 'WEBMCP_TO_BACKGROUND',
            payload: payload
        }, '*');
    }

    // Listen for incoming commands forwarded by the isolated bridge
    window.addEventListener("message", async function(event) {
        if (event.source !== window) return;
        if (event.data && event.data.source === 'WEBMCP_BACKGROUND' && event.data.type === 'WEBMCP_TO_MAIN') {
            const request = event.data.payload;
            console.log("WebMCP: Main script received request:", request);
            
            let result = null;
            switch(request.action) {
                case 'fill_prompt':
                    result = fillPrompt(request.text);
                    break;
                case 'upload_reference':
                    result = await uploadReference(request.imageDataUrl);
                    break;
                case 'click_generate':
                    result = clickGenerate();
                    break;
                case 'get_queue_status':
                    result = getQueueStatus();
                    break;
                case 'get_download_links':
                    result = getDownloadLinks();
                    break;
                case 'get_credits':
                    result = await getCreditsRemaining();
                    break;
                case 'dismiss_overlays':
                    dismissOverlays();
                    result = true;
                    break;
                case 'apply_settings':
                    result = await applySettings(request.config);
                    break;
                case 'attach_avatar_or_character':
                    result = await attachAvatarOrCharacter(request.type, request.name);
                    break;
                case 'attach_card_reference_by_name':
                    result = await attachCardReferenceByName(request.cardName);
                    break;
                case 'download_asset':
                    result = await downloadAsset(request.cardIndex, request.resolution);
                    break;
                default:
                    console.log("WebMCP: Unknown action request:", request.action);
                    return;
            }

            // Return response to isolated script
            window.postMessage({
                source: 'WEBMCP_MAIN',
                type: 'WEBMCP_FROM_MAIN_RESPONSE',
                id: request.id,
                result: result
            }, '*');
        }
    });

    // Expose APIs to global window object
    window.keystoneWebMCP = {
        fillPrompt,
        uploadReference,
        clickGenerate,
        getQueueStatus,
        getDownloadLinks,
        getCreditsRemaining,
        dismissOverlays,
        applySettings,
        attachAvatarOrCharacter,
        attachCardReferenceByName,
        downloadAsset,
        interceptedUrls: interceptedUrls
    };

    console.log("WebMCP: APIs exposed to window.keystoneWebMCP.");
})();
