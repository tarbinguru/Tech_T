import streamlit as st
import yt_dlp
import whisper
from deep_translator import GoogleTranslator
import asyncio
from edge_tts import Communicate
import os

# --- 🎭 NEXTGEN PREMIUM UI CONFIG ---
st.set_page_config(page_title="TECH_T | NEXTGEN AI", page_icon="🔮", layout="wide")

# Custom CSS for NextGen Glassmorphism Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    .stApp {
        background: linear-gradient(160deg, #0f172a 0%, #1e1b4b 100%);
        font-family: 'Inter', sans-serif;
        color: #f8fafc;
    }

    /* Professional Card Container */
    .app-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 35px;
        margin-top: 20px;
    }

    /* Branding Section */
    .branding-box {
        text-align: left;
        margin-bottom: 30px;
        border-left: 4px solid #6366f1;
        padding-left: 20px;
    }
    .main-title {
        font-size: 32px; font-weight: 800;
        background: linear-gradient(90deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-title { color: #94a3b8; font-size: 14px; letter-spacing: 1px; }

    /* Input/Box Styling */
    div[data-baseweb="select"] > div, .stTextArea textarea, .stTextInput input {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    /* Premium Button */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        height: 50px !important;
        font-weight: 600 !important;
        transition: 0.3s;
        width: 100%;
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(99, 102, 241, 0.4);
    }
    
    /* Sidebar/Drawer Style */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.9);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
    
    <div class="branding-box">
        <h1 class="main-title">NEXTGEN TECH_T</h1>
        <p class="sub-title">STUDIO-GRADE AI ENGINE | DEVELOPED BY TARBIN</p>
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
tab1, tab2 = st.tabs(["🎥 TRANSCRIPT AI", "🎙️ PREMIUM VOICE TTS"])

# --- TAB 1: TRANSCRIPT ENGINE ---
with tab1:
    with st.container():
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        
        with col1:
            v_url = st.text_input("Video Link Input (YouTube, FB, TikTok, Rednote)", placeholder="Paste link here...")
            up_file = st.file_uploader("Or Upload Media File", type=['mp4', 'mov', 'mp3'])
        
        with col2:
            out_lang = st.selectbox("Output Translation", ["Burmese (မြန်မာ)", "English (US)", "Thai"])
            accuracy = st.select_slider("AI Precision", options=["Lite (Fast)", "Standard", "Pro (Deep)"])

        if st.button("EXECUTE AI PROCESSING ✨"):
            if v_url or up_file:
                with st.status("Initializing NextGen AI Model...", expanded=True) as status:
                    try:
                        aud_path = "tech_t_core.mp3"
                        if up_file:
                            status.write("📂 Loading Local File...")
                            with open("temp_media", "wb") as f: f.write(up_file.getbuffer())
                            os.system(f'ffmpeg -i temp_media -vn -ar 44100 -ac 2 -b:a 192k {aud_path} -y')
                        else:
                            status.write("🌐 Fetching Remote Data...")
                            ydl_opts = {
                                'format': 'bestaudio/best', 'outtmpl': 'temp', 'quiet': True,
                                'nocheckcertificate': True,
                                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]
                            }
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([v_url])
                            os.rename("temp.mp3", aud_path)

                        status.write("🧠 Whisper Model Transcribing...")
                        model_type = "tiny" if "Lite" in accuracy else "base"
                        model = whisper.load_model(model_type)
                        result = model.transcribe(aud_path)
                        
                        status.write("🌍 Global Translation Engine Active...")
                        t_code = "my" if "Burmese" in out_lang else "en"
                        final_text = GoogleTranslator(source='auto', target=t_code).translate(result['text'])
                        
                        status.update(label="Process Complete ✅", state="complete")
                        st.subheader("Final Output")
                        st.text_area("Resulting Script", final_text, height=300)
                    except Exception as e:
                        st.error("Error: Server block ကြောင့် Link မရပါ။ Video ကို Download ဆွဲပြီး 'Upload' လုပ်ပေးပါ။")
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: PREMIUM VOICE ENGINE ---
with tab2:
    with st.container():
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        
        # Text Input (No Limit)
        v_input = st.text_area("Script Input (Burmese Supported - No Word Limit)", height=200, placeholder="ဒီမှာ စာသားများကို ကန့်သတ်ချက်မရှိ ရိုက်ထည့်နိုင်သည်...")
        
        st.divider()
        
        c_v1, c_v2, c_v3 = st.columns(3)
        with c_v1:
            st.markdown("### 🧬 AI Voice Model")
            v_model = st.radio("Select Persona", 
                ["Thiha (Male - Pro)", "Nilar (Female - Pro)", "Narrator (Storytelling)", "Horror/Deep (Echo)"],
                index=0)
        
        with c_v2:
            st.markdown("### 🎭 Emotional Delivery")
            v_emotion = st.selectbox("Tone Style", ["Natural", "Energetic", "Calm/Serious", "Storytelling", "Spooky"])
        
        with c_v3:
            st.markdown("### ⚙️ Audio Tuning")
            v_speed = st.slider("Speech Rate", 0.5, 2.0, 1.0)
            v_pitch = st.slider("Voice Pitch", -20, 20, 0)

        if st.button("GENERATE PREMIUM VOICE 🎧"):
            if v_input:
                async def build_voice():
                    # Voice Mapping
                    v_code = "my-MM-ThihaNeural"
                    if "Nilar" in v_model: v_code = "my-MM-NilarNeural"
                    elif "Narrator" in v_model: v_code = "en-US-ChristopherNeural"
                    
                    # Pitch/Speed Logic
                    rate_str = f"{'+' if v_speed>=1 else ''}{(v_speed-1)*100:.0f}%"
                    pitch_str = f"{'+' if v_pitch>=0 else ''}{v_pitch}Hz"
                    
                    # Spooky Effect
                    if "Horror" in v_model or "Spooky" in v_emotion:
                        pitch_str = "-15Hz"
                        rate_str = "-10%"

                    comm = Communicate(v_input, v_code, rate=rate_str, pitch=pitch_str)
                    await comm.save("nextgen_output.mp3")
                    st.audio("nextgen_output.mp3")
                    st.success("Audio synthesized successfully.")
                
                asyncio.run(build_voice())
            else:
                st.warning("Please enter text to synthesize.")
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><p style='text-align: center; color: #64748b;'>© 2026 TECH_T NEXTGEN AI. All Rights Reserved.</p>", unsafe_allow_html=True)
