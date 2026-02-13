import os
import re

BASE_DIR = "/Users/bricelengama/Documents/Marketing Opti/LaFrench"
DOMAIN = "https://lafrenchbarcelona-275699211798.europe-west1.run.app"

def get_relative_path(filepath):
    return os.path.relpath(filepath, BASE_DIR)

def get_canonical_suffix(rel_path):
    # Returns the path suffix relative to the language root
    # e.g. "it/clubs/index.html" -> "/clubs/index.html"
    # "index.html" -> "/index.html"
    parts = rel_path.split(os.sep)
    if parts[0] in ["en", "es", "it"]:
        return "/" + "/".join(parts[1:])
    return "/" + "/".join(parts)

def update_hreflangs(filepath):
    rel_path = get_relative_path(filepath)
    suffix = get_canonical_suffix(rel_path)
    
    # Define the block
    hreflang_block = f"""    <!-- Hreflang -->
    <link rel="alternate" hreflang="fr-fr" href="{DOMAIN}{suffix}">
    <link rel="alternate" hreflang="en-gb" href="{DOMAIN}/en{suffix}">
    <link rel="alternate" hreflang="es-es" href="{DOMAIN}/es{suffix}">
    <link rel="alternate" hreflang="it-it" href="{DOMAIN}/it{suffix}">
    <link rel="alternate" hreflang="x-default" href="{DOMAIN}{suffix}">"""

    with open(filepath, 'r') as f:
        content = f.read()

    # Regex to find existing Hreflang block (or insert before </head>)
    # Look for <!-- Hreflang --> ... <link ... x-default ...>
    # Logic: Find <link rel="alternate" hreflang="fr-fr" ...> until end of block?
    # Simpler: Find the whole block if it exists, or insert after <link rel="canonical" ...>
    
    # Regex for existing block
    # Matches simple block start to x-default line
    pattern = r'(<!-- Hreflang -->\s*)?(<link rel="alternate" hreflang=.*?>\s*)+?(<link rel="alternate" hreflang="x-default".*?>)'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        new_content = content.replace(match.group(0), hreflang_block)
    else:
        # Insert after Canonical
        # Find canonical link
        canon_pattern = r'(<link rel="canonical" href=".*?">\s*)'
        canon_match = re.search(canon_pattern, content)
        if canon_match:
            new_content = content.replace(canon_match.group(0), canon_match.group(0) + "\n" + hreflang_block + "\n")
        else:
            print(f"Skipping {filepath}: No canonical tag found to insert after.")
            return

    if content != new_content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        print(f"No changes for {filepath}")

# Walk
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".html") and not file.startswith("update_"):
            update_hreflangs(os.path.join(root, file))
