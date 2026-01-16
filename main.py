import time
from deep_translator import GoogleTranslator

# 1. DATABASE
crop_data = {
    "rice": {"price": "₹45/kg", "market": "Madurai Mandi", "trend": "Stable"},
    "wheat": {"price": "₹32/kg", "market": "Chennai Mandi", "trend": "Rising"},
    "tomato": {"price": "₹18/kg", "market": "Dindigul Market", "trend": "Falling"},
    "potato": {"price": "₹25/kg", "market": "Trichy Mandi", "trend": "Stable"},
    "cotton": {"price": "₹6200/quintal", "market": "Coimbatore", "trend": "High Demand"},
    "onion": {"price": "₹35/kg", "market": "Perambalur Mandi", "trend": "Volatile"},
    "chili": {"price": "₹120/kg", "market": "Virudhunagar", "trend": "High Demand"},
    "sugarcane": {"price": "₹2800/ton", "market": "Thanjavur", "trend": "Stable"},
    "turmeric": {"price": "₹7000/quintal", "market": "Erode Mandi", "trend": "Rising"},
    "maize": {"price": "₹2200/quintal", "market": "Salem", "trend": "Falling"}
}

# 2. LANGUAGE OPTIONS
LANGUAGES = {
    '1': {'code': 'ta', 'name': 'Tamil (தமிழ்)'},
    '2': {'code': 'hi', 'name': 'Hindi (हिंदी)'},
    '3': {'code': 'te', 'name': 'Telugu (తెలుగు)'},
    '4': {'code': 'kn', 'name': 'Kannada (ಕನ್ನಡ)'},
    '5': {'code': 'ml', 'name': 'Malayalam (മലയാളം)'}
}

def get_crop_info(crop_name):
    return crop_data.get(crop_name)

def select_language():
    """Asks user to select a preferred language."""
    print("\n🌍 SELECT LANGUAGE / மொழி தேர்வு:")
    for key, val in LANGUAGES.items():
        print(f"{key}. {val['name']}")
    
    choice = input("\nEnter Option (1-5): ").strip()
    
    # Default to Tamil if input is wrong
    if choice not in LANGUAGES:
        print("⚠️ Invalid choice. Defaulting to Tamil.")
        return 'ta', 'Tamil'
    
    return LANGUAGES[choice]['code'], LANGUAGES[choice]['name']

def main():
    print("\n🌾 KISAN-SAHAYAK ACTIVATED (Farmer Helper) 🌾")
    print("---------------------------------------------")
    
    # Step 1: Select Language ONCE at startup
    target_lang_code, target_lang_name = select_language()
    print(f"✅ Language Set to: {target_lang_name}")

    # --- THE MAGIC LOOP ---
    while True:
        crop = input("\nEnter Crop Name (or type 'exit' to stop): ").lower().strip()
        
        if crop == 'exit':
            print("👋 shutting down... ")
            break
        
        data = get_crop_info(crop)
        
        if data:
            # English Message
            msg = f"Crop: {crop.capitalize()}\nPrice: {data['price']}\nMarket: {data['market']}\nTrend: {data['trend']}"
            
            print("\n" + "-"*30)
            print("📢 ENGLISH REPORT:")
            print(msg)
            
            # Translated Message
            try:
                print(f"\n📢 {target_lang_name.upper()} REPORT:")
                # Uses the selected language code dynamically!
                translated_text = GoogleTranslator(source='auto', target=target_lang_code).translate(msg)
                print(translated_text)
            except Exception as e:
                print("⚠️ (Offline Mode) Could not translate.")
            
            print("-" * 30)
            
        else:
            print(f"\n❌ Error: '{crop}' not found.")

if __name__ == "__main__":
    main()
