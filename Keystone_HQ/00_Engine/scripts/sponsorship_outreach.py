#!/usr/bin/env python3
"""
Keystone Recomposition - B2B Sponsorship Outreach Engine.
Automates personalized, high-fidelity outreach to Tier 1 telehealth and premium supplement targets.
Includes direct support for local secure credential validation and simulation modes.
"""

import os
import sys
import json
import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Dict, Any

# Root Workspace directories
ROOT_DIR = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
PITCH_DECK_MD_PATH = ROOT_DIR / "Master_Docs" / "SPONSORSHIP_PITCH_DECK.md"

# Target Sponsor Leads
SPONSOR_LEADS = [
    {
        "brand_name": "Lifeforce",
        "executive_name": "Head of Brand Partnerships",
        "email": "partnerships@mylifeforce.com",
        "niche": "clinically backed private telehealth and diagnostics"
    },
    {
        "brand_name": "Thorne",
        "executive_name": "VP of Marketing",
        "email": "partnerships@thorne.com",
        "niche": "high-end premium cellular supplementation"
    },
    {
        "brand_name": "Cymbiotika",
        "executive_name": "Head of Brand Relations",
        "email": "partnerships@cymbiotika.com",
        "niche": "luxury liposomal and organic supplementation"
    },
    {
        "brand_name": "Hone Health",
        "executive_name": "VP of Growth & Partnerships",
        "email": "partnerships@honehealth.com",
        "niche": "specialized biomarker optimization and telehealth panels"
    }
]


class SponsorshipOutreachEngine:
    def __init__(self, smtp_user: str = None, smtp_pass: str = None):
        self.smtp_user = smtp_user or os.environ.get("SENDER_GMAIL_USER", "jacobal.business@gmail.com")
        self.smtp_pass = smtp_pass or os.environ.get("SENDER_GMAIL_PASS")
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 587

    def check_auth(self) -> bool:
        if not self.smtp_pass:
            print("[Outreach Warning] Gmail Application Password is not configured.")
            print("Running outreach campaign in MOCK/SIMULATION mode.")
            return False
        return True

    def build_email_body(self, lead: Dict[str, str]) -> str:
        """Fuses the approved executive outreach template with target-specific variables."""
        return (
            f"Dear {lead['executive_name']},\n\n"
            f"The core challenge in scaling a high-ticket, clinically backed platform like {lead['brand_name']} is "
            f"not demonstrating clinical efficacy; it is cutting through mass-market noise to build trust with "
            f"high-intent, affluent consumers who view health optimization as a critical business asset.\n\n"
            f"Keystone Recomposition is a specialized media platform engineered specifically for this high-value "
            f"demographic: high-net-worth male builders, founders, and executives over 40. We bypass standard, "
            f"vanity-driven fitness content to offer a precise, metrics-driven approach to physical optimization, "
            f"emphasizing detailed caloric tracking, protein optimization, and hormone and biomarker management.\n\n"
            f"Given {lead['brand_name']}'s leadership in {lead['niche']}, our audience represents your ideal consumer "
            f"profile. Our viewers do not need to be sold on the importance of biological data; they are actively "
            f"looking for high-end, clinically supervised protocols to protect their physical and cognitive performance.\n\n"
            f"We would love to discuss an integrated partnership for our upcoming Q3 content cycle. Unlike standard, "
            f"uninspired pre-roll ads, we weave our partners directly into our scientific explanations and "
            f"executive-focused lifestyle content—including our specialized focus-audio properties, such as "
            f"\"The Resonance Suite\" and \"The Morning Protocol\".\n\n"
            f"Targeted Demographic & Operational Metrics:\n"
            f"- Primary Audience: Men aged 35–55 holding executive, founder, or senior professional roles.\n"
            f"- Audience Intent: Highly committed to resistance training, metabolic longevity, and rigorous biomarker tracking.\n"
            f"- Integrated Placements: Custom-produced 90-second mid-rolls, cinematic \"Morning Routine\" integrations, and educational, science-first product breakdowns.\n\n"
            f"Are you available for a brief, 10-minute introductory call next Tuesday or Thursday to discuss a "
            f"tailored integration concept designed to acquire high-lifetime-value members for {lead['brand_name']}?\n\n"
            f"We have attached our single-page executive pitch deck, detailing our channel metrics and strategic "
            f"alignment models, for your review.\n\n"
            f"Respectfully,\n\n"
            f"Jacob Al\n"
            f"Founder & Lead Coach, Keystone Recomposition\n"
            f"{self.smtp_user}"
        )

    def execute_campaign(self, pitch_deck_pdf: Path = None, simulate: bool = True):
        """Runs the email dispatch loop across all curated leads."""
        print("=" * 70)
        print("KEYSTONE RECOMPOSITION - B2B COLD SPONSORSHIP OUTREACH ENGINE")
        print("=" * 70)
        
        has_auth = self.check_auth() if not simulate else False
        
        if simulate:
            print("[Simulation Mode] Direct connection to SMTP server bypassed.")
            
        for lead in SPONSOR_LEADS:
            print(f"\nStaging Outreach: {lead['brand_name']} ({lead['email']})")
            
            subject = f"Keystone Recomposition // High-Yield Alignment with High-Net-Worth Men Over 40"
            body = self.build_email_body(lead)
            
            msg = MIMEMultipart()
            msg["From"] = f"Jacob Al <{self.smtp_user}>"
            msg["To"] = lead["email"]
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            
            # Attach Pitch Deck if available
            attached_success = False
            if pitch_deck_pdf and pitch_deck_pdf.exists():
                try:
                    with open(pitch_deck_pdf, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename= {pitch_deck_pdf.name}",
                        )
                        msg.attach(part)
                        attached_success = True
                        print(f"  [Attachment] Pitch deck successfully linked: {pitch_deck_pdf.name}")
                except Exception as attach_err:
                    print(f"  [Attachment Warning] Failed to attach pitch deck: {attach_err}")
            else:
                print("  [Attachment Warning] No physical PDF attachment found. Sending plain email body.")

            if not simulate and has_auth:
                try:
                    print(f"  [SMTP Dispatch] Connecting to {self.smtp_host}:{self.smtp_port}...")
                    server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_pass)
                    
                    print(f"  [SMTP Dispatch] Firing email payload to {lead['email']}...")
                    server.send_message(msg)
                    server.quit()
                    print(f"  [SMTP Success] Message successfully dispatched to {lead['brand_name']}!")
                except Exception as smtp_err:
                    print(f"  [SMTP Failure] Failed to send outreach to {lead['brand_name']}: {smtp_err}")
            else:
                # Simulation Printout
                print("-" * 50)
                print(f"From: Jacob Al <{self.smtp_user}>")
                print(f"To: {lead['email']}")
                print(f"Subject: {subject}")
                print(f"Body Preview:\n{body[:250]}...\n")
                if attached_success:
                    print(f"Attachment Staged: {pitch_deck_pdf.name}")
                print("-" * 50)
                
        print("\n" + "=" * 70)
        print("SPONSORSHIP OUTREACH CAMPAIGN FINISHED")
        print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the B2B Corporate Sponsorship email campaign.")
    parser.add_argument("--pass", dest="gmail_pass", help="Gmail application password.")
    parser.add_argument("--deck", help="Path to the pitch deck PDF to attach.")
    parser.add_argument("--live", action="store_true", help="Launch live outreach directly via SMTP.")
    
    args = parser.parse_args()
    
    deck_path = Path(args.deck) if args.deck else None
    
    # Run simulation by default unless --live is specified and GMAIL password is provided
    run_simulation = not args.live or not args.gmail_pass
    
    engine = SponsorshipOutreachEngine(smtp_pass=args.gmail_pass)
    engine.execute_campaign(pitch_deck_pdf=deck_path, simulate=run_simulation)
