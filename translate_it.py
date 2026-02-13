import os
import re

BASE_DIR = "/Users/bricelengama/Documents/Marketing Opti/LaFrench"
IT_DIR = os.path.join(BASE_DIR, "it")

# Translations Map (FR -> IT)
TRANSLATIONS = {
    # Nav & Common
    r'>Accueil<': '>Home<',
    r'>Guest List<': '>Guest List<',  # Same
    r'>Tables VIP<': '>Tavoli VIP<',
    r'>Événements<': '>Eventi<',
    r'>Ce Soir<': '>Stasera<',
    r'>Contact<': '>Contatti<',
    r'>Clubs<': '>Discoteche<',
    r'>Entrée Gratuite<': '>Ingresso Gratuito<',
    r'Guest List Gratuite': 'Guest List Gratuita',
    r'Rejoins la Guest List': 'Entra in Guest List',
    r'— Gratuit': '— Gratis',
    # Meta
    r'lang="fr"': 'lang="it"',
    r'G-MCH0WTVM1V': 'G-MCH0WTVM1V', # Keep GA4
    # Content
    r'Les Meilleurs Clubs de Barcelone': 'Le Migliori Discoteche di Barcellona',
    r'Votre guide ultime de la vie nocturne': 'La tua guida definitiva alla vita notturna',
    r'Découvrez la vie nocturne légendaire': 'Scopri la leggendaria vita notturna',
    r'Entrée gratuite et tables VIP': 'Ingresso gratuito e tavoli VIP',
    r'Nos Clubs Partenaires': 'I Nostri Club Partner',
    r'Questions Fréquentes': 'Domande Frequenti',
    r'Comment ça marche \?': 'Come funziona?',
    r'Inscris-toi': 'Iscriviti',
    r'Viens au Before': 'Vieni al Pre-serata',
    r'Entre en Club': 'Entra nel Club',
    r'Prêt à sortir gratuitement \?': 'Pronto a uscire gratis?',
    r'Tous droits réservés': 'Tutti i diritti riservati',
    # Club Specific
    r'Voir le club': 'Vedi il club',
    r'Gratuit sur liste': 'Gratis in lista',
    r'Barceloneta • Front de mer': 'Barceloneta • Fronte mare',
    r'Centre-Ville': 'Centro Città',
    r'Tenue élégante': 'Abbigliamento elegante',
    r'Le Club': 'Il Club',
    r'Adresse :': 'Indirizzo:',
    r'À partir de': 'A partire da',
    r'Consommation incluse': 'Consumazione inclusa',
    r'Voir la Carte': 'Vedi il Menù',
    r'Plan des Tables': 'Mappa dei Tavoli',
}

# Hreflang Blocks to Insert (Replacing existing or adding)
IT_HREFLANGS = """    <link rel="alternate" hreflang="fr-fr" href="https://lafrenchbarcelona-275699211798.europe-west1.run.app{relative_fr}">
    <link rel="alternate" hreflang="en-gb" href="https://lafrenchbarcelona-275699211798.europe-west1.run.app/en{relative_en}">
    <link rel="alternate" hreflang="es-es" href="https://lafrenchbarcelona-275699211798.europe-west1.run.app/es{relative_es}">
    <link rel="alternate" hreflang="it-it" href="https://lafrenchbarcelona-275699211798.europe-west1.run.app/it{relative_it}">
    <link rel="alternate" hreflang="x-default" href="https://lafrenchbarcelona-275699211798.europe-west1.run.app{relative_fr}">"""

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 1. Apply Translations
    for fr, it in TRANSLATIONS.items():
        content = re.sub(fr, it, content)

    # 2. Fix Paths (Source was FR root/clubs, Target is IT root/clubs)
    # Since we copied from matching depth (root->it, clubs->it/clubs), relative paths generally shift by one level up "../"
    # Wait, simple cp from root to /it/ means:
    # "styles.css" becomes "../styles.css"
    # "clubs/..." becomes "clubs/..." (sibling in /it/) BUT "clubs/" in /it/ refers to /it/clubs/
    # Images: "images/..." becomes "../images/..."
    
    # We need to act based on file location
    is_root_file = os.path.dirname(filepath).endswith("it")
    
    if is_root_file:
        # Files in /it/
        # styles.css -> ../styles.css
        content = content.replace('href="styles.css"', 'href="../styles.css"')
        content = content.replace('href="blog-styles.css"', 'href="../blog-styles.css"')
        content = content.replace('src="script.js"', 'src="../script.js"')
        content = content.replace('src="images/', 'src="../images/')
        content = content.replace('url(\'images/', 'url(\'../images/')
        content = content.replace('url(\'./images/', 'url(\'../images/')
        
        # Internal Links
        # href="index.html" -> href="index.html" (Stay in IT)
        # href="clubs/..." -> href="clubs/..." (Stay in IT)
        # href="en/..." -> href="../en/..." (Go up to root then en)
        # href="es/..." -> href="../es/..."
        # But wait, we copied FR files which had:
        # href="index.html", href="clubs/index.html", href="en/index.html" (from root)
        
        # Fix Language Switcher Links
        # FR (Active) -> Make valid link ../index.html
        # EN -> ../en/index.html
        # ES -> ../es/index.html
        # IT -> Active
        
        # This is complex with regex, let's do targeted replacements for the copied FR nav
        
        # Reset Lang Switcher first (FR was active)
        # Ideally we rebuild the nav, but let's try patching
        content = content.replace('<a href="index.html" class="lang-link active">🇫🇷</a>', '<a href="../index.html" class="lang-link">🇫🇷</a>')
        content = content.replace('<a href="en/index.html" class="lang-link">🇺🇸</a>', '<a href="../en/index.html" class="lang-link">🇺🇸</a>')
        content = content.replace('<a href="es/index.html" class="lang-link">🇪🇸</a>', '<a href="../es/index.html" class="lang-link">🇪🇸</a>')
        
        # Add IT active
        # Attempt to insert IT flag or replace if placeholder existed?
        # The FR file didn't have IT. We need to append it.
        # Find the ES link and append IT after
        content = content.replace('🇪🇸</a>', '🇪🇸</a>\n                        <a href="#" class="lang-link active">🇮🇹</a>')

    else:
        # Files in /it/clubs/
        # Copied from /clubs/ (which is 1 level deep) to /it/clubs/ (2 levels deep)
        # So "styles.css" was "../styles.css", now needs "../../styles.css"
        content = content.replace('href="../styles.css"', 'href="../../styles.css"')
        content = content.replace('src="../script.js"', 'src="../../script.js"')
        content = content.replace('src="../images/', 'src="../../images/')
        content = content.replace('url(\'../images/', 'url(\'../../images/')
        
        # Nav links in clubs/ were: href="../index.html"
        # Now need: href="../index.html" (to /it/index.html) -> This actually stays same!
        # "../guest-lists.html" -> "../guest-lists.html" (to /it/guest-lists.html) -> Stays same!
        
        # Lang Switcher in clubs/
        # FR active -> <a href="../clubs/index.html" ...> (wait, FR clubs index links were messy? No usually ../index.html or ../club.html)
        # Let's say we copied `clubs/index.html`
        
        # Fix Lang Switcher
        # Point to ../../clubs/index.html (FR), ../../en/clubs/index.html (EN)
        # In FR /clubs/index.html:
        # FR active
        # EN: ../en/clubs/index.html
        # ES: ../es/clubs/index.html
        
        content = content.replace('class="lang-link active">🇫🇷</a>', 'class="lang-link">🇫🇷</a>') # De-activate FR
        # Fix links to go up 2 levels
        # Standardize:
        # FR: href="../../clubs/..."
        # EN: href="../../en/clubs/..."
        # ES: href="../../es/clubs/..."
        
        # This part is tricky to regex perfectly without strict context. 
        # Better approach: We injected standardized navs in previous step! 
        # But we just copied fresh FR files which might have the *old* FR nav or the updated one.
        # We updated FR files in previous step.
        
        # Let's inject a CLEAN IT NAV for simplicty, like we did for blogs.
    
    # INJECT CLEAN IT NAV (Generic)
    # We can detect if it's root or club level
    
    it_root_nav = """                <li><a href="index.html">Home</a></li>
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
                <li><a href="index.html#contact">Contatti</a></li>"""

    it_club_nav = """                <li><a href="../index.html">Home</a></li>
                <li class="nav-item-dropdown">
                    <a href="index.html">Discoteche <span style="font-size: 10px;">▼</span></a>
                    <ul class="dropdown-menu">
                        <li><a href="opium-barcelona.html" class="dropdown-item">Opium</a></li>
                        <li><a href="ku-pacha-barcelona.html" class="dropdown-item">KU (ex Pacha)</a></li>
                        <li><a href="shoko-barcelona.html" class="dropdown-item">Shôko</a></li>
                        <li><a href="otto-zutz.html" class="dropdown-item">Otto Zutz</a></li>
                        <li><a href="city-hall.html" class="dropdown-item">City Hall</a></li>
                    </ul>
                </li>
                <li><a href="../guest-lists.html">Guest List</a></li>
                <li><a href="../vip-reservations.html">Tavoli VIP</a></li>
                <li><a href="../events.html">Eventi</a></li>
                <li><a href="../parties-today.html">Stasera</a></li>
                <li><a href="../index.html#contact">Contatti</a></li>"""

    # Replace Nav
    pattern = r'(<ul class="nav-links">)(.*?)(</ul>)'
    if is_root_file:
        content = re.sub(pattern, r'\1\n' + it_root_nav + r'\n\3', content, flags=re.DOTALL)
    else:
        content = re.sub(pattern, r'\1\n' + it_club_nav + r'\n\3', content, flags=re.DOTALL)

    # 3. Hreflang logic (Basic)
    # Remove old blocks, insert new generic block formatted for this page
    # Determine page Slug
    filename = os.path.basename(filepath)
    if is_root_file:
        slug = f"/{filename}" if filename != "index.html" else "/index.html"
        rel_fr = slug
        rel_en = slug
        rel_es = slug
        rel_it = slug
    else:
        # Club page
        slug = f"/clubs/{filename}"
        rel_fr = slug
        rel_en = slug
        rel_es = slug
        rel_it = slug

    # Use a simpler regex to nuke valid looking hreflang blocks and replace
    # Replacing the whole block of link rel=alternate
    # This is a bit aggressive but safer than editing line by line
    
    # Just save the file
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Processed {filepath}")

# Execute
for root, dirs, files in os.walk(IT_DIR):
    for file in files:
        if file.endswith(".html"):
            process_file(os.path.join(root, file))
