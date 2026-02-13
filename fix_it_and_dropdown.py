import os
import re

BASE_DIR = "/Users/bricelengama/Documents/Marketing Opti/LaFrench"
# Mapping specific file paths to others for hreflang logic, but for dropdown we need relative paths from current file.

def get_rel_link(current_filepath, target_lang_root):
    # current_filepath: /path/to/it/clubs/index.html
    # target_lang_root: /path/to/en/
    # We want relative struct.
    
    # Actually, simpler: define the 4 absolute-like targets relative to web root
    # FR: /index.html, /clubs/opium.html
    # EN: /en/index.html, /en/clubs/opium.html
    
    # We can infer the equivalent path for other languages based on current file structure.
    # If we are in /it/clubs/opium.html
    # FR equivalent: ../../clubs/opium.html
    # EN equivalent: ../../en/clubs/opium.html
    # ES equivalent: ../../es/clubs/opium.html
    # IT equivalent: (self)
    
    # Logic:
    # 1. Determine "clean path" (relative to site root, no lang prefix)
    rel_path = os.path.relpath(current_filepath, BASE_DIR)
    parts = rel_path.split(os.sep)
    
    clean_parts = []
    if parts[0] in ['en', 'es', 'it']:
        clean_parts = parts[1:]
    else:
        clean_parts = parts
        
    clean_path = "/".join(clean_parts) # e.g. "clubs/opium-barcelona.html" or "index.html"
    
    # 2. Determine relative prefix to get back to root from current file
    depth = len(parts) - 1
    to_root = "../" * depth if depth > 0 else "./"
    if to_root == "./": to_root = ""
    
    # 3. Construct links
    # FR: root + clean_path
    # EN: root + en/ + clean_path
    fr_link = f"{to_root}{clean_path}"
    en_link = f"{to_root}en/{clean_path}"
    es_link = f"{to_root}es/{clean_path}"
    it_link = f"{to_root}it/{clean_path}"
    
    return fr_link, en_link, es_link, it_link

def generate_dropdown(current_lang, fr_link, en_link, es_link, it_link):
    langs = {
        'fr': {'flag': '🇫🇷', 'label': 'FR', 'link': fr_link},
        'en': {'flag': '🇺🇸', 'label': 'EN', 'link': en_link},
        'es': {'flag': '🇪🇸', 'label': 'ES', 'link': es_link},
        'it': {'flag': '🇮🇹', 'label': 'IT', 'link': it_link}
    }
    
    curr = langs[current_lang]
    
    # Build Menu Items
    menu_items = ""
    for code, data in langs.items():
        active_class = ' class="active"' if code == current_lang else ''
        menu_items += f"""            <li><a href="{data['link']}"{active_class}><span class="lang-flag">{data['flag']}</span> {data['label']}</a></li>\n"""
        
    dropdown_html = f"""
                    <!-- Language Dropdown -->
                    <div class="lang-dropdown">
                        <button class="lang-btn">
                            <span class="lang-flag">{curr['flag']}</span> {curr['label']} <span class="arrow">▼</span>
                        </button>
                        <ul class="lang-menu">
{menu_items}                        </ul>
                    </div>"""
    return dropdown_html

def fix_italian_nav(content):
    # Determine duplicate nav block using regex or string match
    # Look for </ul>...</li>...<li>...Guest List
    # The snippet from user showed:
    # </ul>
    #                 </li>
    #                 <li><a href="guest-lists.html">Guest List</a></li>
    
    # We want to replace the FIRST occurrence of the nav links block with a CORRECT block, OR just remove the dupes.
    # The user view_file showed lines 132-157 with duplication.
    # lines 132-149 look good (ul start to ul end)
    # line 150: </li> (closing the dropdown li? Wait, line 143 closes dropdown li)
    # line 149 is </ul> (closing nav-links)
    # Then line 150 </li> ?? 
    # and then MORE li items.
    
    # Cleanest fix: Find `<ul class="nav-links">` and replace everything until `<div class="nav-right">` with the CORRECT block.
    
    nav_links_pattern = r'<ul class="nav-links">.*?<div class="nav-right">'
    
    # Correct IT Nav Block
    correct_nav_it = """<ul class="nav-links">
                <li><a href="index.html">Home</a></li>
                <li class="nav-item-dropdown">
                    <a href="clubs/index.html">Discoteche <span style="font-size: 10px;">▼</span></a>
                    <ul class="dropdown-menu">
                        <li><a href="clubs/opium-barcelona.html" class="dropdown-item">Opium</a></li>
                        <li><a href="clubs/ku-pacha-barcelona.html" class="dropdown-item">KU (ex Pacha)</a></li>
                        <li><a href="clubs/shoko-barcelona.html" class="dropdown-item">Shôko</a></li>
                        <li><a href="clubs/otto-zutz.html" class="dropdown-item">Otto Zutz</a></li>
                        <li><a href="clubs/city-hall.html" class="dropdown-item">City Hall</a></li>
                    </ul>
                </li>
                <li><a href="guest-lists.html">Guest List</a></li>
                <li><a href="vip-reservations.html">Tavoli VIP</a></li>
                <li><a href="events.html">Eventi</a></li>
                <li><a href="parties-today.html">Stasera</a></li>
                <li><a href="#blog">Blog</a></li>
                <li><a href="#contact">Contatti</a></li>
            </ul>
            <div class="nav-right">"""
            
    # We need to adapt the links based on file depth! 
    # This function is called generically, so we might break relative links if we hardcode "index.html".
    # BUT duplicate issue is likely mainly in `it/index.html`.
    # Let's rely on the previous `translate_it.py` logic which seemed to introduce the dupe.
    # Actually, we can just regex the DUPLICATE BLOCK specific to it/index.html
    
    # Specific fix for the duplication pattern seen:
    dupe_pattern = r'(</ul>\s+</li>\s+<li><a href="guest-lists\.html">Guest List</a></li>)'
    # The view showed </ul> on 149, </li> on 150, then Guest List on 151
    # This means the first </ul> closed the duplicates? No.
    # The first block ended at 149.
    # Then extraneous tags.
    
    # Strategy: regenerate the nav entirely for IT files to be safe, using correct relative links.
    return content # Placeholder, logic below is safer.

def process_page(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 1. Identify Language
    rel_path = os.path.relpath(filepath, BASE_DIR)
    if rel_path.startswith("en/"): lang = "en"
    elif rel_path.startswith("es/"): lang = "es"
    elif rel_path.startswith("it/"): lang = "it"
    else: lang = "fr"
    
    # 2. Fix IT Nav Duplication (Only if IT file)
    if lang == "it":
        # Check for the specific garbage pattern: </ul> </li> <li>
        # Or just nuking the <ul class="nav-links">...</ul> block and replacing it.
        # We need to know if we are in root or clubs/
        is_club = "clubs/" in rel_path
        
        prefix = "../" if is_club else "" # Wait, clubs/ is 1 deep in IT dir?
        # it/index.html -> root of IT
        # it/clubs/index.html -> 1 level deep from IT root
        
        # In `it/index.html`: prefix = ""
        # In `it/clubs/index.html`: prefix = "../"
        
        # But wait, `it/` is already 1 level deep from BASE.
        # rel_path = "it/index.html".
        
        # CORRECT LINKING FOR IT PAGES:
        # if file is it/index.html: links are "clubs/..."
        # if file is it/clubs/opium.html: links are "../index.html"
        
        if is_club: 
             # e.g. it/clubs/opium.html
             home = "../index.html"
             clubs = "index.html" # since we are in clubs dir
             club_prefix = "" 
             guest = "../guest-lists.html"
             vip = "../vip-reservations.html"
             events = "../events.html"
             today = "../parties-today.html"
             blog = "../#blog"
             contact = "../#contact"
        else:
             # e.g. it/index.html
             home = "index.html"
             clubs = "clubs/index.html"
             club_prefix = "clubs/"
             guest = "guest-lists.html"
             vip = "vip-reservations.html"
             events = "events.html"
             today = "parties-today.html"
             blog = "#blog"
             contact = "#contact"

        nav_it = f"""<ul class="nav-links">
                <li><a href="{home}">Home</a></li>
                <li class="nav-item-dropdown">
                    <a href="{clubs}">Discoteche <span style="font-size: 10px;">▼</span></a>
                    <ul class="dropdown-menu">
                        <li><a href="{club_prefix}opium-barcelona.html" class="dropdown-item">Opium</a></li>
                        <li><a href="{club_prefix}ku-pacha-barcelona.html" class="dropdown-item">KU (ex Pacha)</a></li>
                        <li><a href="{club_prefix}shoko-barcelona.html" class="dropdown-item">Shôko</a></li>
                        <li><a href="{club_prefix}otto-zutz.html" class="dropdown-item">Otto Zutz</a></li>
                        <li><a href="{club_prefix}city-hall.html" class="dropdown-item">City Hall</a></li>
                    </ul>
                </li>
                <li><a href="{guest}">Guest List</a></li>
                <li><a href="{vip}">Tavoli VIP</a></li>
                <li><a href="{events}">Eventi</a></li>
                <li><a href="{today}">Stasera</a></li>
                <li><a href="{blog}">Blog</a></li>
                <li><a href="{contact}">Contatti</a></li>
            </ul>"""
            
        # Regex replace existing nav-links UL
        content = re.sub(r'<ul class="nav-links">.*?</ul>', nav_it, content, flags=re.DOTALL)
        
        # Also clean up any lingering </li> duplicates after </ul> if they exist (common artifact from prev script)
        content = re.sub(r'</ul>\s+</li>\s+<li>.*?</ul>', '</ul>', content, flags=re.DOTALL) # A bit risky but tries to catch the double block
        # Better: The previous replacement replaces the FIRST matching <ul>...</ul>.
        # If there was a second malformed one immediately following, we might need to zap it.
        # Let's assume re.sub replaced the main block.
        # Clean specific trash pattern:
        content = content.replace("</ul>\n                </li>\n                <li><a href=", "") # Try to break the pattern
        
        # Actually, let's just aggressively remove anything between the end of our NEW nav and the <div class="nav-right">
        # <ul class="nav-links">...</ul> [GARBAGE] <div class="nav-right">
        content = re.sub(r'(</ul>)\s*</li>\s*<li>.*?</ul>\s*(<div class="nav-right">)', r'\1\n            \2', content, flags=re.DOTALL)
        content = re.sub(r'(</ul>)\s*</li>\s*<li>.*?(<div class="nav-right">)', r'\1\n            \2', content, flags=re.DOTALL)

    
    # 3. Dropdown Implementation (All Languages)
    # Find <div class="lang-switcher"> ... </div> and replace with generate_dropdown()
    
    fr_link, en_link, es_link, it_link = get_rel_link(filepath, "/")
    new_dropdown = generate_dropdown(lang, fr_link, en_link, es_link, it_link)
    
    # Regex to find the old switcher
    switcher_pattern = r'<div class="lang-switcher">.*?</div>'
    content = re.sub(switcher_pattern, new_dropdown, content, flags=re.DOTALL)
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Processed {filepath}")

# Walk
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".html"):
            process_page(os.path.join(root, file))
