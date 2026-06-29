import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
os.chdir(PARENT_DIR)
sys.path.insert(0, PARENT_DIR)

from social_publisher import SocialPublisher

def main():
    publisher = SocialPublisher()
    
    brand = "recomposition"
    platforms = ["instagram", "facebook"]
    title = "Demolish Stubborn Belly Fat \U0001f3d7\ufe0f\U0001f525"
    media_url = r"C:\Users\Curtis\Desktop\short 2.mov"
    
    content = """Stop wasting hours on the treadmill and killing your joints. Cardio only burns the surface. If you want to demolish stubborn visceral gut fat, you have to bring in the demolition crew. \U0001f3d7\ufe0f\U0001f525

Watch the full breakdown on my YouTube channel now! (Link in bio) \U0001f447

#KeystoneRecomposition #BellyFatDemolition #Over40Fitness #VisceralFat #PeptideTherapy #MensHealth #CJC1295 #Tesamorelin #Biohacking #FatLossTips #HighEndFitness #TestosteroneOptimization"""

    print("Enqueuing post...")
    publisher.enqueue_post(
        brand=brand,
        platforms=platforms,
        content=content,
        title=title,
        media_url=media_url,
        delay_days=0
    )
    
    print("Processing queue...")
    publisher.process_due_posts(dry_run=False)

if __name__ == "__main__":
    main()
