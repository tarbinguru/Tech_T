import streamlit as st
import yt_dlp
import whisper
from deep_translator import GoogleTranslator
import asyncio
from edge_tts import Communicate
import os

# --- 🎨 ADVANCED UI/UX DESIGN ---
st.set_page_config(page_title="Tech_T AI Premium", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stTextInput>div>div>input { border-radius: 10px; }
    .dev-card {
        background: linear-gradient(45deg, #1f2129, #2d2f39);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #3e4149;
        margin-bottom: 25px;
    }
    </style>
    <div class="dev-card">
        <h1 style="color: #FF4B4B; margin-bottom: 0;">🚀 Tech_T AI v2.0</h1>
        <p style="color: #9ea0a9;">Elite Transcription & Voice Synthesis</p>
        <p style="background: #FF4B4B; display: inline-block; padding: 2px 10px; border-radius: 5px; font-size: 12px;">Developed By Tarbin</p>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("Settings")
    mode = st.selectbox("Feature ရွေးချယ်ပါ", ["🎬 Video To Script", "🎙 AI Voice Gen"])
    st.divider()
    st.caption("Status: Server Online 🟢")

# --- FEATURE 1: VIDEO TO SCRIPT ---
if mode == "🎬 Video To Script":
    st.subheader("Extract Script from Video")
    
    # YouTube က block တာကျော်ဖို့ Option နှစ်ခုပေးထားပါတယ်
    input_type = st.radio("အသုံးပြုမည့်နည်းလမ်း:", ["Video Link", "Upload Video File (ပိုစိတ်ချရသည်)"])
    
    lang_map = {"မြန်မာ": "my", "English": "en", "Thai": "th", "Japanese": "ja", "Chinese": "zh-CN"}
    target_lang = st.selectbox("ဘာသာပြန်ရန် ဘာသာစကား ရွေးပါ", list(lang_map.keys()))

    source = None
    if input_type == "Video Link":
        source = st.text_input("YouTube / FB / TikTok Link ထည့်ပါ")
    else:
        source = st.file_uploader("ဗီဒီယိုဖိုင် ရွေးပါ", type=["mp4", "mkv", "mov", "avi"])

    if st.button("Start AI Process ✨"):
        if source:
            with st.status("AI က လုပ်ဆောင်နေပါပြီ...", expanded=True) as status:
                try:
                    audio_path = "processed_audio.mp3"
                    
                    if input_type == "Video Link":
                        st.write("🌐 ဗီဒီယိုမှ အသံဖိုင်ကို ဒေါင်းလုဒ်ဆွဲနေသည်...")
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': 'temp_v',
                            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
                            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36'
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([source])
                        os.rename("temp_v.mp3", audio_path)
                    else:
                        st.write("📁 ဖိုင်မှ အသံကို ထုတ်ယူနေသည်...")
                        with open("temp_file.mp4", "wb") as f:
                            f.write(source.getbuffer())
                        os.system(f'ffmpeg -i temp_file.mp4 -vn -ar 44100 -ac 2 -b:a 192k {audio_path} -y')

                    st.write("🧠 AI စနစ်ဖြင့် စာသားပြောင်းနေသည် (Whisper)...")
                    model = whisper.load_model("tiny")
                    result = model.transcribe(audio_path)
                    
                    st.write("📝 ဘာသာပြန်ဆိုနေသည်...")
                    translated = GoogleTranslator(source='auto', target=lang_map[target_lang]).translate(result['text'])
                    
                    status.update(label="Process ပြီးဆုံးပါပြီ!", state="complete", expanded=False)
                    
                    st.success("✅ Script ထွက်လာပါပြီ")
                    tab1, tab2 = st.tabs(["ဘာသာပြန်", "မူရင်း"])
                    tab1.text_area("Translated", translated, height=250)
                    tab2.text_area("Original", result['text'], height=250)
                    
                    # Clean up
                    if os.path.exists(audio_path): os.remove(audio_path)
                    if os.path.exists("temp_file.mp4"): os.remove("temp_file.mp4")

                except Exception as e:
                    st.error(f"Error: YouTube မှ ဒေါင်းလုဒ်ဆွဲ၍မရပါ။ (Cloud Server Block ဖြစ်နေခြင်း)\nအကြံပြုချက်: ဗီဒီယိုကို ဖုန်းထဲဒေါင်းပြီး 'Upload File' စနစ်ဖြင့် သုံးပေးပါ။")
        else:
            st.warning("Input တစ်ခုခု ထည့်ပေးပါ။")

# --- FEATURE 2: AI VOICE GEN ---
elif mode == "🎙 AI Voice Gen":
    st.subheader("Professional AI Voiceover")
    txt = st.text_area("စာသားများ ရိုက်ထည့်ပါ", placeholder="မင်္ဂလာပါ... Tech_T မှ ကြိုဆိုပါတယ်")
    
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
    with col2:
        speed = st.slider("Speed", 0.5, 2.0, 1.0)

    if st.button("Generate Audio 🎧"):
        if txt:
            v_code = "my-MM-ThihaNeural" if gender == "Male" else "my-MM-NilarNeural"
            async def run_tts():
                comm = Communicate(txt, v_code)
                await comm.save("output.mp3")
            asyncio.run(run_tts())
            st.audio("output.mp3")
        else:
            st.warning("စာသား အရင်ရေးပါ")
