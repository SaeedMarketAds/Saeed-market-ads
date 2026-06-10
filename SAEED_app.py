import streamlit as st
import google.generativeai as genai
import gtts
from io import BytesIO
import base64
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# ========== إعدادات البوت ==========
BOT_NAME = "Saeed DaTaBoT"
OWNER_NAME = "سعيد المسوري"

# ========== إعدادات Telegram ==========
TELEGRAM_BOT_TOKEN = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = st.secrets.get("TELEGRAM_CHANNEL_ID", "@SaeedMarket2026")

# ========== إعداد Gemini ==========
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-3.5-flash')

# ========== الصوت ==========
def text_to_speech(text):
    """تحويل النص إلى صوت"""
    try:
        clean_text = re.sub(r'[^\w\s\.،!؟]', ' ', text)
        tts = gtts.gTTS(clean_text, lang="ar", slow=False)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        audio_base64 = base64.b64encode(audio_bytes.read()).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    except:
        return ""

# ========== تخزين المنشورات ==========
if "posts" not in st.session_state:
    st.session_state.posts = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== ردود البوت ==========
def get_bot_response(user_input):
    """ردود البوت"""
    if not GEMINI_API_KEY:
        return "مرحباً! أنا سعيد داتابوت. كيف我可以 مساعدتك؟"
    
    try:
        response = model.generate_content(f"أنت {BOT_NAME}، مساعد ذكي. رد على: {user_input}")
        return response.text
    except:
        return f"مرحباً! أنا {BOT_NAME}، كيف أخدمك؟"

# ========== الواجهة الرئيسية ==========
st.set_page_config(page_title="Saeed Market", page_icon="🤖", layout="wide")

# عنوان الصفحة
st.markdown(f"""
<div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 20px; margin-bottom: 2rem;">
    <h1 style="color: white; margin: 0;">🤖 {BOT_NAME}</h1>
    <p style="color: #e0e0e0; margin-top: 10px;">منصة ذكية لنشر المنتجات والتسويق بالعمولة</p>
</div>
""", unsafe_allow_html=True)

# عرض الصورة أو الفيديو
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # البحث عن صورة للبوت
    image_paths = ["Saeed_DataBot_Avatar.jpg", "saeed_avatar.jpg", "ROBO.T.jpg"]
    found = False
    for img_path in image_paths:
        if os.path.exists(img_path):
            st.image(img_path, width=150)
            found = True
            break
    
    if not found:
        st.info("📷 قم برفع صورة للبوت")
    
    st.caption(f"🎙️ {BOT_NAME}")

# تبويبات
tab1, tab2 = st.tabs(["📝 نشر المنتجات", "💬 المحادثة"])

# ========== تبويب نشر المنتجات ==========
with tab1:
    st.markdown("### 📝 أنشر منتجك")
    
    with st.form("new_post_form"):
        product_name = st.text_input("اسم المنتج")
        product_price = st.text_input("السعر")
        product_desc = st.text_area("وصف المنتج")
        product_image = st.file_uploader("صورة المنتج", type=["jpg", "png", "jpeg"])
        
        if st.form_submit_button("🚀 نشر"):
            if product_name and product_price:
                new_post = {
                    "id": len(st.session_state.posts) + 1,
                    "product": product_name,
                    "price": product_price,
                    "description": product_desc,
                    "image": product_image,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.posts.insert(0, new_post)
                st.success("✅ تم النشر!")
                st.balloons()
                st.rerun()
            else:
                st.error("يرجى إدخال اسم المنتج والسعر")
    
    # عرض المنشورات
    for post in st.session_state.posts:
        with st.container():
            st.markdown(f"**📦 {post['product']}**")
            st.markdown(f"💰 {post['price']}")
            if post['description']:
                st.markdown(f"📝 {post['description']}")
            if post['image']:
                st.image(post['image'], width=200)
            st.markdown(f"🕐 {post['date']}")
            st.markdown("---")

# ========== تبويب المحادثة ==========
with tab2:
    st.markdown(f"### 💬 تحدث مع {BOT_NAME}")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    user_input = st.chat_input("اكتب رسالتك...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.spinner("🤖 جاري الرد..."):
            response = get_bot_response(user_input)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
        
        # تشغيل الصوت
        audio_html = text_to_speech(response)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)

# ========== الشريط الجانبي ==========
with st.sidebar:
    st.markdown("### 📊 إحصائيات")
    st.metric("📦 المنشورات", len(st.session_state.posts))
    
    st.markdown("---")
    st.markdown("### 🔗 روابط")
    st.markdown("- [SHEIN](https://www.shein.com)")
    st.markdown("- [Noon](https://www.noon.com)")
    st.markdown("- [AliExpress](https://www.aliexpress.com)")
    
    st.markdown("---")
    st.markdown(f"**المطور:** {OWNER_NAME}")
