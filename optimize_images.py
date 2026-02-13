import os
import requests
from PIL import Image
from io import BytesIO

# Configuration: Source URL -> (Destination Base Path, Width, Height)
IMAGES_TO_PROCESS = [
    # Homepage Hero
    (
        "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=1920&h=1080&fit=crop",
        "images/hero/barcelona-night",
        1920, 1080
    ),
    # Club Heroes
    (
        "https://images.unsplash.com/photo-1566737236500-c8ac43014a67?w=1200&h=800&fit=crop",
        "images/clubs/opium",
        1200, 800
    ),
    (
        "https://images.unsplash.com/photo-1545128485-c400e7702796?w=1200&h=800&fit=crop",
        "images/clubs/ku-pacha",
        1200, 800
    ),
    (
        "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=1200&h=800&fit=crop",
        "images/clubs/shoko",
        1200, 800
    ),
    (
        "https://images.unsplash.com/photo-1578736641330-3155e606cd40?w=1200&h=800&fit=crop",
        "images/clubs/otto-zutz",
        1200, 800
    ),
    (
        "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=1200&h=800&fit=crop",
        "images/clubs/city-hall",
        1200, 800
    ),
]

def optimize_images():
    print("Starting image optimization...")
    
    for url, base_path, width, height in IMAGES_TO_PROCESS:
        try:
            print(f"Processing: {base_path}...")
            response = requests.get(url)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            
            # Convert to RGB (in case of RGBA/P)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if needed (Lanczos for high quality downscaling)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Save as WebP
            webp_path = f"{base_path}.webp"
            img.save(webp_path, 'WEBP', quality=85)
            print(f"  Saved: {webp_path}")
            
            # Save as JPEG (fallback)
            jpg_path = f"{base_path}.jpg"
            img.save(jpg_path, 'JPEG', quality=85)
            print(f"  Saved: {jpg_path}")
            
        except Exception as e:
            print(f"  Error processing {url}: {e}")

    print("Done!")

if __name__ == "__main__":
    optimize_images()
