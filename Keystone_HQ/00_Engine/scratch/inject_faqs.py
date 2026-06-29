import os
import re
import json

websites_dir = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\02_Websites"
seo_dir = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\02_Keystone_Possibilities\Local_SEO_Domination"

files1 = [
    "fiduciary-pm-luxury-homes.html",
    "north-vancouver-multiplex-conversions.html",
    "pemberton-luxury-builder.html",
    "squamish-custom-home-builder.html",
    "west-vancouver-luxury-renovations.html",
    "whistler-luxury-builder.html"
]

files2 = [
    "north_vancouver_custom_homes.html",
    "squamish_custom_homes.html",
    "sunshine_coast_custom_homes.html",
    "west_vancouver_custom_homes.html",
    "whistler_custom_homes.html"
]

# FAQ generators by category
def get_faqs(filename):
    city = "Squamish"
    if "whistler" in filename:
        city = "Whistler"
    elif "west-vancouver" in filename or "west_vancouver" in filename:
        city = "West Vancouver"
    elif "north-vancouver" in filename or "north_vancouver" in filename:
        city = "North Vancouver"
    elif "pemberton" in filename:
        city = "Pemberton"
    elif "sunshine" in filename:
        city = "Sunshine Coast"

    if "fiduciary" in filename:
        return [
            {
                "q": "What is fiduciary project management in custom home building?",
                "a": "Fiduciary project management means that Keystone Possibilities acts strictly as the owner's advocate, protecting your financial interests rather than marking up subcontracts. We operate with a 100% open-ledger fee structure, passing all trade discounts directly back to the project."
            },
            {
                "q": "How does a flat-fee model compare to a traditional cost-plus contractor markup?",
                "a": "Traditional cost-plus builders charge a percentage markup on top of every sub-trade invoice, creating a conflict of interest that disincentivizes cost savings. Our flat-fee project management aligns our goals with yours, ensuring that every dollar saved stays in your build ledger."
            },
            {
                "q": "Do we get direct access to subcontractor invoices and trade billing?",
                "a": "Yes. We maintain a 100% open-ledger policy where every single sub-trade contract, invoice, permit, and materials sheet is uploaded directly to your real-time digital dashboard, ensuring absolute financial transparency."
            },
            {
                "q": "How do you handle site safety and WorkSafeBC compliance?",
                "a": "We pre-qualify all sub-trades, requiring proof of general liability insurance and active WorkSafeBC coverage. As the project managers, we maintain strict site safety compliance and coordinate daily operations to minimize liability."
            },
            {
                "q": "How do you track budgets in real time for Whistler or West Vancouver builds?",
                "a": "We use custom digital project dashboards. Every expense is tracked against the original estimate, allowing clients to see real-time updates on labor hours, materials, sub-trade completions, and upcoming cash flows."
            }
        ]
    elif "renovations" in filename:
        return [
            {
                "q": f"What is the average cost of a luxury home renovation in {city}?",
                "a": f"Luxury renovation costs in {city} vary based on scope, finishes, and structural modifications. Typically, premium custom renovations range from $250 to $500+ per square foot. We provide detailed feasibility studies and budget analysis before work begins."
            },
            {
                "q": f"Do I need building permits for a home renovation in {city}?",
                "a": f"Yes. Permitting is required for structural alterations, mechanical changes, and building additions. We represent you in all municipal meetings, managing the permit process from engineering reviews to final inspection."
            },
            {
                "q": "How do you protect my capital during a major renovation?",
                "a": "By using our transparent fiduciary management model. You sign trade contracts directly at their wholesale rates, and we manage the execution for a flat fee. This eliminates the 'black box' margins typical of traditional general contractors."
            },
            {
                "q": "Can we live in the home during a major structural renovation?",
                "a": "For extensive structural renovations, we strongly recommend securing temporary lodging. This ensures site safety, speeds up construction timelines, and protects your family from noise, dust, and hazardous material exposures."
            },
            {
                "q": "What warranties do you offer on luxury renovations?",
                "a": "All our construction work is backed by comprehensive builder warranties. We work with certified trade professionals and coordinate inspections to ensure that all work meets or exceeds the BC Building Code requirements."
            }
        ]
    elif "multiplex" in filename or "conversions" in filename:
        return [
            {
                "q": f"What is BC Bill 44 and how does it affect {city} lots?",
                "a": "BC Bill 44 mandates municipalities to allow Small-Scale Multi-Unit Housing (SSMUH), such as triplexes, fourplexes, and accessory dwelling units (ADUs), on lots previously zoned for single-family homes, bypassing lengthy rezoning processes."
            },
            {
                "q": f"How many units can I build on my lot under Bill 44 in {city}?",
                "a": f"Depending on the lot size and proximity to transit, Bill 44 allows for 3 to 4 units on standard single-family lots, and up to 6 units on larger lots located near frequent transit networks. We perform site analysis to confirm your lot's potential."
            },
            {
                "q": f"What is the estimated cost to build a multiplex in {city}?",
                "a": f"Multiplex construction costs in {city} typically range from $350 to $450+ per square foot. Building multiple units simultaneously provides significant scale efficiencies, reducing the per-unit construction cost compared to standalone custom homes."
            },
            {
                "q": f"How long does it take to secure permits for a Bill 44 multiplex?",
                "a": f"Since Bill 44 eliminates the rezoning phase, permitting timelines are significantly shorter. However, municipal development permit and building permit stages still take 4 to 8 months depending on municipal backlogs."
            },
            {
                "q": "Does a multiplex build require a licensed builder and home warranty?",
                "a": "Yes. In British Columbia, any new residential building, including multiplexes and laneway homes, must be built by a Licensed residential builder (like Keystone Possibilities, License #52603) and carry a 2-5-10 year home warranty."
            }
        ]
    else: # Custom Home Building
        return [
            {
                "q": f"How much does it cost to build a custom home in {city}?",
                "a": f"Custom home building costs in {city} typically range from $450 to $750+ per square foot for premium alpine or waterfront homes, depending on site typography, structural engineering needs, and material choices."
            },
            {
                "q": f"How long does a custom home build take in {city}?",
                "a": "A typical custom home build takes between 14 to 22 months from excavation to occupancy. Geotechnical preparation, municipal permits, and structural engineering for mountain terrain represent the primary timeline variables."
            },
            {
                "q": "Do I need a licensed builder and home warranty for my BC build?",
                "a": "Yes. BC law requires that all new custom homes be built by a Licensed Residential Builder (Keystone Possibilities is licensed under #52603) and carry a WBI 2-5-10 Year National Home Warranty to protect your investment."
            },
            {
                "q": f"What is the BC Energy Step Code, and what step does {city} require?",
                "a": f"The BC Energy Step Code is a provincial standard targeting net-zero energy ready buildings. {city} requires compliance with Step 3 or Step 4, necessitating high-performance windows, advanced insulation, and airtight building envelopes."
            },
            {
                "q": "What is the benefit of your flat-fee project management model compared to cost-plus?",
                "a": "Unlike traditional general contractors who charge a percentage markup on trade costs, our flat fee project management removes the conflict of interest. We negotiate the best trade prices for you, and all savings are retained directly in your project budget."
            }
        ]

# Inject FAQs into file
def inject_faqs_to_file(fpath):
    filename = os.path.basename(fpath)
    faqs = get_faqs(filename)
    
    content = open(fpath, 'r', encoding='utf-8', errors='ignore').read()
    
    # Check if FAQ is already injected
    if "luxury-faq-section" in content or "FAQPage" in content:
        print(f"  {filename}: FAQs already present. Skipping.")
        return False
        
    # 1. Generate FAQ JSON-LD Schema
    schema_items = []
    for faq in faqs:
        schema_items.append({
            "@type": "Question",
            "name": faq["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["a"]
            }
        })
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": schema_items
    }
    faq_schema_str = json.dumps(faq_schema, indent=2, ensure_ascii=False)
    
    # Inject schema into <head>
    head_close = "</head>"
    schema_script = f"\n<script type=\"application/ld+json\">\n{faq_schema_str}\n</script>\n"
    if head_close in content:
        content = content.replace(head_close, schema_script + head_close)
    else:
        # Fallback: prepend to content
        content = schema_script + content
        
    # 2. Generate HTML FAQ Section
    faq_html = '\n<!-- START FAQ SECTION -->\n<section class="luxury-faq-section" style="background-color: #080808; padding: 80px 20px; border-top: 1px solid rgba(196, 162, 101, 0.15); margin-top: 60px;">\n'
    faq_html += '  <div style="max-width: 900px; margin: 0 auto;">\n'
    faq_html += '    <h2 style="font-family: \'Outfit\', sans-serif; font-size: 2.25rem; color: #ffffff; margin-bottom: 40px; text-transform: uppercase; letter-spacing: 0.05em; text-align: center; border-bottom: 2px solid rgba(196, 162, 101, 0.25); padding-bottom: 15px;">Frequently Asked Questions</h2>\n'
    faq_html += '    <div class="faq-accordion" style="display: flex; flex-direction: column; gap: 20px;">\n'
    
    for faq in faqs:
        faq_html += '      <div style="border-bottom: 1px solid rgba(196, 162, 101, 0.1); padding-bottom: 20px;">\n'
        faq_html += f'        <h3 style="font-family: \'Outfit\', sans-serif; font-size: 1.2rem; color: #c4a265; margin: 0 0 10px 0; font-weight: 600;">{faq["q"]}</h3>\n'
        faq_html += f'        <p style="font-family: \'Inter\', sans-serif; font-size: 0.95rem; color: #a3a3a3; line-height: 1.6; margin: 0; font-weight: 300;">{faq["a"]}</p>\n'
        faq_html += '      </div>\n'
        
    faq_html += '    </div>\n  </div>\n</section>\n<!-- END FAQ SECTION -->\n'
    
    # Inject HTML before </main>
    main_close = "</main>"
    if main_close in content:
        content = content.replace(main_close, faq_html + main_close)
    else:
        # Fallback before </body>
        body_close = "</body>"
        if body_close in content:
            content = content.replace(body_close, faq_html + body_close)
        else:
            content += faq_html
            
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"  {filename}: Injected schema and HTML FAQs successfully.")
    return True

# Process files
modified_any = False
for fn in files1:
    fpath = os.path.join(websites_dir, fn)
    if os.path.exists(fpath):
        if inject_faqs_to_file(fpath):
            modified_any = True
for fn in files2:
    fpath = os.path.join(seo_dir, fn)
    if os.path.exists(fpath):
        if inject_faqs_to_file(fpath):
            modified_any = True

if modified_any:
    print("\nInjection complete. Redeploying updated landing pages...")
else:
    print("\nNo files updated. All files already have FAQs.")
