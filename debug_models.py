import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

print("🔍 Listing available models for your API key...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ {m.name} ({m.display_name})")
except Exception as e:
    print(f"❌ Error listing models: {e}")
