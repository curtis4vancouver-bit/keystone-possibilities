/**
 * Keystone WebMCP Service Worker
 * Manages the background download routing, renaming, and the execution queue.
 */

// Memory Cache for active session variables
let activeDownloadMapping = {}; // url -> { filename, projectFolder }
let activeDownloadIds = new Map(); // downloadId -> taskRef
let isProcessingQueue = false;
let currentActiveTask = null; // Currently executing queue task

// Initialize Storage Defaults on install
chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.local.set({
        tasksQueue: [],
        creditsCache: null,
        isProcessing: false
    }, () => {
        console.log("WebMCP: Background Service Worker initialized storage.");
    });
});

// Helper: send tab message safely with promise wrapper
function sendTabMessage(tabId, message) {
    return new Promise((resolve) => {
        chrome.tabs.sendMessage(tabId, message, (response) => {
            if (chrome.runtime.lastError) {
                console.log("WebMCP: Tab communication error:", chrome.runtime.lastError.message);
                resolve({ error: chrome.runtime.lastError.message });
            } else {
                resolve(response);
            }
        });
    });
}

// Intercept file downloads to rename and move to subfolders
chrome.downloads.onDeterminingFilename.addListener((item, suggest) => {
    console.log("WebMCP: Determining filename for item:", item.url);
    
    // Check if the URL matches a registered download task
    let mapping = activeDownloadMapping[item.url];
    if (!mapping) {
        // Fallback: match by URL containing the resource
        const foundKey = Object.keys(activeDownloadMapping).find(k => item.url.includes(k) || k.includes(item.url));
        if (foundKey) {
            mapping = activeDownloadMapping[foundKey];
            delete activeDownloadMapping[foundKey];
        }
    } else {
        delete activeDownloadMapping[item.url];
    }

    // Fallback: map to active task if queue is processing
    if (!mapping && isProcessingQueue && currentActiveTask) {
        const isFlowAsset = item.url.includes('googleusercontent') || 
                            item.url.includes('getMedia') || 
                            item.url.includes('video') || 
                            item.url.includes('.mp4') || 
                            item.url.includes('.png') || 
                            item.url.includes('.jpeg') || 
                            item.url.includes('.jpg');
                            
        if (isFlowAsset) {
            mapping = {
                filename: currentActiveTask.filename,
                projectFolder: currentActiveTask.projectFolder
            };
            console.log("WebMCP: Fallback mapping active task for download:", currentActiveTask.filename);
        }
    }

    if (mapping) {
        // Link the download ID to the active task ID so onChanged will mark it completed
        if (isProcessingQueue && currentActiveTask) {
            activeDownloadIds.set(item.id, currentActiveTask.id);
            console.log(`WebMCP: Linked download ID ${item.id} to task ID ${currentActiveTask.id}`);
        }

        // Format path relative to default download directory
        const cleanProjectFolder = mapping.projectFolder.replace(/[^a-zA-Z0-9_\-\s]/g, '');
        const cleanFilename = mapping.filename.replace(/[^a-zA-Z0-9_\-\.\s]/g, '');
        const structuredPath = `${cleanProjectFolder}/${cleanFilename}`;
        
        console.log(`WebMCP: Intercepting and renaming file. Saving to: ${structuredPath}`);
        suggest({
            filename: structuredPath,
            conflictAction: 'uniquify'
        });
    } else {
        suggest(); // Proceed with default browser download folder / name
    }
});

// Monitor downloads to mark tasks as completed
chrome.downloads.onChanged.addListener(async (delta) => {
    if (activeDownloadIds.has(delta.id)) {
        const taskId = activeDownloadIds.get(delta.id);
        
        if (delta.state && delta.state.current === 'complete') {
            console.log(`WebMCP: Download completed for task: ${taskId}`);
            activeDownloadIds.delete(delta.id);
            await updateTaskStatus(taskId, 'completed');
            // Continue processing the next item in the queue
            if (isProcessingQueue) {
                setTimeout(processNextQueueTask, 1000);
            }
        } else if (delta.state && delta.state.current === 'interrupted') {
            console.log(`WebMCP: Download interrupted for task: ${taskId}`);
            activeDownloadIds.delete(delta.id);
            await updateTaskStatus(taskId, 'failed', `Download interrupted: ${delta.error?.current || 'unknown'}`);
            if (isProcessingQueue) {
                setTimeout(processNextQueueTask, 1000);
            }
        }
    }
});

// Handle incoming messages from popup.js and content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log("WebMCP: Background worker received message:", request);

    switch (request.action) {
        case 'add_task':
            addTask(request.task).then(sendResponse);
            return true;
        case 'get_queue':
            chrome.storage.local.get(['tasksQueue'], (res) => {
                sendResponse(res.tasksQueue || []);
            });
            return true;
        case 'clear_queue':
            chrome.storage.local.set({ tasksQueue: [] }, () => {
                sendResponse({ success: true });
            });
            return true;
        case 'start_queue':
            isProcessingQueue = true;
            chrome.storage.local.set({ isProcessing: true }, () => {
                processNextQueueTask();
                sendResponse({ success: true, processing: true });
            });
            return true;
        case 'pause_queue':
            isProcessingQueue = false;
            chrome.storage.local.set({ isProcessing: false }, () => {
                sendResponse({ success: true, processing: false });
            });
            return true;
        case 'register_download':
            activeDownloadMapping[request.url] = {
                filename: request.filename,
                projectFolder: request.projectFolder
            };
            sendResponse({ success: true });
            break;
        case 'media_url_intercepted':
            console.log("WebMCP: Intercepted media URL registered:", request.url);
            // Can be used by queue watcher
            break;
        case 'update_credits':
            chrome.storage.local.set({ creditsCache: request.credits });
            sendResponse({ success: true });
            break;
        case 'get_status':
            chrome.storage.local.get(['tasksQueue', 'creditsCache', 'isProcessing'], (res) => {
                sendResponse({
                    queue: res.tasksQueue || [],
                    credits: res.creditsCache,
                    isProcessing: isProcessingQueue || res.isProcessing
                });
            });
            return true;
    }
});

// Add new task to the queue
async function addTask(taskData) {
    return new Promise((resolve) => {
        chrome.storage.local.get(['tasksQueue'], (res) => {
            const queue = res.tasksQueue || [];
            const task = {
                id: Math.random().toString(36).substring(2, 11),
                prompt: taskData.prompt,
                projectFolder: taskData.projectFolder || 'Keystone_Flow',
                filename: taskData.filename || `flow_${Date.now()}.mp4`,
                imageDataUrl: taskData.imageDataUrl || null,
                character: taskData.character || null,
                references: taskData.references || null,
                settings: taskData.settings || null,
                resolution: taskData.resolution || null,
                status: 'pending',
                error: null,
                createdAt: new Date().toISOString()
            };
            queue.push(task);
            chrome.storage.local.set({ tasksQueue: queue }, () => {
                resolve({ success: true, task });
                // If already processing, continue
                if (isProcessingQueue) {
                    processNextQueueTask();
                }
            });
        });
    });
}

// Update status of a specific task
async function updateTaskStatus(taskId, status, errorMsg = null) {
    return new Promise((resolve) => {
        chrome.storage.local.get(['tasksQueue'], (res) => {
            const queue = res.tasksQueue || [];
            const task = queue.find(t => t.id === taskId);
            if (task) {
                task.status = status;
                if (errorMsg) task.error = errorMsg;
                chrome.storage.local.set({ tasksQueue: queue }, () => {
                    resolve(true);
                });
            } else {
                resolve(false);
            }
        });
    });
}

// Queue execution loop
async function processNextQueueTask() {
    if (!isProcessingQueue) {
        console.log("WebMCP: Queue processing paused or stopped.");
        currentActiveTask = null;
        return;
    }

    chrome.storage.local.get(['tasksQueue'], async (res) => {
        const queue = res.tasksQueue || [];
        const nextTask = queue.find(t => t.status === 'pending');

        if (!nextTask) {
            console.log("WebMCP: No pending tasks. Queue finished.");
            isProcessingQueue = false;
            currentActiveTask = null;
            chrome.storage.local.set({ isProcessing: false });
            return;
        }

        console.log("WebMCP: Processing next task:", nextTask);
        currentActiveTask = nextTask;

        // Find active Google Flow tab
        const tabs = await chrome.tabs.query({ url: "*://labs.google/fx/tools/flow*" });
        if (tabs.length === 0) {
            console.log("WebMCP: No Google Flow tab active. Pausing queue.");
            isProcessingQueue = false;
            currentActiveTask = null;
            chrome.storage.local.set({ isProcessing: false });
            await updateTaskStatus(nextTask.id, 'pending', 'Google Flow tab not open');
            return;
        }

        const tabId = tabs[0].id;
        await updateTaskStatus(nextTask.id, 'processing');

        try {
            // Step 1: Dismiss any overlays
            await sendTabMessage(tabId, { action: 'dismiss_overlays' });

            // Step 1B: Apply settings if provided
            if (nextTask.settings) {
                console.log("WebMCP: Applying settings...", nextTask.settings);
                const settingsRes = await sendTabMessage(tabId, {
                    action: 'apply_settings',
                    config: nextTask.settings
                });
                if (!settingsRes || settingsRes.error) {
                    throw new Error("Applying settings failed: " + (settingsRes?.error || "unknown"));
                }
                await new Promise(r => setTimeout(r, 500));
            }

            // Step 1C: Attach character/avatar if provided
            if (nextTask.character) {
                console.log("WebMCP: Attaching character/avatar...", nextTask.character);
                const charRes = await sendTabMessage(tabId, {
                    action: 'attach_avatar_or_character',
                    type: nextTask.character.type,
                    name: nextTask.character.name
                });
                if (!charRes || charRes.error) {
                    throw new Error("Attaching character failed: " + (charRes?.error || "unknown"));
                }
                await new Promise(r => setTimeout(r, 500));
            }

            // Step 1D: Attach card references by name if provided
            if (nextTask.references && Array.isArray(nextTask.references)) {
                for (const refName of nextTask.references) {
                    console.log("WebMCP: Attaching card reference:", refName);
                    const refRes = await sendTabMessage(tabId, {
                        action: 'attach_card_reference_by_name',
                        cardName: refName
                    });
                    if (!refRes || refRes.error) {
                        throw new Error(`Attaching reference '${refName}' failed: ` + (refRes?.error || "unknown"));
                    }
                    await new Promise(r => setTimeout(r, 500));
                }
            }

            // Step 2: Upload character reference image if provided
            if (nextTask.imageDataUrl) {
                console.log("WebMCP: Uploading reference image...");
                const uploadRes = await sendTabMessage(tabId, {
                    action: 'upload_reference',
                    imageDataUrl: nextTask.imageDataUrl
                });
                if (!uploadRes || uploadRes.error) {
                    throw new Error("Reference image upload failed: " + (uploadRes?.error || "unknown"));
                }
                // Sleep brief moment for drop processing
                await new Promise(r => setTimeout(r, 1000));
            }

            // Step 3: Inject prompt text
            console.log("WebMCP: Injecting prompt text...");
            const fillRes = await sendTabMessage(tabId, {
                action: 'fill_prompt',
                text: nextTask.prompt
            });
            if (!fillRes || fillRes.error) {
                throw new Error("Prompt injection failed: " + (fillRes?.error || "unknown"));
            }

            // Step 4: Click generate
            console.log("WebMCP: Clicking generate...");
            const clickRes = await sendTabMessage(tabId, { action: 'click_generate' });
            if (!clickRes || clickRes.error) {
                throw new Error("Click generate failed: " + (clickRes?.error || "unknown"));
            }

            // Step 5: Poll for rendering completion (Wait Strategy)
            console.log("WebMCP: Generation submitted. Polling for rendering completion...");
            let generationFinished = false;
            const startTime = Date.now();
            const timeoutMs = 8 * 60 * 1000; // 8 minutes max rendering time
            let initialLinksCount = 0;

            const initLinksRes = await sendTabMessage(tabId, { action: 'get_download_links' });
            if (initLinksRes && !initLinksRes.error && Array.isArray(initLinksRes)) {
                initialLinksCount = initLinksRes.length;
            }

            while (Date.now() - startTime < timeoutMs) {
                // Sleep 15 seconds between polls (4-and-20 protocol compliance)
                await new Promise(r => setTimeout(r, 15000));

                if (!isProcessingQueue) {
                    throw new Error("Queue was paused during generation");
                }

                // Check status
                const statusRes = await sendTabMessage(tabId, { action: 'get_queue_status' });
                let activeCount = 0;
                if (statusRes && !statusRes.error) {
                    activeCount = statusRes.activeCount;
                    console.log(`WebMCP: Active generations: ${statusRes.activeCount}, Failed: ${statusRes.failedCount}`);
                }

                // Query download links
                const linksRes = await sendTabMessage(tabId, { action: 'get_download_links' });
                if (linksRes && !linksRes.error && Array.isArray(linksRes)) {
                    if (linksRes.length > initialLinksCount) {
                        generationFinished = true;
                        break;
                    }
                }

                // Fallback if active count drops to 0
                if (activeCount === 0 && (Date.now() - startTime > 20000)) {
                    await new Promise(r => setTimeout(r, 2000));
                    const doubleCheckLinks = await sendTabMessage(tabId, { action: 'get_download_links' });
                    if (doubleCheckLinks && Array.isArray(doubleCheckLinks) && doubleCheckLinks.length > initialLinksCount) {
                        generationFinished = true;
                        break;
                    }
                }
            }

            if (!generationFinished) {
                throw new Error("Video generation timed out or failed to produce download URL");
            }

            // Step 6: Trigger download of the completed asset (always card 0 because it's the newest)
            const targetResolution = nextTask.resolution || (nextTask.settings && nextTask.settings.mode === 'image' ? '2K' : '1080p');
            console.log(`WebMCP: Triggering download of latest asset with resolution: ${targetResolution}`);

            const downloadRes = await sendTabMessage(tabId, {
                action: 'download_asset',
                cardIndex: 0,
                resolution: targetResolution
            });

            if (!downloadRes || downloadRes.error) {
                throw new Error("Failed to trigger download: " + (downloadRes?.error || "unknown"));
            }

            // Note: onChanged will monitor the download completion and trigger processNextQueueTask

        } catch (err) {
            console.log("WebMCP: Task failed with error:", err.message);
            currentActiveTask = null;
            await updateTaskStatus(nextTask.id, 'failed', err.message);
            // Attempt to continue the queue
            if (isProcessingQueue) {
                setTimeout(processNextQueueTask, 1500);
            }
        }
    });
}
