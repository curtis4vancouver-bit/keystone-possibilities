/**
 * Keystone WebMCP Controller Popup script
 * Interfaces with the background service worker to update UI state and trigger actions.
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const creditsBalance = document.getElementById('credits-balance');
    const btnToggleQueue = document.getElementById('btn-toggle-queue');
    const btnClearQueue = document.getElementById('btn-clear-queue');
    const btnDismissOverlays = document.getElementById('btn-dismiss-overlays');
    const btnAddTask = document.getElementById('btn-add-task');
    
    const inputPrompt = document.getElementById('input-prompt');
    const inputFolder = document.getElementById('input-folder');
    const inputFilename = document.getElementById('input-filename');
    
    const statPending = document.getElementById('stat-pending');
    const statProcessing = document.getElementById('stat-processing');
    const statCompleted = document.getElementById('stat-completed');
    const statFailed = document.getElementById('stat-failed');
    
    const queueCount = document.getElementById('queue-count');
    const queueListContainer = document.getElementById('queue-list-container');

    let isProcessing = false;

    // Load and render status
    function refreshStatus() {
        chrome.runtime.sendMessage({ action: 'get_status' }, (response) => {
            if (chrome.runtime.lastError) {
                console.log("WebMCP Popup Error:", chrome.runtime.lastError.message);
                return;
            }
            if (!response) return;

            // 1. Render Credit Balance
            if (response.credits !== null && response.credits !== undefined) {
                creditsBalance.textContent = `${response.credits} Credits`;
            } else {
                creditsBalance.textContent = `-- Credits`;
            }

            // 2. Render Queue State
            isProcessing = response.isProcessing;
            if (isProcessing) {
                btnToggleQueue.classList.add('btn-danger');
                btnToggleQueue.classList.remove('btn-primary');
                btnToggleQueue.innerHTML = `
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
                    </svg>
                    <span>Pause Queue</span>
                `;
            } else {
                btnToggleQueue.classList.remove('btn-danger');
                btnToggleQueue.classList.add('btn-primary');
                btnToggleQueue.innerHTML = `
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M8 5v14l11-7z"/>
                    </svg>
                    <span>Start Queue</span>
                `;
            }

            // 3. Process Stats Counts
            const queue = response.queue || [];
            let pending = 0;
            let processing = 0;
            let completed = 0;
            let failed = 0;

            queue.forEach(task => {
                if (task.status === 'pending') pending++;
                else if (task.status === 'processing') processing++;
                else if (task.status === 'completed') completed++;
                else if (task.status === 'failed') failed++;
            });

            statPending.textContent = pending;
            statProcessing.textContent = processing;
            statCompleted.textContent = completed;
            statFailed.textContent = failed;

            queueCount.textContent = `${queue.length} tasks`;

            // 4. Render Queue List Items
            renderQueueList(queue);
        });
    }

    // Render tasks list in UI
    function renderQueueList(queue) {
        if (queue.length === 0) {
            queueListContainer.innerHTML = `
                <div style="text-align: center; color: var(--text-muted); font-size: 12px; padding: 12px;">
                    Queue is currently empty.
                </div>
            `;
            return;
        }

        // Display reverse chronological (newest at top or based on order)
        let html = '';
        queue.slice().reverse().forEach(task => {
            const statusDotClass = `status-dot dot-${task.status}`;
            const displayError = task.error ? `<div class="task-file" style="color: var(--danger); font-size: 9px;">Error: ${task.error}</div>` : '';
            
            html += `
                <div class="task-item">
                    <div class="task-info">
                        <div class="task-prompt" title="${task.prompt}">${task.prompt}</div>
                        <div class="task-file" title="${task.projectFolder}/${task.filename}">
                            ${task.projectFolder}/${task.filename}
                        </div>
                        ${displayError}
                    </div>
                    <div class="task-status">
                        <span class="${statusDotClass}"></span>
                        <span>${task.status}</span>
                    </div>
                </div>
            `;
        });
        queueListContainer.innerHTML = html;
    }

    // Event Listeners
    btnToggleQueue.addEventListener('click', () => {
        const action = isProcessing ? 'pause_queue' : 'start_queue';
        chrome.runtime.sendMessage({ action }, () => {
            refreshStatus();
        });
    });

    btnClearQueue.addEventListener('click', () => {
        if (confirm("Are you sure you want to clear the entire task queue?")) {
            chrome.runtime.sendMessage({ action: 'clear_queue' }, () => {
                refreshStatus();
            });
        }
    });

    btnDismissOverlays.addEventListener('click', () => {
        chrome.tabs.query({ url: "*://labs.google/fx/tools/flow*" }, (tabs) => {
            if (tabs.length === 0) {
                alert("Google Flow tab is not open.");
                return;
            }
            chrome.tabs.sendMessage(tabs[0].id, { action: 'dismiss_overlays' }, (response) => {
                console.log("Dismiss overlays response:", response);
            });
        });
    });

    btnAddTask.addEventListener('click', () => {
        const prompt = inputPrompt.value.trim();
        const projectFolder = inputFolder.value.trim();
        let filename = inputFilename.value.trim();

        if (!prompt) {
            alert("Prompt text cannot be empty.");
            return;
        }

        if (!filename) {
            filename = `flow_${Date.now()}.mp4`;
        } else if (!filename.endsWith('.mp4')) {
            filename += '.mp4';
        }

        const task = {
            prompt,
            projectFolder: projectFolder || 'Keystone_Flow',
            filename
        };

        chrome.runtime.sendMessage({ action: 'add_task', task }, (response) => {
            if (response && response.success) {
                inputPrompt.value = '';
                // auto generate a new random suffix filename to prevent collision
                inputFilename.value = '';
                refreshStatus();
            } else {
                alert("Failed to queue task.");
            }
        });
    });

    // Initial load and start periodic refresh
    refreshStatus();
    setInterval(refreshStatus, 1500);
});
