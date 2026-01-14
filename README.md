# Kisan-Sahayak
Kisan-Sahayak (AI for Bharat): A Python-based AI tool that helps rural farmers access real-time crop market prices and expert advice in their local language (Tamil/Hindi) using NLP translation. Built for the 'AI For Bharat' Hackathon 2026.
# 🌾 Kisan-Sahayak (Farmer's Helper)

> **Empowering Rural India with AI-Driven Agricultural Insights** > *Submitted for "AI For Bharat" Hackathon 2026*

## 💡 Problem Statement
In rural India, many farmers face two major challenges:
1.  **Language Barrier:** Most agricultural market data is available only in English.
2.  **Information Gap:** Lack of instant access to real-time market prices and expert crop advice.

**Kisan-Sahayak** bridges this gap by providing an AI-powered interface that translates critical farming data into local languages (Tamil & Hindi), making technology accessible to the grassroots level.

---

## 🚀 Key Features
* **Real-Time Price Check:** Fetches current market prices for major crops (Rice, Wheat, Cotton, etc.).
* **AI Translation:** Uses `deep-translator` API to convert English output into **Tamil** or **Hindi** instantly.
* **Expert Advice:** Provides automated farming tips based on the selected crop.
* **Simple Interface:** Designed for ease of use on basic hardware.

---

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Libraries:** `deep-translator`, `random`
* **Concept:** Natural Language Processing (NLP), API Integration

---

## ⚙️ How to Run Locally

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YourUsername/Kisan-Sahayak.git](https://github.com/YourUsername/Kisan-Sahayak.git)
    cd Kisan-Sahayak
    ```

2.  **Install Dependencies**
    You need the translation library to run the AI features.
    ```bash
    pip install deep-translator
    ```

3.  **Run the Application**
    ```bash
    python main.py
    ```

4.  **Usage**
    * Enter the crop name (e.g., "Rice").
    * Select your preferred language (1 for English, 2 for Tamil, 3 for Hindi).
    * Get instant advice!

---

## 📸 Demo Output
*(Below is a sample of how the tool works)*

**Input:**
> Crop: Rice | Language: Tamil

**Output:**
> 📢 **RESULT:**
> தற்போதைய சந்தை விலை: ₹2500 ஒரு குவிண்டால்.
> நிபுணர் ஆலோசனை: நீர் மட்டத்தை 5 செமீ பராமரிக்கவும். பூச்சிகளை சரிபார்க்கவும்.

---

## 🔮 Future Scope
* **Voice Integration:** Adding Speech-to-Text so farmers can just speak to the app.
* **Weather API:** Integrating live weather alerts for the user's location.
* **Image Recognition:** Scanning crop leaves to detect diseases using Computer Vision.

---

### 👨‍💻 Team: Agri-Minds
* **Leader:** Jawahar R (Dhanalakshmi Srinivasan Engineering College)
* **Focus:** AI & Data Science
