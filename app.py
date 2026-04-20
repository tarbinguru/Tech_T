import streamlit as st
import yt_dlp
import whisper
from deep_translator import GoogleTranslator
import asyncio
from edge_tts import Communicate
import os

# --- Page Config & Styling ---
st.set_page_config(page_title="Tech_T AI", page_icon="🤖", layout="wide")

# Logo နှင့် နာမည်ကို လှလှပပ ပြုလုပ်ခြင်း
st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #FF4B4B;">🤖 Tech_T AI Tool</h1>
        <p style="font-size: 20px; font-weight: bold;">Developed By Tarbin</p>
        <hr>
    </div>
    """, unsafe_allow_html=True)

# Sidebar Menu
st.sidebar.markdown("### 🛠 Main Menu")
choice = st.sidebar.radio("ဘယ်အမျိုးအစား သုံးမလဲ?", ["Video to Script", "Text to Voice"])

# --- ၁။ Video to Script ပိုင်း (Error ပြင်ဆင်ပြီး) ---
if choice == "Video to Script":
    st.header("📜 Video to Script (Global Support)")
    st.info("YouTube, FB, TikTok နှင့် Rednote လင့်များ ထည့်နိုင်သည်")
    
    video_url = st.text_input("Video Link ကို ဒီမှာ ထည့်ပါ:")
    lang_map = {"မြန်မာ": "my", "English": "en", "Thai": "th", "Japanese": "ja", "Chinese": "zh-CN"}
    target_lang = st.selectbox("ဘာသာပြန်ရန် ရွေးပါ", list(lang_map.keys()))
    
    if st.button("Script ထုတ်မည် ✨"):
        if video_url:
            with st.spinner("AI က အလုပ်လုပ်နေပါပြီ၊ ခဏစောင့်ပေးပါ..."):
                try:
                    # Audio Download ဆွဲခြင်း (403 Forbidden Error ကျော်ရန်)
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': 'temp_audio.%(ext)s',
                        'quiet': True,
                        'no_warnings': True,
                        'nocheckcertificate': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                        'referer': 'https://www.google.com/',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    }

                    # ဖိုင်ဟောင်းရှိရင် ဖျက်မယ်
                    if os.path.exists("temp_audio.mp3"):
                        os.remove("temp_audio.mp3")

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                    
                    # AI စာသားပြောင်းခြင်း
                    model = whisper.load_model("tiny")
                    result = model.transcribe("temp_audio.mp3")
                    
                    # ဘာသာပြန်ခြင်း
                    translated = GoogleTranslator(source='auto', target=lang_map[target_lang]).translate(result['text'])
                    
                    st.success("အောင်မြင်စွာ ပြီးဆုံးပါပြီ!")
                    
                    # ရလဒ်ပြသခြင်း
                    t1, t2 = st.tabs(["ဘာသာပြန်ထားသော စာသား", "မူရင်း စာသား"])
                    with t1:
                        st.text_area("ဘာသာပြန် script", translated, height=300)
                    with t2:
                        st.text_area("Original script", result['text'], height=300)
                    
                    # Cleanup
                    os.remove("temp_audio.mp3")
                        
                except Exception as e:
                    st.error(f"⚠️ Error: YouTube က ပိတ်ထားဆဲ ဖြစ်နိုင်သည်။ (Error Detail: {str(e)})")
        else:
            st.warning("လင့်တစ်ခုခု အရင်ထည့်ပေးပါဗျာ။")

# --- ၂။ Text to Voice ပိုင်း ---
elif choice == "Text to Voice":
    st.header("🎙 Professional Text-to-Voice")
    input_txt = st.text_area("အသံပြောင်းလိုသော စာသားများ ရေးပါ:", height=200)
    
    v_map = {
        "မြန်မာ (အမျိုးသား)": "my-MM-ThihaNeural",
        "English (Male)": "en-US-ChristopherNeural",
        "Thai (Female)": "th-TH-AcharaNeural"
    }
    v_choice = st.selectbox("အသံပုံစံ ရွေးပါ", list(v_map.keys()))

    if st.button("အသံထုတ်မည် 🎧"):
        if input_txt:
            async def generate():
                comm = Communicate(input_txt, v_map[v_choice])
                await comm.save("voice_output.mp3")
                st.audio("voice_output.mp3")
            asyncio.run(generate())
        else:
            st.warning("စာသား အရင်ရိုက်ပါ")
