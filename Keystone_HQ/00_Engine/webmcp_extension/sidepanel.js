// sidepanel.js - Core UI and Automation Engine for Keystone Flow Commander

// Global state variables
let queue = [];
let characters = [];
let projectCards = [];   // cached list of all project cards
let galleryImages = [];  // cached image list for wardrobe/bg dropdowns
let isRunning = false;
let isPaused = false;
let isReloading = false;
let currentTabId = null;
let characterWardrobeRefs = {};  // { "WAYNE": "mediaId", "VICTORIA": "mediaId", ... }
let backgroundRef = "";
let serializedDownloadQueue = [];
let serializedDownloadLock = false;

// Default Configs
let settings = {
  mode: "VIDEO",
  model: "abra",
  duration: "10",
  ratio: "LANDSCAPE",
  downloadQuality: "1080p",
  imageDownloadQuality: "2K",
  projectFolder: "FLOW_RUN",
  outputs: "1",
  outputDirectory: "../Desktop/",
  prependOrder: true
};

// Helper: Determine if a sequence name represents a video, image, or thumbnail
function getItemMode(sequenceName) {
  const name = sequenceName.toUpperCase();
  if (name.startsWith("T")) {
    return "IMAGE";
  }
  if (name.startsWith("A") || name.startsWith("BV")) {
    return "VIDEO";
  }
  // For "B" prefix, default to IMAGE (since B-roll videos use "BV" prefix)
  if (name.startsWith("B")) {
    return "IMAGE";
  }
  return settings.mode; // default fallback
}

// UI Elements cache
const els = {
  connectionStatus: document.getElementById("connectionStatus"),
  settingMode: document.getElementById("settingMode"),
  settingModel: document.getElementById("settingModel"),
  settingDuration: document.getElementById("settingDuration"),
  settingRatio: document.getElementById("settingRatio"),
  settingDownload: document.getElementById("settingDownload"),
  settingImageDownload: document.getElementById("settingImageDownload"),
  durationGroup: document.getElementById("durationGroup"),
  videoQualityGroup: document.getElementById("videoQualityGroup"),
  imageQualityGroup: document.getElementById("imageQualityGroup"),
  projectFolderName: document.getElementById("projectFolderName"),
  outputDirectory: document.getElementById("outputDirectory"),
  prependOrder: document.getElementById("prependOrder"),
  applySettings: document.getElementById("applySettings"),
  characterList: document.getElementById("characterList"),
  backgroundRefSelect: document.getElementById("backgroundRefSelect"),
  refreshRefs: document.getElementById("refreshRefs"),
  refreshGallery: document.getElementById("refreshGallery"),
  galleryList: document.getElementById("galleryList"),
  scriptInput: document.getElementById("scriptInput"),
  parseScript: document.getElementById("parseScript"),
  clearQueue: document.getElementById("clearQueue"),
  queueList: document.getElementById("queueList"),
  progressBar: document.getElementById("progressBar"),
  progressText: document.getElementById("progressText"),
  batchText: document.getElementById("batchText"),
  downloadText: document.getElementById("downloadText"),
  retryText: document.getElementById("retryText"),
  startBtn: document.getElementById("startBtn"),
  pauseBtn: document.getElementById("pauseBtn"),
  stopBtn: document.getElementById("stopBtn"),
  logEntries: document.getElementById("logEntries"),
  
  // Prompt Queue Default Avatar selector
  defaultQueueAvatar: document.getElementById("defaultQueueAvatar"),
  thumbPreviewDefaultAvatar: document.getElementById("thumb-preview-DEFAULT-AVATAR"),

  // Custom Download Modal Overlay
  downloadModal: document.getElementById("downloadModal"),
  modalFilename: document.getElementById("modalFilename"),
  modalDirectory: document.getElementById("modalDirectory"),
  modalCancel: document.getElementById("modalCancel"),
  modalConfirm: document.getElementById("modalConfirm")
};

// Helper: Update settings form controls dynamically based on active Mode
function updateSettingsForm() {
  const mode = els.settingMode.value;
  
  // Cache currently selected model before we change options
  const currentModel = els.settingModel.value;
  
  let optionsHtml = '';
  if (mode === "VIDEO") {
    optionsHtml = `
      <option value="abra">Omni Flash</option>
      <option value="veo_3_1_quality">Veo 3.1 Quality</option>
      <option value="veo_3_1_fast">Veo 3.1 Fast</option>
      <option value="veo_3_1_lite">Veo 3.1 Lite</option>
    `;
    if (els.durationGroup) els.durationGroup.style.display = "flex";
    if (els.videoQualityGroup) els.videoQualityGroup.style.display = "flex";
    if (els.imageQualityGroup) els.imageQualityGroup.style.display = "none";
  } else {
    optionsHtml = `
      <option value="nano_banana_pro">Banana Pro</option>
      <option value="narwhal_display">Narwhal Display</option>
    `;
    if (els.durationGroup) els.durationGroup.style.display = "none";
    if (els.videoQualityGroup) els.videoQualityGroup.style.display = "none";
    if (els.imageQualityGroup) els.imageQualityGroup.style.display = "flex";
  }
  
  els.settingModel.innerHTML = optionsHtml;
  
  // Try to preserve current selection if valid for new mode
  if ([...els.settingModel.options].some(o => o.value === currentModel)) {
    els.settingModel.value = currentModel;
  } else {
    els.settingModel.value = mode === "VIDEO" ? "abra" : "nano_banana_pro";
  }

}

// Helper: Normalize the output directory path (ensure trailing slash)
function normalizeOutputDir(path) {
  let p = (path || '../Desktop/').trim();
  if (p === '.' || p === './') return '';
  if (p && !p.endsWith('/')) p += '/';
  return p;
}

// Helper: Add message to activity log console
function log(msg, type = "info") {
  const time = new Date().toLocaleTimeString();
  const entry = document.createElement("div");
  entry.className = `log-entry ${type}`;
  entry.innerHTML = `<span class="log-timestamp">[${time}]</span> ${msg}`;
  els.logEntries.appendChild(entry);
  els.logEntries.scrollTop = els.logEntries.scrollHeight;
}

// Helper: sleep/wait timer
const sleep = (ms) => new Promise(res => setTimeout(res, ms));

// Check active tab and query connectivity to content script
async function checkTabConnection() {
  return new Promise((resolve) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (!tabs || tabs.length === 0) {
        setConnected(false);
        resolve(false);
        return;
      }
      
      const activeTab = tabs[0];
      if (!activeTab.url || !activeTab.url.includes("labs.google/fx/tools/flow")) {
        // Fallback: search for any open Flow tab
        chrome.tabs.query({ url: "*://labs.google/fx/tools/flow*" }, (flowTabs) => {
          if (flowTabs && flowTabs.length > 0) {
            currentTabId = flowTabs[0].id;
            chrome.tabs.sendMessage(currentTabId, { action: "PING" }, (response) => {
              if (chrome.runtime.lastError || !response || !response.connected) {
                setConnected(false);
                resolve(false);
              } else {
                setConnected(true);
                resolve(true);
              }
            });
          } else {
            setConnected(false);
            resolve(false);
          }
        });
        return;
      }

      currentTabId = activeTab.id;
      
      // Ping content script
      chrome.tabs.sendMessage(currentTabId, { action: "PING" }, (response) => {
        if (chrome.runtime.lastError || !response || !response.connected) {
          setConnected(false);
          resolve(false);
        } else {
          setConnected(true);
          resolve(true);
        }
      });
    });
  });
}


// Default avatar choice
let defaultQueueAvatarVal = "WAYNE";
let activeModalResolve = null;

// Get thumbnail for a speaker/character
function getSpeakerThumbnail(speaker, useCharacter) {
  if (!useCharacter || speaker === "BROLL" || !speaker) {
    return "";
  }
  
  if (speaker === "WAYNE") {
    // Try to find a Wayne likeness or me card in projectCards
    const meCard = projectCards.find(c => c.type === 'character' && (c.name.toLowerCase().includes('wayne') || c.name.toLowerCase().includes('me')));
    if (meCard && meCard.thumbnailUrl) return meCard.thumbnailUrl;
    
    // Look for any card with me/likeness matching IDs
    const anyLikeness = projectCards.find(c => c.mediaId && (c.mediaId.includes('0278d9a4') || c.mediaId.includes('2e00f1a0')));
    if (anyLikeness && anyLikeness.thumbnailUrl) return anyLikeness.thumbnailUrl;

    const firstChar = projectCards.find(c => c.type === 'character');
    if (firstChar && firstChar.thumbnailUrl) return firstChar.thumbnailUrl;
    return "";
  }
  
  // Dynamic characters
  const matchedChar = characters.find(c => c.name.toUpperCase() === speaker);
  if (matchedChar && matchedChar.thumbnailUrl) {
    return matchedChar.thumbnailUrl;
  }
  
  const matchedCard = projectCards.find(c => c.name.toUpperCase() === speaker || (matchedChar && c.mediaId === matchedChar.serverId));
  if (matchedCard && matchedCard.thumbnailUrl) {
    return matchedCard.thumbnailUrl;
  }
  
  return "";
}

// Build queue item speaker dropdown select
function buildQueueItemSpeakerSelect(selectedSpeaker, useCharacter, index) {
  const currentVal = (!useCharacter || selectedSpeaker === "BROLL" || !selectedSpeaker) ? "BROLL" : selectedSpeaker;
  let html = `<select class="queue-item-speaker-select" data-index="${index}" style="margin-left: 4px;">`;
  html += `<option value="BROLL" ${currentVal === "BROLL" ? "selected" : ""}>B-Roll (None)</option>`;
  html += `<option value="WAYNE" ${currentVal === "WAYNE" ? "selected" : ""}>Wayne (Me)</option>`;
  characters.forEach(char => {
    const uName = char.name.toUpperCase();
    html += `<option value="${uName}" ${currentVal === uName ? "selected" : ""}>${char.name}</option>`;
  });
  html += `</select>`;
  return html;
}

// Update default avatar dropdown select options
function updateDefaultAvatarDropdown() {
  if (!els.defaultQueueAvatar) return;
  
  let html = `
    <option value="BROLL" ${defaultQueueAvatarVal === "BROLL" ? "selected" : ""}>B-Roll (None)</option>
    <option value="WAYNE" ${defaultQueueAvatarVal === "WAYNE" ? "selected" : ""}>Wayne (Me)</option>
  `;
  characters.forEach(char => {
    const uName = char.name.toUpperCase();
    html += `<option value="${uName}" ${defaultQueueAvatarVal === uName ? "selected" : ""}>${char.name}</option>`;
  });
  
  els.defaultQueueAvatar.innerHTML = html;
  updateDefaultAvatarPreview();
}

// Update default avatar visual preview
function updateDefaultAvatarPreview() {
  const container = els.thumbPreviewDefaultAvatar;
  if (!container) return;
  
  const val = els.defaultQueueAvatar.value;
  const useChar = val !== "BROLL";
  const thumbUrl = getSpeakerThumbnail(val, useChar);
  
  if (thumbUrl) {
    container.innerHTML = `<img src="${thumbUrl}" class="thumb-preview-img" style="width: 24px; height: 24px;" />`;
  } else {
    container.innerHTML = `<span class="material-symbols-outlined" style="font-size: 20px; color: var(--text-muted);">person</span>`;
  }
}

// Opens the custom download modal and resolves with { filename, directory } or null
function promptDownloadSettings(defaultName) {
  return new Promise((resolve) => {
    const modal = els.downloadModal;
    if (!modal) {
      resolve(null);
      return;
    }
    
    els.modalFilename.value = defaultName;
    els.modalDirectory.value = settings.outputDirectory || '../Desktop/';
    
    modal.style.display = "flex";
    activeModalResolve = resolve;
  });
}

// Bind modal listeners
if (els.modalCancel) {
  els.modalCancel.addEventListener("click", () => {
    els.downloadModal.style.display = "none";
    if (activeModalResolve) {
      activeModalResolve(null);
      activeModalResolve = null;
    }
  });
}

if (els.modalConfirm) {
  els.modalConfirm.addEventListener("click", () => {
    const filename = els.modalFilename.value.trim();
    const directory = els.modalDirectory.value.trim();
    
    els.downloadModal.style.display = "none";
    if (activeModalResolve) {
      activeModalResolve({ filename, directory });
      activeModalResolve = null;
    }
  });
}

// Bind default avatar change
if (els.defaultQueueAvatar) {
  els.defaultQueueAvatar.addEventListener("change", () => {
    defaultQueueAvatarVal = els.defaultQueueAvatar.value;
    updateDefaultAvatarPreview();
    settings.defaultAvatar = defaultQueueAvatarVal;
    saveState();
  });
}

// Update connection status dot in header
function setConnected(connected) {
  const dot = els.connectionStatus.querySelector(".status-dot");
  const text = els.connectionStatus.querySelector(".status-text");
  
  if (connected) {
    dot.className = "status-dot connected";
    text.textContent = "Connected";
  } else {
    dot.className = "status-dot pulsing";
    text.textContent = "Disconnected (Open Flow Tab)";
  }
}

// Send command to content script safely
function sendToContentScript(action, payload = {}) {
  return new Promise((resolve) => {
    if (!currentTabId) {
      resolve({ success: false, error: "No connected Flow tab active." });
      return;
    }
    chrome.tabs.sendMessage(currentTabId, { action, payload }, (res) => {
      if (chrome.runtime.lastError) {
        resolve({ success: false, error: chrome.runtime.lastError.message });
      } else {
        resolve(res);
      }
    });
  });
}

// Collapsible Panels listener setup
document.querySelectorAll(".panel-header").forEach(header => {
  header.addEventListener("click", () => {
    const targetId = header.getAttribute("data-toggle");
    if (!targetId) return;

    const content = document.getElementById(targetId);
    if (!content) return;

    content.classList.toggle("expanded");
    header.classList.toggle("expanded-header");
  });
});

// Load state from local storage on startup
function loadState() {
  chrome.storage.local.get(["settings", "queue", "characters", "projectCards", "characterWardrobeRefs", "backgroundRef"], (data) => {
    if (data.settings) {
      settings = { ...settings, ...data.settings };
      settings.outputs = "1"; // Force 1 output to prevent credit waste
      // Populate inputs
      els.settingMode.value = settings.mode;
      els.settingModel.value = settings.model;
      els.settingDuration.value = settings.duration;
      els.settingRatio.value = settings.ratio;
      els.settingDownload.value = settings.downloadQuality;
      els.settingImageDownload.value = settings.imageDownloadQuality;
      els.projectFolderName.value = settings.projectFolder;
      
      if (settings.outputDirectory) els.outputDirectory.value = settings.outputDirectory;
      if (settings.prependOrder !== undefined) els.prependOrder.checked = settings.prependOrder;
      if (settings.defaultAvatar) defaultQueueAvatarVal = settings.defaultAvatar;

      updateSettingsForm();
      
      // Update background task folder name and output directory
      chrome.runtime.sendMessage({ 
        action: "SET_PROJECT_FOLDER", 
        payload: { 
          folderName: settings.projectFolder,
          outputDirectory: settings.outputDirectory
        } 
      });
    } else {
      updateSettingsForm();
    }
    
    if (data.queue) {
      queue = data.queue;
      updateQueueUI();
      updateProgressUI();
    }

    if (data.characters) {
      characters = data.characters;
    }

    if (data.projectCards) {
      projectCards = data.projectCards;
      galleryImages = projectCards.filter(c => c.type === 'image' && c.status === 'done');
      updateGalleryUI();
    }

    if (data.characterWardrobeRefs) {
      characterWardrobeRefs = data.characterWardrobeRefs;
    }

    if (data.backgroundRef) {
      backgroundRef = data.backgroundRef;
    }

    updateCharacterUI();
    updateDefaultAvatarDropdown();
    
    log("Loaded state from local storage.");
    checkTabConnection().then(connected => {
      if (connected) {
        syncProjectDetails();
      }
    });
  });
}

// Save state to local storage
function saveState() {
  // Ensure settings object is updated from active UI values
  settings.mode = els.settingMode.value;
  settings.model = els.settingModel.value;
  settings.duration = els.settingDuration.value;
  settings.ratio = els.settingRatio.value;
  settings.downloadQuality = els.settingDownload.value;
  settings.imageDownloadQuality = els.settingImageDownload.value;
  settings.projectFolder = els.projectFolderName.value.trim() || "FLOW_RUN";
  settings.outputDirectory = els.outputDirectory.value.trim() || '../Desktop/';
  settings.prependOrder = els.prependOrder.checked;
  settings.defaultAvatar = defaultQueueAvatarVal;

  chrome.storage.local.set({
    settings: settings,
    queue: queue,
    characters: characters,
    projectCards: projectCards,
    characterWardrobeRefs: characterWardrobeRefs,
    backgroundRef: backgroundRef
  });
}

// Synchronize project details (characters, gallery cards) from the connected tab
async function syncProjectDetails() {
  log("Scanning project details from active Flow tab...");
  const res = await sendToContentScript("GET_PROJECT_INFO");
  if (res && res.success) {
    if (res.characters && res.characters.length > 0) {
      characters = res.characters;
    }
    
    // Cache all non-character cards
    projectCards = res.cards || [];
    // Cache gallery images for dropdown population
    galleryImages = projectCards.filter(c => c.type === 'image' && c.status === 'done');
    
    updateCharacterUI();
    updateGalleryUI();
    
    // Auto-detect project folder name from page title if default is used
    if (settings.projectFolder === "FLOW_RUN") {
      chrome.tabs.get(currentTabId, (tab) => {
        if (tab && tab.title) {
          const cleanTitle = tab.title.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '').substring(0, 30);
          els.projectFolderName.value = `FLOW_${cleanTitle}`;
          settings.projectFolder = `FLOW_${cleanTitle}`;
          chrome.runtime.sendMessage({ action: "SET_PROJECT_FOLDER", payload: { folderName: settings.projectFolder, outputDirectory: settings.outputDirectory } });
          saveState();
        }
      });
    }

    log(`Synced. ${characters.length} characters, ${galleryImages.length} images found.`);
  } else {
    log("Failed to sync project details: " + (res ? res.error : "Unknown connection issue"), "warning");
  }
}

// Build <option> HTML for wardrobe dropdown from cached gallery images
function buildWardrobeOptionsHtml() {
  let html = '<option value="">No Wardrobe Ref</option>';
  galleryImages.forEach((img, idx) => {
    const label = img.name && img.name.trim() ? img.name : `Image #${idx + 1}`;
    const optionValue = img.mediaName ? `fe_id_${img.mediaName}` : `fe_id_${img.mediaId}`;
    const displayId = img.mediaName || img.mediaId;
    html += `<option value="${optionValue}">${label} (${displayId.substring(0, 6)})</option>`;
  });
  return html;
}

// Populate unified characters & references panel
function updateCharacterUI() {
  const wardrobeOpts = buildWardrobeOptionsHtml();
  
  // Wayne (Me) card — always first
  const wayneWardrobeVal = characterWardrobeRefs["WAYNE"] || "";
  let html = `
    <div class="char-card active" data-speaker="WAYNE">
      <div class="char-card-header">
        <span class="material-symbols-outlined char-icon">face</span>
        <span class="char-name">Wayne (Me)</span>
        <span class="char-badge likeness">Likeness</span>
      </div>
      <div class="char-card-ref">
        <span class="material-symbols-outlined ref-icon">checkroom</span>
        <select class="char-wardrobe-ref" data-speaker="WAYNE">
          ${wardrobeOpts}
        </select>
        <div class="ref-thumb-preview" id="thumb-preview-WAYNE"></div>
      </div>
    </div>
  `;
  
  // Dynamic characters from project scan
  characters.forEach(char => {
    const speakerKey = char.name.toUpperCase();
    const savedVal = characterWardrobeRefs[speakerKey] || "";
    html += `
      <div class="char-card" data-speaker="${speakerKey}" data-server-id="${char.serverId}">
        <div class="char-card-header">
          <span class="material-symbols-outlined char-icon">accessibility_new</span>
          <span class="char-name">${char.name}</span>
          <span class="char-badge">Character</span>
        </div>
        <div class="char-card-ref">
          <span class="material-symbols-outlined ref-icon">checkroom</span>
          <select class="char-wardrobe-ref" data-speaker="${speakerKey}">
            ${wardrobeOpts}
          </select>
          <div class="ref-thumb-preview" id="thumb-preview-${speakerKey}"></div>
        </div>
      </div>
    `;
  });
  
  els.characterList.innerHTML = html;
  
  // Restore saved wardrobe selections and display previews
  document.querySelectorAll(".char-wardrobe-ref").forEach(sel => {
    const speaker = sel.getAttribute("data-speaker");
    if (characterWardrobeRefs[speaker]) {
      sel.value = characterWardrobeRefs[speaker];
    }
    updateThumbPreview(speaker, sel.value);
    
    // Save on change
    sel.addEventListener("change", () => {
      characterWardrobeRefs[speaker] = sel.value;
      log(`${speaker} wardrobe ref set to: ${sel.value ? sel.options[sel.selectedIndex].text : 'None'}`);
      updateThumbPreview(speaker, sel.value);
      saveState();
    });
  });
  
  // Also populate the global background ref dropdown
  let bgHtml = '<option value="">None (Disabled)</option>';
  galleryImages.forEach((img, idx) => {
    const label = img.name && img.name.trim() ? img.name : `Image #${idx + 1}`;
    const optionValue = img.mediaName ? `fe_id_${img.mediaName}` : `fe_id_${img.mediaId}`;
    const displayId = img.mediaName || img.mediaId;
    bgHtml += `<option value="${optionValue}">${label} (${displayId.substring(0, 6)})</option>`;
  });
  els.backgroundRefSelect.innerHTML = bgHtml;
  els.backgroundRefSelect.value = backgroundRef;
  updateThumbPreview("BACKGROUND", backgroundRef);
}

// Update wardrobe or background thumbnail preview next to selector
function updateThumbPreview(speakerKey, value) {
  const container = document.getElementById(`thumb-preview-${speakerKey}`);
  if (!container) return;
  
  if (!value) {
    container.innerHTML = '';
    return;
  }
  
  const cleanId = value.startsWith("fe_id_") ? value.substring(6) : value;
  const matchedCard = projectCards.find(c => c.mediaId === cleanId || (c.mediaName && c.mediaName === cleanId));
  if (matchedCard && matchedCard.thumbnailUrl) {
    container.innerHTML = `<img src="${matchedCard.thumbnailUrl}" class="thumb-preview-img" title="${matchedCard.name || cleanId}" />`;
  } else {
    container.innerHTML = '';
  }
}

// Populate Media Library (Manual Upscale & Download) list
function updateGalleryUI() {
  const doneCards = projectCards.filter(c => c.status === 'done');
  
  if (doneCards.length === 0) {
    els.galleryList.innerHTML = '<div class="gallery-empty">No completed media found in project. Click Refresh below.</div>';
    return;
  }
  
  let html = "";
  doneCards.forEach(card => {
    const isVideo = card.type === 'video';
    const icon = isVideo ? "play_circle" : "image";
    const iconClass = isVideo ? "video" : "image";
    
    const thumbHtml = card.thumbnailUrl 
      ? `<img class="gallery-item-thumb" src="${card.thumbnailUrl}" />` 
      : `<span class="material-symbols-outlined gallery-item-icon ${iconClass}">${icon}</span>`;
    
    html += `
      <div class="gallery-item">
        ${thumbHtml}
        <div class="gallery-item-details">
          <span class="gallery-item-name" title="${card.name}">${card.name}</span>
          <span class="gallery-item-id">ID: ${card.mediaId.substring(0, 8)} (${card.type.toUpperCase()})</span>
        </div>
        <div class="gallery-item-actions">
          <button class="btn btn-secondary btn-small download-card-btn" data-id="${card.mediaId}" data-type="${card.type}" data-name="${card.name}">
            <span class="material-symbols-outlined" style="font-size: 14px !important;">download</span> Download
          </button>
        </div>
      </div>
    `;
  });
  
  els.galleryList.innerHTML = html;
   // Add click handlers for manual downloads
  document.querySelectorAll(".download-card-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      const mediaId = btn.getAttribute("data-id");
      const type = btn.getAttribute("data-type");
      const currentName = btn.getAttribute("data-name");
      
      // Prompt for download settings using our modal
      const modalRes = await promptDownloadSettings(currentName);
      if (modalRes === null) return;
      
      const cleanName = modalRes.filename.trim().replace(/[^a-zA-Z0-9_\-]/g, '_') || currentName;
      log(`Manual download triggered for ${cleanName} (${type})...`);
      
      // Determine folder & extension
      const subfolder = type === 'video' ? "Videos" : "Images";
      const extension = type === 'video' ? ".mp4" : ".png";
      const resolution = type === 'video' ? settings.downloadQuality : settings.imageDownloadQuality;
      
      // 1. Register file expectation
      const regRes = await chrome.runtime.sendMessage({
        action: "REGISTER_DOWNLOAD",
        payload: {
          sequenceName: cleanName,
          subfolder: subfolder,
          extension: extension,
          outputDirectory: modalRes.directory
        }
      });
      
      if (!regRes || !regRes.queued) {
        log(`Failed to register download path for: ${cleanName}`, "error");
        return;
      }
      
      // 2. Trigger click-by-click download menu
      const dlRes = await sendToContentScript("TRIGGER_DOWNLOAD", {
        mediaId: mediaId,
        resolution: resolution
      });
      
      if (dlRes && dlRes.success) {
        log(`📥 Download started for ${cleanName} (${resolution})!`, "success");
      } else {
        log(`❌ Download failed for ${cleanName}: ${dlRes ? dlRes.error : "Timeout"}`, "error");
      }
    });
  });
}

// Parse script logic
els.parseScript.addEventListener("click", () => {
  const text = els.scriptInput.value.trim();
  if (!text) {
    log("Please paste a script first.", "warning");
    return;
  }

  queue = [];
  
  // 1. Try parsing standard Keystone Markdown Format:
  // ### 📋 CLIP A1 — WAYNE
  // THIS IS THE SCRIPT:
  // Dialogue
  // THIS IS THE VIDEO PROMPT:
  // Prompt text
  
  const keystoneRegex = /###\s*📋\s*CLIP\s+([A-Za-z0-9_]+)\s*—\s*([A-Za-z0-9_]+)[\s\S]*?THIS IS THE SCRIPT:\s*([\s\S]*?)THIS IS THE VIDEO PROMPT:\s*([\s\S]*?)(?=###|$)/gi;
  let match;
  let parsedCount = 0;

  while ((match = keystoneRegex.exec(text)) !== null) {
    const sequenceName = match[1].trim();
    const speakerName = match[2].trim().toUpperCase();
    const dialogue = match[3].trim();
    const promptVisual = match[4].trim();

    // Construct talking head instructions
    const combinedPrompt = `He says: "${dialogue}". ${promptVisual}. No subtitles!`;

    let finalSpeaker = speakerName;
    let useChar = true;
    if (finalSpeaker === "BROLL" || finalSpeaker === "NONE" || !finalSpeaker) {
      if (defaultQueueAvatarVal === "BROLL") {
        useChar = false;
        finalSpeaker = "BROLL";
      } else {
        useChar = true;
        finalSpeaker = defaultQueueAvatarVal;
      }
    }

    queue.push({
      sequenceName,
      speaker: finalSpeaker,
      prompt: combinedPrompt,
      status: "queued",
      mediaId: null,
      retryCount: 0,
      maxRetries: 2,
      downloadStatus: "pending",
      useCharacter: useChar
    });
    parsedCount++;
  }

  // 2. Fallback: Parse simple pipe format (A1|WAYNE|Prompt Text) or A1|Prompt Text (no speaker)
  if (parsedCount === 0) {
    const lines = text.split('\n');
    lines.forEach(line => {
      const parts = line.split('|');
      let sequenceName = "";
      let speaker = "";
      let prompt = "";
      
      if (parts.length === 2) {
        sequenceName = parts[0].trim();
        speaker = defaultQueueAvatarVal;
        prompt = parts[1].trim();
      } else if (parts.length >= 3) {
        sequenceName = parts[0].trim();
        speaker = parts[1].trim().toUpperCase();
        prompt = parts.slice(2).join('|').trim();
      } else {
        return;
      }
      
      let finalSpeaker = speaker;
      let useChar = true;
      if (finalSpeaker === "BROLL" || finalSpeaker === "NONE" || !finalSpeaker) {
        if (defaultQueueAvatarVal === "BROLL") {
          useChar = false;
          finalSpeaker = "BROLL";
        } else {
          useChar = true;
          finalSpeaker = defaultQueueAvatarVal;
        }
      }
      
      queue.push({
        sequenceName,
        speaker: finalSpeaker,
        prompt,
        status: "queued",
        mediaId: null,
        retryCount: 0,
        maxRetries: 2,
        downloadStatus: "pending",
        useCharacter: useChar
      });
      parsedCount++;
    });
  }

  if (parsedCount > 0) {
    log(`Successfully parsed ${parsedCount} prompts into queue.`);
    els.scriptInput.value = "";
    updateQueueUI();
    updateProgressUI();
    saveState();
  } else {
    log("Format unrecognized. Paste Keystone CLIP markup or line-separated pipe entries (e.g. A1|WAYNE|Prompt visual details).", "error");
  }
});

// Update the queue list DOM elements
function updateQueueUI() {
  if (queue.length === 0) {
    els.queueList.innerHTML = '<div class="queue-empty">Queue is empty. Parse a script or enter prompts to begin.</div>';
    return;
  }

  let html = "";
  queue.forEach((item, index) => {
    let icon = "hourglass_empty";
    let iconClass = "queued";
    
    if (item.status === "submitting") {
      icon = "pending";
      iconClass = "submitting";
    } else if (item.status === "rendering") {
      icon = "sync";
      iconClass = "rendering";
    } else if (item.status === "done") {
      icon = "check_circle";
      iconClass = "done";
    } else if (item.status === "failed") {
      icon = "error";
      iconClass = "failed";
    }

    const dlClass = item.downloadStatus;
    const dlLabel = item.downloadStatus.toUpperCase();

    const thumbUrl = getSpeakerThumbnail(item.speaker, item.useCharacter !== false);
    let thumbHtml = "";
    if (thumbUrl) {
      thumbHtml = `<img src="${thumbUrl}" class="queue-item-speaker-thumb" style="width: 24px; height: 24px; border-radius: 50%; object-fit: cover; border: 1px solid rgba(255, 255, 255, 0.15);" />`;
    } else {
      thumbHtml = `<span class="material-symbols-outlined" style="font-size: 20px; color: var(--text-muted);">person</span>`;
    }

    html += `
      <div class="queue-item" style="position: relative;">
        <span class="material-symbols-outlined queue-item-icon ${iconClass}">${icon}</span>
        <div class="queue-item-details" style="margin-left: 2px;">
          <div class="queue-item-meta">
            <span class="queue-item-label">${item.sequenceName}</span>
            <span>Retries: ${item.retryCount}</span>
          </div>
          <div class="queue-item-text" title="${item.prompt}">${item.prompt}</div>
        </div>
        <div style="display: flex; align-items: center; gap: 6px; margin-right: 6px;">
          ${thumbHtml}
          ${buildQueueItemSpeakerSelect(item.speaker, item.useCharacter !== false, index)}
        </div>
        <span class="queue-item-dl ${dlClass}">${dlLabel}</span>
      </div>
    `;
  });
  
  els.queueList.innerHTML = html;

  // Bind event listeners for queue character dropdowns
  document.querySelectorAll(".queue-item-speaker-select").forEach(sel => {
    sel.addEventListener("change", (e) => {
      const idx = parseInt(sel.getAttribute("data-index"));
      if (queue[idx]) {
        const val = sel.value;
        if (val === "BROLL") {
          queue[idx].useCharacter = false;
          queue[idx].speaker = "BROLL";
        } else {
          queue[idx].useCharacter = true;
          queue[idx].speaker = val;
        }
        log(`Set character for ${queue[idx].sequenceName} to: ${val}`);
        updateQueueUI();
        updateProgressUI();
        saveState();
      }
    });
  });
}

// Update the progress bars and metrics panel
function updateProgressUI() {
  const total = queue.length;
  if (total === 0) {
    els.progressBar.style.width = "0%";
    els.progressText.textContent = "0/0 Prompts";
    els.downloadText.textContent = "Downloads: 0/0 completed";
    return;
  }

  const finished = queue.filter(item => item.status === "done" || item.status === "failed").length;
  const downloads = queue.filter(item => item.downloadStatus === "complete").length;
  const retries = queue.reduce((sum, item) => sum + item.retryCount, 0);

  const pct = Math.round((finished / total) * 100);
  els.progressBar.style.width = `${pct}%`;
  els.progressText.textContent = `${finished}/${total} Prompts (${pct}%)`;
  els.downloadText.textContent = `Downloads: ${downloads}/${total} completed`;
  els.retryText.textContent = `Retries: ${retries}`;
}

// Event: Clear Queue
els.clearQueue.addEventListener("click", () => {
  if (isRunning) return;
  queue = [];
  updateQueueUI();
  updateProgressUI();
  saveState();
  log("Queue cleared.");
});

// Event: Mode Change updates available models and fields
els.settingMode.addEventListener("change", () => {
  updateSettingsForm();
  saveState();
});

// Event: Apply and Save settings to page store
els.applySettings.addEventListener("click", async () => {
  const connected = await checkTabConnection();
  if (!connected) {
    log("Cannot apply settings: Open and connect a Google Flow project tab first.", "error");
    return;
  }

  settings.mode = els.settingMode.value;
  settings.model = els.settingModel.value;
  settings.duration = els.settingDuration.value;
  settings.ratio = els.settingRatio.value;
  settings.downloadQuality = els.settingDownload.value;
  settings.imageDownloadQuality = els.settingImageDownload.value;
  settings.projectFolder = els.projectFolderName.value.trim() || "FLOW_RUN";
  settings.backgroundRef = els.backgroundRefSelect.value;
  settings.outputDirectory = els.outputDirectory.value.trim() || '../Desktop/';
  settings.prependOrder = els.prependOrder.checked;

  log("Applying settings to Google Flow store context...");
  const res = await sendToContentScript("SET_SETTINGS", settings);
  
  if (res && res.success) {
    // Notify background script of the active target folder and output directory
    chrome.runtime.sendMessage({ 
      action: "SET_PROJECT_FOLDER", 
      payload: { 
        folderName: settings.projectFolder,
        outputDirectory: settings.outputDirectory
      } 
    });
    log("Settings applied successfully! Store state updated.", "success");
    saveState();
  } else {
    log("Failed to update Flow store: " + (res ? res.error : "API unavailable"), "error");
  }
});

// Refresh dropdown lists and references on demand
els.refreshRefs.addEventListener("click", async () => {
  const connected = await checkTabConnection();
  if (!connected) return;
  await syncProjectDetails();
  log("Project details updated.");
});

// Refresh gallery panel list on demand
els.refreshGallery.addEventListener("click", async () => {
  const connected = await checkTabConnection();
  if (!connected) return;
  await syncProjectDetails();
  log("Gallery media list refreshed.");
});

// Save background ref changes
els.backgroundRefSelect.addEventListener("change", () => {
  backgroundRef = els.backgroundRefSelect.value;
  log(`Global background ref set to: ${backgroundRef ? els.backgroundRefSelect.options[els.backgroundRefSelect.selectedIndex].text : 'None'}`);
  updateThumbPreview("BACKGROUND", backgroundRef);
  saveState();
});

// Main Queue Pacing Loop: 4-and-20 pacing protocol
async function runQueue() {
  const BATCH_SIZE = 4;
  const BATCH_DELAY_MS = 20000;
  
  // Synchronize settings one last time before starting
  await sendToContentScript("SET_SETTINGS", settings);

  while (isRunning && hasQueuedItems()) {
    if (isPaused) {
      els.batchText.textContent = "Paused";
      await sleep(1000);
      continue;
    }

    const batch = getNextBatch(BATCH_SIZE);
    if (batch.length === 0) break;

    log(`Starting batch submission of ${batch.length} prompts...`);
    els.batchText.textContent = `Submitting batch of ${batch.length}...`;

    for (const item of batch) {
      if (!isRunning || isPaused) break;
      
      item.status = "submitting";
      updateQueueUI();
      updateProgressUI();

      // Enforce correct mode and model based on sequence name prefix
      const targetMode = getItemMode(item.sequenceName);
      const targetModel = (targetMode === "VIDEO") ? settings.model : "nano_banana_pro";
      
      console.log(`Auto-switching mode to ${targetMode} (${targetModel}) for ${item.sequenceName}`);
      const setRes = await sendToContentScript("SET_SETTINGS", {
        mode: targetMode,
        model: targetModel,
        duration: settings.duration,
        ratio: settings.ratio,
        outputs: settings.outputs
      });

      // Validate mode actually switched
      if (setRes && setRes.success && setRes.mode) {
        const actualMode = (setRes.mode || "").toUpperCase();
        if (actualMode !== targetMode) {
          log(`⚠️ Mode mismatch for ${item.sequenceName}: wanted ${targetMode}, got ${actualMode}. Retrying...`, "warning");
          await sleep(500);
          await sendToContentScript("SET_SETTINGS", {
            mode: targetMode,
            model: targetModel,
            duration: settings.duration,
            ratio: settings.ratio,
            outputs: settings.outputs
          });
          await sleep(300);
        }
      }

      // Prepare text prompt. Fallback to solid black background if background ref is disabled
      let promptText = item.prompt;
      const bg = els.backgroundRefSelect.value;
      if (!bg) {
        promptText = promptText.replace(/\s*\.\s*No subtitles!/i, "") + ", solid black background. No subtitles!";
      }

      // Check if character toggle is checked for this item
      const useCharacter = item.useCharacter !== false;

      // Determine speaker settings
      const isLikeness = item.speaker === "WAYNE" && useCharacter;
      let characterId = null;
      let likenessId = null;

      if (isLikeness) {
        likenessId = "0278d9a4-7377-08f0-0000-000000000000"; // Wayne's likeness ID
      } else if (useCharacter) {
        // Find matching dynamic character UUID
        const matchedChar = characters.find(c => c.name.toUpperCase() === item.speaker);
        if (matchedChar) {
          characterId = matchedChar.serverId;
        } else {
          log(`Warning: Character name '${item.speaker}' not detected in project. Submitting without character.`, "warning");
        }
      }

      // Collect PER-CHARACTER wardrobe ref + global background ref (only attach character ref if toggled)
      const refImageIds = [];
      if (useCharacter) {
        const speakerWardrobe = characterWardrobeRefs[item.speaker] || "";
        if (speakerWardrobe) refImageIds.push(speakerWardrobe);
      }
      if (bg) refImageIds.push(bg);

      // Submit prompt call
      log(`Submitting ${item.sequenceName}...`);
      const result = await sendToContentScript("SUBMIT_PROMPT", {
        text: promptText,
        characterId: characterId,
        likenessId: likenessId,
        referenceImageIds: refImageIds,
        sequenceName: item.sequenceName
      });

      if (result && result.success && result.mediaId) {
        item.status = "rendering";
        item.mediaId = result.mediaId;
        log(`✅ ${item.sequenceName} submitted rendering! MediaID: ${result.mediaId.substring(0, 8)}`, "success");
      } else {
        item.status = "failed";
        log(`❌ ${item.sequenceName} submission failed: ${result ? result.error : 'Unknown API response'}`, "error");
      }
      
      updateQueueUI();
      updateProgressUI();
      saveState();

      await sleep(1500); // 1.5s separation delay between individual prompt submits
    }

    // Wait 20 seconds before starting the next batch
    if (isRunning && hasQueuedItems()) {
      log("⏳ 4-and-20 Protocol: Pacing queue. Pausing for 20 seconds...");
      for (let i = 20; i > 0; i--) {
        if (!isRunning || isPaused) break;
        els.batchText.textContent = `Batch cooldown: ${i}s...`;
        await sleep(1000);
      }
    }
  }

  if (isRunning && !isPaused) {
    els.batchText.textContent = "Rendering...";
    log("All prompts submitted. Monitoring render outputs...");
    await startCompletionMonitoring();
  }
}

// Queue Helper: Check if queue has items left to prompt
function hasQueuedItems() {
  return queue.some(item => item.status === "queued");
}

// Queue Helper: Get next batch of items
function getNextBatch(size) {
  return queue.filter(item => item.status === "queued").slice(0, size);
}

// Check for rendering active items
function hasRenderingItems() {
  return queue.some(item => item.status === "rendering");
}

// Completion and Automatic Download Monitor Loop
async function startCompletionMonitoring() {
  let consecutiveErrors = 0;

  while (isRunning && (hasRenderingItems() || hasQueuedItems())) {
    if (isPaused) {
      await sleep(2000);
      continue;
    }

    // Check statuses on the Flow page cards
    const res = await sendToContentScript("GET_CARD_STATUS");
    if (!res || !res.success) {
      if (isReloading) {
        // Ignore connection errors while reload is in progress
        await sleep(4000);
        continue;
      }
      consecutiveErrors++;
      if (consecutiveErrors > 15) {
        log("Render monitor connection lost. Pausing run.", "error");
        pauseRun();
        break;
      }
      await sleep(5000);
      continue;
    }
    consecutiveErrors = 0;

    const pageStatuses = res.cards || [];

    for (const item of queue) {
      if (item.status !== "rendering" || !item.mediaId) continue;

      const pageCard = pageStatuses.find(c => c.mediaId === item.mediaId);
      if (!pageCard) continue;

      if (pageCard.status === "done") {
        item.status = "done";
        log(`🎉 ${item.sequenceName} finished rendering! Triggering sequential download...`, "success");
        updateQueueUI();
        updateProgressUI();
        saveState();
        
        // Trigger sequential download automatically
        queueDownload(item);
      } else if (pageCard.status === "failed") {
        log(`⚠️ ${item.sequenceName} reported failed. Waiting 12 seconds before self-healing refresh...`, "info");
        isReloading = true;
        try {
          await sleep(12000); // Wait longer than 10 seconds before resetting it (reload)
          log(`Performing self-healing refresh...`, "info");
          chrome.tabs.reload(currentTabId);
          await sleep(10000); // Wait 10 seconds for reload and connection restoration
        } finally {
          isReloading = false;
        }
        
        // Re-check card status after reload
        const retryRes = await sendToContentScript("GET_CARD_STATUS");
        if (retryRes && retryRes.success) {
          const recheckedCard = (retryRes.cards || []).find(c => c.mediaId === item.mediaId);
          if (recheckedCard && recheckedCard.status === "done") {
            item.status = "done";
            log(`🎉 ${item.sequenceName} recovered and completed after refresh! Triggering download...`, "success");
            updateQueueUI();
            updateProgressUI();
            saveState();
            queueDownload(item);
            continue;
          }
        }
        
        log(`❌ ${item.sequenceName} generation actually failed on server.`, "error");
        if (item.retryCount < item.maxRetries) {
          item.retryCount++;
          item.status = "queued"; // Re-queue item at same position
          item.mediaId = null;
          log(`🔄 Re-queuing ${item.sequenceName} for retry (${item.retryCount}/${item.maxRetries})`, "info");
        } else {
          item.status = "failed";
          log(`❌ ${item.sequenceName} permanently failed after maximum retries.`, "error");
        }
        
        updateQueueUI();
        updateProgressUI();
        saveState();
      } else if (pageCard.status === "rendering") {
        // Update progress percentages in logs occasionally
        console.log(`[Status] ${item.sequenceName}: Rendering ${pageCard.percent}%`);
      }
    }

    // If any items were re-queued, run them in the next batch
    if (hasQueuedItems()) {
      await runQueue();
    }

    await sleep(5000); // Check statuses every 5 seconds
  }

  if (!hasRenderingItems() && !hasQueuedItems() && isRunning) {
    // Wait for any in-flight serialized downloads to finish before checking
    log("All renders complete. Waiting for download queue to drain...");
    let drainWait = 0;
    while (serializedDownloadLock && drainWait < 60) {
      await sleep(1000);
      drainWait++;
    }

    // Download Retry Sweep: find any items that rendered but didn't download
    const failedDownloads = queue.filter(i => i.status === "done" && i.downloadStatus !== "complete" && i.downloadStatus !== "downloading");
    if (failedDownloads.length > 0) {
      log(`⚠️ ${failedDownloads.length} download(s) incomplete. Running retry sweep...`, "warning");
      for (const item of failedDownloads) {
        item.downloadStatus = "pending";
        log(`🔄 Retrying download for ${item.sequenceName}...`, "info");
        await queueDownload(item);
      }
      // Wait for retry downloads to complete
      let retryWait = 0;
      while (serializedDownloadLock && retryWait < 30) {
        await sleep(1000);
        retryWait++;
      }
      // Check if retries fixed it
      const stillFailed = queue.filter(i => i.status === "done" && i.downloadStatus !== "complete");
      if (stillFailed.length > 0) {
        log(`❌ ${stillFailed.length} download(s) still failed after retry: ${stillFailed.map(i => i.sequenceName).join(", ")}`, "error");
      } else {
        log("✅ All retry downloads completed successfully!", "success");
      }
    }

    log("🎉 Job run complete! All items processed.", "success");
    
    // Final summary
    const totalDone = queue.filter(i => i.status === "done").length;
    const totalFailed = queue.filter(i => i.status === "failed").length;
    const totalDownloaded = queue.filter(i => i.downloadStatus === "complete").length;
    log(`📊 Summary: ${totalDone} rendered, ${totalFailed} failed, ${totalDownloaded}/${queue.length} downloaded.`);
    
    stopRun();
  }
}

// Sequential Download Trigger
// Run a single download automation
async function runSingleDownload(item) {
  const mode = getItemMode(item.sequenceName);
  const isVideo = mode === "VIDEO";
  
  // Subfolder mapping:
  // A -> Videos
  // T -> Thumbnails
  // B -> Images (both video B-rolls and image B-rolls go here)
  const name = item.sequenceName.toUpperCase();
  let subfolder = "Images";
  if (name.startsWith("A") || name.startsWith("BV")) {
    subfolder = "Videos";
  } else if (name.startsWith("T")) {
    subfolder = "Thumbnails";
  } else if (name.startsWith("B")) {
    subfolder = "Images";
  }

  const extension = isVideo ? ".mp4" : ".png";
  const resolution = isVideo ? settings.downloadQuality : settings.imageDownloadQuality;

  item.downloadStatus = "downloading";
  updateQueueUI();

  // Prefix sequence order if enabled (e.g. 001_A1)
  let targetFilename = item.sequenceName;
  if (settings.prependOrder !== false) {
    const queueIndex = queue.indexOf(item);
    if (queueIndex !== -1) {
      const paddedIndex = String(queueIndex + 1).padStart(3, '0');
      targetFilename = `${paddedIndex}_${targetFilename}`;
    }
  }

  // 1. Register file expectations with the background script
  const regRes = await chrome.runtime.sendMessage({
    action: "REGISTER_DOWNLOAD",
    payload: {
      sequenceName: targetFilename,
      subfolder: subfolder,
      extension: extension
    }
  });

  if (!regRes || !regRes.queued) {
    log(`Failed to register download path for: ${item.sequenceName}`, "error");
    item.downloadStatus = "pending";
    updateQueueUI();
    return;
  }

  // 2. Trigger the page context click series to initiate download
  log(`Triggering download submenu click for ${item.sequenceName} (${resolution})...`);
  const dlRes = await sendToContentScript("TRIGGER_DOWNLOAD", {
    mediaId: item.mediaId,
    resolution: resolution
  });

  if (!dlRes || !dlRes.success) {
    log(`Download trigger failed for ${item.sequenceName}: ${dlRes ? dlRes.error : "Timeout"}`, "error");
    item.downloadStatus = "pending";
    updateQueueUI();
  }
}

// Queue a download to be run sequentially with a 1-second delay
async function queueDownload(item) {
  if (serializedDownloadQueue.includes(item)) return;
  
  serializedDownloadQueue.push(item);
  if (serializedDownloadLock) return;
  
  serializedDownloadLock = true;
  while (serializedDownloadQueue.length > 0) {
    const nextItem = serializedDownloadQueue.shift();
    await runSingleDownload(nextItem);
    // Wait 1 second before starting next download to ensure name order matching
    await sleep(1000);
  }
  serializedDownloadLock = false;
}

// Listen to messages
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "DOWNLOAD_COMPLETE") {
    console.log("[Sidepanel] Received download complete notification:", msg.payload);
    
    // Try to match by sequenceName extracted from the download path
    let item = null;
    if (msg.payload.filename) {
      const basename = msg.payload.filename.split(/[\/\\]/).pop().replace(/\.[^.]+$/, ''); // e.g. "001_A1"
      // Strip the 001_ prefix to get the raw sequenceName
      const rawName = basename.replace(/^\d{3}_/, '');
      item = queue.find(i => i.downloadStatus === "downloading" && i.sequenceName === rawName);
    }
    
    // Fallback: match first item with "downloading" status (original behavior)
    if (!item) {
      item = queue.find(i => i.downloadStatus === "downloading");
    }
    
    if (item) {
      item.downloadStatus = "complete";
      log(`📥 Download finished & saved: ${item.sequenceName} -> ${msg.payload.filename.split(/[\/\\]/).pop()}`, "success");
      updateQueueUI();
      updateProgressUI();
      saveState();
    }
  }
  if (msg.action === "START_QUEUE") {
    log("▶ Start request received from content script. Automating click on START.");
    const startBtn = document.getElementById("startBtn");
    if (startBtn && !startBtn.disabled) {
      startBtn.click();
      if (sendResponse) sendResponse({ success: true });
    } else {
      if (sendResponse) sendResponse({ success: false, error: "Start button disabled or not found" });
    }
  }
  return true;
});

// UI Control: Start Run
els.startBtn.addEventListener("click", async () => {
  const connected = await checkTabConnection();
  if (!connected) {
    log("Cannot start: No connected Google Flow tab found.", "error");
    return;
  }

  if (queue.length === 0) {
    log("Cannot start: Queue is empty.", "warning");
    return;
  }

  isRunning = true;
  isPaused = false;
  
  els.startBtn.disabled = true;
  els.pauseBtn.disabled = false;
  els.stopBtn.disabled = false;
  
  log("▶ Starting Keystone Flow Commander queue run.");
  runQueue();
});

// UI Control: Pause Run
function pauseRun() {
  isPaused = true;
  els.pauseBtn.innerHTML = '<span class="material-symbols-outlined">play_arrow</span> RESUME';
  els.pauseBtn.className = "btn btn-primary btn-large";
  log("⏸ Run paused by user.");
}

function resumeRun() {
  isPaused = false;
  els.pauseBtn.innerHTML = '<span class="material-symbols-outlined">pause</span> PAUSE';
  els.pauseBtn.className = "btn btn-warning btn-large";
  log("▶ Resuming run queue.");
}

els.pauseBtn.addEventListener("click", () => {
  if (isPaused) {
    resumeRun();
  } else {
    pauseRun();
  }
});

// UI Control: Stop Run
function stopRun() {
  isRunning = false;
  isPaused = false;
  
  els.startBtn.disabled = false;
  els.pauseBtn.disabled = true;
  els.stopBtn.disabled = true;
  els.pauseBtn.innerHTML = '<span class="material-symbols-outlined">pause</span> PAUSE';
  els.pauseBtn.className = "btn btn-warning btn-large";
  els.batchText.textContent = "Stopped";
  
  // Clear background queue to prevent filename alignment mismatches on next runs
  chrome.runtime.sendMessage({ action: "CLEAR_DOWNLOAD_QUEUE" });
  log("⏹ Run stopped. Background download registers cleared.");
}

els.stopBtn.addEventListener("click", () => {
  stopRun();
  log("Run terminated by user.");
});

// Periodically check tab connection status
setInterval(checkTabConnection, 4000);

// Listen to storage changes to update UI dynamically when programmed from page context
chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === 'local') {
    if (changes.queue) {
      queue = changes.queue.newValue || [];
      updateQueueUI();
      updateProgressUI();
    }
    if (changes.settings) {
      settings = { ...settings, ...changes.settings.newValue };
      // Update UI elements
      if (els.settingMode) {
        els.settingMode.value = settings.mode;
        updateSettingsForm();
      }
      if (els.settingModel) els.settingModel.value = settings.model;
      if (els.settingDuration) els.settingDuration.value = settings.duration;
      if (els.settingRatio) els.settingRatio.value = settings.ratio;
      if (els.settingDownload) els.settingDownload.value = settings.downloadQuality;
      if (els.settingImageDownload) els.settingImageDownload.value = settings.imageDownloadQuality;
      if (els.projectFolderName) els.projectFolderName.value = settings.projectFolder;
    }
    if (changes.projectCards) {
      projectCards = changes.projectCards.newValue || [];
      galleryImages = projectCards.filter(c => c.type === 'image' && c.status === 'done');
      updateGalleryUI();
    }
    if (changes.characterWardrobeRefs) {
      characterWardrobeRefs = changes.characterWardrobeRefs.newValue || {};
      updateCharacterUI();
    }
  }
});

// Initialize application on load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadState);
} else {
  loadState();
}
