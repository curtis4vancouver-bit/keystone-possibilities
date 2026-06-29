# Webmaster Deployment SOP (WP Pusher)

**Metadata:**
*   **ID:** doc-webmaster-deployment-sop
*   **Type:** SOP
*   **Tags:** #okf, #sop

---

## The Core Rule of Website Deployment
**NEVER make changes to a static frontend or try to manually deploy `.txt` files or code via direct server uploads.** 
All web operations for Keystone Possibilities and Keystone Recomposition must run through **WP Pusher** via GitHub.

---

## 1. The Deployment Workflow
To update website functionality, schemas, endpoints, or design:

1. **Locate local WordPress theme directory:**
   `C:\Users\Curtis\New folder\construction-website\Keystone_HQ\WordPress_Theme_Scaffold\astra-child\`
2. **Modify files** (e.g., `functions.php`, `style.css`).
3. **Commit and push** changes to the GitHub repository: `curtis4vancouver-bit/construction-website`
4. **WP Pusher** automatically detects the push and deploys the updated `astra-child` theme directly to the live WordPress server.

---

## 2. Prevention of Synchronization Issues (AI Amnesia Fix)
Directly writing static files (such as `llms.txt`) to the server or editing local dummy repositories causes the system to lose synchronization with the live site. 
By routing all changes strictly through the GitHub -> WP Pusher pipeline, the codebase remains version-controlled. This allows AI agents to read the repository and accurately identify the live state of the site.

---

## 3. Dynamic Endpoints vs. Static Files
Do not create static files for crawlers (like `llms.txt`, `robots.txt`, or external API endpoints). Instead, write a PHP intercept hook in `functions.php` to ensure the endpoint updates dynamically across all servers upon pushing to GitHub.

### Implementation Logic:
```php
add_action('init', 'custom_dynamic_endpoint');
function custom_dynamic_endpoint() {
    $request = $_SERVER['REQUEST_URI'];
    if (strpos($request, '/llms.txt') !== false) {
        header('Content-Type: text/plain; charset=utf-8');
        echo "Dynamic content here.";
        exit;
    }
}
```