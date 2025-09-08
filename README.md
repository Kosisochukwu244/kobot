#  Kobot  

A  friendly AI chatbot ** powered by **Google Gemini AI**.  
This project provides a minimal yet modern chat UI built with Flask, HTML/CSS/JS, and integrates with the **Gemini 1.5 Pro API** for natural language responses.  

---

## ✨ Features  
- 🖤 **Dark theme** with glowing Web3-inspired design  
- 💬 Real-time chatbot interface with maximized chat borders  
- 🔄 Persistent chat sessions  
- ⚡ Gemini API integration (`gemini-1.5-pro`)  
- 🛡️ Error handling for quota & API issues  
- 🔌 Easy to extend with new models or APIs  

---

## 📂 Project Structure  

├── static/ # CSS, JS, images
│ ├── style.css # Custom dark theme styles
│ └── script.js # Client-side interactions
├── templates/
│ └── index.html # Chat UI frontend
├── app.py # Flask backend (API integration)
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## 🚀 Getting Started  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/your-username/web3-ai-assistant.git
cd web3-ai-assistant


python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

pip install -r requirements.txt

GEMINI_API_KEY=your_api_key_here

flask run


📜 License

MIT License © 2025 Kosisochukwu
