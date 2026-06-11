import json
import os
import streamlit as st
import google.generativeai as genai
import gtts
from io import BytesIO
import base64
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

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

# ========== حفظ المنشورات في ملف JSON ==========
POSTS_FILE = "posts.json"

def load_posts():
    """تحميل المنشورات من الملف"""
    if os.path.exists(POSTS_FILE):
        try:
            with open(POSTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_posts(posts):
    """حفظ المنشورات في الملف"""
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

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
    except Exception as e:
        print(f"خطأ في الصوت: {e}")
        return ""

# ========== إرسال إلى تليجرام ==========
def send_to_telegram_simple(product_name, price, description, platform, image_bytes=None):
    """إرسال إلى تليجرام"""
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

# ========== تحليل رابط المنتج ==========
def analyze_product_link(url):
    """تحليل رابط المنتج"""
    try:
        if "shein" in url.lower():
            return {"store": "SHEIN", "suggestion": "منتج رائع من SHEIN", "hashtags": "#SHEIN #تسوق"}
        elif "noon" in url.lower():
            return {"store": "Noon", "suggestion": "توصيل سريع من Noon", "hashtags": "#Noon #تسوق"}
        elif "aliexpress" in url.lower():
            return {"store": "AliExpress", "suggestion": "شحن عالمي", "hashtags": "#AliExpress"}
        elif "amazon" in url.lower():
            return {"store": "Amazon", "suggestion": "منتج أصلي", "hashtags": "#Amazon"}
        else:
            return {"store": "متجر آخر", "suggestion": "تم تحليل الرابط", "hashtags": "#تسوق"}
    except:
        return {"store": "خطأ", "suggestion": "يرجى التحقق", "hashtags": ""}

# ========== ردود البوت ==========
def get_bot_response(user_input):
    """ردود البوت"""
    if not model:
        return f"مرحباً! أنا {BOT_NAME}. كيف أخدمك اليوم؟"
    try:
        prompt = f"""أنت {BOT_NAME}، مساعد تسوق ذكي. الرد على: {user_input}"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"مرحباً! أنا {BOT_NAME}. كيف أخدمك اليوم؟"

# ========== الواجهة الرئيسية ==========
st.set_page_config(page_title="Saeed Market", page_icon="🤖", layout="wide")

# تهيئة session state
if "current_user" not in st.session_state:
    st.session_state.current_user = "تاجر يمني"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "hidden_product_link" not in st.session_state:
    st.session_state.hidden_product_link = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# CSS
st.markdown("""
<style>
    .post-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
        background-color: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .product-price { color: #28a745; font-size: 20px; font-weight: bold; }
    .hidden-link { background-color: #f5f5f5; padding: 10px; border-radius: 8px; word-break: break-all; }
</style>
""", unsafe_allow_html=True)

# العنوان
st.markdown(f"""
<div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 20px; margin-bottom: 2rem;">
    <h1 style="color: white;">🤖 {BOT_NAME}</h1>
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
            hidden_link = st.text_input("🔗 رابط المنتج (مخفي)", placeholder="https://...")
        
        with col_b:
            product_image = st.file_uploader("صورة المنتج", type=["jpg", "png", "jpeg"])
            if product_image:
                st.image(product_image, width=150)
        
        if st.button("🚀 نشر", type="primary"):
            if product_name and product_price:
                posts = load_posts()
                new_post = {
                    "id": len(posts) + 1 if posts else 1,
                    "user": st.session_state.current_user,
                    "product": product_name,
                    "price": product_price,
                    "description": product_desc,
                    "image": None,
                    "likes": 0,
                    "comments": [],
                    "platform": platform_choice,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "hidden_link": hidden_link,
                    "analysis": st.session_state.analysis_result
                }
                posts.insert(0, new_post)
                save_posts(posts)
                st.success("✅ تم النشر وحفظه بشكل دائم!")
                
                if send_to_tg and TELEGRAM_BOT_TOKEN:
                    img_bytes = product_image.getvalue() if product_image else None
                    send_to_telegram_simple(product_name, product_price, product_desc, platform_choice, img_bytes)
                    st.info("📨 تم الإرسال لتليجرام")
                
                st.balloons()
                st.rerun()
            else:
                st.error("يرجى إدخال الاسم والسعر")
    
    # عرض المنشورات المحفوظة
    saved_posts = load_posts()
    
    if not saved_posts:
        st.info("📭 لا توجد منشورات بعد. ابدأ بنشر منتجك الأول")
    else:
        for post in saved_posts:
            with st.container():
                st.markdown(f"""
                <div class="post-card">
                    <div><strong>👤 {post['user']}</strong> | 🕐 {post['date']} | 📱 {post['platform']}</div>
                    <h3>📦 {post['product']}</h3>
                    <div class="product-price">💰 {post['price']}</div>
                    <p>{post['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # ===== إصلاح TypeError النهائي =====
                # استخدام st.text بدلاً من st.code لتجنب المشكلة تماماً
                try:
                    post_text = f"اسم المنتج: {post['product']} | السعر: {post['price']} | الوصف: {post['description']}"
                    if post_text and len(post_text) > 0:
                        st.text(post_text)
                    else:
                        st.info("لا يوجد نص لعرضه")
                except Exception as e:
                    st.warning(f"⚠️ لا يمكن عرض النص: {str(e)[:50]}")
                
                # عرض الرابط المخفي
                if post.get('hidden_link') and post['hidden_link'].strip():
                    with st.expander("🔗 رابط المنتج (مخفي)"):
                        st.markdown(f'<div class="hidden-link">{post["hidden_link"]}</div>', unsafe_allow_html=True)
                
                # أزرار التفاعل
                col_l, col_c, _ = st.columns([1, 1, 2])
                with col_l:
                    if st.button(f"❤️ {post['likes']}", key=f"like_{post['id']}"):
                        posts2 = load_posts()
                        for p in posts2:
                            if p["id"] == post["id"]:
                                p["likes"] += 1
                                break
                        save_posts(posts2)
                        st.rerun()
                
                if post.get('comments'):
                    with st.expander(f"💬 {len(post['comments'])} تعليق"):
                        for c in post['comments']:
                            st.markdown(f"**{c['user']}:** {c['text']}")
                
                comment = st.text_input("💬 تعليق", key=f"comment_{post['id']}", placeholder="اكتب تعليقاً...")
                if st.button("📨 إرسال", key=f"send_{post['id']}"):
                    if comment:
                        posts2 = load_posts()
                        for p in posts2:
                            if p["id"] == post["id"]:
                                p["comments"].append({"user": st.session_state.current_user, "text": comment})
                                break
                        save_posts(posts2)
                        st.success("✅ تم إضافة التعليق")
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
        
        audio_html = text_to_speech(response)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
    
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

# ========== تبويب 3: التسويق ==========
with tab3:
    st.markdown("### 🛍️ التسويق بالعمولة - فحص الروابط")
    
    url = st.text_input("🔗 رابط المنتج للفحص", placeholder="https://www.shein.com/...")
    
    if url and st.button("📊 تحليل", type="primary"):
        with st.spinner("🔄 جاري التحليل..."):
            analysis = analyze_product_link(url)
            st.session_state.hidden_product_link = url
            st.session_state.analysis_result = analysis
            
            st.success("✅ تم تحليل الرابط!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**المتجر:** {analysis.get('store', '')}")
                st.markdown(f"**الاقتراح:** {analysis.get('suggestion', '')}")
            with col2:
                st.markdown(f'<div class="hidden-link">{url}</div>', unsafe_allow_html=True)
            
            st.markdown("### 🏷️ هاشتاجات مقترحة")
            st.code(analysis.get('hashtags', ''), language="markdown")
            
            # ===== إصلاح TypeError للمنشور المقترح =====
            try:
                suggested_post = f"📦 منتج ممتاز! 💰 سعر ممتاز {analysis.get('suggestion', '')} {analysis.get('hashtags', '')}"
                if suggested_post and len(suggested_post) > 0:
                    st.text(suggested_post)
                else:
                    st.info("لا يوجد منشور مقترح")
            except Exception as e:
                st.warning(f"⚠️ لا يمكن عرض المنشور المقترح: {str(e)[:50]}")

# ========== الشريط الجانبي ==========
with st.sidebar:
    st.markdown("### 👤 حسابي")
    st.session_state.current_user = st.text_input("اسم التاجر", value=st.session_state.current_user)
    
    st.markdown("---")
    st.markdown("### 📊 إحصائيات")
    saved_posts_count = len(load_posts())
    total_likes = sum(p.get("likes", 0) for p in load_posts())
    st.metric("📦 المنشورات", saved_posts_count)
    st.metric("❤️ الإعجابات", total_likes)
    
    st.markdown("---")
    st.markdown("### 🛒 أسواق مدعومة")
    st.markdown("- SHEIN ✅\n- Noon ✅\n- AliExpress ✅\n- Amazon ✅")
    
    st.markdown("---")
    st.markdown(f"**المطور:** {OWNER_NAME}")
    st.markdown(f"**البوت:** {BOT_NAME}")
