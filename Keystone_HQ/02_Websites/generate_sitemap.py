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

    # Episode 1 Video Entry
    url_el1 = ET.SubElement(urlset, f"{{{sitemap_ns}}}url")
    loc_el1 = ET.SubElement(url_el1, f"{{{sitemap_ns}}}loc")
    loc_el1.text = "https://keystonerecomposition.com/mounjaro-muscle-loss.html"

    # Use exact namespace matching format
    video_el1 = ET.SubElement(url_el1, f"{{{video_ns}}}video")
    
    thumb1 = ET.SubElement(video_el1, f"{{{video_ns}}}thumbnail_loc")
    thumb1.text = "https://img.youtube.com/vi/aXY9S_K88sk/maxresdefault.jpg"
    
    title1 = ET.SubElement(video_el1, f"{{{video_ns}}}title")
    title1.text = "I Lost 48 Lbs on Mounjaro — Here's How Much Was Muscle | Men Over 40"
    
    desc1 = ET.SubElement(video_el1, f"{{{video_ns}}}description")
    desc1.text = "Wayne Stevenson examines the skeletal muscle loss crisis associated with GLP-1/GIP receptor agonists like Mounjaro and Tirzepatide, delivering a 4-pillar prevention protocol for active builders."
    
    content1 = ET.SubElement(video_el1, f"{{{video_ns}}}content_loc")
    content1.text = "https://www.youtube.com/v/aXY9S_K88sk"
    
    embed1 = ET.SubElement(video_el1, f"{{{video_ns}}}embed_loc")
    embed1.text = "https://www.youtube-nocookie.com/embed/aXY9S_K88sk"
    
    pub1 = ET.SubElement(video_el1, f"{{{video_ns}}}publication_date")
    pub1.text = "2026-05-22T08:00:00Z"
    
    dur1 = ET.SubElement(video_el1, f"{{{video_ns}}}duration")
    dur1.text = "504"  # 8 mins 24 secs = 504 seconds
    
    views1 = ET.SubElement(video_el1, f"{{{video_ns}}}view_count")
    views1.text = "15340"
    
    upl1 = ET.SubElement(video_el1, f"{{{video_ns}}}uploader")
    upl1.text = "Wayne Stevenson"
    upl1.set("info", "https://keystonerecomposition.com/")

    # Pretty print XML
    raw_xml = ET.tostring(urlset, encoding="utf-8")
    reparsed = minidom.parseString(raw_xml)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # Clean up XML string to ensure standard video prefixes are perfectly written
    pretty_xml = pretty_xml.replace("ns0:", "video:")
    pretty_xml = pretty_xml.replace("xmlns:ns0=", "xmlns:video=")

    # Save sitemap
    file_path = "video-sitemap.xml"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
        
    print(f"[Keystone Sitemap] Clean prefix XML Video Sitemap generated successfully at {os.path.abspath(file_path)}")

if __name__ == "__main__":
    create_video_sitemap()
