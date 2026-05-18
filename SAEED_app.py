
import streamlit as st
from google import genai
import gtts
import os

st.set_page_config(page_title="Saeed DataBot", page_icon="🚀")

st.image("saeed_avatar.jpg", use_column_width=True)
st.title("Saeed Market Ads | AI Bot")
st.write("Welcome to Saeed Market Ads Smart Assistant.")

st.audio("saeed_voice.mp3")

try:
    YOUR_API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=YOUR_API_KEY)
except Exception as e:
    st.error("API Key missing in Streamlit Secrets.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "audio" in message:
            st.audio(message["audio"])

audio_value = st.audio_input("🎙️ Speak to the Bot")
user_input = st.chat_input("Or type your message here...")

if audio_value:
    st.info("Audio received! Processing...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            prompt_instructions = (
                f"أنت بوت ذكي وصوتي لبراند 'saeedmarketads' المتخصص في التسويق الإلكتروني وإعلانات المتاجر مثل AliExpress و Noon و SHEIN. "
                f"تحدث بذكاء، وود، واحترافية باللغة العربية واجعل إجابتك مختصرة ومناسبة للقراءة الصوتية من خلال ميكروفون الهاتف. رسالة المستخدم هي: {user_input}"
            )
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_instructions
            )
            
            bot_reply = response.text
            message_placeholder.markdown(bot_reply)
            
            tts = gtts.gTTS(text=bot_reply, lang='ar')
            audio_file = "bot_reply.mp3"
            tts.save(audio_file)
            
            st.audio(audio_file)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply, "audio": audio_file})
            
        except Exception as e:
            message_placeholder.markdown("Error in generation.")
