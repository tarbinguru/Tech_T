import streamlit as st
import yt_dlp
import whisper
from deep_translator import GoogleTranslator
import asyncio
from edge_tts import Communicate
import os

st.set_page_config(page_title="AI Multi-Tool", layout="wide")
st.title("🎥 All-in-One AI Script & Voice")

choice = st.sidebar.selectbox("လုပ်ဆောင်ချက် ရွေးချယ်ပါ", ["Video to Script", "Text to Voice"])

if choice == "Video to Script":
    st.header("📜 Video to Script (Any Platform)")
    video_url = st.text_input("Video Link ထည့်ပါ:")
    lang_map = {"မြန်မာ": "my", "English": "en", "Thai": "th", "Japanese": "ja", "Chinese": "zh-CN"}
    target_lang = st.selectbox("ဘာသာပြန်ရန်", list(lang_map.keys()))
    
    if st.button("Script ထုတ်မည်"):
        if video_url:
            with st.spinner("Processing... ခဏစောင့်ပါ (Video အတိုဆိုလျှင် ပိုမြန်ပါသည်)"):
                try:
                    # ၁။ Audio ဆွဲထုတ်ခြင်း (Error 403 ကျော်ရန် Settings များ)
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': 'downloaded_audio.%(ext)s',
                        'noplaylist': True,
                        'quiet': True,
                        'nocheckcertificate': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    }
                    
                    if os.path.exists("downloaded_audio.mp3"):
                        os.remove("downloaded_audio.mp3")

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                    
                    # ၂။ AI စာသားပြောင်းခြင်း (Tiny model သုံးထား၍ ပိုမြန်ပါမည်)
                    model = whisper.load_model("tiny") 
                    result = model.transcribe("downloaded_audio.mp3")
                    
                    # ၃။ ဘာသာပြန်ခြင်း
                    translated = GoogleTranslator(source='auto', target=lang_map[target_lang]).translate(result['text'])
                    
                    st.success("အောင်မြင်သည်!")
                    st.subheader("ဘာသာပြန်ထားသော စာသား:")
                    st.write(translated)
                    
                    # Cleanup
                    if os.path.exists("downloaded_audio.mp3"):
                        os.remove("downloaded_audio.mp3")
                        
                except Exception as e:
                    st.error(f"Error တက်ရခြင်း အကြောင်းရင်း: {str(e)}")
        else:
            st.warning("Link တစ်ခုခု ထည့်ပေးပါ")

elif choice == "Text to Voice":
    st.header("🎙 Text to Voice")
    text = st.text_area("စာသားများ ရိုက်ထည့်ပါ:")
    v_opt = st.selectbox("အသံရွေးချယ်ပါ", ["my-MM-ThihaNeural", "en-US-ChristopherNeural", "th-TH-AcharaNeural"])
    if st.button("အသံထုတ်မည်"):
        async def make_voice():
            c = Communicate(text, v_opt)
            await c.save("out.mp3")
            st.audio("out.mp3")
        asyncio.run(make_voice())
