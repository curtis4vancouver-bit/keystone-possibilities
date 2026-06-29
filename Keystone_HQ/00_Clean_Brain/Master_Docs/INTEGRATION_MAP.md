---
id: doc-integrationmap
title: Integration Map
type: document
summary: '> Central hub linking all services, tokens, and endpoints. See also: AGENTS|Agent
  Fleet · DIRECTIVES|Directives · MasterDocs/00INFRASTRUCTUREANDEVO...'
entities:
- DaVinci
- YouTube
created: '2026-06-10T08:53:36.536950'
updated: '2026-06-14T19:57:36.023381'
---
# Keystone Integration Map

> Central hub linking all services, tokens, and endpoints. See also: Agent Fleet · [[DIRECTIVES|Directives]] · Infrastructure

<!-- CONTEXT: Integration Map / MCP Servers (Active) -->
## MCP Servers (Active)
| Server | Script | Port/Method | Status |
|--------|--------|-------------|--------|
| keystone-brain | Qdrant_Brain/keystone_brain_v2_mcp.py | stdio | ✅ Active |
| youtube-manager | youtube_mcp | stdio | ✅ Active |
| youtube-researcher | youtube_researcher_mcp | stdio | ✅ Active |
| chrome-devtools-mcp | npx chrome-devtools-mcp | stdio | ✅ Active |
| brave-search | npx @modelcontextprotocol/server-brave-search | stdio | ✅ Active |
| sequential-thinking | npx @modelcontextprotocol/server-sequential-thinking | stdio | ✅ Active |
| davinci-resolve-mcp | davinci-resolve-mcp/src/resolve_mcp_server.py | stdio | ✅ Active (328 tools) |
| content-engine | content_engine_mcp | stdio | ✅ Active (8 tools) |

<!-- CONTEXT: Integration Map / Docker Services -->
## Docker Services
| Container | Image | Ports | Volume |
|-----------|-------|-------|--------|
| keystone_qdrant_brain | qdrant/qdrant:v1.18.2 | 6333-6334 | Qdrant_Brain/ |
| keystone_qdrant_clone | qdrant/qdrant:v1.18.2 | 7333-7334 | (backup) |

<!-- CONTEXT: Integration Map / Token Files -->
## Token Files
| Platform | Token File | Brand |
|----------|-----------|-------|
| YouTube [[possibilities|Possibilities]] | youtube_token_possibilities.json | Construction |
| YouTube OAC | youtube_token_oac.json | Recomposition (shared with Protocol) |
| YouTube Protocols | youtube_token_protocols.json | Protocol channel |
| Meta/Social | social_tokens.json | All brands |

<!-- CONTEXT: Integration Map / Websites -->
## Websites
| Site | Platform | Purpose |
|------|----------|---------|
| keystonepossibilities.com | WordPress | Construction business |
| keystonerecomposition.com | WordPress | Health/wellness/[[music|music]] |

<!-- CONTEXT: Integration Map / Google Service Account -->
## Google Service Account
| Purpose | Key Location |
|---------|-------------|
| Indexing API | `keystone-[[wiki/index|index]]-service-key.json` |


---
📁 **See also:** [[Master_Docs/INDEX|← Directory Index]]
