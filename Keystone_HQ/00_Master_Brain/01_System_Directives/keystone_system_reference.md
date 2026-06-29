# Keystone Sovereign System Reference Manual
> Technical Architecture Guide for Ada, Vector Brain, and Obsidian Ecosystem

---

## 1. AIDA (Ada) Framework & Control Center
The **A.I.D.A. (Ada)** application serves as the primary desktop interface and control console for Wayne Stevenson's dual-brand operations.

### Backend Architecture
*   **Engine:** Built using `FastAPI` (Python) serving a REST API and WebSockets on `localhost` port 8000.
*   **Startup Sequence:** Automates the instantiation of system managers and starts the background **Voice Bridge** connection if it is not currently active.
*   **Managers:**
    *   **ChatManager:** Orchestrates user interactions, manages the state of individual chats, maps user prompts to appropriate model configurations (Flash Lite, Flash, Pro), and records conversations.
    *   **SystemMonitor:** Interfaces with local system APIs to track system metrics (CPU, RAM, disk space, Docker container status).
    *   **AppLauncher:** Provides programmatic execution hooks to start/stop relevant software packages (Docker engines, OBS, DaVinci Resolve, Chrome).
    *   **VoiceBridgeAPI:** Creates a text-to-speech (TTS) and speech-to-text (STT) pipeline to read from `voice_outbox.txt` and convert spoken input to text queries.

---

## 2. Qdrant Unified Vector Brain
The long-term cognitive memory of the Keystone empire is anchored by a local **Qdrant Vector Database** instance.

### System Configuration
*   **Primary Database:** Runs locally inside a Docker container bound to `localhost:6333`.
*   **Backup / Clone:** Runs a secondary container on `localhost:7333` for data redundancy.
*   **Collection:** Uses a single unified collection named `keystone_unified`.
*   **Embedding Model:** Local embeddings are generated using `fastembed` with the `BAAI/bge-small-en-v1.5` model.
*   **Total Capacity:** Currently holds **15,370 vectors** representing operational rules, historical logs, research digests, and system guidelines.

### Routing and Filtering
*   **Tenant Segmentation:** Payloads are tagged with a `tenant_id` namespace filter to segment retrieval context and prevent cross-brand hallucinations. Key namespaces include:
    *   `webmaster`: Technical SEO data, hosting logs, and link-building strategies.
    *   `local_seo`: Map pack optimizations and directory rankings.
    *   `content_pipeline`: Scripts, production timelines, B-roll tags, and publishing records.
    *   `music`: ISRC cataloging, track data, and music release templates.
    *   `protocol_brand`: Scientific research, peptide dosing tables, and health protocols.
*   **Hybrid Search:** Restructured to support dense vector similarity queries combined with sparse token keyword matches (BM25) to prioritize exact operational playbooks over loose semantic research papers.

---

## 3. Obsidian Knowledge Graph & Vault
Obsidian functions as the human-readable visual interface to the Master Brain directory (`00_Master_Brain`).

### Vault Organization
*   **Central Hub:** The `INDEX.md` node serves as the entry point of the neural map.
*   **Relationships:** Entities are linked using standard markdown links (e.g., `[[AGENTS]]`, `[[DIRECTIVES]]`, `[[STATE]]`).
*   **Synchronizers:**
    *   **Error Prevention:** The `.learnings/correction_journal.json` captures all runtime execution fixes.
    *   **Drive Sync:** The `sync_brain_to_drive.py` script automatically packages updates to the correction journal, daily digests, and proposals, formatting them to sync with Wayne's Google Docs and NotebookLM systems.

---

## 4. Operational Fleet
A fleet of 13 active, specialized agents resides under `Agent_Fleet/`, each running with isolated context folders, inbox message queues, and specific skill directives to automate tasks from construction planning to music publishing.