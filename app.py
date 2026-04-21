import streamlit as st
import yt_dlp
import whisper
from deep_translator import GoogleTranslator
import asyncio
from edge_tts import Communicate
import os

# --- 💡 PROFESSIONAL LIGHT UI CONFIG ---
st.set_page_config(page_title="TECH_T | AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Light Mode Professional Background */
    .stApp { background-color: #F8F9FA; }
    
    /* Header Container */
    .main-header {
        text-align: center;
        padding: 40px;
        background: #FFFFFF;
        border-radius: 0 0 30px 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }
    
    .app-title {
        font-size: 55px; font-weight: 800;
        color: #1A73E8; /* Premium Blue */
        margin-bottom: 5px;
        letter-spacing: -1px;
    }
    
    .dev-label {
        color: #5F6368; font-size: 13px; font-weight: 600;
        text-transform: uppercase; letter-spacing: 4px;
    }

    /* Cards & Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background: #FFFFFF !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 12px !important;
        color: #3C4043 !important;
        padding: 10px 25px !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: #1A73E8 !important;
        color: white !important;
        border: none !important;
    }

    /* Input Styling for Visibility */
    .stTextInput input, .stTextArea textarea, .stSelectbox div {
        background: #FFFFFF !important;
        color: #202124 !important;
        border: 1px solid #DADCE0 !important;
        border-radius: 10px !important;
    }
    
    /* Professional Action Button */
    .stButton>button {
        background: #1A73E8 !important;
        color: white !important;
        border-radius: 12px !important;
        height: 55px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        width: 100%;
        border: none !important;
        box-shadow: 0 4px 10px rgba(26, 115, 232, 0.2);
    }
    </style>
    
    <div class="main-header">
        <h1 class="app-title">TECH_T</h1>
        <p class="dev-label">Developed By Tarbin</p>
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
tab1, tab2 = st.tabs(["🎥 TRANSCRIPT AI", "🎙️ ADVANCED VOICE ENGINE"])

# --- TAB 1: SCRIPT GEN ---
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        v_url = st.text_input("🔗 Video Link (YouTube, TikTok, FB, etc.)", placeholder="Paste URL...")
        up_file = st.file_uploader("📁 Or Upload Video (၁၀၀% စိတ်ချရသည်)", type=['mp4', 'mov'])
    with c2:
        out_l = st.selectbox("Output Language", ["မြန်မာ", "English", "Thai"])
        st.info("💡 Link မရလျှင် ဗီဒီယိုတင်ပေးပါ။")

    if st.button("RUN ENGINE"):
        if v_url or up_file:
            with st.spinner("AI Processing..."):
                try:
                    aud = "t_audio.mp3"
                    if up_file:
                        with open("tmp.mp4", "wb") as f: f.write(up_file.getbuffer())
                        os.system(f'ffmpeg -i tmp.mp4 -vn -ar 44100 -ac 2 -b:a 192k {aud} -y')
                    else:
                        ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'tmp', 'quiet': True,
                                    'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]}
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_url])
                        os.rename("tmp.mp3", aud)
                    
                    model = whisper.load_model("tiny")
                    res = model.transcribe(aud)
                    trans = GoogleTranslator(source='auto', target='my' if out_l=="မြန်မာ" else "en").translate(res['text'])
                    st.success("ပြီးဆုံးပါပြီ")
                    st.text_area("Result", trans, height=350)
                except Exception as e:
                    st.error("လင့်ပိတ်ထားပါသည်။ ဗီဒီယိုဖိုင်တင်ပေးပါ။")

# --- TAB 2: ADVANCED VOICE (MULTIPLE STYLES) ---
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    v_txt = st.text_area("အသံပြောင်းရန် စာသားများရိုက်ထည့်ပါ", height=150, placeholder="ဒီမှာ ရေးပါ...")
    
    col_a, col_b = st.columns(2)
    with col_a:
        # အမျိုးမျိုးသော အသံပုံစံများကို ရွေးချယ်နိုင်ရန် စီစဉ်ထားသည်
        v_style = st.selectbox("အသံပုံစံ ရွေးချယ်ပါ (Voice Style)", [
            "အမျိုးသား - ပုံမှန် (Thiha)", 
            "အမျိုးသမီး - ပုံမှန် (Nilar)",
            "အမျိုးသား - Story ပြောရန် (Narrator)", 
            "အမျိုးသမီး - Story ပြောရန် (Narrator)",
            "ခြောက်ခြားဖွယ်/ထူးခြားအသံ (Deep Echo)"
        ])
    
    with col_b:
        v_speed = st.select_slider("အသံအမြန်နှုန်း (Speed)", options=["0.8x", "1.0x (Normal)", "1.2x", "1.5x"], value="1.0x (Normal)")

    if st.button("GENERATE AI VOICE 🎧"):
        if v_txt:
            async def generate_voice():
                # အသံပုံစံအလိုက် Code များ သတ်မှတ်ခြင်း
                styles = {
                    "အမျိုးသား - ပုံမှန် (Thiha)": "my-MM-ThihaNeural",
                    "အမျိုးသမီး - ပုံမှန် (Nilar)": "my-MM-NilarNeural",
                    "အမျိုးသား - Story ပြောရန် (Narrator)": "en-US-ChristopherNeural", # မြန်မာစာဆိုလျှင် Thiha ပဲ သုံးရမည် (Engine ကန့်သတ်ချက်အရ)
                    "အမျိုးသမီး - Story ပြောရန် (Narrator)": "en-US-JennyNeural",
                    "ခြောက်ခြားဖွယ်/ထူးခြားအသံ (Deep Echo)": "my-MM-ThihaNeural"
                }
                v_code = styles[v_style]
                
                # Speed ချိန်ညှိခြင်း
                rate = "+0%"
                if "0.8x" in v_speed: rate = "-20%"
                elif "1.2x" in v_speed: rate = "+20%"
                elif "1.5x" in v_speed: rate = "+50%"
                
                # ခြောက်ခြားဖွယ်အတွက် Pitch ကို လျှော့ချခြင်း
                pch = "-0Hz"
                if "ခြောက်ခြားဖွယ်" in v_style: pch = "-25Hz"

                comm = Communicate(v_txt, v_code, rate=rate, pitch=pch)
                await comm.save("gen_v.mp3")
                st.audio("gen_v.mp3")
            
            asyncio.run(generate_voice())
        else:
            st.warning("စာသား အရင်ရိုက်ပါ။")
