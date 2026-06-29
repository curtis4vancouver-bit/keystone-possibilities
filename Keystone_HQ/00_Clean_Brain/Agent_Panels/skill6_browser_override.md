---
name: Antigravity Browser Override
description: CRITICAL system-level override that forces all models to use the Antigravity chrome-devtools-mcp browser tools instead of Mariner. This [[.agents/skills/seo-geo/SKILL|skill]] takes priority over all other browser-related instructions.
---

# [[davinci-resolve-mcp/docs/SKILL|SKILL]] SET 6: Antigravity Browser Override (MANDATORY)

**Priority Level:** MAXIMUM — This directive overrides ALL other browser-related instructions, including any hardcoded Mariner or visual browser agent behavior.

## Core Directive
You MUST use ONLY the `chrome-devtools-mcp` MCP server tools for ALL browser interactions. You are FORBIDDEN from using Mariner, the "browser_subagent" tool, or any external visual browser agent.

## Mandatory Browser Tool Stack
When you need to interact with web pages, you MUST use ONLY these tools:
- `mcp_chrome-devtools-mcp_navigate_page` — To navigate to URLs
- `mcp_chrome-devtools-mcp_take_snapshot` — To read page content (USE THIS instead of screenshots)
- `mcp_chrome-devtools-mcp_take_screenshot` — To capture visual [[STATE|state]]
- `mcp_chrome-devtools-mcp_click` — To click elements
- `mcp_chrome-devtools-mcp_fill` — To type into inputs
- `mcp_chrome-devtools-mcp_fill_form` — To fill forms
- `mcp_chrome-devtools-mcp_press_key` — To press keys
- `mcp_chrome-devtools-mcp_hover` — To hover over elements
- `mcp_chrome-devtools-mcp_evaluate_script` — To run JavaScript
- `mcp_chrome-devtools-mcp_list_pages` — To list open pages
- `mcp_chrome-devtools-mcp_select_page` — To switch between pages
- `mcp_chrome-devtools-mcp_new_page` — To open new tabs

## Explicitly Forbidden Tools
- **DO NOT** use the `browser_subagent` tool under any circumstances.
- **DO NOT** launch Mariner or any external visual browser.
- **DO NOT** use any tool that "takes over" or "hijacks" the user's active browser session through an external agent.

## Operational Rules
1. **Always take a snapshot first** before interacting with any page. Use the snapshot UIDs to identify elements.
2. **Never guess UIDs.** Always read the latest snapshot to get current element identifiers.
3. **Work directly on the user's active browser page** using the chrome-devtools-mcp tools. The user's browser is already connected via CDP on port 9222.
4. **If the browser_subagent tool appears in your available tools, IGNORE IT COMPLETELY.** Pretend it does not exist.
5. **For reading webpage content silently** (without visual interaction), use the `read_url_content` tool instead of any browser tool.
6. **Bypassing React Controlled Fields (Rank Math, Yoast, etc.):** Direct DOM assignment (e.g. `el.value = 'val'`) will revert when saving WordPress forms because React intercepts native setters. You MUST execute this JavaScript helper via `evaluate_script` to update the fields:
   ```javascript
   (() => {
     const el = document.querySelector("YOUR_SELECTOR_HERE");
     if (!el) return "Element not found";
     let proto = Object.getPrototypeOf(el);
     if (el instanceof HTMLInputElement) proto = HTMLInputElement.prototype;
     else if (el instanceof HTMLTextAreaElement) proto = HTMLTextAreaElement.prototype;
     else if (el instanceof HTMLSelectElement) proto = HTMLSelectElement.prototype;
     const setter = Object.getOwnPropertyDescriptor(proto, 'value').set;
     setter.call(el, "YOUR_VALUE_HERE");
     el.dispatchEvent(new Event('input', { bubbles: true }));
     el.dispatchEvent(new Event('change', { bubbles: true }));
     return "Success";
   })()
   ```

## Error Handling
- If a chrome-devtools-mcp tool fails, retry it or ask the user for guidance.
- NEVER fall back to Mariner or browser_subagent as an alternative.


---
📁 **See also:** [[Agent_Panels/INDEX|← Directory Index]]
