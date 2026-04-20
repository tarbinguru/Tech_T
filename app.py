import streamlit as st
import yt_dlp
import whisper
from googletrans import Translator
import asyncio
from edge_tts import Communicate
import os

st.set_page_config(page_title="AI Multi-Tool", layout="wide")
st.title("🎥 All-in-One AI Script & Voice")

choice = st.sidebar.selectbox("လုပ်ဆောင်ချက် ရွေးချယ်ပါ", ["Video to Script", "Text to Voice"])

if choice == "Video to Script":
    st.header("📜 Video to Script (YT, FB, TikTok, Rednote)")
    video_url = st.text_input("Video Link ထည့်ပါ:")
    lang = st.selectbox("ဘာသာပြန်ရန်", ["my", "en", "th", "ja", "zh-cn"])
    
    if st.button("Script ထုတ်မည်"):
        with st.spinner("အလုပ်လုပ်နေပါသည်..."):
            ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'audio.mp3', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            model = whisper.load_model("base")
            result = model.transcribe("audio.mp3")
            ts = Translator()
            translated = ts.translate(result['text'], dest=lang)
            st.subheader("ဘာသာပြန်ထားသော စာသား:")
            st.write(translated.text)

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

