// background.js for Keystone Flow Commander

// Initialize storage settings
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({
    downloadQueue: [],
    projectFolder: "FLOW_RUN_DEFAULT"
  });
});

// Configure Side Panel behavior to open on action click
chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true }).catch((err) => {
  console.error("Failed to set panel behavior:", err);
});

// Handle incoming messages
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "OPEN_SIDEPANEL") {
    chrome.sidePanel.open({ tabId: sender.tab.id })
      .then(() => sendResponse({ success: true }))
      .catch((err) => sendResponse({ success: false, error: err.message }));
    return true;
  }

  if (msg.action === "RELOAD_EXTENSION") {
    console.log("[Background] Reloading extension via API request...");
    chrome.runtime.reload();
    sendResponse({ success: true });
    return true;
  }

  if (msg.action === "REGISTER_DOWNLOAD") {
    chrome.storage.local.get({ downloadQueue: [] }, (data) => {
      const queue = data.downloadQueue;
      queue.push(msg.payload);
      chrome.storage.local.set({ downloadQueue: queue }, () => {
        console.log(`[Background] Registered expected download for: ${msg.payload.sequenceName}`);
        sendResponse({ queued: true, queueLength: queue.length });
      });
    });
    return true; // Keep message channel open for async response
  }

  if (msg.action === "SET_PROJECT_FOLDER") {
    const updateObj = { projectFolder: msg.payload.folderName };
    if (msg.payload.downloadBaseFolder) updateObj.downloadBaseFolder = msg.payload.downloadBaseFolder;
    if (msg.payload.customDownloadPath !== undefined) updateObj.customDownloadPath = msg.payload.customDownloadPath;
    
    chrome.storage.local.set(updateObj, () => {
      console.log(`[Background] Project folder set to: ${msg.payload.folderName}`);
      sendResponse({ set: true });
    });
    return true;
  }

  if (msg.action === "CLEAR_DOWNLOAD_QUEUE") {
    chrome.storage.local.set({ downloadQueue: [] }, () => {
      console.log("[Background] Cleared download queue");
      sendResponse({ cleared: true });
    });
    return true;
  }
});

// Intercept downloads and rename them
chrome.downloads.onDeterminingFilename.addListener((downloadItem, suggest) => {
  // Verify download is originating from Google Flow or Google's media hosting domains
  const isGoogleFlow = downloadItem.url.includes("labs.google") ||
                       downloadItem.url.includes("lh3.googleusercontent.com") ||
                       downloadItem.url.includes("video-downloads") ||
                       downloadItem.url.includes("googleusercontent");

  if (!isGoogleFlow) {
    // Let other downloads pass through unmodified
    suggest();
    return;
  }

  chrome.storage.local.get({ 
    downloadQueue: [], 
    projectFolder: "FLOW_RUN_DEFAULT",
    downloadBaseFolder: "Desktop",
    customDownloadPath: ""
  }, (data) => {
    const queue = data.downloadQueue;
    const folder = data.projectFolder;
    const baseFolder = data.downloadBaseFolder;
    const customPath = data.customDownloadPath;

    if (queue.length === 0) {
      console.warn("[Background] Intercepted Google Flow download but queue is empty!");
      suggest(); // Proceed with default naming to prevent hanging
      return;
    }

    // Dequeue the next expected download (FIFO)
    const entry = queue.shift();
    
    // Save updated queue back to storage
    chrome.storage.local.set({ downloadQueue: queue }, () => {
      // Build absolute target path relative to Chrome's default Downloads folder.
      // Chrome sandbox allows relative paths to write into parent/sibling folders.
      let prefix = "../Desktop"; // Default base folder
      if (baseFolder === "Downloads") {
        prefix = ".";
      } else if (baseFolder === "Documents") {
        prefix = "../Documents";
      } else if (baseFolder === "Custom" && customPath) {
        prefix = customPath;
      }

      // Ensure prefix ends with a slash if it doesn't already, or is simple dot
      if (prefix && prefix !== "." && !prefix.endsWith("/")) {
        prefix += "/";
      } else if (prefix === ".") {
        prefix = "";
      }

      const filename = `${prefix}${folder}/${entry.subfolder}/${entry.sequenceName}${entry.extension}`;
      console.log(`[Background] Renaming download ${downloadItem.id} to: ${filename}`);

      suggest({
        filename: filename,
        conflictAction: "overwrite"
      });
    });
  });

  return true; // Keep channel open for async suggest
});

// Monitor download status changes
chrome.downloads.onChanged.addListener((delta) => {
  if (delta.state && delta.state.current === "complete") {
    // Retrieve details to notify the UI
    chrome.downloads.search({ id: delta.id }, (results) => {
      if (results && results.length > 0) {
        const item = results[0];
        console.log(`[Background] Download completed: ${item.filename}`);
        chrome.runtime.sendMessage({
          action: "DOWNLOAD_COMPLETE",
          payload: {
            id: delta.id,
            filename: item.filename,
            url: item.url
          }
        });
      }
    });
  }
});
