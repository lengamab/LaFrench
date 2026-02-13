# Domain Migration Guide — La French Barcelona

## Current Setup
- **URL**: `https://lafrenchbarcelona-275699211798.europe-west1.run.app`
- **Hosting**: Google Cloud Run (static site)
- **Structure**: `/fr`, `/en/`, `/es/` language folders

## Recommended: Custom Domain

### Option 1: `lafrenchbarcelona.com` (Best for SEO)

1. **Buy the domain** on Namecheap, Google Domains, or Cloudflare Registrar
2. **Map to Cloud Run** via `gcloud run domain-mappings create`:
   ```bash
   gcloud run domain-mappings create \
     --service=lafrenchbarcelona \
     --domain=lafrenchbarcelona.com \
     --region=europe-west1
   ```
3. **DNS Records** — Add the records shown by Google Cloud Console (usually an A record + AAAA record, or CNAME)
4. **SSL** — Cloud Run auto-provisions an SSL certificate for custom domains

### After Domain Switch — SEO Checklist

| Step | Action |
|------|--------|
| 1 | Update all `<link rel="canonical">` tags in every HTML file from Cloud Run URL → `lafrenchbarcelona.com` |
| 2 | Update all `<xhtml:link hreflang>` tags in `sitemap.xml` |
| 3 | Update all hreflang `<link>` tags in HTML `<head>` sections |
| 4 | Update JSON-LD schema `"url"` fields |
| 5 | Submit new sitemap in Google Search Console |
| 6 | Set up 301 redirects from old Cloud Run URL → new domain (via Cloud Run or Cloudflare) |
| 7 | Re-verify site in Google Search Console with new domain |
| 8 | Update Google Analytics property URL |

### Quick Find-and-Replace
When ready, run this in terminal to update all references:
```bash
# Replace Cloud Run URL with custom domain in all HTML and XML files
find /path/to/LaFrench -name "*.html" -o -name "*.xml" | \
  xargs sed -i '' 's|https://lafrenchbarcelona-275699211798.europe-west1.run.app|https://lafrenchbarcelona.com|g'
```

## robots.txt
Create a `robots.txt` at the site root:
```
User-agent: *
Allow: /

Sitemap: https://lafrenchbarcelona.com/sitemap.xml
```

## Google Search Console Setup
1. Add property → `https://lafrenchbarcelona.com`
2. Verify via DNS TXT record
3. Submit `sitemap.xml`
4. Monitor indexing for all 39 URLs
