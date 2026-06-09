import streamlit as st
import google.generativeai as genai
import gtts
from io import BytesIO
import base64
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import asyncio
from telegram import Bot
import tempfile
import os

# ========== إعدادات البوت ==========
BOT_NAME = "Saeed DaTaBoT"
OWNER_NAME = "سعيد المسوري"
SMART_SAEED = "سعيد الذكي"

# ========== إعدادات Telegram ==========
TELEGRAM_BOT_TOKEN = st.secrets.get("TELEGRAM_BOT_TOKEN", "ضع_توكن_البوت_هنا")
TELEGRAM_CHANNEL_ID = st.secrets.get("TELEGRAM_CHANNEL_ID", "@SaeedMarket2026")
telegram_bot = None
if TELEGRAM_BOT_TOKEN != "ضع_توكن_البوت_هنا":
    telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

# ========== إعداد Gemini ==========
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "ضع_مفتاحك_هنا")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ========== إعداد ElevenLabs ==========
ELEVENLABS_API_KEY = st.secrets.get("ELEVENLABS_API_KEY", "ضع_مفتاح_ElevenLabs_هنا")
ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # صوت Arabic

def elevenlabs_tts(text):
    """تحويل النص إلى صوت باستخدام ElevenLabs"""
    if ELEVENLABS_API_KEY == "ضع_مفتاح_ElevenLabs_هنا":
        return text_to_speech_fallback(text)
    
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            audio_base64 = base64.b64encode(response.content).decode()
            return f'<audio autoplay="true" src="data:audio/mpeg;base64,{audio_base64}">'
        else:
            return text_to_speech_fallback(text)
    except:
        return text_to_speech_fallback(text)

def text_to_speech_fallback(text):
    """النسخة الاحتياطية باستخدام gTTS"""
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
    st.session_state.posts = []  # تم إفراغ المنشورات الافتراضية

if "current_user" not in st.session_state:
    st.session_state.current_user = "تاجر يمني"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== وظيفة إرسال إلى تليجرام ==========
async def send_to_telegram(product_name, price, description, platform, image_bytes=None):
    """إرسال المنشور إلى قناة التليجرام"""
    if not telegram_bot:
        return False
    
    message = f"""📦 **{product_name}**

💰 **السعر:** {price}

📝 **الوصف:**
{description}

📱 **تم النشر عبر:** {platform}
👤 **بواسطة:** {st.session_state.current_user}
🕐 **التاريخ:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

#SaeedMarket #تسوق #منتج_جديد
"""
    try:
        if image_bytes:
            await telegram_bot.send_photo(
                chat_id=TELEGRAM_CHANNEL_ID,
                photo=image_bytes,
                caption=message,
                parse_mode='Markdown'
            )
        else:
            await telegram_bot.send_message(
                chat_id=TELEGRAM_CHANNEL_ID,
                text=message,
                parse_mode='Markdown'
            )
        return True
    except Exception as e:
        st.error(f"خطأ في الإرسال لتليجرام: {e}")
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

# ========== وظائف التفاعل ==========
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

# ========== ردود البوت باستخدام Gemini ==========
def get_bot_response(user_input, chat_history=None):
    """ردود البوت باستخدام Gemini AI"""
    
    system_prompt = f"""أنت {BOT_NAME}، مساعد ذكي جداً تم تطويره بواسطة {OWNER_NAME} ({SMART_SAEED}).
    
مهمتك:
1. مساعدة المستخدمين في نشر منتجاتهم للتسويق
2. تقديم استشارات تسويقية ذكية
3. الرد بذكاء واحترافية على جميع الاستفسارات
4. تحليل روابط المنتجات واقتراح منشورات تسويقية

ممنوع منعاً باتاً:
- ذكر أي معلومات عن "المركز الدولي للهواتف الذكية"
- الترويج لأي متجر معين بشكل حصري
- عرض قوائم أسعار ثابتة للهواتف

تحدث بذكاء، حماس، واحترافية. استخدم الإيموجيات المناسبة. كن مفيداً وخلاقاً في اقتراحاتك التسويقية.
"""
    
    full_prompt = system_prompt + f"\n\nالمستخدم: {user_input}\n\n{SMART_SAEED}:"
    
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"عذراً، حدث خطأ: {e}\n\nالرجاء المحاولة مرة أخرى."

# ========== تحليل الروابط ==========
def extract_product_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        product_info = {'title': 'غير معروف', 'price': 'غير معروف', 'platform': 'غير معروف', 'url': url}
        
        if 'noon.com' in url:
            product_info['platform'] = 'noon'
            title_tag = soup.find('h1')
            if title_tag:
                product_info['title'] = title_tag.text.strip()[:100]
        elif 'aliexpress' in url:
            product_info['platform'] = 'AliExpress'
        elif 'shein' in url:
            product_info['platform'] = 'SHEIN'
        elif 'amazon' in url:
            product_info['platform'] = 'Amazon'
        
        return product_info
    except:
        return {'title': 'خطأ في التحليل', 'price': 'غير معروف', 'platform': 'غير معروف', 'url': url}

def generate_marketing_post(product_info):
    """توليد منشور تسويقي باستخدام Gemini"""
    prompt = f"""اكتب منشور تسويقي احترافي وجذاب بالعربية لهذا المنتج:

المتجر: {product_info['platform']}
الرابط: {product_info['url']}

المطلوب:
- عنوان جذاب
- وصف مميزات المنتج
- دعوة للشراء (CTA)
- هاشتاجات مناسبة
- إيموجيات

اجعل المنشور بحماس واحترافية:"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "🔥 منتج رائع بجودة عالية وسعر مميز! لا تفوت الفرصة 🛍️\n#تسوق #عروض #تخفيضات"

# ========== الواجهة الرئيسية ==========
st.set_page_config(page_title="Saeed Market", page_icon="📱", layout="wide")

# CSS للواجهة الشبيهة بفيسبوك
st.markdown("""
<style>
    .post-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
        background-color: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .post-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .post-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }
    .avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 20px;
    }
    .user-name {
        font-weight: bold;
        font-size: 16px;
    }
    .post-time {
        font-size: 12px;
        color: #65676b;
    }
    .product-price {
        color: #28a745;
        font-size: 20px;
        font-weight: bold;
    }
    .reaction-btn {
        background: none;
        border: none;
        padding: 8px 12px;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.2s;
    }
    .reaction-btn:hover {
        background-color: #f0f2f5;
    }
    .chat-message {
        padding: 10px 15px;
        border-radius: 18px;
        margin: 5px 0;
        max-width: 80%;
    }
    .user-message {
        background-color: #0084ff;
        color: white;
        align-self: flex-end;
        margin-left: auto;
    }
    .assistant-message {
        background-color: #e4e6eb;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# عنوان الصفحة
st.markdown("""
<div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 20px; margin-bottom: 2rem;">
    <h1 style="color: white; margin: 0;">📱 سعيد ماركت</h1>
    <p style="color: #e0e0e0; margin-top: 10px;">منصة ذكية لنشر المنتجات والتسويق بالعمولة</p>
    <p style="color: #ffd700; font-size: 14px;">✨ أنشر منتجك - تواصل مع العملاء - حقق مبيعات ✨</p>
</div>
""", unsafe_allow_html=True)

# إنشاء التبويبات
tab1, tab2, tab3 = st.tabs(["🌐 النشر الاجتماعي", "🤖 المساعد الذكي", "🛍️ التسويق بالعمولة"])

# ========== TAB 1: النشر الاجتماعي (مثل فيسبوك) ==========
with tab1:
    st.markdown("### 📝 أنشر منتجك الآن")
    
    # نموذج نشر منتج جديد
    with st.expander("➕ إنشاء منشور جديد", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            product_name = st.text_input("اسم المنتج", placeholder="مثال: هاتف Samsung A54")
            product_price = st.text_input("السعر", placeholder="مثال: $350 أو 70,000 ريال")
            product_desc = st.text_area("وصف المنتج", placeholder="اكتب مميزات المنتج هنا...", height=100)
            platform_choice = st.selectbox("منصة النشر", ["Facebook", "Instagram", "Twitter", "TikTok", "WhatsApp", "Telegram"])
            send_to_tg = st.checkbox("📨 إرسال إلى قناة التليجرام تلقائياً", value=True)
        
        with col2:
            st.markdown("### 🖼️ صورة المنتج")
            product_image = st.file_uploader("اختر صورة", type=["jpg", "png", "jpeg"])
            if product_image:
                st.image(product_image, width=150)
        
        if st.button("🚀 نشر المنتج", use_container_width=True, type="primary"):
            if product_name and product_price:
                new_post = add_new_post(product_name, product_price, product_desc, platform_choice, product_image)
                st.success("✅ تم نشر منتجك بنجاح!")
                
                if send_to_tg and telegram_bot:
                    with st.spinner("جاري الإرسال إلى تليجرام..."):
                        image_bytes = product_image.getvalue() if product_image else None
                        try:
                            asyncio.run(send_to_telegram(product_name, product_price, product_desc, platform_choice, image_bytes))
                            st.success("📨 تم الإرسال إلى قناة التليجرام")
                        except:
                            st.warning("⚠️ لم يتم الإرسال إلى تليجرام، تأكد من التوكن والقناة")
                
                st.balloons()
                st.rerun()
            else:
                st.error("يرجى إدخال اسم المنتج والسعر")
    
    st.markdown("---")
    st.markdown("### 📱 المنشورات")
    
    if not st.session_state.posts:
        st.info("📭 لا توجد منشورات بعد. ابدأ بنشر منتجك الأول!")
    
    # عرض المنشورات
    for post in st.session_state.posts:
        with st.container():
            st.markdown(f"""
            <div class="post-card">
                <div class="post-header">
                    <div class="avatar">👤</div>
                    <div>
                        <div class="user-name">{post['user']}</div>
                        <div class="post-time">{post['date']} • على {post['platform']}</div>
                    </div>
                </div>
                <h3 style="margin: 10px 0;">📦 {post['product']}</h3>
                <div class="product-price">{post['price']}</div>
                <p style="margin: 12px 0; color: #333;">{post['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # عرض الصورة إذا وجدت
            if post['image']:
                st.image(post['image'], width=200)
            
            # أزرار التفاعل
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button(f"❤️ {post['likes']}", key=f"like_{post['id']}"):
                    like_post(post['id'])
                    st.rerun()
            with col2:
                st.button(f"💬 {len(post['comments'])}", key=f"comment_btn_{post['id']}")
            
            # عرض التعليقات
            if post['comments']:
                with st.expander(f"💬 تعليقات ({len(post['comments'])})"):
                    for comment in post['comments']:
                        st.markdown(f"**{comment['user']}:** {comment['text']}")
            
            # إضافة تعليق جديد
            new_comment = st.text_input("اكتب تعليقاً...", key=f"new_comment_{post['id']}", placeholder="اكتب ردك...")
            if st.button("إرسال", key=f"submit_comment_{post['id']}"):
                if new_comment:
                    add_comment(post['id'], new_comment)
                    st.success("✅ تم إضافة تعليقك")
                    st.rerun()
            
            st.markdown("---")

# ========== TAB 2: المحادثة الذكية ==========
with tab2:
    st.markdown("### 💬 المساعد الذكي (Gemini AI)")
    st.caption("اسألني أي شيء - استشارات تسويقية، تحليل منتجات، أفكار إعلانية")
    
    # عرض المحادثة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    user_input = st.chat_input("✍️ اكتب سؤالك هنا...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.spinner("🤖 جاري التفكير..."):
            response = get_bot_response(user_input)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
        
        # تشغيل الصوت
        audio_html = elevenlabs_tts(response)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
    
    # زر مسح المحادثة
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

# ========== TAB 3: التسويق بالعمولة ==========
with tab3:
    st.markdown("### 🛍️ التسويق بالعمولة الذكي")
    st.markdown("أرسل رابط منتج وسأقوم بتحليله وكتابة منشور تسويقي احترافي لك")
    
    affiliate_url = st.text_input("رابط المنتج", placeholder="https://www.noon.com/... أو https://www.amazon.com/...")
    
    if affiliate_url:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 تحليل الرابط وتوليد منشور", use_container_width=True, type="primary"):
                with st.spinner("جاري التحليل والتوليد..."):
                    info = extract_product_from_url(affiliate_url)
                    st.success(f"✅ تم التحليل - المتجر: {info['platform']}")
                    
                    # توليد المنشور
                    marketing_post = generate_marketing_post(info)
                    
                    st.markdown("### 📝 المنشور التسويقي المقترح:")
                    st.info(marketing_post)
                    
                    # زر نسخ
                    st.code(marketing_post, language="markdown")
        
        with col2:
            if st.button("🎯 طلب استشارة تسويقية", use_container_width=True):
                with st.spinner("🤖 جاري توليد استشارة..."):
                    prompt = f"قدم لي استشارة تسويقية احترافية لمنتج من {affiliate_url}، كيف يمكن تسويقه بنجاح؟"
                    advice = get_bot_response(prompt)
                    st.markdown("### 💡 الاستشارة التسويقية:")
                    st.success(advice)

# ========== الشريط الجانبي ==========
with st.sidebar:
    st.markdown("### 👤 حسابي")
    st.session_state.current_user = st.text_input("اسم الناشر", value=st.session_state.current_user)
    
    st.markdown("---")
    st.markdown("### 📊 إحصائيات اليوم")
    st.metric("📦 إجمالي المنشورات", len(st.session_state.posts))
    total_likes = sum(p["likes"] for p in st.session_state.posts)
    st.metric("❤️ إجمالي الإعجابات", total_likes)
    total_comments = sum(len(p["comments"]) for p in st.session_state.posts)
    st.metric("💬 التعليقات", total_comments)
    
    st.markdown("---")
    st.markdown("### 🔗 روابط سريعة")
    st.markdown("- [Noon](https://www.noon.com)")
    st.markdown("- [AliExpress](https://www.aliexpress.com)")
    st.markdown("- [Amazon](https://www.amazon.com)")
    
    st.markdown("---")
    st.markdown(f"**المطور:** {OWNER_NAME}")
    st.markdown(f"**البوت:** {BOT_NAME}")
    
    # حالة التليجرام
    if telegram_bot:
        st.success("✅ متصل بتليجرام")
    else:
        st.warning("⚠️ تليجرام غير متصل")
