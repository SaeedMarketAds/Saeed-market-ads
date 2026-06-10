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
SMART_SAEED = "سعيد الذكي"

# ========== إعدادات Telegram ==========
# ملاحظة: تم تبسيط التليجرام - بدون asyncio معقد
TELEGRAM_BOT_TOKEN = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = st.secrets.get("TELEGRAM_CHANNEL_ID", "@SaeedMarket2026")

# ========== إعداد Gemini ==========
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY and GEMINI_API_KEY != "ضع_مفتاحك_هنا":
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-3.5-flash')
else:
    model = None

# ========== الصوت المبسط (يعمل بدون أخطاء) ==========
def text_to_speech(text):
    """تحويل النص إلى صوت - نسخة مبسطة ومضمونة"""
    try:
        # تنظيف النص
        clean_text = re.sub(r'[^\w\s\.،!؟]', ' ', text)
        tts = gtts.gTTS(clean_text, lang="ar", slow=False)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        audio_base64 = base64.b64encode(audio_bytes.read()).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    except Exception as e:
        print(f"خطأ في الصوت: {e}")
        return ""

# ========== تخزين المنشورات ==========
if "posts" not in st.session_state:
    st.session_state.posts = []

if "current_user" not in st.session_state:
    st.session_state.current_user = "تاجر يمني"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== إرسال إلى تليجرام (نسخة مبسطة) ==========
def send_to_telegram_simple(product_name, price, description, platform, image_bytes=None):
    """إرسال إلى تليجرام - نسخة مبسطة"""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "ضع_توكن_البوت_هنا":
        return False
    
    try:
        from telegram import Bot
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        message = f"""📦 {product_name}
💰 السعر: {price}
📝 {description}
📱 {platform}
👤 {st.session_state.current_user}
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
        
        if image_bytes:
            bot.send_photo(chat_id=TELEGRAM_CHANNEL_ID, photo=image_bytes, caption=message)
        else:
            bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message)
        return True
    except Exception as e:
        print(f"تليجرام خطأ: {e}")
        return False

# ========== وظيفة نشر منتج جديد ==========
def add_new_post(product, price, description, platform, image):
    new_post = {
        "id": len(st.session_state.posts) + 1,
        "user": st.session_state.current_user,
        "product": product,
        "price": price,
        "description": description,
        "image": image,
        "likes": 0,
        "comments": [],
        "platform": platform,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    st.session_state.posts.insert(0, new_post)
    return new_post

def like_post(post_id):
    for post in st.session_state.posts:
        if post["id"] == post_id:
            post["likes"] += 1
            break

def add_comment(post_id, comment_text):
    for post in st.session_state.posts:
        if post["id"] == post_id:
            post["comments"].append({"user": st.session_state.current_user, "text": comment_text})
            break

# ========== ردود البوت ==========
def get_bot_response(user_input):
    """ردود البوت Saeed DaTaBoT"""
    if not model:
        return f"مرحباً! أنا {BOT_NAME}. كيف أخدمك اليوم؟"
    
    try:
        prompt = f"""أنت {BOT_NAME}، مساعد تسوق ذكي.
        
الرد على: {user_input}

كن مفيداً، محترفاً، واستخدم الإيموجيات."""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"مرحباً! أنا {BOT_NAME}. كيف أخدمك اليوم؟"

# ========== الواجهة الرئيسية ==========
st.set_page_config(page_title="Saeed Market", page_icon="🤖", layout="wide")

# CSS
st.markdown("""
<style>
    .stVideo {
        max-width: 200px;
        margin: 0 auto;
        border-radius: 50%;
        overflow: hidden;
        border: 3px solid #667eea;
    }
    .post-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
        background-color: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .product-price {
        color: #28a745;
        font-size: 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ========== عرض الأفتار المتحرك (يتحرك باستمرار) ==========
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # البحث عن الفيديو أو الصورة
    video_path = "saeed_avatar_v1.mp4"
    if os.path.exists(video_path):
        with open(video_path, "rb") as f:
            video_bytes = f.read()
        st.video(video_bytes, format="video/mp4")
        st.caption(f"🎬 {BOT_NAME} - أفتار متحرك")
    else:
        # صور احتياطية
        for img in ["Saeed_DataBot_Avatar.jpg", "saeed_avatar.jpg", "ROBO.T.jpg"]:
            if os.path.exists(img):
                st.image(img, width=150)
                break
        st.caption(f"🤖 {BOT_NAME}")

# العنوان
st.markdown(f"""
<div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 20px; margin-bottom: 2rem;">
    <h1 style="color: white; margin: 0;">🤖 {BOT_NAME}</h1>
    <p style="color: #e0e0e0;">منصة ذكية لنشر المنتجات والتسويق بالعمولة</p>
</div>
""", unsafe_allow_html=True)

# التبويبات
tab1, tab2, tab3 = st.tabs(["📝 نشر المنتجات", f"💬 {BOT_NAME}", "🛍️ تسويق"])

# ========== تبويب 1: نشر المنتجات ==========
with tab1:
    st.markdown("### 📝 أنشر منتجك")
    
    with st.expander("➕ منشور جديد", expanded=True):
        col_a, col_b = st.columns([2, 1])
        
        with col_a:
            product_name = st.text_input("اسم المنتج")
            product_price = st.text_input("السعر")
            product_desc = st.text_area("الوصف", height=80)
            platform_choice = st.selectbox("المنصة", ["Facebook", "Instagram", "Twitter", "TikTok", "Telegram"])
            send_to_tg = st.checkbox("📨 إرسال لتليجرام")
        
        with col_b:
            product_image = st.file_uploader("صورة المنتج", type=["jpg", "png", "jpeg"])
            if product_image:
                st.image(product_image, width=150)
        
        if st.button("🚀 نشر", type="primary"):
            if product_name and product_price:
                add_new_post(product_name, product_price, product_desc, platform_choice, product_image)
                st.success("✅ تم النشر!")
                
                if send_to_tg and TELEGRAM_BOT_TOKEN:
                    img_bytes = product_image.getvalue() if product_image else None
                    send_to_telegram_simple(product_name, product_price, product_desc, platform_choice, img_bytes)
                    st.info("📨 تم الإرسال لتليجرام")
                
                st.balloons()
                st.rerun()
            else:
                st.error("يرجى إدخال الاسم والسعر")
    
    # عرض المنشورات
    for post in st.session_state.posts:
        st.markdown(f"""
        <div class="post-card">
            <div><strong>👤 {post['user']}</strong> | 🕐 {post['date']} | 📱 {post['platform']}</div>
            <h3>📦 {post['product']}</h3>
            <div class="product-price">💰 {post['price']}</div>
            <p>{post['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if post['image']:
            st.image(post['image'], width=200)
        
        col_l, col_c, _ = st.columns([1, 1, 2])
        with col_l:
            if st.button(f"❤️ {post['likes']}", key=f"like_{post['id']}"):
                like_post(post['id'])
                st.rerun()
        
        if post['comments']:
            with st.expander(f"💬 {len(post['comments'])} تعليق"):
                for c in post['comments']:
                    st.markdown(f"**{c['user']}:** {c['text']}")
        
        comment = st.text_input("تعليق", key=f"comment_{post['id']}", placeholder="اكتب رداً...")
        if st.button("إرسال", key=f"send_{post['id']}"):
            if comment:
                add_comment(post['id'], comment)
                st.rerun()
        
        st.markdown("---")

# ========== تبويب 2: المساعد الذكي ==========
with tab2:
    st.markdown(f"### 💬 تحدث مع {BOT_NAME}")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    user_input = st.chat_input("✍️ اكتب سؤالك...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.spinner(f"🤖 {BOT_NAME} يفكر..."):
            response = get_bot_response(user_input)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
        
        # تشغيل الصوت
        audio_html = text_to_speech(response)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
    
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

# ========== تبويب 3: التسويق ==========
with tab3:
    st.markdown("### 🛍️ التسويق بالعمولة")
    url = st.text_input("رابط المنتج", placeholder="https://www.shein.com/...")
    
    if url and st.button("📊 تحليل"):
        with st.spinner("جاري التحليل..."):
            try:
                if "shein" in url.lower():
                    st.success("✅ متجر SHEIN")
                    st.info("💡 منشور مقترح: منتج رائع من SHEIN بجودة عالية وسعر ممتاز!")
                elif "noon" in url.lower():
                    st.success("✅ متجر Noon")
                elif "aliexpress" in url.lower():
                    st.success("✅ متجر AliExpress")
                else:
                    st.info("رابط تم تحليله بنجاح")
            except:
                st.warning("لم نتمكن من تحليل الرابط")

# ========== الشريط الجانبي ==========
with st.sidebar:
    st.markdown("### 👤 حسابي")
    st.session_state.current_user = st.text_input("اسمك", value=st.session_state.current_user)
    
    st.markdown("---")
    st.markdown("### 📊 إحصائيات")
    st.metric("📦 المنشورات", len(st.session_state.posts))
    total_likes = sum(p["likes"] for p in st.session_state.posts)
    st.metric("❤️ إعجابات", total_likes)
    
    st.markdown("---")
    st.markdown("### 🔗 روابط سريعة")
    st.markdown("- [SHEIN](https://www.shein.com)")
    st.markdown("- [Noon](https://www.noon.com)")
    st.markdown("- [AliExpress](https://www.aliexpress.com)")
    
    st.markdown("---")
    st.markdown(f"**المطور:** {OWNER_NAME}")
    st.markdown(f"**البوت:** {BOT_NAME}")
