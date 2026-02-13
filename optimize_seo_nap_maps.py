import os
import re
import urllib.parse

BASE_DIR = "/Users/bricelengama/Documents/Marketing Opti/LaFrench"

CLUBS_DATA = {
    "opium-barcelona": "Pg. Marítim de la Barceloneta, 34, 08003 Barcelona, Spain",
    "ku-pacha-barcelona": "Ramón Trias Fargas, 2, 08005 Barcelona, Spain",
    "shoko-barcelona": "Pg. Marítim de la Barceloneta, 36, 08003 Barcelona, Spain",
    "otto-zutz": "Carrer de Lincoln, 15, 08006 Barcelona, Spain",
    "city-hall": "Rambla de Catalunya, 2-4, 08007 Barcelona, Spain"
}

NAP_FR = """            <div class="footer-nap">
                <strong>La French Barcelona</strong><br>
                Barcelona, Spain<br>
                <a href="mailto:lafrenchbcn@gmail.com">lafrenchbcn@gmail.com</a>
            </div>"""

NAP_EN = """            <div class="footer-nap">
                <strong>La French Barcelona</strong><br>
                Barcelona, Spain<br>
                <a href="mailto:lafrenchbcn@gmail.com">lafrenchbcn@gmail.com</a>
            </div>"""

NAP_ES = """            <div class="footer-nap">
                <strong>La French Barcelona</strong><br>
                Barcelona, España<br>
                <a href="mailto:lafrenchbcn@gmail.com">lafrenchbcn@gmail.com</a>
            </div>"""

NAP_IT = """            <div class="footer-nap">
                <strong>La French Barcelona</strong><br>
                Barcellona, Spagna<br>
                <a href="mailto:lafrenchbcn@gmail.com">lafrenchbcn@gmail.com</a>
            </div>"""

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    filename = os.path.basename(filepath)
    
    # 1. NAP Injection
    # Find <p class="footer-copy"> and insert NAP before it
    # Determine language
    if "/en/" in filepath:
        nap = NAP_EN
    elif "/es/" in filepath:
        nap = NAP_ES
    elif "/it/" in filepath:
        nap = NAP_IT
    else:
        nap = NAP_FR
        
    if "footer-nap" not in content:
        # Regex to find footer-copy line
        pattern = r'(<p class="footer-copy">)'
        content = re.sub(pattern, nap + "\n            " + r'\1', content)
        
    # 2. Google Maps Injection (Clubs Only)
    # Check if club page
    club_key = None
    for key in CLUBS_DATA:
        if key in filename:
            club_key = key
            break
            
    if club_key and "map-container" not in content:
        address_encoded = urllib.parse.quote(CLUBS_DATA[club_key])
        map_html = f"""
    <!-- Location Map -->
    <section class="section" style="padding-top: 0;">
        <div class="container">
            <h3 style="color: var(--color-gold); font-family: var(--font-heading); text-align: center; margin-bottom: 20px;">Location</h3>
            <div class="map-container">
                <iframe 
                    src="https://maps.google.com/maps?q={address_encoded}&t=&z=15&ie=UTF8&iwloc=&output=embed" 
                    allowfullscreen>
                </iframe>
            </div>
        </div>
    </section>"""
        # Insert before CTA section or Footer?
        # Find "club-cta-section"
        if "club-cta-section" in content:
            content = content.replace('<section class="club-cta-section">', map_html + '\n    <section class="club-cta-section">')
            
    # 3. Google Maps Injection (Contact Page/Section) -> index.html?
    # User asked for /en/contact, which might vary.
    # We'll skip generic map for now to avoid cluttering index unless specifically requested for a contact.html file.
    # Logic: The user wants it on "Contact" page. We use #contact section in index.html.
    # Hard to inject map into #contact section cleanly with regex without proper markers.
    # Skipping general map to focus on Clubs.
            
    # 4. Event Schema (Clubs Only)
    # This is advanced regex. Let's skip for this pass to avoid breaking JSON.
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")

# Walk
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".html"):
            process_file(os.path.join(root, file))
