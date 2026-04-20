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
    st.header("📜 Video to Script (YT, FB, TikTok, Rednote)")
    video_url = st.text_input("Video Link ထည့်ပါ:")
    # Language code တွေကို deep-translator နဲ့ ကိုက်အောင် ပြင်ထားပါတယ်
    lang_map = {"မြန်မာ": "my", "English": "en", "Thai": "th", "Japanese": "ja", "Chinese": "zh-CN"}
    target_lang = st.selectbox("ဘာသာပြန်ရန်", list(lang_map.keys()))
    
    if st.button("Script ထုတ်မည်"):
        if video_url:
            with st.spinner("အလုပ်လုပ်နေပါသည်..."):
                try:
                    # Audio ဆွဲထုတ်ခြင်း
                    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'audio.mp3', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                    
                    # AI စာသားပြောင်းခြင်း
                    model = whisper.load_model("base")
                    result = model.transcribe("audio.mp3")
                    
                    # ဘာသာပြန်ခြင်း (Deep Translator သုံးထားပါတယ်)
                    translated = GoogleTranslator(source='auto', target=lang_map[target_lang]).translate(result['text'])
                    
                    st.success("အောင်မြင်သည်!")
                    st.subheader("ဘာသာပြန်ထားသော စာသား:")
                    st.write(translated)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Link ထည့်ပါ")

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
