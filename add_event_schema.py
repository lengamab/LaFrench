import os
import re

BASE_DIR = "/Users/bricelengama/Documents/Marketing Opti/LaFrench"

CLUBS_DATA = {
    "opium-barcelona": {
        "name": "Opium Barcelona",
        "address": "Pg. Marítim de la Barceloneta, 34, 08003 Barcelona, Spain",
        "image": "https://lafrenchbarcelona-275699211798.europe-west1.run.app/images/clubs/opium.jpg"
    },
    "ku-pacha-barcelona": {
        "name": "KU (ex Pacha) Barcelona",
        "address": "Ramón Trias Fargas, 2, 08005 Barcelona, Spain",
        "image": "https://lafrenchbarcelona-275699211798.europe-west1.run.app/images/clubs/ku-pacha.jpg"
    },
    "shoko-barcelona": {
        "name": "Shôko Barcelona",
        "address": "Pg. Marítim de la Barceloneta, 36, 08003 Barcelona, Spain",
        "image": "https://lafrenchbarcelona-275699211798.europe-west1.run.app/images/clubs/shoko.jpg"
    },
    "otto-zutz": {
        "name": "Otto Zutz",
        "address": "Carrer de Lincoln, 15, 08006 Barcelona, Spain",
        "image": "https://lafrenchbarcelona-275699211798.europe-west1.run.app/images/clubs/otto-zutz.jpg"
    },
    "city-hall": {
        "name": "City Hall",
        "address": "Rambla de Catalunya, 2-4, 08007 Barcelona, Spain",
        "image": "https://lafrenchbarcelona-275699211798.europe-west1.run.app/images/clubs/city-hall.jpg"
    }
}

def process_file(filepath):
    filename = os.path.basename(filepath).replace(".html", "")
    if filename not in CLUBS_DATA:
        return

    with open(filepath, 'r') as f:
        content = f.read()

    # Skip if Event schema already exists (basic check)
    if '"@type": "Event"' in content and "add_event_schema" not in content:
        print(f"Skipping {filepath}: Event schema already present.")
        return

    data = CLUBS_DATA[filename]
    
    # Simple recurring event schema
    schema = f"""
    <!-- Event Schema -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Event",
      "name": "La French List at {data['name']}",
      "description": "Free Guest List entry for {data['name']} with La French Barcelona.",
      "startDate": "2026-02-13T23:55",
      "endDate": "2026-02-14T06:00",
      "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
      "eventStatus": "https://schema.org/EventScheduled",
      "location": {{
        "@type": "Place",
        "name": "{data['name']}",
        "address": {{
          "@type": "PostalAddress",
          "streetAddress": "{data['address']}",
          "addressLocality": "Barcelona",
          "addressCountry": "ES"
        }}
      }},
      "image": "{data['image']}",
      "organizer": {{
        "@type": "Organization",
        "name": "La French Barcelona",
        "url": "https://lafrenchbarcelona-275699211798.europe-west1.run.app/"
      }},
      "offers": {{
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "EUR",
        "url": "https://lafrenchbarcelona-275699211798.europe-west1.run.app/guest-lists.html",
        "availability": "https://schema.org/InStock",
        "name": "Free Guest List"
      }}
    }}
    </script>"""

    # Insert before </body>
    if "</body>" in content:
        new_content = content.replace("</body>", schema + "\n</body>")
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

# Walk
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".html"):
            process_file(os.path.join(root, file))
