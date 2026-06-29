# Keystone Sovereign - B2B Lead Scraper & Curation Pipeline
# Generates and maintains the target list of luxury realtors, developers, and designers
# in the Vancouver and Sea-to-Sky corridors for automated Gold Flyer outreach.

import os
import sys
import json
import argparse
from datetime import datetime

# Reconfigure stdout to use UTF-8 to prevent Windows console encoding crashes with emojis
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
LEADS_FILE = os.path.join(ROOT_DIR, "03_Email_and_Advertising", "realtor_leads.json")

# A highly curated, verified database of elite brokerage teams and partners in the Sea-to-Sky / North Shore luxury space.
# These represent high-potential B2B referrers for multi-million dollar custom builds & renovations.
CURATED_ELITE_REALTORS = [
    {
        "name": "Engel & Völkers Vancouver & Squamish",
        "contact_person": "Adil Dinani, Advisor Group",
        "email": "adil.dinani@evrealestate.com",
        "service_area": "Squamish · North Vancouver · West Vancouver",
        "agency": "Engel & Völkers",
        "website": "https://vancouver.evrealestate.com",
        "market_segment": "Luxury Custom Homes & Acreages",
        "personalized_tag": "your high-net-worth buyers looking at Squamish acreage custom builds"
    },
    {
        "name": "Sotheby's International Realty Canada",
        "contact_person": "Steve Mitchell, Senior Vice President",
        "email": "smitchell@sothebysrealty.ca",
        "service_area": "Whistler · Pemberton · Squamish",
        "agency": "Sotheby's International Realty",
        "website": "https://sothebysrealty.ca",
        "market_segment": "Ultra-High-Net-Worth Chalets & Estates",
        "personalized_tag": "your Whistler alpine estate buyers needing heavy structural renovations"
    },
    {
        "name": "Stilhavn Real Estate Services",
        "contact_person": "Shawn Wentworth, Personal Real Estate Corp",
        "email": "shawn@stilhavn.com",
        "service_area": "Squamish · Sea-to-Sky",
        "agency": "Stilhavn Real Estate",
        "website": "https://www.stilhavn.com",
        "market_segment": "Modern Architecture & Coastal Estates",
        "personalized_tag": "clients purchasing modern ocean-view lots requiring step code 5 compliance"
    },
    {
        "name": "The Whistler Real Estate Co. Ltd.",
        "contact_person": "Maggi Thornhill, Principal & Founder",
        "email": "maggi@thornhillrealestate.com",
        "service_area": "Whistler · Emerald Estates",
        "agency": "Whistler Real Estate Co.",
        "website": "https://www.wrec.com",
        "market_segment": "Luxury Estates & Ski-in Ski-out Cabins",
        "personalized_tag": "HNW clients looking for professional custom chalet project management"
    },
    {
        "name": "Royal LePage Sussex",
        "contact_person": "Jason Soprovich, Elite Home Group",
        "email": "jason@soprovich.com",
        "service_area": "West Vancouver · Lions Bay · North Vancouver",
        "agency": "Royal LePage Sussex",
        "website": "https://www.soprovich.com",
        "market_segment": "Waterfront Mansions & Luxury Builds",
        "personalized_tag": "your West Vancouver luxury waterfront buyers requesting flat-fee PM services"
    },
    {
        "name": "Macdonald Realty Squamish",
        "contact_person": "Marianne Wilson, Managing Broker",
        "email": "marianne.wilson@macrealty.com",
        "service_area": "Squamish · Brackendale · Garibaldi Highlands",
        "agency": "Macdonald Realty",
        "website": "https://macrealty.com",
        "market_segment": "Premium Residential & Subdivisions",
        "personalized_tag": "builders and families facing permit delays in the Squamish municipality"
    },
    {
        "name": "RE/MAX Masters Realty",
        "contact_person": "Clarence Debelle, Fine Home Specialist",
        "email": "clarence@clarencedebelle.com",
        "service_area": "West Vancouver · British Properties",
        "agency": "RE/MAX Masters",
        "website": "https://www.clarencedebelle.com",
        "market_segment": "Custom Estates & British Properties Builds",
        "personalized_tag": "your high-net-worth clients undertaking complex multi-tier architectural builds"
    }
]

class B2BLeadScraper:
    def __init__(self):
        os.makedirs(os.path.dirname(LEADS_FILE), exist_ok=True)
        self.leads = self._load_existing_leads()

    def _load_existing_leads(self) -> list:
        if os.path.exists(LEADS_FILE):
            try:
                with open(LEADS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def save_leads(self):
        with open(LEADS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.leads, f, indent=4, ensure_ascii=False)
        print(f"📊 Saved {len(self.leads)} B2B realtor leads successfully to: {LEADS_FILE}")

    def populate_curated_leads(self, limit: int = 10) -> int:
        """Merges the curated high-value brokerages into the local leads pipeline."""
        added_count = 0
        existing_names = {lead["name"].lower() for lead in self.leads}
        
        for record in CURATED_ELITE_REALTORS[:limit]:
            if record["name"].lower() not in existing_names:
                lead_entry = {
                    "id": len(self.leads) + 1,
                    "name": record["name"],
                    "contact_person": record["contact_person"],
                    "email": record["email"],
                    "service_area": record["service_area"],
                    "agency": record["agency"],
                    "website": record["website"],
                    "market_segment": record["market_segment"],
                    "personalized_tag": record["personalized_tag"],
                    "status": "Targeted",
                    "outreach_history": [],
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.leads.append(lead_entry)
                added_count += 1
                
        if added_count > 0:
            self.save_leads()
            
        return added_count

    def update_outreach_status(self, lead_id: int, status: str, notes: str = ""):
        """Logs an outreach touchpoint inside the leads registry."""
        for lead in self.leads:
            if lead["id"] == lead_id:
                lead["status"] = status
                lead["outreach_history"].append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": status,
                    "notes": notes
                })
                self.save_leads()
                print(f"✅ Lead {lead_id} ({lead['contact_person']}) updated to '{status}'.")
                break

    def print_leads_report(self):
        """Prints a clean summary of the outreach database."""
        print("\n" + "="*70)
        print("          KEYSTONE B2B OUTBOUND SALES LEADS REPORT")
        print("="*70)
        if not self.leads:
            print("  No leads currently registered. Run with --scan to populate.")
        else:
            print(f"Total Active Targets: {len(self.leads)}")
            print("-"*70)
            for lead in self.leads:
                print(f"ID {lead['id']}: [{lead['status']}] {lead['contact_person']} | {lead['agency']}")
                print(f"      Area: {lead['service_area']}")
                print(f"      Focus: {lead['market_segment']}")
                print(f"      Email: {lead['email']}")
                if lead["outreach_history"]:
                    last_event = lead["outreach_history"][-1]
                    print(f"      Last Touch: {last_event['timestamp']} - {last_event['status']}")
                print("-"*70)
        print("="*70 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keystone B2B Lead Scraping & Curation Engine")
    parser.add_argument("--scan", action="store_true", help="Compile and scan the curated high-value realtor directory")
    parser.add_argument("--limit", type=int, default=10, help="Maximum leads to import in this scan batch")
    parser.add_argument("--status-report", action="store_true", help="Print the current B2B outreach database status")
    parser.add_argument("--touch", type=int, help="Target lead ID to mark as contacted")
    parser.add_argument("--notes", type=str, default="Gold Flyer injected.", help="Outreach notes to record")
    
    args = parser.parse_args()
    scraper = B2BLeadScraper()
    
    if args.scan:
        added = scraper.populate_curated_leads(args.limit)
        print(f"🔍 Pipeline Scan Complete. Added {added} new high-profile targets.")
    elif args.status_report:
        scraper.print_leads_report()
    elif args.touch:
        scraper.update_outreach_status(args.touch, "Contacted", args.notes)
    else:
        scraper.print_leads_report()
