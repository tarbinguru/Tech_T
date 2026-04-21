import streamlit as st
import yt_dlp
import whisper
from deep_translator import GoogleTranslator
import asyncio
from edge_tts import Communicate
import os
import time

# --- 💡 LIGHT MODE & VISIBILITY CONFIG ---
st.set_page_config(page_title="TECH_T | PRO", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* အဖြူရောင်နောက်ခံနှင့် အနက်ရောင်စာသား (မြင်သာစေရန်) */
    .stApp { background-color: #FFFFFF; color: #000000; }
    
    /* Title Styling */
    .main-header {
        text-align: center;
        padding: 30px;
        background: #F0F4F8;
        border-radius: 20px;
        color: #1A73E8;
        font-family: 'Arial', sans-serif;
        border-bottom: 5px solid #1A73E8;
    }

    /* Card Box */
    .content-card {
        background: #FFFFFF;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #E0E0E0;
        margin-top: 20px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #1A73E8 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        height: 50px;
        width: 100%;
    }
    
    /* Text Input Visibility */
    input, textarea, [data-baseweb="select"] {
        background-color: #F8F9FA !important;
        color: #000000 !important;
        border: 1px solid #CED4DA !important;
    }
    </style>
    
    <div class="main-header">
        <h1 style="margin:0;">TECH_T NEXTGEN</h1>
        <p style="color:#555;">PREMIUM AI STUDIO | BY TARBIN</p>
    </div>
    """, unsafe_allow_html=True)

# --- TABS ---
tab1, tab2 = st.tabs(["🎥 ဗီဒီယိုမှ စာသားထုတ်ယူရန်", "🎙️ AI အသံဖန်တီးရန် (TTS)"])

# --- TAB 1: TRANSCRIPT ---
with tab1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    v_url = st.text_input("🔗 ဗီဒီယို လင့်ခ်ထည့်ပါ (YouTube, FB, TikTok, Rednote)", placeholder="https://...")
    up_file = st.file_uploader("📁 သို့မဟုတ် ဖိုင်တင်ပါ", type=['mp4', 'mp3'])
    
    if st.button("RUN TRANSCRIPTION ✨"):
        if v_url or up_file:
            with st.status("🚀 စနစ်စတင်နေပါပြီ...", expanded=True) as status:
                # Progress Bar ပြခြင်း
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                status.write("🧠 AI က စာသားများကို ဖတ်နေပါသည်...")
                # (ဒီနေရာမှာ အပေါ်က လုပ်ငန်းစဉ် Code များ ထည့်သွင်းရန်)
                status.update(label="ပြီးဆုံးပါပြီ!", state="complete")
        else:
            st.warning("လင့်ခ် သို့မဟုတ် ဖိုင် ထည့်ပေးပါ။")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: VOICE ENGINE ---
with tab2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    
    # No word limit text area
    v_input = st.text_area("ပြောစေလိုသော စာသားများ (ကန့်သတ်ချက်မရှိ)", height=250, placeholder="ဒီမှာ ရိုက်ထည့်ပါ...")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        v_model = st.selectbox("👤 အသံရွေးချယ်ရန်", ["အမျိုးသား (ဦးသီဟ)", "အမျိုးသမီး (မနီလာ)", "ပုံပြောသူ (Narrator)"])
    with c2:
        v_emotion = st.selectbox("🎭 အသံနေအသံထား", ["ပုံမှန်", "တက်ကြွသော", "အေးဆေးသော", "ပုံပြောဟန်", "လေးနက်သော"])
    with c3:
        v_speed = st.slider("⚡ အမြန်နှုန်း", 0.5, 2.0, 1.0)

    if st.button("GENERATE PREMIUM VOICE 🎧"):
        if v_input:
            # အလုပ်လုပ်နေတဲ့ Animation ပြခြင်း
            with st.spinner('🤖 AI အသံဖိုင် ဖန်တီးနေပါသည်... ခဏစောင့်ပေးပါ'):
                # Progress bar လေး ပြေးနေတဲ့ပုံ
                my_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.02)
                    my_bar.progress(percent_complete + 1)
                
                async def build_voice():
                    v_code = "my-MM-ThihaNeural" if "သီဟ" in v_model else "my-MM-NilarNeural"
                    rate = f"{'+' if v_speed>=1 else ''}{(v_speed-1)*100:.0f}%"
                    
                    communicate = Communicate(v_input, v_code, rate=rate)
                    await communicate.save("output_final.mp3")
                    st.audio("output_final.mp3")
                    st.success("✅ အသံဖိုင် ဖန်တီးပြီးပါပြီ!")
                
                asyncio.run(build_voice())
        else:
            st.warning("စာသား အရင်ရိုက်ပါ။")
    st.markdown('</div>', unsafe_allow_html=True)
