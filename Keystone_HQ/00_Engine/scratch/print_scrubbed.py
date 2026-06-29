import os
import sys

ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, ROOT_DIR)

from sovereign_coordinator import KeystoneSovereign

def main():
    sovereign = KeystoneSovereign()
    
    description = """You are losing weight on Mounjaro but destroying your structural foundation. In the clinical trials up to 40% of weight lost was lean muscle, not fat. I lost 48 pounds on Mounjaro, but my strength was tanking, so I built a 4-pillar protocol to stop the muscle wasting immediately.

⚠️ Medical Disclaimer: I am not a doctor. This video is a personal case study and should not be taken as medical advice. Always consult your physician before making any changes to your health protocol.

🤖 Note: Wayne runs an AI Digital Twin avatar (generated via HeyGen) as the primary on-camera host for all Recomposition video content.

#Mounjaro #MuscleLoss #GLP1 #WeightLossJourney #Recomposition #FatLoss #FitnessOver40 #Peptides

🔗 Connect & Learn More:
📘 The Protocol & Website: https://keystonerecomposition.com
▶️ The Protocol (YouTube): https://www.youtube.com/@keystonerecomposition
🎵 My Music Channel: https://www.youtube.com/@waynestevenson-y6o"""

    scrubbed = sovereign.run_ymyl_compliance_check(description)
    with open("scratch/scrubbed_desc.txt", "w", encoding="utf-8") as f:
        f.write(scrubbed)
    print("SUCCESS: Scrubbed text saved to scratch/scrubbed_desc.txt")

if __name__ == "__main__":
    main()
