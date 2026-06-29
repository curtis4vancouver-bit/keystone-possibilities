#!/usr/bin/env python3
"""
KEYSTONE POSSIBILITIES - B2B LEAD TRACKER & ANALYTICAL CO-PILOT
Automates high-value joint-venture construction lead processing for Wayne Stevenson (BC Builder #52603).
"""

import os
import csv
import sys

LEADS_CSV = os.path.join(os.path.dirname(__file__), "hnw_bc_leads.csv")

def load_leads():
    if not os.path.exists(LEADS_CSV):
        print(f"❌ Error: Lead directory not found at {LEADS_CSV}")
        sys.exit(1)
        
    leads = []
    with open(LEADS_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
    return leads

def print_dashboard():
    leads = load_leads()
    
    print("\n" + "="*80)
    print(" 🌲 KEYSTONE POSSIBILITIES - HNW B2B JOINT-VENTURE PIPELINE 🌲")
    print("="*80)
    print(f" Total Target Opportunities Tracked: {len(leads)}")
    print("-"*80)
    
    for idx, lead in enumerate(leads, 1):
        print(f" [{idx}] {lead['Target Entity'].upper()} | {lead['Location']}")
        print(f"     📍 Corridor: {lead['Zoning/Land Corridor']}")
        print(f"     💎 JV Pitch: {lead['Alignment/JV Entry Pitch']}")
        print(f"     🔗 Resource: {lead['Contact Resource']}")
        print(f"     💰 Estimated Capital: {lead['Estimated Project Value']}")
        print("-"*80)
        
    print("\n💡 Tip: Pitch your BC Licensed Builder status (#52603) and steep-slope rock anchoring expertise.")
    print("="*80 + "\n")

if __name__ == "__main__":
    print_dashboard()
