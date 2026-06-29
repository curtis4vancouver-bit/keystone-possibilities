import os
import subprocess
import sys
from PIL import Image, ImageDraw

def generate_aida_orb_icon():
    print("[Build] Generating AIDA glowing orb icon with solid premium backplate...")
    size = 256
    # Create high-res image with transparent background
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    
    # 1. Draw a solid black premium circular backplate
    draw.ellipse(
        [16, 16, size - 16, size - 16],
        fill=(0, 0, 0, 255), # Solid pitch black background so background is invisible
        outline=(0, 212, 255, 255), # Glow border
        width=6
    )
    
    # 2. Draw thicker, brighter glowing rings on top of the backplate
    glow_colors = [
        (0, 102, 255, 30),   # Deeper blue soft glow
        (0, 212, 255, 80),   # Rich cyan glow
        (0, 212, 255, 150),  # Bright cyan ring
        (0, 212, 255, 220),  # Intense core cyan
        (255, 255, 255, 255) # Pure white core ring
    ]
    
    radii = [80, 70, 60, 50, 46]
    widths = [26, 20, 14, 8, 4]
    
    for r, w, color in zip(radii, widths, glow_colors):
        draw.ellipse(
            [center - r, center - r, center + r, center + r],
            outline=color,
            width=w
        )
    
    # Save PNG and ICO to both assets and dist
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(current_dir, "frontend", "assets")
    dist_assets_dir = os.path.join(current_dir, "frontend", "dist", "assets")
    
    os.makedirs(assets_dir, exist_ok=True)
    os.makedirs(dist_assets_dir, exist_ok=True)
    
    for folder in [assets_dir, dist_assets_dir]:
        png_path = os.path.join(folder, "aida.png")
        ico_path = os.path.join(folder, "aida.ico")
        img.save(png_path, "PNG")
        img.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        
    print(f"[Build] App icon saved successfully.")

def run_pyinstaller():
    print("[Build] Running PyInstaller...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    entry_script = os.path.join(current_dir, "app_entry.py")
    icon_path = os.path.join(current_dir, "frontend", "assets", "aida.ico")
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir", # Directory mode is highly recommended for faster start times and stability
        "--noconsole", # Completely hides the command prompt window
        f"--icon={icon_path}",
        "--name=AIDA_App",
        f"--paths={os.path.join(current_dir, 'backend')}",
        f"--add-data={os.path.join(current_dir, 'frontend')};frontend",
        f"--add-data={os.path.join(current_dir, 'backend')};backend",
        # Include hidden imports for all server dependencies
        "--hidden-import=uvicorn",
        "--hidden-import=fastapi",
        "--hidden-import=psutil",
        "--hidden-import=websocket",
        "--hidden-import=pydantic",
        "--hidden-import=uvicorn.logging",
        "--hidden-import=uvicorn.protocols.http",
        "--hidden-import=googleapiclient",
        "--hidden-import=google.oauth2.credentials",
        "--hidden-import=markdown",
        entry_script
    ]
    
    print(f"[Build] Command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, cwd=current_dir)
    print("\n[Build] SUCCESS! A.I.D.A. desktop application compiled inside dist/AIDA/")

if __name__ == "__main__":
    # Ensure frontend is built first
    print("[Build] Compiling React frontend...")
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
    try:
        subprocess.run("npm run build", shell=True, check=True, cwd=frontend_dir)
        print("[Build] Frontend built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[Build] Frontend compilation failed: {e}")
        sys.exit(1)
        
    generate_aida_orb_icon()
    
    try:
        run_pyinstaller()
    except subprocess.CalledProcessError as e:
        print(f"[Build] PyInstaller compilation failed: {e}")
        sys.exit(1)
