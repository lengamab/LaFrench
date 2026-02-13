import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import datetime
import json
import re

# Setup Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def get_model():
    # Try the 2.0 Flash Exp first
    try:
        return genai.GenerativeModel('gemini-2.0-flash-exp')
    except Exception as e:
        print(f"⚠️ Could not load gemini-2.0-flash-exp, trying 1.5: {e}")
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

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
    
    TASK: Determine which clubs are open TONIGHT and create content for 4 languages (FR, EN, ES, IT).
    
    1. INTRO: Write a short, exciting 1-2 sentence summary of TONIGHT's specific vibe (mention specific DJs or event names if found). 
       Example: "Tonight at Opium, DJ Frank is spinning for Ladies Night. Shoko brings the heat with..."
       Style: Premium nightlife guide. SEO optimized.
       
    2. CARDS: Generate HTML cards for open clubs.
    
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
    Values: {{
        "intro": "The short text summary here...",
        "cards": "The HTML string containing cards here..."
    }}
    """
    
    # Define models to try in order of preference (Verified from debug run)
    models_to_try = [
        'gemini-2.5-flash', 
        'gemini-2.0-flash', 
        'gemini-flash-latest'
    ]
    
    last_error = None
    for model_name in models_to_try:
        try:
            print(f"🤖 Trying model: {model_name}...")
            # Note: list_models showed 'models/...' prefix, but SDK often handles without it
            # We'll try with 'models/' prefix just to be safe as per the debug output
            full_model_name = f"models/{model_name}" if not model_name.startswith("models/") else model_name
            current_model = genai.GenerativeModel(full_model_name)
            response = current_model.generate_content(
                prompt, 
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            last_error = e
            print(f"⚠️ Model {model_name} failed: {e}")
            continue
            
    raise Exception(f"All models failed. Last error: {last_error}")

def update_page(file_path, content_data):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Update Summary
    summary_el = soup.find(id='ai-daily-summary')
    if summary_el:
        summary_el.string = content_data.get('intro', '')
        print(f"Updated summary in {file_path}")
    else:
        print(f"Could not find #ai-daily-summary in {file_path}")

    # Update Cards
    container = soup.find('div', class_='tonight-clubs-grid')
    if container:
        # Use a new soup to parse the generated HTML and inject it
        new_soup = BeautifulSoup(content_data.get('cards', ''), 'html.parser')
        container.clear()
        container.append(new_soup)
        
        # Save back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        print(f"Updated cards in {file_path}")
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
