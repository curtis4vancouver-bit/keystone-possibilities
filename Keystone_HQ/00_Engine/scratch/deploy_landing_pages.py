import os
import glob
import re
import urllib.request
import json

def clean_html_links(html_text):
    # Standardize links to clean WordPress paths
    # e.g., squamish-custom-home-builder.html -> /squamish-custom-home-builder/
    # squamish_custom_homes.html -> /squamish-custom-homes/
    def repl(m):
        filename = m.group(1)
        slug = filename.replace('_', '-')
        return f'href="/{slug}/"'
    
    cleaned = re.sub(r'href=["\'](?:\./)?([a-zA-Z0-9_-]+)\.html["\']', repl, html_text)
    return cleaned

def extract_page_data(fpath):
    try:
        content = open(fpath, 'r', encoding='utf-8', errors='ignore').read()
        
        # 1. Title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else 'No Title'
        # Clean title (e.g., strip ' | Keystone Possibilities')
        title_clean = re.sub(r'\s*\|\s*Keystone.*$', '', title, flags=re.IGNORECASE)
        
        # 2. Meta description
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        meta_desc = desc_match.group(1).strip() if desc_match else ''
        if not meta_desc:
            meta_desc = f"Elite custom home building and fiduciary construction project management services in Squamish, Whistler, and North Shore."
            
        # 3. Focus keyword from keywords meta
        keywords_match = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        focus_keyword = ''
        if keywords_match:
            kws = [k.strip() for k in keywords_match.group(1).split(',')]
            if len(kws) > 0 and kws[0]:
                focus_keyword = kws[0]
        if not focus_keyword:
            focus_keyword = "Custom Home Builder"
            
        # 4. Extract style block
        style_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
        style_block = style_match.group(0) if style_match else ''
        
        # 5. Extract main block or body block
        main_match = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL | re.IGNORECASE)
        if main_match:
            main_block = main_match.group(0)
        else:
            # Take body content excluding header/footer
            body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
            if body_match:
                body_content = body_match.group(1)
                body_content = re.sub(r'<header[^>]*>.*?</header>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                body_content = re.sub(r'<footer[^>]*>.*?</footer>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                main_block = body_content
            else:
                main_block = content
                
        # Clean links inside main_block
        main_block_clean = clean_html_links(main_block)
        
        # Combine style + main block
        full_content = style_block + "\n" + main_block_clean
        
        # Determine slug
        basename = os.path.basename(fpath)
        slug = os.path.splitext(basename)[0].replace('_', '-')
        
        return {
            'slug': slug,
            'title': title_clean,
            'content': full_content,
            'excerpt': meta_desc,
            'meta_description': meta_desc,
            'focus_keyword': focus_keyword
        }
    except Exception as e:
        print(f"Error extracting data from {fpath}: {e}")
        return None

def deploy_page(page_data):
    url = "https://keystonepossibilities.ca/?update_page_sovereign=1"
    req_body = json.dumps(page_data).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=req_body,
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res_body = response.read().decode('utf-8')
            res_data = json.loads(res_body)
            return res_data
    except Exception as e:
        print(f"Error deploying page '{page_data['slug']}': {e}")
        return {'status': 'error', 'message': str(e)}

def main():
    pages_to_deploy = []
    
    # 1. Read files in 02_Websites
    websites_dir = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\02_Websites"
    files1 = [
        "fiduciary-pm-luxury-homes.html",
        "north-vancouver-multiplex-conversions.html",
        "pemberton-luxury-builder.html",
        "squamish-custom-home-builder.html",
        "west-vancouver-luxury-renovations.html",
        "whistler-luxury-builder.html"
    ]
    for fn in files1:
        fpath = os.path.join(websites_dir, fn)
        if os.path.exists(fpath):
            data = extract_page_data(fpath)
            if data:
                pages_to_deploy.append(data)
                
    # 2. Read files in Local_SEO_Domination
    seo_dir = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\02_Keystone_Possibilities\Local_SEO_Domination"
    files2 = [
        "north_vancouver_custom_homes.html",
        "squamish_custom_homes.html",
        "sunshine_coast_custom_homes.html",
        "west_vancouver_custom_homes.html",
        "whistler_custom_homes.html"
    ]
    for fn in files2:
        fpath = os.path.join(seo_dir, fn)
        if os.path.exists(fpath):
            data = extract_page_data(fpath)
            if data:
                pages_to_deploy.append(data)
                
    print(f"Found {len(pages_to_deploy)} pages to deploy.\n")
    
    results = []
    for pdata in pages_to_deploy:
        print(f"Deploying slug: '/{pdata['slug']}/' | Title: '{pdata['title']}'...")
        res = deploy_page(pdata)
        if res.get('status') == 'success':
            print(f"  --> SUCCESS: Post ID {res.get('post_id')} | Permalink: {res.get('permalink')}")
        else:
            print(f"  --> FAILED: {res.get('error') or res.get('message')}")
        results.append((pdata['slug'], res))
        
    print("\n=== DEPLOYMENT SUMMARY ===")
    for slug, res in results:
        status_str = "SUCCESS" if res.get('status') == 'success' else "FAILED"
        print(f"/{slug}/ : {status_str} (ID: {res.get('post_id') or 'N/A'})")

if __name__ == "__main__":
    main()
