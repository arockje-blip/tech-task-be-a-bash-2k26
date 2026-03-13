# 🌶️ Tamil Nadu COMPLETE Slang Translator — Voice Edition

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white) 
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)

A highly sophisticated, voice-enabled translator designed to preserve and celebrate the rich linguistic diversity of all **38 districts** across Tamil Nadu. This project maps authentic street slang to their English and Tamil meanings using a modern, interactive web interface.

## 🚀 Live Demo
**Web App:** [https://tech-task-be-a-bash-2k26-b6gx.vercel.app/](https://tech-task-be-a-bash-2k26-b6gx.vercel.app/)

## ✨ Key Features
- **🎙️ Voice-to-Text Search:** Integrated Web Speech API allows users to search for slangs by simply speaking in Tamil or English.
- **🔊 Text-to-Speech (TTS):** Each search result includes a "Speak" function to hear the regional pronunciation or meaning.
- **📍 38 District Mapping:** From the *Madras Bashai* of North Chennai to the *Kumari Tamil* of Kanyakumari.
- **🔄 Dynamic Data Engine:** Powered by a CSV-to-JSON pipeline for lightning-fast search performance across 495+ entries.
- **📱 Responsive UI:** Modern CSS animations, gradients, and a mobile-friendly layout.

## 📍 Authentic Slang Highlights
- **Chennai:** *Bejaar, Naina, Gethu, Peter*
- **Coimbatore/Kongu:** Polite suffixes like *-nga* (*Ennanga, Angutu*)
- **Madurai:** *Ennappa, Podi-Paiya, Jigarthanda*
- **Nellai/Tirunelveli:** The iconic *Le* suffix and *Halwa-Maari*

## 🛠️ Tech Stack
- **Frontend:** HTML5, CSS3, ES6 JavaScript
- **Backend/Dashboard:** Python, Streamlit
- **Data Handling:** Pandas, JSON, CSV
- **Deployment:** Vercel (Static HTML), Streamlit Cloud (Python App)

## 📁 Project Structure
```text
├── app.py                  # Streamlit Dashboard application
├── index.html              # Main standalone Voice-Enabled Web App
├── slang_data.json         # Centralized database (495 entries)
├── slang_data/             # Individual CSV files per district (38 folders)
├── convert_csv_to_json.py  # Data processing pipeline script
├── slang_stats.txt         # Auto-generated statistics report
└── presentation.pptx       # Project presentation deck
```

## ⚙️ Local Setup
1. **Clone the Repo:**
   ```bash
   git clone <repo-url>
   ```
2. **Run the Streamlit App:**
   ```bash
   pip install streamlit pandas
   streamlit run app.py
   ```
3. **Run the Web Interface:**
   Simply open `index.html` in your browser (Chrome/Edge recommended for Voice API support).

## 📊 Statistics
A complete breakdown of slang counts per district can be found in `slang_stats.txt`.

---
**Developed for Tech Task BE A BASH 2K26**  
*Preserving Culture, One Slang at a Time.* 🌶️
