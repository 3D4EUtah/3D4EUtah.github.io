# to run: python optimize_images.py

import os
from PIL import Image

# Configuration
TARGET_DIR = './media'
MAX_DIMENSION = 1080
EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}

def resize_images():
    count = 0
    saved_space = 0

    print(f"Scanning '{TARGET_DIR}' for images larger than {MAX_DIMENSION}px...")

    for root, _, files in os.walk(TARGET_DIR):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in EXTENSIONS:
                continue

            file_path = os.path.join(root, file)
            
            try:
                with Image.open(file_path) as img:
                    # Check existing size
                    width, height = img.size
                    longest_side = max(width, height)

                    # Only process if image is too big
                    if longest_side > MAX_DIMENSION:
                        original_size = os.path.getsize(file_path)
                        
                        # Calculate new dimensions
                        ratio = MAX_DIMENSION / longest_side
                        new_width = int(width * ratio)
                        new_height = int(height * ratio)

                        # Resize using high-quality resampling
                        print(f"Resizing: {file} ({width}x{height} -> {new_width}x{new_height})")
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        
                        # Overwrite the original file
                        # We convert to RGB to handle PNGs dropping transparency if converting to JPG, 
                        # but here we keep original format usually. 
                        # To be safe with PNG transparency, we just save it back.
                        img.save(file_path, optimize=True, quality=85)
                        
                        new_size = os.path.getsize(file_path)
                        saved_space += (original_size - new_size)
                        count += 1
                        
            except Exception as e:
                print(f"Error processing {file}: {e}")

    print(f"\nDone! Resized {count} images.")
    print(f"Disk space saved: {saved_space / (1024*1024):.2f} MB")

if __name__ == "__main__":
    resize_images()