# Image Optimization Guide — La French Barcelona

## Current State
All pages currently use **Unsplash hotlinks** (`https://images.unsplash.com/...`). This works but has drawbacks:
- No control over caching, CDN performance, or availability
- Images are not optimized for your specific layout sizes
- No WebP/AVIF serving based on browser support

## Recommended: Self-Host Optimized Images

### Step 1: Download & Convert Images

```bash
# Create images directory
mkdir -p images/clubs images/events images/hero

# Download and convert to WebP (requires cwebp from libwebp)
# Install: brew install webp

# Example for each club hero image:
curl -o images/clubs/opium-original.jpg "https://images.unsplash.com/photo-1566737236500-c8ac43014a67?w=1200&h=800&fit=crop"
cwebp -q 80 images/clubs/opium-original.jpg -o images/clubs/opium.webp
```

### Step 2: Use `<picture>` Element for Format Fallback

```html
<picture>
    <source srcset="images/clubs/opium.webp" type="image/webp">
    <source srcset="images/clubs/opium.jpg" type="image/jpeg">
    <img src="images/clubs/opium.jpg" 
         alt="Opium Barcelona nightclub" 
         width="1200" height="800"
         loading="lazy">
</picture>
```

### Step 3: Add Lazy Loading

For images below the fold, add `loading="lazy"`:
```html
<img src="image.jpg" loading="lazy" alt="Description" width="600" height="400">
```

For CSS background images (club heroes), use Intersection Observer:
```javascript
const lazyBgs = document.querySelectorAll('[data-bg]');
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.backgroundImage = `url('${entry.target.dataset.bg}')`;
            observer.unobserve(entry.target);
        }
    });
});
lazyBgs.forEach(el => observer.observe(el));
```

### Step 4: Responsive Sizes with `srcset`

```html
<img srcset="images/clubs/opium-400.webp 400w,
             images/clubs/opium-800.webp 800w,
             images/clubs/opium-1200.webp 1200w"
     sizes="(max-width: 600px) 400px,
            (max-width: 1024px) 800px,
            1200px"
     src="images/clubs/opium-800.webp"
     alt="Opium Barcelona"
     loading="lazy">
```

## Image Inventory

| Usage | Current Source | Recommended Size | Priority |
|-------|--------------|-----------------|----------|
| Homepage hero | Unsplash hotlink | 1920×1080 → WebP | High |
| Club page hero (×5) | Unsplash hotlink | 1200×800 → WebP | High |
| Event cards | Unsplash hotlink | 600×400 → WebP | Medium |
| Club card thumbnails | Unsplash hotlink | 400×300 → WebP | Medium |

## Quick Wins (No Image Download Needed)
1. Add `width` and `height` attributes to all `<img>` tags to prevent CLS
2. Add `loading="lazy"` to all below-fold images
3. Add `fetchpriority="high"` to hero/LCP images
4. Use Unsplash's built-in sizing: append `&w=800&q=75&fm=webp` to URLs
