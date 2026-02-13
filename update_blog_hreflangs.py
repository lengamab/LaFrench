
import os
import re

BASE_DIR = "/Users/bricelengama/Documents/Marketing Opti/LaFrench"
BASE_URL = "https://lafrenchbarcelona-275699211798.europe-west1.run.app"

BLOG_FILES = [
    "blog-befores.html",
    "blog-clubs-barcelone.html",
    "blog-entree-gratuite.html",
    "blog-erasmus.html",
    "blog-vip.html",
    "blog-weekend.html"
]

DIRS = {
    "fr": "",
    "en": "en/",
    "es": "es/",
    "it": "it/"
}

def generate_hreflang_block(filename):
    # Construct the full updated hreflang block
    # Note: filename is "blog-xyz.html"
    
    block = f"""    <!-- Hreflang -->
    <link rel="alternate" hreflang="fr-fr" href="{BASE_URL}/{filename}">
    <link rel="alternate" hreflang="en-gb" href="{BASE_URL}/en/{filename}">
    <link rel="alternate" hreflang="es-es" href="{BASE_URL}/es/{filename}">
    <link rel="alternate" hreflang="it-it" href="{BASE_URL}/it/{filename}">
    <link rel="alternate" hreflang="x-default" href="{BASE_URL}/{filename}">"""
    return block

def update_file(filepath, filename):
    if not os.path.exists(filepath):
        return

    with open(filepath, 'r') as f:
        content = f.read()

    # Regex to find existing hreflang block (loose match to catch variations)
    # We look for a block starting with <!-- Hreflang --> and ending before <link rel="stylesheet"
    # Or just replace specific lines if we know the format.
    # The previous files had:
    # <link rel="alternate" hreflang="fr-fr" ...>
    # ...
    # <link rel="alternate" hreflang="x-default" ...>
    
    # Let's use a simpler approach: Remove old hreflang lines and inject new block
    # But removing is risky with regex if formatting varies.
    
    # Strategy: Look for the FR line and replace the whole chunk until x-default
    
    new_block = generate_hreflang_block(filename)
    
    # Regex to match the block
    pattern = r'(<!-- Hreflang -->\s*)?<link rel="alternate" hreflang="fr-fr".+?hreflang="x-default".+?>'
    
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, new_block, content, flags=re.DOTALL)
        if new_content != content:
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"Updated {filepath}")
    else:
        print(f"Hreflang block not found in {filepath}")

def run():
    for filename in BLOG_FILES:
        # Update Root (FR)
        update_file(os.path.join(BASE_DIR, filename), filename)
        
        # Update EN
        update_file(os.path.join(BASE_DIR, "en", filename), filename)
        
        # Update ES
        update_file(os.path.join(BASE_DIR, "es", filename), filename)
        
        # Update IT (Already has it from creation script? Let's ensure consistency)
        update_file(os.path.join(BASE_DIR, "it", filename), filename)

if __name__ == "__main__":
    run()
