import random
from deep_translator import GoogleTranslator

# --- DATA: MOCK DATABASE OF CROPS (In Real Life, this comes from an API) ---
# This dictionary acts as our "Knowledge Base"
crop_database = {
    "rice": {"base_price": 2500, "advice": "Maintain water level at 5cm. Check for pests."},
    "wheat": {"base_price": 2100, "advice": "Irrigate at crown root initiation stage."},
    "tomato": {"base_price": 1500, "advice": "Support plants with stakes. Watch for blight."},
    "cotton": {"base_price": 6000, "advice": "Monitor for bollworms. Keep field weed-free."},
    "sugarcane": {"base_price": 3000, "advice": "Ensure proper drainage. Apply urea timely."}
}

def get_market_data(crop_name):
    """
    Simulates fetching live market data.
    """
    crop_name = crop_name.lower()
    if crop_name in crop_database:
        data = crop_database[crop_name]
        # Simulate slight market fluctuation
        current_price = data["base_price"] + random.randint(-200, 200)
        return current_price, data["advice"]
    else:
        return None, None

def translate_text(text, target_lang):
    """
    Uses AI Translation to convert English to Tamil/Hindi.
    """
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        return "Error in translation. Check internet."

# --- MAIN APP INTERFACE ---
def main():
    print("========================================")
    print("      🌾 KISAN-SAHAYAK (AI TOOL) 🌾      ")
    print("   Helping Bharat's Farmers with Tech   ")
    print("========================================")

    # 1. Get User Input
    print("\nAvailable Crops: Rice, Wheat, Tomato, Cotton, Sugarcane")
    crop_input = input("Enter Crop Name (in English): ").strip()
    
    # 2. Select Language
    print("\nSelect Output Language:")
    print("1. English")
    print("2. Tamil")
    print("3. Hindi")
    choice = input("Enter choice (1/2/3): ").strip()

    target_lang = 'en'
    if choice == '2': target_lang = 'ta'
    elif choice == '3': target_lang = 'hi'

    print(f"\n... Fetching data for '{crop_input}' ...")

    # 3. Process Data
    price, advice = get_market_data(crop_input)

    if price:
        # Create the final message in English first
        output_msg = f"Current Market Price: ₹{price} per quintal.\nExpert Advice: {advice}"
        
        # 4. Translate if needed (The AI Part)
        if target_lang != 'en':
            print("... Translating via AI ...")
            final_output = translate_text(output_msg, target_lang)
        else:
            final_output = output_msg

        # 5. Show Result
        print("\n" + "-"*30)
        print("📢 RESULT:")
        print(final_output)
        print("-" * 30)
    else:
        print("\n❌ Error: Crop not found in database. Try 'Rice' or 'Tomato'.")

if __name__ == "__main__":
    main()