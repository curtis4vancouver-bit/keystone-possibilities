import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

def create_video_sitemap():
    # Namespaces
    sitemap_ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    video_ns = "http://www.google.com/schemas/sitemap-video/1.1"

    # Register namespaces globally to prevent generic ns0 prefixes
    ET.register_namespace("", sitemap_ns)
    ET.register_namespace("video", video_ns)

    # Root element
    urlset = ET.Element(f"{{{sitemap_ns}}}urlset")

    episodes = [
        {
            "loc": "https://keystonerecomposition.com/mounjaro-muscle-loss.html",
            "video_id": "aXY9S_K88sk",
            "title": "I Lost 48 Lbs on Mounjaro — Here's How Much Was Muscle | Men Over 40",
            "description": "Wayne Stevenson examines the skeletal muscle loss crisis associated with GLP-1/GIP receptor agonists like Mounjaro and Tirzepatide, delivering a 4-pillar prevention protocol for active builders.",
            "pub_date": "2026-05-22T08:00:00Z",
            "duration": "504",
            "views": "15340"
        },
        {
            "loc": "https://keystonerecomposition.com/wolverine-stack.html",
            "video_id": "o9fIpKUUXWE",
            "title": "The Molecular Architecture of Repair: A Comprehensive Analysis of the BPC-157 and Thymosin Beta-4 Synergy",
            "description": "A highly detailed scientific analysis examining the cellular synergy, angiogenesis pathways, and safety benchmarks of BPC-157 and Thymosin Beta-4.",
            "pub_date": "2026-06-03T12:00:00Z",
            "duration": "720",
            "views": "8250"
        },
        {
            "loc": "https://keystonerecomposition.com/retatrutide-phase-3-data.html",
            "video_id": "ov51ES_PcKk",
            "title": "Retatrutide Phase 3 Data: The Most Powerful GLP-1 Ever Built",
            "description": "Wayne Stevenson and Victoria break down the Phase 3 TRIUMPH trial data, muscle loss risks, and the Builder's Protocol for protection.",
            "pub_date": "2026-06-11T12:00:00Z",
            "duration": "480",
            "views": "9340"
        },
        {
            "loc": "https://keystonerecomposition.com/cjc-1295-ipamorelin-glp-1-fatigue.html",
            "video_id": "lcHYhRvxsqM",
            "title": "CJC-1295 & Ipamorelin for GLP-1 Fatigue | 60-Day Recomposition Case Study",
            "description": "Wayne Stevenson examines the severe daytime fatigue associated with GLP-1 receptor agonists (Tirzepatide) and delivers a morning CJC-1295 and Ipamorelin protocol to restore energy.",
            "pub_date": "2026-06-29T12:00:00Z",
            "duration": "492",
            "views": "12850"
        }
    ]

    for ep in episodes:
        url_el = ET.SubElement(urlset, f"{{{sitemap_ns}}}url")
        loc_el = ET.SubElement(url_el, f"{{{sitemap_ns}}}loc")
        loc_el.text = ep["loc"]

        video_el = ET.SubElement(url_el, f"{{{video_ns}}}video")
        
        thumb = ET.SubElement(video_el, f"{{{video_ns}}}thumbnail_loc")
        thumb.text = f"https://img.youtube.com/vi/{ep['video_id']}/maxresdefault.jpg"
        
        title = ET.SubElement(video_el, f"{{{video_ns}}}title")
        title.text = ep["title"]
        
        desc = ET.SubElement(video_el, f"{{{video_ns}}}description")
        desc.text = ep["description"]
        
        content = ET.SubElement(video_el, f"{{{video_ns}}}content_loc")
        content.text = f"https://www.youtube.com/v/{ep['video_id']}"
        
        embed = ET.SubElement(video_el, f"{{{video_ns}}}embed_loc")
        embed.text = f"https://www.youtube-nocookie.com/embed/{ep['video_id']}"
        
        pub = ET.SubElement(video_el, f"{{{video_ns}}}publication_date")
        pub.text = ep["pub_date"]
        
        dur = ET.SubElement(video_el, f"{{{video_ns}}}duration")
        dur.text = ep["duration"]
        
        views = ET.SubElement(video_el, f"{{{video_ns}}}view_count")
        views.text = ep["views"]
        
        upl = ET.SubElement(video_el, f"{{{video_ns}}}uploader")
        upl.text = "Wayne Stevenson"
        upl.set("info", "https://keystonerecomposition.com/")

    # Pretty print XML
    raw_xml = ET.tostring(urlset, encoding="utf-8")
    reparsed = minidom.parseString(raw_xml)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # Clean up XML string to ensure standard video prefixes are perfectly written
    pretty_xml = pretty_xml.replace("ns0:", "video:")
    pretty_xml = pretty_xml.replace("xmlns:ns0=", "xmlns:video=")
    # Fix the XML declaration to include UTF-8 encoding
    pretty_xml = pretty_xml.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>')

    # Save sitemap
    file_path = "video-sitemap.xml"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
        
    print(f"[Keystone Sitemap] Clean prefix XML Video Sitemap generated successfully at {os.path.abspath(file_path)}")

if __name__ == "__main__":
    create_video_sitemap()
