
import os

SITEMAP_PATH = "/Users/bricelengama/Documents/Marketing Opti/LaFrench/sitemap.xml"
BASE_URL = "https://lafrenchbarcelona-275699211798.europe-west1.run.app"

IT_PAGES = [
    {"path": "it/index.html", "priority": "0.9", "freq": "weekly"},
    {"path": "it/guest-lists.html", "priority": "0.8", "freq": "weekly"},
    {"path": "it/vip-reservations.html", "priority": "0.8", "freq": "weekly"},
    {"path": "it/events.html", "priority": "0.8", "freq": "weekly"},
    {"path": "it/parties-today.html", "priority": "0.8", "freq": "daily"},
    {"path": "it/weekend-events.html", "priority": "0.7", "freq": "weekly"},
    {"path": "it/clubs/opium-barcelona.html", "priority": "0.8", "freq": "monthly"},
    {"path": "it/clubs/ku-pacha-barcelona.html", "priority": "0.8", "freq": "monthly"},
    {"path": "it/clubs/shoko-barcelona.html", "priority": "0.8", "freq": "monthly"},
    {"path": "it/clubs/otto-zutz.html", "priority": "0.7", "freq": "monthly"},
    {"path": "it/clubs/city-hall.html", "priority": "0.7", "freq": "monthly"},
]

def generate_url_block(page_info):
    path = page_info["path"]
    priority = page_info["priority"]
    freq = page_info["freq"]
    
    # Path without language prefix for alternates
    # e.g. "it/index.html" -> "index.html"
    # "it/clubs/opium.html" -> "clubs/opium.html"
    rel_path = path.replace("it/", "", 1)
    
    fr_url = f"{BASE_URL}/{rel_path}"
    en_url = f"{BASE_URL}/en/{rel_path}"
    es_url = f"{BASE_URL}/es/{rel_path}"
    it_url = f"{BASE_URL}/it/{rel_path}"
    
    block = f"""    <url>
        <loc>{it_url}</loc>
        <lastmod>2026-02-11</lastmod>
        <changefreq>{freq}</changefreq>
        <priority>{priority}</priority>
        <xhtml:link rel="alternate" hreflang="fr-fr" href="{fr_url}"/>
        <xhtml:link rel="alternate" hreflang="en-gb" href="{en_url}"/>
        <xhtml:link rel="alternate" hreflang="es-es" href="{es_url}"/>
        <xhtml:link rel="alternate" hreflang="x-default" href="{fr_url}"/>
    </url>
"""
    return block

def update_sitemap():
    with open(SITEMAP_PATH, 'r') as f:
        content = f.read()
    
    if "<loc>https://lafrenchbarcelona-275699211798.europe-west1.run.app/it/index.html</loc>" in content:
        print("Italian URLs seem to be present already.")
        return

    # Find insertion point before closing tag
    if "</urlset>" not in content:
        print("Error: closing </urlset> not found.")
        return
    
    new_blocks = "\n    <!-- ===================== ITALIAN PAGES ===================== -->\n"
    for page in IT_PAGES:
        new_blocks += generate_url_block(page)
    
    new_content = content.replace("</urlset>", new_blocks + "</urlset>")
    
    with open(SITEMAP_PATH, 'w') as f:
        f.write(new_content)
    print("Updated sitemap.xml with Italian pages.")

if __name__ == "__main__":
    update_sitemap()
