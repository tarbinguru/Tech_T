import streamlit as st
import yt_dlp
import whisper
from deep_translator import GoogleTranslator
import asyncio
from edge_tts import Communicate
import os

# --- 🚀 ULTRA-PREMIUM UI SETUP ---
st.set_page_config(page_title="Tech_T", page_icon="⚡", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;700&display=swap');
    
    .main { background-color: #050505; }
    
    /* App Title with Neon Effect */
    .app-name {
        font-family: 'Orbitron', sans-serif;
        font-size: 60px;
        font-weight: 900;
        background: linear-gradient(90deg, #00F2FF, #007BFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: -20px;
    }
    
    .dev-by {
        color: #555;
        text-align: center;
        letter-spacing: 5px;
        font-size: 12px;
        margin-bottom: 40px;
    }
    
    /* Glassmorphism Cards */
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) {
        background: rgba(20, 20, 20, 0.8);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #222;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(45deg, #00F2FF, #007BFF) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        height: 50px;
        font-weight: bold;
        transition: 0.3s;
    }
    
    /* Hide Error Message box red background */
    .stAlert { border-radius: 15px; border: none; }
    </style>
    
    <div class="app-name">TECH_T</div>
    <div class="dev-by">DEVELOPED BY TARBIN</div>
    """, unsafe_allow_html=True)

# --- APP LOGIC ---
tab1, tab2 = st.tabs(["🎥 AI VIDEO SCRIPT", "🎙️ PREMIUM VOICE"])

with tab1:
    st.subheader("Link to Script (YouTube, FB, TikTok)")
    link = st.text_input("Video URL ကို ဒီမှာထည့်ပါ", placeholder="https://...")
    target_l = st.selectbox("ဘာသာစကားရွေးပါ", ["မြန်မာ", "English", "Thai"])
    
    if st.button("RUN TECH_T AI ✨"):
        if link:
            with st.spinner("AI စနစ်ဖြင့် အလုပ်လုပ်နေပါပြီ..."):
                try:
                    # အရင်ဖိုင်ဟောင်းရှိရင် ဖျက်မယ်
                    if os.path.exists("t_audio.mp3"): os.remove("t_audio.mp3")
                    
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': 't_audio.%(ext)s',
                        'quiet': True,
                        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([link])
                    
                    model = whisper.load_model("tiny")
                    res = model.transcribe("t_audio.mp3")
                    
                    dest_lang = "my" if target_l == "မြန်မာ" else "en"
                    translated = GoogleTranslator(source='auto', target=dest_lang).translate(res['text'])
                    
                    st.success("အောင်မြင်စွာ ပြီးဆုံးပါပြီ")
                    st.text_area("ရလဒ်", translated, height=300)
                    
                except Exception as e:
                    st.error("⚠️ Server က လင့်ကို ပိတ်ထားပါသည်။ ဗီဒီယိုကို ဖုန်းထဲဒေါင်းပြီး Upload လုပ်သည့် စနစ်ကို စမ်းသုံးကြည့်ပါ။")

with tab2:
    st.subheader("Text to Professional Voice")
    v_text = st.text_area("စာသားများ ရိုက်ထည့်ပါ", height=150)
    if st.button("GENERATE VOICE 🎧"):
        if v_text:
            async def run_v():
                c = Communicate(v_text, "my-MM-ThihaNeural")
                await c.save("v.mp3")
                st.audio("v.mp3")
            asyncio.run(run_v())
