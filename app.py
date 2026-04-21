import streamlit as st
import yt_dlp
import whisper
from deep_translator import GoogleTranslator
import asyncio
from edge_tts import Communicate
import os

# --- UI CONFIG ---
st.set_page_config(page_title="TECH_T | NEXTGEN AI", page_icon="🔮", layout="wide")

# Custom CSS for Visibility and Modern Look
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0e14;
        color: #ffffff;
    }
    /* Card Style */
    .option-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .main-header {
        font-size: 35px;
        font-weight: bold;
        color: #7000ff;
        text-shadow: 0px 0px 10px rgba(112, 0, 255, 0.5);
    }
    /* Input Text Area */
    .stTextArea textarea {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-header">NEXTGEN TECH_T</h1>', unsafe_allow_html=True)
st.write("STUDIO-GRADE AI ENGINE | DEVELOPED BY TARBIN")

# --- TABS ---
tab1, tab2 = st.tabs(["🎥 ဗီဒီယိုမှ စာသားထုတ်ယူရန်", "🎙️ AI အသံဖန်တီးရန် (TTS)"])

with tab1:
    st.markdown('<div class="option-card">', unsafe_allow_html=True)
    v_url = st.text_input("ဗီဒီယို လင့်ခ်ထည့်ပါ (YouTube, FB, TikTok)", placeholder="https://...")
    up_file = st.file_uploader("သို့မဟုတ် ဖိုင်တင်ပါ", type=['mp4', 'mp3'])
    
    out_lang = st.selectbox("ဘာသာပြန်မည့် ဘာသာစကား", ["မြန်မာ", "English", "Thai"])
    
    if st.button("စတင် လုပ်ဆောင်မည် ✨"):
        st.info("AI လုပ်ဆောင်နေပါသည်... ခဏစောင့်ပေးပါ။")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="option-card">', unsafe_allow_html=True)
    
    # Text Input with No Limit
    v_input = st.text_area("ပြောစေလိုသော စာသားများကို ရိုက်ထည့်ပါ (စာလုံးရေ ကန့်သတ်ချက်မရှိ)", 
                           height=250, 
                           placeholder="ဒီမှာ စာသားများကို ကြိုက်သလောက် အရှည်ကြီး ရေးသားနိုင်ပါသည်။")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 အသံရွေးချယ်ရန်")
        v_model = st.radio("အသံ အမျိုးအစား", 
                          ["အမျိုးသား - ဦးသီဟ (Thiha)", 
                           "အမျိုးသမီး - မနီလာ (Nilar)", 
                           "ပုံပြောသူ (Narrator)"], index=0)
    
    with col2:
        st.subheader("🎭 အသံနေအသံထား (Emotional)")
        # Box selection for Emotions
        v_emotion = st.selectbox("အသံထွက် ပုံစံရွေးပါ", 
                                ["ပုံမှန် (Natural)", 
                                 "တက်ကြွသော (Energetic)", 
                                 "အေးဆေးသော (Calm)", 
                                 "ပုံပြောဟန် (Storytelling)", 
                                 "လေးနက်သော (Serious)"])
    
    st.divider()
    
    # Tuning Controls
    c1, c2 = st.columns(2)
    with c1:
        v_speed = st.slider("အသံ အမြန်နှုန်း (Speed)", 0.5, 2.0, 1.0)
    with c2:
        v_pitch = st.slider("အသံ အနိမ့်အမြင့် (Pitch)", -20, 20, 0)

    if st.button("PREMIUM AI အသံထုတ်မည် 🎧"):
        if v_input:
            async def generate_audio():
                # Logic for Voice Selection
                v_code = "my-MM-ThihaNeural" if "Thiha" in v_model else "my-MM-NilarNeural"
                if "Narrator" in v_model: v_code = "en-US-ChristopherNeural"
                
                # Speed/Pitch formatting
                rate = f"{'+' if v_speed>=1 else ''}{(v_speed-1)*100:.0f}%"
                pitch = f"{'+' if v_pitch>=0 else ''}{v_pitch}Hz"

                try:
                    communicate = Communicate(v_input, v_code, rate=rate, pitch=pitch)
                    await communicate.save("output.mp3")
                    st.audio("output.mp3")
                    st.success("အသံဖိုင် ဖန်တီးမှု အောင်မြင်ပါသည်။")
                except Exception as e:
                    st.error(f"အမှားအယွင်း ရှိနေပါသည်: {e}")
            
            asyncio.run(generate_audio())
        else:
            st.warning("စာသား အရင်ရိုက်ထည့်ပေးပါ။")
            
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: gray;'>© 2026 TECH_T NEXTGEN AI. All Rights Reserved.</p>", unsafe_allow_html=True)
