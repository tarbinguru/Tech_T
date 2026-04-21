import streamlit as st
import yt_dlp
import whisper
from deep_translator import GoogleTranslator
import asyncio
from edge_tts import Communicate
import os
from PIL import Image

# --- 🚀 ELITE SYSTEM CONFIG ---
st.set_page_config(page_title="TECH_T | AI", page_icon="🧬", layout="wide")

# Custom Professional CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;700&display=swap');
    
    /* Background & Global Text */
    .stApp {
        background: linear-gradient(135deg, #050505 0%, #0a0a15 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Header & Branding */
    .header-box {
        text-align: center;
        padding: 50px 0;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 0 0 40px 40px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 40px;
    }
    
    .main-title {
        font-size: 80px; font-weight: 800;
        background: linear-gradient(90deg, #00D1FF, #7000FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -3px;
        margin-bottom: 0;
    }
    
    .dev-by { color: #888; font-size: 14px; letter-spacing: 5px; text-transform: uppercase; }

    /* Tabs UI */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        color: #fff !important;
        padding: 12px 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    .stTabs [aria-selected="true"] { background: #00D1FF !important; color: #000 !important; border: none !important; }

    /* Action Button - High Contrast */
    .stButton>button {
        background: #00D1FF !important;
        color: #000 !important;
        border-radius: 15px !important;
        height: 60px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        border: none !important;
        box-shadow: 0 0 20px rgba(0, 209, 255, 0.3);
        width: 100%;
    }
    
    /* Input Boxes Visibility */
    .stTextInput input, .stTextArea textarea, .stSelectbox div {
        background: #121212 !important;
        color: #FFFFFF !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
    }
    </style>
    
    <div class="header-box">
        <h1 class="main-title">TECH_T</h1>
        <p class="dev-by">DEVELOPED BY TARBIN</p>
    </div>
    """, unsafe_allow_html=True)

# --- APP NAVIGATION ---
tab1, tab2 = st.tabs(["[ 🎥 TRANSCRIPT AI ]", "[ 🎙️ VOICE SYNTH ]"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    
    with c1:
        v_url = st.text_input("🔗 Paste Social Media Link (YT, FB, TT, Rednote)", placeholder="https://...")
        up_file = st.file_uploader("📁 Or Upload Video File (100% Success Rate)", type=['mp4', 'mkv', 'mov'])
        
    with c2:
        out_lang = st.selectbox("Output Language", ["Burmese (မြန်မာ)", "English", "Thai"])
        ai_speed = st.select_slider("AI Engine", options=["Lite", "Standard"])

    if st.button("PROCESS TECH_T INTELLIGENCE"):
        if v_url or up_file:
            with st.status("🛠️ System Active. Initializing AI...", expanded=True) as s:
                try:
                    aud_path = "tech_t_temp.mp3"
                    
                    if up_file:
                        s.write("📂 Processing File Data...")
                        with open("temp.mp4", "wb") as f: f.write(up_file.getbuffer())
                        os.system(f'ffmpeg -i temp.mp4 -vn -ar 44100 -ac 2 -b:a 192k {aud_path} -y')
                    else:
                        s.write("🌐 Accessing Remote Stream...")
                        ydl_opts = {
                            'format': 'bestaudio/best', 'outtmpl': 'temp', 'quiet': True,
                            'nocheckcertificate': True,
                            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36',
                            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_url])
                        os.rename("temp.mp3", aud_path)

                    s.write("🧠 AI Transcription Engine (Whisper)...")
                    model = whisper.load_model("tiny")
                    result = model.transcribe(aud_path)
                    
                    s.write("📝 Finalizing Translation...")
                    t_dest = "my" if "Burmese" in out_lang else "en"
                    final_script = GoogleTranslator(source='auto', target=t_dest).translate(result['text'])
                    
                    s.update(label="System Finished!", state="complete")
                    st.success("✅ Script successfully generated.")
                    st.text_area("Final Transcript", final_script, height=400)
                    
                    if os.path.exists(aud_path): os.remove(aud_path)
                except Exception as e:
                    st.error("🚫 Link Blocked. Please download the video and 'Upload' directly to TECH_T.")
        else:
            st.warning("Input required.")

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    v_txt = st.text_area("Enter Text for Professional Voiceover", height=200, placeholder="ဒီမှာ စာရိုက်ပါ...")
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        v_sel = st.selectbox("Select Voice Identity", ["Male (Thiha)", "Female (Nilar)"])
    
    if st.button("SYNTHESIZE AUDIO 🎧"):
        if v_txt:
            async def run_tts():
                v_code = "my-MM-ThihaNeural" if "Male" in v_sel else "my-MM-NilarNeural"
                comm = Communicate(v_txt, v_code)
                await comm.save("voice.mp3")
                st.audio("voice.mp3")
            asyncio.run(run_tts())
        else:
            st.warning("Empty text field.")
