import streamlit as st
import yt_dlp
import whisper
from deep_translator import GoogleTranslator
import asyncio
from edge_tts import Communicate
import os

# --- 🎨 PREMIUM UI/UX CONFIGURATION ---
st.set_page_config(page_title="Tech_T", page_icon="⚡", layout="wide")

# Custom CSS for Modern UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main { background-color: #050505; }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(90deg, #121212 0%, #1e1e1e 100%);
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #333;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .app-title { color: #00D1FF; font-size: 42px; font-weight: 800; margin-bottom: 5px; }
    .dev-tag { color: #888; font-size: 14px; letter-spacing: 2px; }
    
    /* Card Styling */
    .feature-card {
        background: #111;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #222;
        transition: 0.3s;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(45deg, #00D1FF, #0076FF);
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { opacity: 0.8; transform: translateY(-2px); }
    
    /* Selectbox & Input */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    </style>
    
    <div class="header-container">
        <div class="app-title">TECH_T</div>
        <div class="dev-tag">DEVELOPED BY TARBIN</div>
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
tab1, tab2 = st.tabs(["🎥 VIDEO TO SCRIPT", "🎙️ AI VOICE SYNTHESIS"])

# --- FEATURE 1: MULTI-LINK SCRIPT GENERATOR ---
with tab1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("Any Link to Script")
    st.caption("Supports: YouTube, Facebook, TikTok, Rednote (Xiaohongshu)")
    
    col_input, col_lang = st.columns([2, 1])
    
    with col_input:
        video_url = st.text_input("Paste Video Link Here:", placeholder="https://...")
        uploaded_file = st.file_uploader("Or Upload Video File (၁၀၀% စိတ်ချရသည်):", type=["mp4", "mkv", "mov"])
        
    with col_lang:
        lang_options = {"မြန်မာ": "my", "English": "en", "Thai": "th", "Japanese": "ja", "Chinese": "zh-CN"}
        target_lang = st.selectbox("Translate To:", list(lang_options.keys()))
        model_size = st.select_slider("AI Accuracy (Tiny is faster)", options=["tiny", "base"], value="tiny")

    if st.button("GENERATE SCRIPT ✨"):
        if video_url or uploaded_file:
            with st.status("Tech_T AI Processing...", expanded=True) as status:
                try:
                    audio_path = "tech_t_audio.mp3"
                    
                    if uploaded_file:
                        st.write("📂 Processing Uploaded File...")
                        with open("temp_v.mp4", "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        os.system(f'ffmpeg -i temp_v.mp4 -vn -ar 44100 -ac 2 -b:a 192k {audio_path} -y')
                    else:
                        st.write("🌐 Extracting from Link (Bypassing Restrictions)...")
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': 'temp_v',
                            'quiet': True,
                            'nocheckcertificate': True,
                            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36',
                            'referer': 'https://www.google.com/',
                            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([video_url])
                        os.rename("temp_v.mp3", audio_path)

                    st.write("🧠 AI Transcribing (Whisper)...")
                    model = whisper.load_model(model_size)
                    result = model.transcribe(audio_path)
                    
                    st.write("📝 Translating Content...")
                    translated = GoogleTranslator(source='auto', target=lang_options[target_lang]).translate(result['text'])
                    
                    status.update(label="Complete!", state="complete")
                    
                    # RESULTS DISPLAY
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.info("Translated Script")
                        st.text_area("", translated, height=350, key="trans")
                    with res_col2:
                        st.info("Original Script")
                        st.text_area("", result['text'], height=350, key="orig")
                        
                    # Cleanup
                    if os.path.exists(audio_path): os.remove(audio_path)
                    if os.path.exists("temp_v.mp4"): os.remove("temp_v.mp4")

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.warning("မှတ်ချက်: Link မှမရပါက Video ကိုဒေါင်းပြီး 'Upload' လုပ်ပေးပါ။ Cloud Server Block ကြောင့်ဖြစ်နိုင်ပါသည်။")
        else:
            st.warning("Please provide a link or a file.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- FEATURE 2: AI VOICE ---
with tab2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("Professional Voiceover")
    voice_text = st.text_area("Enter Text:", placeholder="မင်္ဂလာပါ...")
    
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        v_gender = st.selectbox("Voice Style:", ["Thiha (Male)", "Nilar (Female)"])
    with v_col2:
        v_speed = st.slider("Pitch/Speed:", 0.8, 1.5, 1.0)
        
    if st.button("CREATE VOICE 🎧"):
        if voice_text:
            v_code = "my-MM-ThihaNeural" if "Thiha" in v_gender else "my-MM-NilarNeural"
            async def tts():
                c = Communicate(voice_text, v_code)
                await c.save("output.mp3")
            asyncio.run(tts())
            st.audio("output.mp3")
    st.markdown('</div>', unsafe_allow_html=True)
import streamlit as st
import yt_dlp
import whisper
from deep_translator import GoogleTranslator
import asyncio
from edge_tts import Communicate
import os

# --- 🎨 PREMIUM UI/UX CONFIGURATION ---
st.set_page_config(page_title="Tech_T", page_icon="⚡", layout="wide")

# Custom CSS for Modern UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main { background-color: #050505; }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(90deg, #121212 0%, #1e1e1e 100%);
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #333;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .app-title { color: #00D1FF; font-size: 42px; font-weight: 800; margin-bottom: 5px; }
    .dev-tag { color: #888; font-size: 14px; letter-spacing: 2px; }
    
    /* Card Styling */
    .feature-card {
        background: #111;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #222;
        transition: 0.3s;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(45deg, #00D1FF, #0076FF);
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { opacity: 0.8; transform: translateY(-2px); }
    
    /* Selectbox & Input */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    </style>
    
    <div class="header-container">
        <div class="app-title">TECH_T</div>
        <div class="dev-tag">DEVELOPED BY TARBIN</div>
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
tab1, tab2 = st.tabs(["🎥 VIDEO TO SCRIPT", "🎙️ AI VOICE SYNTHESIS"])

# --- FEATURE 1: MULTI-LINK SCRIPT GENERATOR ---
with tab1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("Any Link to Script")
    st.caption("Supports: YouTube, Facebook, TikTok, Rednote (Xiaohongshu)")
    
    col_input, col_lang = st.columns([2, 1])
    
    with col_input:
        video_url = st.text_input("Paste Video Link Here:", placeholder="https://...")
        uploaded_file = st.file_uploader("Or Upload Video File (၁၀၀% စိတ်ချရသည်):", type=["mp4", "mkv", "mov"])
        
    with col_lang:
        lang_options = {"မြန်မာ": "my", "English": "en", "Thai": "th", "Japanese": "ja", "Chinese": "zh-CN"}
        target_lang = st.selectbox("Translate To:", list(lang_options.keys()))
        model_size = st.select_slider("AI Accuracy (Tiny is faster)", options=["tiny", "base"], value="tiny")

    if st.button("GENERATE SCRIPT ✨"):
        if video_url or uploaded_file:
            with st.status("Tech_T AI Processing...", expanded=True) as status:
                try:
                    audio_path = "tech_t_audio.mp3"
                    
                    if uploaded_file:
                        st.write("📂 Processing Uploaded File...")
                        with open("temp_v.mp4", "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        os.system(f'ffmpeg -i temp_v.mp4 -vn -ar 44100 -ac 2 -b:a 192k {audio_path} -y')
                    else:
                        st.write("🌐 Extracting from Link (Bypassing Restrictions)...")
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': 'temp_v',
                            'quiet': True,
                            'nocheckcertificate': True,
                            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36',
                            'referer': 'https://www.google.com/',
                            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([video_url])
                        os.rename("temp_v.mp3", audio_path)

                    st.write("🧠 AI Transcribing (Whisper)...")
                    model = whisper.load_model(model_size)
                    result = model.transcribe(audio_path)
                    
                    st.write("📝 Translating Content...")
                    translated = GoogleTranslator(source='auto', target=lang_options[target_lang]).translate(result['text'])
                    
                    status.update(label="Complete!", state="complete")
                    
                    # RESULTS DISPLAY
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.info("Translated Script")
                        st.text_area("", translated, height=350, key="trans")
                    with res_col2:
                        st.info("Original Script")
                        st.text_area("", result['text'], height=350, key="orig")
                        
                    # Cleanup
                    if os.path.exists(audio_path): os.remove(audio_path)
                    if os.path.exists("temp_v.mp4"): os.remove("temp_v.mp4")

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.warning("မှတ်ချက်: Link မှမရပါက Video ကိုဒေါင်းပြီး 'Upload' လုပ်ပေးပါ။ Cloud Server Block ကြောင့်ဖြစ်နိုင်ပါသည်။")
        else:
            st.warning("Please provide a link or a file.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- FEATURE 2: AI VOICE ---
with tab2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("Professional Voiceover")
    voice_text = st.text_area("Enter Text:", placeholder="မင်္ဂလာပါ...")
    
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        v_gender = st.selectbox("Voice Style:", ["Thiha (Male)", "Nilar (Female)"])
    with v_col2:
        v_speed = st.slider("Pitch/Speed:", 0.8, 1.5, 1.0)
        
    if st.button("CREATE VOICE 🎧"):
        if voice_text:
            v_code = "my-MM-ThihaNeural" if "Thiha" in v_gender else "my-MM-NilarNeural"
            async def tts():
                c = Communicate(voice_text, v_code)
                await c.save("output.mp3")
            asyncio.run(tts())
            st.audio("output.mp3")
    st.markdown('</div>', unsafe_allow_html=True)
