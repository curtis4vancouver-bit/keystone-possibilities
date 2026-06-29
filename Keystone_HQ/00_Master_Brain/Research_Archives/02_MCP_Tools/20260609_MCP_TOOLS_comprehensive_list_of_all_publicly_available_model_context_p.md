# Deep Research: Comprehensive list of all publicly available Model Context Protocol (MCP) servers as of June 2026. Include servers for: browser automation, file management, database access, API integration, code execution, image generation, video editing, social media management, email, calendar, project management. For each, list the server name, available tools, and GitHub repo.
**Domain:** Mcp Tools
**Researched:** 2026-06-09 23:07
**Source:** Google Deep Research via Chrome Automation

---

Comprehensive Analysis of Publicly Available Model Context Protocol (MCP) Servers (June 2026)

The emergence of the Model Context Protocol (MCP) has catalyzed a fundamental paradigm shift in artificial intelligence architecture, transitioning Large Language Models (LLMs) from isolated reasoning engines into highly interconnected, agentic systems capable of executing complex workflows. By establishing a standardized, open protocol for seamless integration between AI applications and external data sources, MCP provides a uniform layer for exposing local and remote resources through standardized server implementations. Originally developed and spearheaded by Anthropic, the protocol has since transitioned into an open-source project hosted by The Linux Foundation, signaling its widespread adoption as an industry standard. As of June 2026, the ecosystem has matured significantly, evolving from a handful of reference implementations into a massive, decentralized registry encompassing hundreds of specialized servers.   

This report systematically categorizes, analyzes, and details the publicly available MCP servers currently driving advanced AI workflows. By examining the available tools, underlying architectures, and GitHub repositories across eleven critical domains—browser automation, file management, database access, API integration, code execution, image generation, video editing, social media management, email, calendar, and project management—this analysis highlights the operational mechanics and strategic implications of this rapidly expanding technological framework.

1. Architectural Foundations and the MCP Ecosystem

Before dissecting individual domains, it is critical to understand the infrastructure that governs the MCP ecosystem. The official Model Context Protocol GitHub organization acts as the central hub for protocol specification, core Software Development Kits (SDKs), and reference server implementations. To facilitate broad adoption across disparate engineering environments, official SDKs are now actively maintained in a multitude of languages, including TypeScript, Python, Java, Kotlin, C#, Go, PHP, Ruby, Rust, and Swift. This linguistic diversity ensures that organizations can deploy MCP servers within their existing infrastructure without requiring extensive re-engineering.   

The proliferation of community and enterprise servers necessitated the creation of the MCP Registry, a centralized metadata repository backed by major contributors including Anthropic, GitHub, PulseMCP, and Microsoft. Operating akin to a package manager or app store, the registry allows clients to discover servers while enforcing strict namespace validation. For example, publishing under a specific namespace like io.github.username/server requires verifiable proof of ownership of the associated GitHub account or domain via Domain Name System (DNS) or Hypertext Transfer Protocol (HTTP) challenges. This verification infrastructure is paramount for security, as MCP servers inherently grant AI models access to sensitive local and remote environments.   

Communication between the AI client (such as Claude Desktop, Cursor, or specialized integrated development environments) and the MCP server typically occurs via two primary transport layers: Standard Input/Output (stdio) for local execution, and Server-Sent Events (SSE) for remote, cloud-hosted capabilities. The local stdio transport is heavily utilized for operations requiring deep host-machine access, such as local file system manipulation or localized database queries, whereas the SSE transport enables lightweight clients to offload intensive tasks—such as browser rendering or code execution—to secure, isolated cloud sandboxes.   

2. Browser Automation and Web Scraping

Browser automation via MCP represents a critical capability, allowing LLMs to break out of their static training data and interact dynamically with the live web. This category has seen rapid innovation, diverging into two distinct methodological approaches: Document Object Model (DOM) vision interaction and structured accessibility snapshots. The shift toward accessibility snapshots represents a maturation in the field, moving away from computationally expensive and occasionally error-prone vision models toward deterministic, token-efficient text representations of web interfaces.

The official Microsoft Playwright MCP server has emerged as a dominant force in this category. Rather than relying on visual screenshots, this server enables LLMs to interact with web pages through structured accessibility trees, bypassing the need for visually-tuned models entirely. This provides a highly reliable methodology for navigating URLs, clicking elements, filling forms, and managing browser dialogs, making it highly effective for exploratory automation, self-healing test generation, and autonomous workflows that require persistent browser states.   

Conversely, cloud-based solutions like Browserbase provide a hosted execution environment that handles the complexities of headless browser management, anti-bot mitigation, and session persistence without straining the user's local hardware. Powered by frameworks like Stagehand, Browserbase allows models to execute complex multi-step interactions through simplified commands, delegating the low-level DOM manipulation to the cloud infrastructure. Other robust implementations include the Puppeteer MCP, which allows both local and remote browser connections, and Firecrawl, which adds powerful web scraping capabilities specifically optimized for LLM ingestion.   

For simpler use cases, the official reference Fetch server provides direct web content extraction, converting HyperText Markup Language (HTML) layouts directly into Markdown for easier reading by the AI. However, these simpler servers require careful network security configurations, as they can inadvertently expose internal network addresses, presenting Server-Side Request Forgery risks if strict URL validation parameters are not enforced by the developer.   

Server Name & Description	Available Tools	GitHub Repository


Playwright MCP (Microsoft)




Structured accessibility snapshots for deterministic browser control without vision models.

	

browser_navigate, browser_click, browser_type, browser_take_screenshot, browser_select_option, browser_file_upload, browser_tab_list, browser_handle_dialog 

	

github.com/microsoft/playwright-mcp 




Browserbase MCP




Cloud-hosted browser automation utilizing Stagehand for complex interactions.

	

start, end, navigate, act, observe, extract 

	

github.com/browserbase/mcp-server-browserbase 




Puppeteer MCP




Traditional browser automation supporting local/remote Chrome execution.

	

Navigation, screenshot capture, JavaScript execution 

	

github.com/modelcontextprotocol/servers/tree/main/src/puppeteer 




Fetch MCP (Official)




Direct web content fetching and HTML-to-Markdown conversion.

	

fetch (with url, max_length, start_index, raw parameters) 

	

github.com/modelcontextprotocol/servers/tree/main/src/fetch 




Firecrawl MCP




Advanced web scraping and search capabilities optimized for LLM context.

	

Web scraping, crawling, and data extraction 

	

github.com/mendableai/firecrawl-mcp-server 




Search1API




Unified API for search, crawling, and sitemap extraction.

	

Search, crawling, sitemap processing 

	

github.com/fatwang2/search1api-mcp 




Chrome DevTools MCP




Official server for controlling and inspecting a live Chrome browser.

	

Live DOM inspection, network monitoring, performance profiling 

	

Maintained officially; indexed in modelcontextprotocol registries 




Browser Use MCP




Packaged automation including a Dockerfile for Chromium in Docker.

	

Autonomous web tasks, navigation, content extraction 

	

github.com/co-browser/browser-use-mcp-server 




Web Eval Agent




Autonomous debugging of web applications using browser-use [[AGENTS|agents]].

	

Web app evaluation, autonomous debugging 

	

github.com/Operative-Sh/web-eval-agent 

  
3. File Management and Local Storage

The ability for an AI agent to read, write, organize, and search local file systems is foundational to its utility in software engineering, data analysis, and document management. The reference Filesystem MCP server acts as a highly secure bridge, translating an AI's natural language requests into concrete, low-level file operations.   

Due to the inherent risks of granting an AI read and write access to a host machine, the official filesystem server relies on strict, configurable root directories passed as arguments during the initialization phase. This ensures the model cannot traverse outside of authorized workspaces or access critical system files. The capabilities of this server have evolved beyond simple whole-file overwriting; advanced tools like edit_file allow for precise, targeted line-based updates within a document. This targeted editing solves significant context-window inefficiencies, as the LLM is no longer required to output the entire contents of a large file merely to change a single function or paragraph.   

Beyond local disks, the ecosystem has rapidly expanded to interface with cloud storage systems and specialized knowledge vaults. The Google Drive MCP enables comprehensive searching, listing, and reading of cloud documents directly from the chat interface. Similarly, specialized servers like the Obsidian MCP permit AI [[AGENTS|agents]] to query and retrieve semantic context directly from local markdown-based personal knowledge vaults, turning a user's disparate notes into a cohesive, queryable memory bank for the agent.   

Server Name & Description	Available Tools	GitHub Repository


Filesystem (Official)




Secure, restricted local file operations with line-based editing.

	

read_file, write_file, edit_file, list_directory, create_directory, move_file, search_files, get_file_info, list_allowed_directories 

	

github.com/modelcontextprotocol/servers/tree/main/src/filesystem 




Google Drive MCP




Cloud file access, organization, and search capabilities.

	

drive_search_files, drive_get_file, drive_create_doc, drive_update_file, drive_move_file, drive_delete_file 

	

github.com/modelcontextprotocol/servers/tree/main/src/gdrive 




Obsidian MCP




Markdown vault semantic search and retrieval.

	

Read and search Obsidian vault markdown notes 

	

github.com/smithery-ai/mcp-obsidian 




Everything Search




Lightning-fast Windows file search integration.

	

File system search powered by the Everything SDK 

	

github.com/modelcontextprotocol/servers (Reference section) 




llm-context




Share code context via clipboard or MCP.

	

Context sharing, code retrieval 

	

github.com/modelcontextprotocol/servers (Community section) 

  
4. Database Access and Vector Storage

Connecting AI models directly to enterprise data stores historically required building fragile, bespoke application programming interfaces. The introduction of Database MCP servers standardizes this interaction, allowing LLMs to safely inspect schemas, execute complex queries, and synthesize analytical reports directly from raw structured data.   

The most prominent and robust framework in this domain is the Google MCP Toolbox for Databases. This server utilizes a sophisticated dual-tier architecture that balances developer flexibility with enterprise-grade security. At build-time, it provides prebuilt tools for immediate data interaction, mapping standard commands across a vast array of supported databases—including AlloyDB, BigQuery, PostgreSQL, MySQL, SQL Server, Spanner, and MongoDB. At run-time, it functions as a highly secure framework where system administrators define strict configurations via tools.yaml manifests. This completely restricts the LLM from executing arbitrary, potentially destructive SQL commands, instead forcing it to use predefined, parameterized semantic searches and natural-language-to-SQL logic.   

Other notable implementations focus on high-performance execution and specific database architectures. For instance, several Rust-based connectors offer zero-runtime dependencies for MySQL and SQL Server, while Go-based high-performance servers provide built-in transaction management and schema exploration. The SQLite MCP provides localized database interaction heavily intertwined with business intelligence capabilities, enabling the server to automatically generate business insight memos directly from queried local data. Furthermore, vector databases like Qdrant and Elasticsearch are heavily represented, providing semantic memory capabilities that allow [[AGENTS|agents]] to recall historical context and perform complex vector searches across disparate chat sessions.   

Server Name & Description	Available Tools	GitHub Repository


Google MCP Toolbox for Databases




Multi-database support with prebuilt exploratory and custom parameterized run-time tools.

	

list_tables, execute_sql, custom parameterized SQL execution schemas, skills-generation 

	

github.com/googleapis/mcp-toolbox 




PostgreSQL (Official)




Read-only database access and schema inspection.

	

Schema introspection, safe read-only SQL execution 

	

github.com/modelcontextprotocol/servers/tree/main/src/postgres 




SQLite




Local DB interaction and business intelligence.

	

SQL query execution, automated business memo generation 

	

github.com/modelcontextprotocol/servers/tree/main/src/sqlite 




Redis




In-memory data store access.

	

Key-value retrieval and standard store interaction tools 

	

github.com/modelcontextprotocol/servers/tree/main/src/redis 




Neon MCP




Serverless Postgres platform interaction.

	

Serverless database querying and schema management 

	

github.com/neondatabase/mcp-server-neon 




Qdrant MCP




Vector database integration for semantic memory.

	

Semantic memory storage and vector search 

	

github.com/qdrant/mcp-server-qdrant 




Elasticsearch




Connecting to ES data indices.

	

Search queries, mappings, ES|QL execution, shard information retrieval 

	

Maintained by Elastic 




MongoDB MCP Server




Full-featured MongoDB Database integration.

	

Schema exploration, document retrieval, query execution 

	

github.com/furey/mongodb-lens 




High-Performance DB Connectors (Rust/Go)




Zero-dependency connections for MS SQL, MySQL, and MariaDB.

	

SSH tunneling, DDL/DML execution, query building 

	

github.com/daedalus repositories, github.com/FreePeak/db-mcp-server 




Convex Backend MCP




Convex database integration.

	

Introspect tables, functions, run one-off queries 

	

github.com/get-convex/convex-backend 




GreptimeDB MCP




Time-series database querying.

	

Time-series data retrieval and querying 

	

github.com/GreptimeTeam/greptimedb-mcp-server 

  
5. API Integration and System Monitoring

Integrating third-party Software as a Service (SaaS) platforms and system monitoring tools directly into the reasoning loop of an LLM severely reduces context switching for developers. MCP servers in this domain act as highly specialized middleware, translating complex Representational [[STATE|State]] Transfer (REST) and GraphQL APIs into easily consumable tool structures that the agent can autonomously trigger.

A prime example of this workflow optimization is the Sentry MCP server. Designed specifically for human-in-the-loop coding [[AGENTS|agents]] like Cursor or Claude Code, this remote MCP server pulls error tracking, issue details, and performance traces directly into the integrated development environment. The server exposes sophisticated tools like analyze_issue_with_seer, which triggers an auxiliary AI analysis of stack traces to pinpoint root causes, allowing the primary coding agent to immediately ingest the findings and generate a patch for the developer to review.   

Other crucial infrastructure integrations include Cloudflare, which permits [[AGENTS|agents]] to interrogate and configure edge resources like Workers, Key-Value stores, and R2 data buckets natively. To manage raw telemetry, the Axiom MCP allows models to query and analyze logs, traces, and event data using natural language, which the server translates into Axiom Processing Language under the hood. Communication APIs are also heavily represented, with the Slack MCP standardizing interactions to allow models to list channels, retrieve history, and send thread replies on behalf of the user, facilitating automated status reporting and alert triaging.   

Furthermore, specialized knowledge retrieval servers like the AWS Knowledge Base Retrieval implementation allow [[AGENTS|agents]] to pull proprietary corporate data using the Bedrock Agent Runtime, while tools like the QA Sphere MCP enable LLMs to interact directly with test cases to discover and summarize testing workflows within the IDE.   

Server Name & Description	Available Tools	GitHub Repository


Sentry MCP




Error monitoring, stack trace retrieval, and debugging logic.

	

get_sentry_resource, analyze_issue_with_seer, error fetching 

	

github.com/getsentry/sentry-mcp 




Cloudflare MCP




Edge resource deployment and platform management.

	

Manage Workers, KV, R2, and D1 resources 

	

github.com/cloudflare/mcp-server-cloudflare 




Slack (Official)




Workspace communication and channel management.

	

slack_list_channels, slack_create_channel, slack_send_message, slack_send_thread_reply, slack_get_channel_history 

	

github.com/modelcontextprotocol/servers/tree/main/src/slack 




Axiom MCP




Log and trace analysis via natural language.

	

Natural language querying via Axiom Processing Language (APL) 

	

github.com/axiomhq/mcp-server-axiom 




AWS KB Retrieval




Retrieval from AWS Knowledge Base.

	

Document retrieval using Bedrock Agent Runtime 

	

github.com/modelcontextprotocol/servers/tree/main/src/aws-kb-retrieval-server 




Brave Search




Web and local search integration.

	

Web search, local search execution 

	

github.com/modelcontextprotocol/servers/tree/main/src/brave-search 




PBS API MCP




Access to the Australian Pharmaceutical Benefits Scheme.

	

Retrieve medicine information, pricing, and availability 

	

github.com/matthewdcage/pbs-mcp-server 




QA Sphere MCP




Direct interaction with QA test cases.

	

Discover, summarize, and query QA Sphere test cases 

	

github.com/Hypersequent/qasphere-mcp 




Home Assistant MCP




Access data and control smart home devices.

	

Device control (lights, switches, thermostats), [[STATE|state]] retrieval 

	

github.com/tevonsb/homeassistant-mcp 

  
6. Code Execution and Developer Workflows

While standard filesystem tools allow LLMs to write code to a disk, Code Execution MCP servers grant them the critical, dynamic ability to run and test that code. Because executing arbitrary code generated by an AI on a local user machine presents an extreme security risk, this domain relies heavily on hardware virtualization and secure cloud sandboxing protocols.

The E2B MCP server leads this category by a significant margin. It provides secure, ephemeral cloud development environments for AI [[AGENTS|agents]], executing untrusted Python or JavaScript code inside completely isolated containers. Through a unified tool interface like run_code, an LLM can write a script, push it to the E2B sandbox, automatically install necessary dependencies via install-commands (such as pip install or npm install), execute the code, and instantly read the standard output or runtime errors. This creates a powerful, closed feedback loop where the model can autonomously debug its own programmatic outputs without ever jeopardizing the integrity of the user's local operating system.   

In tandem with raw execution, the management of developer workflows is handled through sophisticated GitHub and GitLab MCP servers. These tools allow [[AGENTS|agents]] to search across repositories, manage branches, read specific file contexts, and manipulate pull requests and issues. This effectively turns the LLM into an active, autonomous collaborator within the version control system, capable of reviewing code and merging approved changes. To manage local infrastructure, Kubernetes and Docker servers allow [[AGENTS|agents]] to execute container management, monitor pod health, and analyze network stacks autonomously directly from the chat interface. Furthermore, highly specialized servers like ghidraMCP expose reverse-engineering toolkits, allowing the LLM to autonomously analyze compiled application binaries.   

Server Name & Description	Available Tools	GitHub Repository


E2B MCP Server




Secure cloud-based code execution sandbox for JS and Python.

	

run_code, package installation commands, multi-shot execution workflows 

	

github.com/e2b-dev/mcp-server 




GitHub (Official)




Repository, issue, and pull request automation.

	

github_list_repos, github_create_branch, github_create_pr, github_search_issues, github_merge_pr, file operations 

	

github.com/modelcontextprotocol/servers/tree/main/src/github 




GitLab (Official)




GitLab API project and code management.

	

Manage projects, merge requests, releases, and files 

	

github.com/modelcontextprotocol/servers/tree/main/src/gitlab 




Docker MCP




Seamless container and compose stack management.

	

Manage containers, images, volumes, and networks 

	

github.com/ckreiling/mcp-server-docker 




Kubernetes MCP




Cluster orchestration and management.

	

Manage pods, deployments, and services 

	

github.com/Flux159/mcp-server-kubernetes 




Ghidra MCP




Autonomous application reverse engineering.

	

Exposes core Ghidra functionality for binary analysis 

	

github.com/LaurieWired/GhidraMCP 

  
7. Multimedia: Image Generation, Video Editing, and Design

The integration of multimedia capabilities via MCP pushes LLM utility beyond traditional text and data processing into complex, multi-modal creative workflows. These servers interface with specialized generative APIs, 3D engines, and local creative software.

For image and video generation, servers like Runware and EverArt connect the LLM to rapid inference APIs, allowing users to prompt multimedia creation directly within conversational interfaces. The Runware server notably supports both SSE and local stdio transports, providing lightning-fast asset generation as a callable tool, bypassing the need for users to manually navigate to external generation platforms. Other implementations, like the OpenAI GPT Image MCP and Google VEO2 MCP, wrap frontier proprietary models into standardized tool calls.   

More complex is the Video Jungle MCP server, which facilitates genuine, non-linear video editing executed by an AI agent. This server approaches video not as raw pixels, but through dense, multi-modal metadata analysis. Using tools like add-video, the server ingests media and generates embeddings, allowing the LLM to use search-videos to find specific moments based on the audio transcript or visual content occurring in the frame. The agent can then use generate-edit-from-videos to compile these specific moments, or execute edit-locally to create an OpenTimelineIO project and download it directly into professional local editing software like DaVinci Resolve. If authorized via local environment variables, the server can even scan the user's MacOS Photos application to retrieve personal media for the edit.   

In the realm of design and 3D modeling, tools like BlenderMCP connect Claude directly to the Blender engine, allowing programmatic, prompt-assisted 3D modeling and scene manipulation. Similarly, the Unity MCP acts as a bridge for automating workflows and manipulating assets within the Unity Editor, while the Framelink Figma MCP pulls design data directly into the LLM, enabling one-shot frontend code generation based on precise design specifications.   

Server Name & Description	Available Tools	GitHub Repository


Video Jungle




Multi-modal video analysis and nonlinear editing workflows.

	

add-video, create-videojungle-project, edit-locally, generate-edit-from-videos, search-videos, update-video-edit, search-local-videos 

	

github.com/burningion/video-editing-mcp 




Runware MCP




High-speed image and video generation API.

	

Image and video generation requests via SSE/stdio 

	

github.com/Runware/MCP-Runware 




EverArt




AI image generation using varied models.

	

Interface with EverArt generative APIs 

	

github.com/modelcontextprotocol/servers/tree/main/src/everart 




Google VEO2 MCP




Video and image generation via Google VEO2.

	

Generative video and image tool calls 

	

github.com/mario-andreschak/mcp-veo2 




OpenAI GPT Image MCP




OpenAI generation/editing API wrapper.

	

Image generation and editing via DALL-E/GPT 

	

github.com/SureScaleAI/openai-gpt-image-mcp 




BlenderMCP




3D modeling and scene manipulation engine control.

	

Programmatic control of Blender for prompt-assisted 3D creation 

	

github.com/ahujasid/blender-mcp 




Unity MCP




Unity Editor automation bridge.

	

Automate workflows, manipulate assets, control the Unity Editor programmatically 

	

github.com/justinpbarnett/unity-mcp 




Figma Context MCP




Connects [[AGENTS|agents]] to Figma design data.

	

Retrieve design data for automated frontend generation 

	

github.com/GLips/Figma-Context-MCP 




Spotify MCP




Controls playback and playlists.

	

Playback control, playlist management 

	

github.com/varunneal/spotify-mcp 

  
8. Social Media Management and Content Distribution

Automating a comprehensive social media presence requires interaction with notoriously complex, rate-limited, and fragmented APIs. MCP servers in this domain attempt to unify content distribution, audience analytics, and follower management into a single conversational interface.

The isteamhq/mcp-servers repository provides a highly utilized suite of individual servers for platforms like Twitter, LinkedIn, Bluesky, and Hacker News. Using standard OAuth 1.0a or API keys, an AI agent can autonomously draft content, format it according to specific platform constraints, and publish it directly without the user needing to interact with the native applications.   

For comprehensive multi-platform management, servers like the content-to-social-mcp-server act as automated content orchestration engines. This server transforms single blog URLs into platform-specific posts distributed across Twitter/X, LinkedIn, Facebook, and Instagram simultaneously via the Apify platform, handling all API routing internally. Furthermore, analytical tools like the GitHub Follower Manager enable the LLM to manage and analyze follow relationships natively, while tools like News MCP and Tabnews integrate real-time current events into the assistant's context window, allowing the AI to generate highly relevant, timely social media commentary. Closed-beta systems like Socialync are beginning to offer true omni-channel management, routing operations for up to eight major platforms (including TikTok and YouTube) through a single connection, indicating a trend toward massive aggregation in social API handling.   

Server Name & Description	Available Tools	GitHub Repository


is.team Social MCPs




Individual platform connectivity.

	

Post creation, thread management for Twitter, LinkedIn, Bluesky, and Hacker News 

	

github.com/isteamhq/mcp-servers 




Content-to-Social MCP




URL-to-post transformation engine.

	

Blog URL parsing, multi-platform formatting, scheduling 

	

github.com/Lebedinskas/content-to-social-mcp-server 




GitHub Follower Manager




Manage follow relationships.

	

Analyze and manage GitHub followers via natural language 

	

github.com/Alirezawmoradi/github-follower-manager-mcp 




BulkPublish API MCP




Publishing across 11 platforms.

	

Create posts, schedule, upload media, track analytics 

	

github.com/azeemkafridi/bulkpublish-api 




News MCP / Tabnews




Current events context retrieval.

	

Retrieve and integrate current news into AI context 

	

github.com/Zmingfeng/news_mcp, github.com/renant/mcp-tabnews 




Socialync (Closed Beta)




Omni-channel social media management.

	

Multi-platform unified API interactions for 8 major networks 

	

Proprietary / Closed Beta 

  
9. Communications: Email Ecosystems

Email management remains a central pillar of digital productivity, and MCP servers have rapidly evolved to provide comprehensive, secure inbox orchestration. Rather than simple read-only access, modern email MCPs handle complex threading protocols, attachment management, draft saving, and rigorous OAuth authentication processes.

The standout implementation is the unified Email MCP by MarlinJai, a TypeScript server that aggregates Gmail, Outlook, Apple iCloud, and generic IMAP/SMTP services under a single endpoint, radically reducing integration effort. It exposes an impressive 47 distinct tools, enabling AI [[AGENTS|agents]] to search attachments (search_attachments), manage drafts (save_draft, send_draft), apply variable-substituted templates, and triage emails with provider-aware label management.   

For environments where strict performance, concurrency, and security are required, Rust-based alternatives like the mail-imap-mcp-rs server have emerged. This asynchronous server utilizes the Tokio runtime to handle multiple accounts simultaneously without choking, and solves the limitations of earlier iterations by fully supporting the Microsoft Graph API—essential for corporate environments where standard SMTP ports are blocked. Notably, it feeds the LLM step-by-step OAuth 2.0 device code flow instructions, allowing the AI to successfully guide the human user through complex configuration processes. Furthermore, platform-specific implementations like the Shinzo-Labs Gmail MCP provide complete Google Workspace API coverage, including granular control over vacation responders, IMAP/POP settings, and mailbox history tracking.   

Server Name & Description	Available Tools	GitHub Repository


Unified Email MCP (MarlinJai)




Cross-provider email orchestration (Gmail, Outlook, iCloud, IMAP).

	

send_email, search_attachments, forward_email, save_draft, send_draft, apply_template (47 tools total) 

	

github.com/marlinjai/email-mcp 




Mail IMAP MCP (Rust)




High-performance IMAP/Graph API server.

	

Folder creation, threading headers, bulk operations, OAuth2 device flow execution 

	

github.com/tecnologicachile/mail-imap-mcp-rs 




Gmail MCP (Shinzo-Labs)




Complete Google Workspace integration.

	

Label management, thread operations, settings management, draft handling, history tracking 

	

github.com/shinzo-labs/gmail-mcp 




Gmail MCP Server (GongRzhe)




Gmail filter management.

	

Comprehensive Gmail filter CRUD operations 

	

github.com/GongRzhe/Gmail-MCP-Server 

  
10. Time Management: Calendar and Scheduling

Calendar integrations allow LLMs to transition from passive information responders to active temporal planners. The predominant platform driving this automation via MCP is Cal.com, an open-source scheduling infrastructure known for its robust APIs.

Multiple implementations of the Cal.com server exist, reflecting exceptionally high developer demand. The bcharleson/calcom-cli server is exceptionally robust, operating in dual-mode (both as a Command Line Interface and an MCP server) to prevent any functional drift between human and agent interfaces. It exposes 61 distinct MCP tools, all featuring strict Zod-validated input schemas, structured JSON outputs, and descriptive error messages designed explicitly for LLM ingestion. [[AGENTS|Agents]] can utilize these tools to find available slots, manage webhooks, handle complex out-of-office logic, coordinate destination calendars, and process Stripe integration data. Crucially, the server is highly resilient, featuring automatic retries with exponential backoff for rate limits (HTTP 429) and server errors.   

Other implementations, such as the official hosted mcp.cal.com server, provide immediate plug-and-play functionality for creating (create_booking), rescheduling (reschedule_booking), canceling, and confirming appointments via natural language without any local installation. For environments utilizing CalDAV-compatible servers (such as Yandex Calendar, Nextcloud, ownCloud, and Apple iCloud), generalized email/calendar MCP wrappers allow [[AGENTS|agents]] to search events, retrieve event Unique Identifiers (UIDs), and create appointments with recurrence rules and priority categories.   

Server Name & Description	Available Tools	GitHub Repository


Cal.com MCP (Bcharleson)




Comprehensive API v2 coverage with Zod-validated schemas and auto-retry logic.

	

61 tools including slot finding, webhook management, out-of-office coordination, Stripe, and team schedules 

	

github.com/bcharleson/calcom-cli 




Cal.com FastMCP (Danielpeter-99)




Python-based server for core scheduling interaction.

	

get_api_status, list_event_types, get_bookings 

	

github.com/Danielpeter-99/calcom-mcp 




Cal MCP (Official Hosted)




Hosted server for instant cloud execution.

	

create_booking, reschedule_booking, cancel_booking, confirm_booking 

	

github.com/calcom/cal-mcp 




Cal.com Calendar API (Mumunha)




Basic appointment management.

	

calcom_add_appointment, modify, delete, and list appointments 

	

github.com/mumunha/cal_dot_com_mcpserver 

  
11. Project Management and Issue Tracking

For AI [[AGENTS|agents]] integrated into corporate software engineering and product workflows, the ability to directly interact with project management software is essential. By connecting to these platforms, an agent can read deep organizational context, track task progress, and autonomously generate technical documentation.

The Atlassian Rovo MCP Server is a highly sophisticated implementation providing deep integration with both Jira and Confluence. Exposing 72 specific tools, the server allows the AI to perform complex operations like jira_search (using native Jira Query Language), jira_transition_issue to alter workflow states, and confluence_search (using Confluence Query Language). Security is strictly enforced; the server utilizes advanced OAuth 2.1 authorization (or Personal Access Tokens for on-premise Data Center deployments) to ensure the AI agent operates under the exact permissions of the authenticated user, automatically honoring corporate IP allowlisting rules and HTTPS TLS 1.2 encryption protocols.   

Linear has also enthusiastically adopted the protocol, with servers like tacticlaunch/mcp-linear exposing GraphQL endpoints to AI assistants. This enables the generation of contextual resources via custom URIs (e.g., linear://project/{id}/issues), allowing an LLM to seamlessly query project status, assign team members, and add comments without leaving the IDE. The is.team MCP server further expands on task management by combining project boards with real-time notifications (subscribe_card), creating an event-driven system where the AI does not need to constantly poll the server, but is instead actively notified when tasks are updated. To complete the enterprise suite, specialized servers exist for Notion API interaction and deep Microsoft Excel manipulation (handling over 173 operations including Power Query and Data Analysis Expressions), allowing [[AGENTS|agents]] to manage spreadsheets and wikis autonomously.   

Server Name & Description	Available Tools	GitHub Repository


Atlassian MCP (Sooperset)




Jira and Confluence orchestration with OAuth 2.1 security.

	

jira_search, jira_create_issue, jira_transition_issue, confluence_search, confluence_create_page (72 tools total) 

	

github.com/sooperset/mcp-atlassian 




Linear MCP




GraphQL interface for issue and project management.

	

Create/update issues, manage projects, assign team members, alter issue status 

	

github.com/tacticlaunch/mcp-linear 




is.team Core MCP




Task management with real-time event webhooks.

	

list_cards, create_task, move_task, log_time, subscribe_card, chat_respond 

	

github.com/isteamhq/mcp-servers (package @isteam/mcp) 




Excel MCP Server




Advanced spreadsheet manipulation.

	

173 operations including Power Query, DAX, pivot tables, formatting 

	

github.com/sbroenne/mcp-server-excel, github.com/haris-musa/excel-mcp-server 




Notion MCP Server




Interacting with the Notion API.

	

Database retrieval, page creation, block management 

	

github.com/suekou/mcp-notion-server 




GitLab / Jira Unified




Unified project and code management.

	

Manage projects, merge requests, files, releases, tickets 

	

github.com/HainanZhao/mcp-gitlab-jira 

  
Strategic Synthesis and Future Outlook

The landscape of Model Context Protocol servers as of June 2026 demonstrates an ecosystem moving rapidly from experimental integration to mission-critical infrastructure. The evolution of tools—from basic read-only access to parameterized execution, real-time webhooks, and complex OAuth2 device flows—highlights a broader industry shift toward secure, autonomous agentic operations across every layer of the enterprise technology stack.

Several key trends define the current [[STATE|state]] and future trajectory of the protocol. The initial danger of granting an LLM arbitrary execution rights has been effectively mitigated by hyper-specific tool design and hardware virtualization. By moving away from arbitrary code or SQL execution toward structured, Zod-validated schemas and cloud-sandboxed containers, developers are ensuring that [[AGENTS|agents]] can fail safely without compromising enterprise networks. Furthermore, the transition in categories like browser automation—from visual pixel interpretation to structured accessibility trees—signifies a push toward absolute determinism. [[AGENTS|Agents]] no longer need to approximate coordinates to click a button; they target exact DOM nodes, radically decreasing token costs, latency, and failure rates.

Finally, while single-platform servers still dominate the GitHub registries numerically, the emergence of unified, omni-channel servers indicates a strong market desire for aggregation. AI systems benefit greatly from generalized toolsets that abstract away underlying proprietary API logic, pointing toward a future where MCP acts not just as a connection layer, but as the universal translator for all digital interactions.

---
*Auto-ingested into Keystone Brain Vector DB*


---
📁 **See also:** ← Directory Index

**Related:** 20260613_VIDEO_PROD_building_a_model_context_protocol_(mcp)_server_for_davinci_r · [[20260613_AGENT_ARCH_model_context_protocol_(mcp)_tool_orchestration_optimization]] · [[20260609_AGENT_ARCH_research_the_integration_of_model_context_protocol_(mcp)_ser]]

**Related:** [[20260609_AGENT_ARCH_deep_research_into_model_context_protocol_(mcp)_session_stat]]
