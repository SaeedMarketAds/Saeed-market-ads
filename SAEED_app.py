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
import random

# ========== إعدادات البوت ==========
BOT_NAME = "Saeed DaTaBoT"
OWNER_NAME = "سعيد المسوري"
SMART_SAEED = "سعيد الذكي"

# ========== إعدادات Telegram ==========
TELEGRAM_BOT_TOKEN = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = st.secrets.get("TELEGRAM_CHANNEL_ID", "@SaeedMarket2026")

# ========== إعداد Gemini ==========
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY and GEMINI_API_KEY != "ضع_مفتاحك_هنا":
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-3.5-flash')
else:
    model = None

# ========== الصوت ==========
def text_to_speech(text):
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

if "current_user" not in st.session_state:
    st.session_state.current_user = "تاجر يمني"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== إرسال إلى تليجرام ==========
def send_to_telegram_simple(product_name, price, description, platform, image_bytes=None, market_type=""):
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "ضع_توكن_البوت_هنا":
        return False
    try:
        from telegram import Bot
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        market_emoji = "🌍" if market_type == "global" else "🇾🇪"
        market_text = "سوق عالمي" if market_type == "global" else "سوق يمني"
        
        message = f"""🛍️ **منتج جديد**

{market_emoji} **{market_text}**
📦 **المنتج:** {product_name}
💰 **السعر:** {price}
📝 **الوصف:** {description}
📱 **النشر عبر:** {platform}
👤 **الناشر:** {st.session_state.current_user}
🕐 **التاريخ:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

#SaeedMarket #تسوق #منتج_جديد"""
        
        if image_bytes:
            bot.send_photo(chat_id=TELEGRAM_CHANNEL_ID, photo=image_bytes, caption=message, parse_mode='Markdown')
        else:
            bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message, parse_mode='Markdown')
        return True
    except:
        return False

# ========== وظائف المنشورات ==========
def add_new_post(product, price, description, platform, image, market_type):
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
        "market_type": market_type,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
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
    if not model:
        return f"مرحباً! أنا {BOT_NAME}. كيف أخدمك اليوم؟"
    try:
        prompt = f"""أنت {BOT_NAME}، مساعد تسوق ذكي للتجار اليمنيين والأسواق العالمية مثل SHEIN وNoon وAliExpress.
        
الرد على: {user_input}

كن ودوداً، محترفاً، وقدم نصائح تسويقية مفيدة."""
        response = model.generate_content(prompt)
        return response.text
    except:
        return f"مرحباً! أنا {BOT_NAME}. كيف أساعدك في تسويق منتجك اليوم؟"

# ========== تحليل روابط التسويق ==========
def analyze_marketing_link(url):
    """تحليل رابط منتج وتوليد منشور تسويقي"""
    url_lower = url.lower()
    
    if "shein" in url_lower:
        return {
            "platform": "SHEIN",
            "emoji": "👗",
            "suggestion": "🔥 **منتج حصري من SHEIN!**\n\n✨ جودة عالية - أسعار تنافسية\n🚚 توصيل سريع\n\n🛍️ لا تفوت الفرصة!",
            "hashtags": "#SHEIN #أزياء #تسوق_أونلاين"
        }
    elif "noon" in url_lower:
        return {
            "platform": "Noon",
            "emoji": "📦",
            "suggestion": "🎯 **عرض مميز من Noon!**\n\n✅ أفضل العروض اليوم\n✅ توصيل مجاني للطلبات الأولى\n\nاطلب الآن!",
            "hashtags": "#Noon #تخفيضات #عروض_اليوم"
        }
    elif "aliexpress" in url_lower:
        return {
            "platform": "AliExpress",
            "emoji": "🌏",
            "suggestion": "⭐ **منتج من AliExpress بجودة عالية!**\n\n💰 أسعار لا تقبل المنافسة\n🌍 شحن عالمي\n\nتسوق بثقة!",
            "hashtags": "#AliExpress #تسوق_عالمي"
        }
    elif "amazon" in url_lower:
        return {
            "platform": "Amazon",
            "emoji": "📚",
            "suggestion": "📦 **منتج من Amazon الأصلي!**\n\n✅ ضمان الجودة\n✅ تقييمات ممتازة\n\nاطلب الآن!",
            "hashtags": "#Amazon #متجر_موثوق"
        }
    else:
        return {
            "platform": "متجر عام",
            "emoji": "🛒",
            "suggestion": "🛍️ **منتج رائع بمواصفات مميزة!**\n\n💎 جودة عالية - سعر مناسب\n📞 للطلب والاستفسار",
            "hashtags": "#تسوق #عروض #تخفيضات"
        }

# ========== الواجهة الرئيسية ==========
st.set_page_config(page_title="سعيد ماركت", page_icon="🛍️", layout="wide")

# ========== CSS الجذاب ==========
st.markdown("""
<style>
    /* الخطوط والألوان */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    
    * {
        font-family: 'Tajawal', sans-serif;
    }
    
    /* البطاقات */
    .post-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .post-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* بطاقات الأسواق */
    .market-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .market-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* أزرار مخصصة */
    .stButton > button {
        border-radius: 12px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* الشريط الجانبي */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        color: white;
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0e0;
    }
    
    /* العنوان الرئيسي */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* أزرار التفاعل */
    .reaction-btn {
        background: #f0f2f5;
        border: none;
        border-radius: 25px;
        padding: 8px 20px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .reaction-btn:hover {
        background: #e4e6eb;
        transform: scale(1.05);
    }
    
    /* فيديو الأفتار */
    .avatar-video {
        border-radius: 50%;
        overflow: hidden;
        border: 4px solid #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ========== الأفتار المتحرك ==========
col_av1, col_av2, col_av3 = st.columns([1, 2, 1])
with col_av2:
    video_path = "saeed_avatar_v1.mp4"
    if os.path.exists(video_path):
        with open(video_path, "rb") as f:
            video_bytes = f.read()
        st.video(video_bytes, format="video/mp4")
    else:
        for img in ["Saeed_DataBot_Avatar.jpg", "saeed_avatar.jpg", "ROBO.T.jpg"]:
            if os.path.exists(img):
                st.image(img, width=150)
                break
    st.caption(f"🎙️ {BOT_NAME} - بوت التسوق الذكي")

# ========== العنوان الرئيسي ==========
st.markdown(f"""
<div class="main-header">
    <h1 style="color: white; margin: 0; font-size: 2.5rem;">🛍️ {BOT_NAME}</h1>
    <p style="color: #ffd700; margin-top: 10px; font-size: 1.2rem;">منصة ذكية للتجار اليمنيين والأسواق العالمية</p>
    <p style="color: #e0e0e0; font-size: 0.9rem;">✨ أنشر منتجك - تواصل مع العملاء - حقق مبيعات ✨</p>
</div>
""", unsafe_allow_html=True)

# ========== التبويبات ==========
tab1, tab2, tab3, tab4 = st.tabs(["📝 نشر المنتجات", "🤖 المساعد الذكي", "🛍️ تحليل روابط", "📊 المنشورات"])

# ========== تبويب 1: نشر المنتجات ==========
with tab1:
    st.markdown("### 📦 أنشر منتجك")
    
    # اختيار نوع السوق
    market_type = st.radio(
        "نوع السوق",
        ["🇾🇪 سوق يمني", "🌍 سوق عالمي (SHEIN, Noon, AliExpress)"],
        horizontal=True
    )
    market_value = "local" if "يمني" in market_type else "global"
    
    with st.form("publish_form", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            product_name = st.text_input("🏷️ اسم المنتج", placeholder="مثال: هاتف iPhone 13 - ملابس شتوية - عطر فاخر")
            product_price = st.text_input("💰 السعر", placeholder="مثال: 150$ أو 50,000 ريال")
            product_desc = st.text_area("📝 وصف المنتج", placeholder="اكتب مميزات المنتج هنا...", height=100)
            platform_choice = st.selectbox("📱 منصة النشر", ["Facebook", "Instagram", "Twitter", "TikTok", "Telegram", "WhatsApp"])
            send_to_tg = st.checkbox("📨 إرسال إلى قناة التليجرام تلقائياً")
        
        with col2:
            st.markdown("### 🖼️ صورة المنتج")
            product_image = st.file_uploader("اختر صورة", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
            if product_image:
                st.image(product_image, width=180)
        
        submitted = st.form_submit_button("🚀 نشر المنتج", use_container_width=True, type="primary")
        
        if submitted:
            if product_name and product_price:
                add_new_post(product_name, product_price, product_desc, platform_choice, product_image, market_value)
                st.success("✅ تم نشر منتجك بنجاح!")
                
                if send_to_tg and TELEGRAM_BOT_TOKEN:
                    img_bytes = product_image.getvalue() if product_image else None
                    send_to_telegram_simple(product_name, product_price, product_desc, platform_choice, img_bytes, market_value)
                    st.info("📨 تم الإرسال إلى تليجرام")
                
                st.balloons()
                st.rerun()
            else:
                st.error("❌ يرجى إدخال اسم المنتج والسعر")

# ========== تبويب 2: المساعد الذكي ==========
with tab2:
    st.markdown(f"### 💬 تحدث مع {BOT_NAME}")
    st.markdown("اسألني عن: التسويق، تحليل المنتجات، نصائح البيع، وأكثر!")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    user_input = st.chat_input("✍️ اكتب سؤالك هنا...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.spinner(f"🤖 {BOT_NAME} يفكر..."):
            response = get_bot_response(user_input)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
        
        audio_html = text_to_speech(response)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
    
    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ========== تبويب 3: تحليل روابط التسويق ==========
with tab3:
    st.markdown("### 🛍️ تحليل روابط المنتجات")
    st.markdown("أدخل رابط منتج من SHEIN، Noon، AliExpress أو Amazon وسأقوم بتحليله واقتراح منشور تسويقي")
    
    affiliate_url = st.text_input("🔗 رابط المنتج", placeholder="https://www.shein.com/... أو https://www.noon.com/...")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn1:
        analyze_clicked = st.button("📊 تحليل الرابط", use_container_width=True, type="primary")
    
    if analyze_clicked and affiliate_url:
        with st.spinner("جاري تحليل الرابط وتوليد المنشور..."):
            result = analyze_marketing_link(affiliate_url)
            
            st.markdown("---")
            
            # عرض نتيجة التحليل
            col_r1, col_r2 = st.columns([1, 2])
            with col_r1:
                st.markdown(f"### {result['emoji']}")
            with col_r2:
                st.markdown(f"### ✅ المتجر: {result['platform']}")
            
            st.markdown("---")
            
            # المنشور المقترح
            st.markdown("#### 📝 منشور تسويقي مقترح:")
            st.success(result['suggestion'])
            
            st.markdown("#### 🏷️ هاشتاجات مقترحة:")
            st.code(result['hashtags'], language="markdown")
            
            # زر نسخ
            full_post = f"{result['suggestion']}\n\n{result['hashtags']}\n\n🔗 {affiliate_url}"
            st.code(full_post, language="markdown", help="انسخ هذا المنشور")
            
            st.info("💡 يمكنك تعديل المنشور حسب رغبتك ثم نشره في المنصة!")
    
    elif analyze_clicked and not affiliate_url:
        st.warning("⚠️ يرجى إدخال رابط المنتج أولاً")
    
    # نصائح سريعة
    with st.expander("💡 نصائح سريعة للتسويق الناجح"):
        st.markdown("""
        - 📸 **الصور مهمة**: استخدم صور عالية الجودة للمنتج
        - ✍️ **وصف جذاب**: اكتب مميزات المنتج بشكل واضح
        - 💰 **سعر تنافسي**: ابحث عن أسعار السوق قبل التحديد
        - 🕐 **توقيت النشر**: أفضل أوقات النشر المساء والجمعة
        - 🔄 **التفاعل**: رد على التعليقات بسرعة لزيادة المبيعات
        """)

# ========== تبويب 4: المنشورات ==========
with tab4:
    st.markdown("### 📱 جميع المنشورات")
    
    if not st.session_state.posts:
        st.info("📭 لا توجد منشورات بعد. ابدأ بنشر منتجك الأول!")
    else:
        for post in st.session_state.posts:
            market_emoji = "🌍" if post.get("market_type") == "global" else "🇾🇪"
            market_text = "سوق عالمي" if post.get("market_type") == "global" else "سوق يمني"
            
            st.markdown(f"""
            <div class="post-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div>
                        <span style="font-size: 1.2rem;">👤 {post['user']}</span>
                        <span style="margin-left: 10px; font-size: 0.8rem; color: #888;">🕐 {post['date']}</span>
                    </div>
                    <div>
                        <span style="background: #667eea20; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem;">
                            {market_emoji} {market_text}
                        </span>
                        <span style="background: #28a74520; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; margin-left: 5px;">
                            📱 {post['platform']}
                        </span>
                    </div>
                </div>
                <h3 style="margin: 10px 0;">📦 {post['product']}</h3>
                <div style="color: #28a745; font-size: 1.5rem; font-weight: bold;">💰 {post['price']}</div>
                <p style="margin: 12px 0; color: #555;">{post['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if post['image']:
                st.image(post['image'], width=250)
            
            # أزرار التفاعل
            col_like, col_comment, _ = st.columns([1, 2, 5])
            with col_like:
                if st.button(f"❤️ {post['likes']}", key=f"like_{post['id']}"):
                    like_post(post['id'])
                    st.rerun()
            
            # التعليقات
            if post['comments']:
                with st.expander(f"💬 {len(post['comments'])} تعليق"):
                    for c in post['comments']:
                        st.markdown(f"**{c['user']}:** {c['text']}")
            
            # إضافة تعليق جديد
            new_comment = st.text_input("💬 اكتب تعليقاً...", key=f"comment_{post['id']}", placeholder="رد على هذا المنشور...")
            if new_comment and st.button("إرسال", key=f"send_{post['id']}"):
                add_comment(post['id'], new_comment)
                st.rerun()
            
            st.markdown("---")

# ========== الشريط الجانبي ==========
with st.sidebar:
    # صورة مصغرة في الشريط
    if os.path.exists("Saeed_DataBot_Avatar.jpg"):
        st.image("Saeed_DataBot_Avatar.jpg", width=80)
    
    st.markdown(f"### 🤖 {BOT_NAME}")
    st.caption("مساعدك الذكي للتسويق")
    
    st.markdown("---")
    
    # معلومات المستخدم
    st.markdown("### 👤 حسابي")
    st.session_state.current_user = st.text_input("اسم الناشر", value=st.session_state.current_user)
    
    st.markdown("---")
    
    # إحصائيات
    st.markdown("### 📊 إحصائيات اليوم")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("📦 المنشورات", len(st.session_state.posts))
    with col_s2:
        total_likes = sum(p["likes"] for p in st.session_state.posts)
        st.metric("❤️ الإعجابات", total_likes)
    
    st.markdown("---")
    
    # الأسواق المدعومة
    st.markdown("### 🛍️ أسواق مدعومة")
    
    markets = {
        "SHEIN": "👗", "Noon": "📦", "AliExpress": "🌏", "Amazon": "📚"
    }
    
    for market, emoji in markets.items():
        st.markdown(f"- {emoji} {market}")
    
    st.markdown("---")
    
    # روابط سريعة
    st.markdown("### 🔗 روابط سريعة")
    st.markdown("""
    - [SHEIN](https://www.shein.com)
    - [Noon](https://www.noon.com)
    - [AliExpress](https://www.aliexpress.com)
    - [Amazon](https://www.amazon.com)
    """)
    
    st.markdown("---")
    st.markdown(f"**👨‍💻 المطور:** {OWNER_NAME}")
    st.markdown(f"**🤖 البوت:** {BOT_NAME}")
    
    # حالة التليجرام
    if TELEGRAM_BOT_TOKEN and TELEGRAM_BOT_TOKEN != "ضع_توكن_البوت_هنا":
        st.success("✅ متصل بتليجرام")
    else:
        st.warning("⚠️ تليجرام غير متصل")
