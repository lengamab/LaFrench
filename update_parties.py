import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import datetime
import json
import re

# Setup Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Club sources
CLUB_SOURCES = [
    {"name": "Opium Barcelona", "url": "https://opiumbarcelona.com/events/"},
    {"name": "Shoko Barcelona", "url": "https://shoko.biz/events/"},
    {"name": "City Hall", "url": "https://www.cityhallbarcelona.com/events"},
    {"name": "Otto Zutz", "url": "https://www.ottozutz.com/en/events"}
]

def fetch_club_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Filter out scripts/styles
        for script in soup(["script", "style"]):
            script.extract()
        return soup.body.get_text(separator=' ', strip=True)[:4000]
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def generate_parties_content():
    raw_data = ""
    for club in CLUB_SOURCES:
        text = fetch_club_text(club['url'])
        raw_data += f"\n--- CLUB: {club['name']} ---\n{text}\n"

    today = datetime.datetime.now().strftime("%A, %d %B %Y")
    
    prompt = f"""
    Today is {today}. Location: Barcelona.
    Scraped data from club websites:
    {raw_data}
    
    TASK: Determine which clubs are open TONIGHT and create 4 versions of HTML (FR, EN, ES, IT).
    Use a premium, nightlife-focused style.
    
    HTML structure for each card:
    <a href="clubs/CLUB-SLUG" class="tonight-club-card">
        <div class="tonight-club-img" style="background-image: url('IMAGE_URL');">
            <span class="day-tag">LOCALIZED_DAY_TAG</span>
        </div>
        <div class="tonight-club-body">
            <h3>CLUB_NAME</h3>
            <p>📍 LOCALIZED_NEIGHBORHOOD</p>
            <p class="club-music">MUSIC_GENRE</p>
        </div>
    </a>
    
    Return ONLY a valid JSON object. 
    Keys: "fr", "en", "es", "it". 
    Values: The HTML string containing 3-5 cards.
    """
    
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
    return json.loads(response.text)

def update_page(file_path, new_html):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    container = soup.find('div', class_='tonight-clubs-grid')
    if container:
        # Use a new soup to parse the generated HTML and inject it
        new_soup = BeautifulSoup(new_html, 'html.parser')
        container.clear()
        container.append(new_soup)
        
        # Save back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        print(f"Updated {file_path}")
    else:
        print(f"Could not find tonight-clubs-grid in {file_path}")

if __name__ == "__main__":
    try:
        print("🤖 AI is fetching club data...")
        ai_payload = generate_parties_content()
        
        # Map silos to file paths
        silos = {
            "fr": "parties-today.html",
            "en": "en/parties-today.html",
            "es": "es/parties-today.html",
            "it": "it/parties-today.html"
        }
        
        for lang, path in silos.items():
            if lang in ai_payload:
                update_page(path, ai_payload[lang])
        
        print("✅ All event pages updated successfully!")
    except Exception as e:
        print(f"❌ Automation failed: {e}")
