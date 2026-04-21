import streamlit as st
import yt_dlp
import whisper
from deep_translator import GoogleTranslator
import asyncio
from edge_tts import Communicate
import os

# --- 🛠️ SYSTEM SETTINGS ---
st.set_page_config(page_title="TECH_T | AI", layout="centered")

# --- 🎨 ADVANCED CSS DESIGN ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #0A0A0A; }
    
    /* Global Text Color */
    html, body, [class*="css"], p, span { color: #FFFFFF !important; }

    /* Title Styling */
    .header-box {
        text-align: center;
        padding: 40px 10px;
        background: linear-gradient(180deg, #111, #000);
        border-radius: 25px;
        border-bottom: 2px solid #00D1FF;
        margin-bottom: 30px;
    }
    
    .app-title {
        font-family: 'Segoe UI', sans-serif;
        font-size: 55px;
        font-weight: 800;
        background: linear-gradient(to right, #00D1FF, #007BFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        letter-spacing: 2px;
    }
    
    .dev-text {
        font-size: 14px;
        color: #888 !important;
        text-transform: uppercase;
        letter-spacing: 5px;
    }

    /* Input & Boxes Styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>textarea {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
    }

    /* Action Button */
    .stButton>button {
        background: #00D1FF !important;
        color: #000000 !important;
        font-weight: bold !important;
        width: 100%;
        height: 50px;
        border-radius: 12px !important;
        border: none !important;
        font-size: 18px !important;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background: #007BFF !important;
        color: #FFFFFF !important;
        transform: scale(1.02);
    }
    
    /* Result Box Styling */
    .result-card {
        background: #111111;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #222;
        margin-top: 20px;
    }
    </style>
    
    <div class="header-box">
        <h1 class="app-title">TECH_T</h1>
        <p class="dev-text">Developed By Tarbin</p>
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
tab1, tab2 = st.tabs(["[ 🎥 AI SCRIPT GENERATOR ]", "[ 🎙️ PREMIUM AI VOICE ]"])

# --- TAB 1: SCRIPT GEN ---
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    v_url = st.text_input("🔗 Video Link (YouTube, TikTok, FB, etc.)", placeholder="Paste link here...")
    
    col1, col2 = st.columns(2)
    with col1:
        lang_choice = st.selectbox("Output Language", ["မြန်မာ", "English", "Thai"])
    with col2:
        st.info("💡 Link မှမရပါက Video ကိုဒေါင်း၍ Upload တင်ပါ။")

    if st.button("RUN TECH_T ENGINE ✨"):
        if v_url:
            with st.status("⚙️ Tech_T AI Processing...", expanded=True) as status:
                try:
                    audio_fn = "temp_audio.mp3"
                    if os.path.exists(audio_fn): os.remove(audio_fn)
                    
                    status.write("🌐 Connecting to Server...")
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': 'temp_v',
                        'quiet': True,
                        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_url])
                    os.rename("temp_v.mp3", audio_fn)
                    
                    status.write("🧠 AI Transcribing...")
                    model = whisper.load_model("tiny")
                    result = model.transcribe(audio_fn)
                    
                    status.write("📝 Translating Content...")
                    target = "my" if lang_choice == "မြန်မာ" else "en"
                    final_txt = GoogleTranslator(source='auto', target=target).translate(result['text'])
                    
                    status.update(label="Process Complete!", state="complete")
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.subheader("Results:")
                    st.text_area("", final_txt, height=350)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    if os.path.exists(audio_fn): os.remove(audio_fn)
                except Exception as e:
                    st.error(f"Error: YouTube မှ ဒေါင်းလုဒ်ဆွဲခြင်းကို ပိတ်ထားပါသည်။ အခြားလင့်ဖြင့်စမ်းပါ သို့မဟုတ် ဗီဒီယိုတင်ပေးပါ။")
        else:
            st.warning("လင့်တစ်ခုခု အရင်ထည့်ပေးပါဗျာ။")

# --- TAB 2: VOICE GEN ---
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    v_input = st.text_area("Write Script for Voiceover", placeholder="မင်္ဂလာပါ...", height=200)
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        v_style = st.selectbox("Voice Style", ["Thiha (Male)", "Nilar (Female)"])
    
    if st.button("GENERATE AI AUDIO 🎧"):
        if v_input:
            async def generate():
                v_code = "my-MM-ThihaNeural" if "Thiha" in v_style else "my-MM-NilarNeural"
                comm = Communicate(v_input, v_code)
                await comm.save("v_out.mp3")
                st.audio("v_out.mp3")
            asyncio.run(generate())
        else:
            st.warning("စာသား အရင်ရိုက်ပေးပါ။")
