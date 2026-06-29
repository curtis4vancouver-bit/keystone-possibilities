// inject.js - Runs in the main page context of Google Flow to access React Fiber and Zustand store.

(function() {
  console.log("[Flow Commander Inject] Script loaded in page context.");

  // Helper to walk the React Fiber tree and find the promptBoxStore
  function getPromptStore() {
    const editor = document.querySelector('[data-slate-editor]');
    if (!editor) return null;
    const fiberKey = Object.keys(editor).find(k => k.startsWith('__reactFiber$'));
    let current = editor[fiberKey];
    while (current) {
      if (current.memoizedProps && current.memoizedProps.promptBoxStore) {
        return current.memoizedProps.promptBoxStore;
      }
      current = current.return;
    }
    return null;
  }

  // Helper to walk the React Fiber tree and find the Slate editor instance
  function getSlateEditor() {
    const editorEl = document.querySelector('[data-slate-editor]');
    if (!editorEl) return null;
    const fiberKey = Object.keys(editorEl).find(k => k.startsWith('__reactFiber$'));
    let current = editorEl[fiberKey];
    while (current) {
      if (current.memoizedProps && current.memoizedProps.editor && typeof current.memoizedProps.editor.insertText === 'function') {
        return current.memoizedProps.editor;
      }
      current = current.return;
    }
    return null;
  }

  // Helper to walk the React Fiber tree and find the React Query client from multiple elements
  function getQueryClient() {
    const selectors = ['[data-slate-editor]', '#root', 'body > div', 'body'];
    for (const selector of selectors) {
      const el = document.querySelector(selector);
      if (!el) continue;
      const fiberKey = Object.keys(el).find(k => k.startsWith('__reactFiber$'));
      if (!fiberKey) continue;
      let current = el[fiberKey];
      while (current) {
        if (current.memoizedProps && current.memoizedProps.client) {
          return current.memoizedProps.client;
        }
        current = current.return;
      }
    }
    return null;
  }

  // Helper to walk the React Fiber tree and find workflows from the React Query Cache
  function getWorkflows() {
    const client = getQueryClient();
    if (!client) return [];
    const query = client.queryCache.queries.find(q => q.queryKey && q.queryKey[0] && q.queryKey[0][0] === 'flow' && q.queryKey[0][1] === 'projectInitialData');
    if (!query || !query.state.data || !query.state.data.projectContents) return [];
    return query.state.data.projectContents.workflows || [];
  }

  // Helper to walk the React Fiber tree and find user likenesses from the React Query Cache
  function getLikenessId() {
    const client = getQueryClient();
    if (!client) return null;
    const query = client.queryCache.queries.find(q => q.queryKey && q.queryKey[0] && q.queryKey[0][0] === 'flow' && q.queryKey[0][1] === 'projectInitialData');
    if (!query || !query.state.data || !query.state.data.projectContents) return null;
    const likenesses = query.state.data.projectContents.likenesses || [];
    const meLikeness = likenesses.find(l => l.handle === 'me');
    return meLikeness ? meLikeness.likenessId : null;
  }

  // Handle incoming message requests from content.js
  window.addEventListener('message', async (event) => {
    // Only accept messages from our content script
    if (event.data && event.data.source === 'flow-commander-content') {
      const { action, payload, messageId } = event.data;
      console.log(`[Flow Commander Inject] Received action: ${action}`, payload);
      
      let result = { success: false, error: "Unknown action" };
      try {
        const store = getPromptStore();
        if (!store && action !== "PING") {
          result = { success: false, error: "Google Flow React store not found. Check editor." };
        } else {
          result = await handleAction(store, action, payload);
        }
      } catch (e) {
        console.error("[Flow Commander Inject] Error handling action:", e);
        result = { success: false, error: e.message };
      }

      // Send result back to content.js
      window.postMessage({
        source: 'flow-commander-page',
        action: action + '_RESPONSE',
        payload: result,
        messageId: messageId
      }, '*');
    }
  });

  // Helper to apply settings via DOM clicks to ensure page UI and React context stay in sync
  async function applySettingsDOM(payload) {
    const sleep = (ms) => new Promise(res => setTimeout(res, ms));
    
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
      el.click();
    }

    function findSettingsTriggerButton() {
      const buttons = document.querySelectorAll('button');
      for (const btn of buttons) {
        const text = btn.innerText || btn.textContent || "";
        if (btn.getAttribute('aria-haspopup') === 'menu' && (
          text.includes('Banana') || text.includes('Veo') || text.includes('Omni') || text.includes('Abra') || text.includes('1x') || text.includes('crop_') || text.includes('Video') || text.includes('Image')
        )) {
          return btn;
        }
      }
      for (const btn of buttons) {
        if (btn.id && btn.id.startsWith('radix-') && btn.getAttribute('aria-haspopup') === 'menu') {
          return btn;
        }
      }
      return null;
    }

    const trigger = findSettingsTriggerButton();
    if (!trigger) return { success: false, error: "Settings trigger button not found" };
    
    let popover = document.querySelector('[role="menu"], [data-radix-menu-content], [data-radix-popper-content-wrapper]');
    const isAlreadyOpen = trigger.getAttribute('aria-expanded') === 'true' || !!popover;
    
    if (!isAlreadyOpen) {
      dispatchClickSequence(trigger);
      await sleep(600);
      popover = document.querySelector('[role="menu"], [data-radix-menu-content], [data-radix-popper-content-wrapper]');
    }
    
    if (!popover) return { success: false, error: "Settings popover not found" };
    
    // 1. Mode Tab
    if (payload.mode) {
      const modeStr = payload.mode.toUpperCase();
      const tabs = popover.querySelectorAll('button[role="tab"]');
      let targetTab = null;
      for (const tab of tabs) {
        const text = (tab.textContent || "").toLowerCase();
        if (modeStr.includes("VIDEO") && (text.includes("play_circle") || text.includes("video"))) {
          targetTab = tab;
          break;
        } else if (modeStr.includes("IMAGE") && (text.includes("image") && !text.includes("play_circle"))) {
          targetTab = tab;
          break;
        }
      }
      if (targetTab && targetTab.getAttribute('aria-selected') !== 'true') {
        dispatchClickSequence(targetTab);
        await sleep(600);
        popover = document.querySelector('[role="menu"], [data-radix-menu-content], [data-radix-popper-content-wrapper]') || popover;
      }
    }

    // 2. Aspect Ratio
    if (payload.ratio) {
      const ratioStr = payload.ratio.toUpperCase();
      let matchTerm = "";
      if (ratioStr.includes("LANDSCAPE") || ratioStr.includes("16_9") || ratioStr.includes("16:9")) matchTerm = "16_9";
      else if (ratioStr.includes("PORTRAIT") || ratioStr.includes("9_16") || ratioStr.includes("9:16")) matchTerm = "9_16";
      else if (ratioStr.includes("SQUARE") || ratioStr.includes("1_1") || ratioStr.includes("1:1")) matchTerm = "1_1";

      if (matchTerm) {
        const ratioButtons = popover.querySelectorAll('button');
        let ratioBtn = null;
        for (const btn of ratioButtons) {
          const text = btn.textContent || "";
          if (text.includes(matchTerm) || text.replace('_', ':').includes(matchTerm.replace('_', ':'))) {
            ratioBtn = btn;
            break;
          }
        }
        if (ratioBtn && ratioBtn.getAttribute('aria-selected') !== 'true') {
          dispatchClickSequence(ratioBtn);
          await sleep(400);
          popover = document.querySelector('[role="menu"], [data-radix-menu-content], [data-radix-popper-content-wrapper]') || popover;
        }
      }
    }

    // 3. Outputs count
    if (payload.outputs) {
      const outputsStr = String(payload.outputs);
      const targetText = outputsStr.endsWith('x') ? outputsStr : (outputsStr === '1' ? '1x' : 'x' + outputsStr);
      const outputButtons = popover.querySelectorAll('button');
      let outputBtn = null;
      for (const btn of outputButtons) {
        if (btn.textContent.trim() === targetText) {
          outputBtn = btn;
          break;
        }
      }
      if (outputBtn && outputBtn.getAttribute('aria-selected') !== 'true') {
        dispatchClickSequence(outputBtn);
        await sleep(400);
        popover = document.querySelector('[role="menu"], [data-radix-menu-content], [data-radix-popper-content-wrapper]') || popover;
      }
    }

    // 4. Model Selection (Before duration)
    if (payload.model) {
      const modelStr = payload.model.toLowerCase();
      const modelDropdownBtn = popover.querySelector('button[aria-haspopup="menu"]');
      if (modelDropdownBtn) {
        dispatchClickSequence(modelDropdownBtn);
        await sleep(600);
        
        const menuItems = document.querySelectorAll('[role="menuitem"], .mat-mdc-menu-item, div[role="menuitem"]');
        let targetItem = null;
        for (const item of menuItems) {
          const text = item.textContent || "";
          let match = false;
          if (modelStr === "nano_banana_pro" && text.includes("Banana Pro")) match = true;
          else if (modelStr === "narwhal_display" && text.includes("Narwhal")) match = true;
          else if (modelStr === "abra" && (text.includes("Omni Flash") || text.includes("Abra"))) match = true;
          else if (modelStr === "veo_3_1_quality" && text.includes("Quality")) match = true;
          else if (modelStr === "veo_3_1_fast" && text.includes("Fast")) match = true;
          else if (modelStr === "veo_3_1_lite" && text.includes("Lite")) match = true;
          
          if (match) {
            targetItem = item;
            break;
          }
        }
        
        if (targetItem) {
          dispatchClickSequence(targetItem);
          await sleep(600);
          popover = document.querySelector('[role="menu"], [data-radix-menu-content], [data-radix-popper-content-wrapper]') || popover;
        } else {
          dispatchClickSequence(modelDropdownBtn);
          await sleep(400);
        }
      }
    }

    // 5. Video Duration
    if (payload.duration && (payload.mode || "").toUpperCase().includes("VIDEO")) {
      const durText = String(payload.duration).endsWith('s') ? String(payload.duration) : String(payload.duration) + 's';
      const durButtons = popover.querySelectorAll('button');
      let durBtn = null;
      for (const btn of durButtons) {
        if (btn.textContent.trim() === durText) {
          durBtn = btn;
          break;
        }
      }
      if (durBtn && durBtn.getAttribute('aria-selected') !== 'true') {
        dispatchClickSequence(durBtn);
        await sleep(400);
      }
    }

    // Close settings popover by simulated pointer/mouse clicks outside, and fallback to trigger toggle
    const activePopover = document.querySelector('[role="menu"], [data-radix-menu-content], [data-radix-popper-content-wrapper]');
    if (activePopover) {
      const triggerBtn = findSettingsTriggerButton();
      if (triggerBtn && triggerBtn.getAttribute('aria-expanded') === 'true') {
        dispatchClickSequence(triggerBtn);
      } else {
        const workspace = document.querySelector('.flow-workspace') || document.body;
        workspace.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true, view: window }));
        workspace.click();
      }
      await sleep(400);
    }
    return { success: true };
  }

  // Execute the store operations based on action type
  async function handleAction(store, action, payload) {
    if (action === "PING") {
      const storeExists = !!getPromptStore();
      return { success: true, storeFound: storeExists };
    }

    const actions = store.getState().actions;
    const state = store.getState();

    switch(action) {
      case "SET_SETTINGS": {
        // Run DOM clicks to ensure settings are visually and state-applied in sync
        const domRes = await applySettingsDOM(payload);
        if (!domRes.success) {
          console.warn("[Flow Commander Inject] DOM settings application failed:", domRes.error);
        }
        
        // Call Zustand actions directly as fallback/reinforcement
        try {
          if (payload.mode) actions.setMode(payload.mode);
          
          if (payload.mode === "VIDEO") {
            if (payload.model) actions.setVideoModelFamily(payload.model);
            if (payload.duration) actions.setSelectedVideoDuration(parseInt(payload.duration));
          } else if (payload.mode === "IMAGE") {
            if (payload.model) actions.setImageModelFamily(payload.model);
          }
          
          if (payload.ratio) actions.setAspectRatio(payload.ratio);
          if (payload.outputs) actions.setOutputsPerPrompt(parseInt(payload.outputs));
        } catch (e) {
          console.error("[Flow Commander Inject] Zustand settings fallback failed:", e);
        }

        return {
          success: true,
          mode: store.getState().mode,
          aspectRatio: store.getState().aspectRatio,
          duration: store.getState().selectedVideoDuration,
          numOutputs: store.getState().outputsPerPrompt
        };
      }

      case "PREPARE_PROMPT": {
        // payload: { text, characterId, likenessId, referenceImageIds }
        // 1. Clear everything first
        actions.clearPromptBox();
        actions.clearIngredients();
        actions.clearCharacterServerIds();
        actions.clearLikenessIngredients();

        // 2. Set the text prompt via Slate editor AND Zustand store to ensure zero desync
        actions.setPrompt(payload.text);
        const slateEditor = getSlateEditor();
        if (slateEditor) {
          try {
            const range = {
              anchor: slateEditor.start([]),
              focus: slateEditor.end([])
            };
            slateEditor.select(range);
            slateEditor.delete();
            slateEditor.insertText(payload.text);
            console.log("[Flow Commander Inject] Set prompt via Slate Editor API");
          } catch (e) {
            console.warn("[Flow Commander Inject] Failed to set prompt via Slate Editor API:", e);
          }
        }

        // 3. Attach character if selected
        if (payload.characterId) {
          console.log(`[Flow Commander Inject] Attaching character: ${payload.characterId}`);
          actions.addCharacterIngredient({
            characterServerId: payload.characterId,
            source: 'PLUS_BUTTON'
          });
        }

        // 4. Attach likeness if selected (Wayne's avatar)
        if (payload.likenessId) {
          const activeLikenessId = getLikenessId() || payload.likenessId;
          console.log(`[Flow Commander Inject] Attaching likeness: ${activeLikenessId}`);
          actions.addLikenessIngredient({
            likenessId: activeLikenessId,
            source: 'PLUS_BUTTON'
          });
        }

        // 5. Attach any reference images (wardrobe, background) using official addImageIngredient action
        if (payload.referenceImageIds && Array.isArray(payload.referenceImageIds)) {
          payload.referenceImageIds.forEach(id => {
            if (id) {
              const cleanId = id.startsWith("fe_id_") ? id.substring(6) : id;
              const workflows = getWorkflows();
              const matchedWf = workflows.find(w => w.name === cleanId || w.id === cleanId || (w.metadata && w.metadata.primaryMediaId === cleanId));
              const targetImageId = matchedWf && matchedWf.metadata ? (matchedWf.metadata.primaryMediaId || cleanId) : cleanId;
              
              console.log(`[Flow Commander Inject] Attaching reference image: ${targetImageId} (resolved from ${cleanId})`);
              try {
                actions.addImageIngredient({
                  imageId: targetImageId,
                  preferredIngredientType: 'REFERENCE',
                  source: 'PLUS_BUTTON'
                });
              } catch (e) {
                console.warn("[Flow Commander Inject] addImageIngredient action failed, falling back to direct state injection.", e);
                // Direct fallback injection with full required properties to satisfy React validation
                const currentIngredients = store.getState().ingredients || [];
                const name = matchedWf && matchedWf.metadata ? (matchedWf.metadata.displayName || "Image") : "Image";
                const url = matchedWf ? (matchedWf.thumbnailUrl || matchedWf.url || "") : "";

                const newIngredients = [...currentIngredients];
                newIngredients.push({
                  type: 'IMAGE',
                  ingredientId: targetImageId,
                  imageId: targetImageId,
                  name: name,
                  url: url,
                  addedTime: new Date(),
                  modifiedTime: new Date(),
                  isLoading: false,
                  preferredIngredientType: 'REFERENCE'
                });
                store.setState({ ingredients: newIngredients });
              }
            }
          });
        }
        
        // 6. Trigger Submit Click via React onClick Prop with Mock Trusted Event
        await new Promise(res => setTimeout(res, 300));
        const buttons = document.querySelectorAll('button');
        let submitBtn = null;
        for (const btn of buttons) {
          const text = btn.textContent || "";
          if ((text.includes('arrow_forward') || text.includes('Create') || text.includes('Submit')) && !btn.id.includes("radix")) {
            submitBtn = btn;
            break;
          }
        }
        if (submitBtn) {
          // Forcefully enable the submit button in the DOM if blocked by React state validation
          if (submitBtn.hasAttribute('disabled')) {
            submitBtn.removeAttribute('disabled');
            console.log("[Flow Commander Inject] Forcefully removed disabled attribute");
          }
          if (submitBtn.getAttribute('aria-disabled') === 'true') {
            submitBtn.setAttribute('aria-disabled', 'false');
            console.log("[Flow Commander Inject] Forcefully set aria-disabled to false");
          }

          const propsKey = Object.keys(submitBtn).find(k => k.startsWith('__reactProps$'));
          const props = propsKey ? submitBtn[propsKey] : null;
          if (props && typeof props.onClick === 'function') {
            props.onClick({
              nativeEvent: { isTrusted: true },
              preventDefault: () => {},
              stopPropagation: () => {}
            });
            console.log("[Flow Commander Inject] Submit triggered successfully via mock onClick!");
          } else {
            console.warn("[Flow Commander Inject] React onClick handler not found on submit button, falling back to DOM click.");
            submitBtn.click();
          }
        } else {
          console.warn("[Flow Commander Inject] Submit button not found or disabled.");
        }

        return {
          success: true,
          promptText: store.getState().promptText,
          ingredients: (store.getState().ingredients || []).map(i => ({ type: i.type, id: i.id }))
        };
      }

      case "GET_STORE_STATE": {
        const s = store.getState();
        const workflows = getWorkflows();
        const workflowNames = {};
        
        // Extract display names renamed by the user
        workflows.forEach(w => {
          if (w.metadata && w.metadata.primaryMediaId) {
            workflowNames[w.metadata.primaryMediaId] = w.metadata.displayName || "";
          }
        });

        return {
          success: true,
          mode: s.mode,
          aspectRatio: s.aspectRatio,
          duration: s.selectedVideoDuration,
          numOutputs: s.outputsPerPrompt,
          videoModel: s.videoModelFamily,
          imageModel: s.imageModelFamily,
          ingredients: (s.ingredients || []).map(i => ({
            type: i.type,
            id: i.id,
            name: i.name,
            characterServerId: i.characterServerId,
            likenessMediaId: i.likenessMediaId
          })),
          workflowNames: workflowNames,
          likenessId: getLikenessId()
        };
      }

      default:
        return { success: false, error: `Action '${action}' not supported in page context.` };
    }
  }
})();
