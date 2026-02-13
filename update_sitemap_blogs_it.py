
import os

SITEMAP_PATH = "/Users/bricelengama/Documents/Marketing Opti/LaFrench/sitemap.xml"
BASE_URL = "https://lafrenchbarcelona-275699211798.europe-west1.run.app"

IT_BLOG_PAGES = [
    "it/blog-befores.html",
    "it/blog-clubs-barcelone.html",
    "it/blog-entree-gratuite.html",
    "it/blog-erasmus.html",
    "it/blog-vip.html",
    "it/blog-weekend.html"
]

def generate_url_block(path):
    # Path without language prefix for alternates
    rel_path = path.replace("it/", "", 1)
    
    fr_url = f"{BASE_URL}/{rel_path}"
    en_url = f"{BASE_URL}/en/{rel_path}"
    es_url = f"{BASE_URL}/es/{rel_path}"
    it_url = f"{BASE_URL}/{path}"
    
    block = f"""    <url>
        <loc>{it_url}</loc>
        <lastmod>2026-02-11</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
        <xhtml:link rel="alternate" hreflang="fr-fr" href="{fr_url}"/>
        <xhtml:link rel="alternate" hreflang="en-gb" href="{en_url}"/>
        <xhtml:link rel="alternate" hreflang="es-es" href="{es_url}"/>
        <xhtml:link rel="alternate" hreflang="it-it" href="{it_url}"/>
        <xhtml:link rel="alternate" hreflang="x-default" href="{fr_url}"/>
    </url>
"""
    return block

def update_sitemap_blogs():
    with open(SITEMAP_PATH, 'r') as f:
        content = f.read()
    
    if "it/blog-clubs-barcelone.html" in content:
        print("Italian Blog URLs seem to be present already.")
        return

    # Find insertion point before closing tag
    if "</urlset>" not in content:
        print("Error: closing </urlset> not found.")
        return
    
    new_blocks = "\n    <!-- ===================== ITALIAN BLOG POSTS ===================== -->\n"
    for path in IT_BLOG_PAGES:
        new_blocks += generate_url_block(path)
    
    new_content = content.replace("</urlset>", new_blocks + "</urlset>")
    
    with open(SITEMAP_PATH, 'w') as f:
        f.write(new_content)
    print("Updated sitemap.xml with Italian blog pages.")

if __name__ == "__main__":
    update_sitemap_blogs()
