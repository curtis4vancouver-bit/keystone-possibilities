import os
from PIL import Image, ImageDraw

def generate_icons():
    # Target directory
    icons_dir = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Engine\webmcp_extension\icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    # Standard sizes
    sizes = [16, 48, 128]
    
    for size in sizes:
        # Create a new image with transparent background
        img = Image.new("RGBA", (size, size), (15, 23, 42, 255)) # Dark slate background #0f172a
        draw = ImageDraw.Draw(img)
        
        # Draw a stylized K logo with cyan accents
        # Coordinate calculations based on size scale
        padding = max(2, int(size * 0.15))
        left = padding
        top = padding
        right = size - padding
        bottom = size - padding
        width = max(2, int(size * 0.12))
        
        # Left bar of K
        draw.rectangle([left, top, left + width, bottom], fill=(0, 242, 254, 255)) # Cyan
        
        # Diagonal bars
        center_y = size // 2
        # Upper diagonal
        draw.line([left + width, center_y, right, top], fill=(79, 172, 254, 255), width=width) # Blue
        # Lower diagonal
        draw.line([left + width, center_y, right, bottom], fill=(79, 172, 254, 255), width=width)
        
        # Draw tech circles (nodes)
        node_r = max(1, int(size * 0.06))
        # Top-right node
        draw.ellipse([right - node_r, top - node_r, right + node_r, top + node_r], fill=(0, 242, 254, 255))
        # Bottom-right node
        draw.ellipse([right - node_r, bottom - node_r, right + node_r, bottom + node_r], fill=(79, 172, 254, 255))
        
        # Save output png
        output_path = os.path.join(icons_dir, f"icon{size}.png")
        img.save(output_path, "PNG")
        print(f"Generated {output_path}")

if __name__ == "__main__":
    generate_icons()
