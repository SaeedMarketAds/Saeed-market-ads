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

# ========== إعدادات البوت ==========
BOT_NAME = "Saeed DaTaBoT"
OWNER_NAME = "سعيد المسوري"
SMART_SAEED = "سعيد الذكي"

# ========== إعداد Gemini ==========
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "ضع_مفتاحك_هنا")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3.5-flash')

# ========== إعدادات الصوت ==========
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

def play_welcome_audio():
    try:
        with open("welcome_voice.mp3", "rb") as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    except:
        return text_to_speech("السلام عليكم ورحمة الله وبركاته، أنا سعيد داتابوت")

# ========== تخزين المنشورات ==========
if "posts" not in st.session_state:
    st.session_state.posts = [
        {
            "id": 1,
            "user": "سعيد المسوري",
            "product": "هاتف Samsung A54",
            "price": "$350",
            "description": "هاتف ممتاز بكاميرا 50 ميجابكسل، شحن سريع 25 واط",
            "image": None,
            "likes": 15,
            "comments": [
                {"user": " Ahmed", "text": "كم السعر؟"},
                {"user": " Fatima", "text": "هل متوفر في صنعاء؟"}
            ],
            "platform": "Facebook",
            "date": "2024-01-15"
        },
        {
            "id": 2,
            "user": "المركز الدولي للهواتف",
            "product": "هاتف VIVO Y16",
            "price": "$120",
            "description": "هاتف اقتصادي ببطارية كبيرة 5000mAh",
            "image": None,
            "likes": 8,
            "comments": [],
            "platform": "Instagram",
            "date": "2024-01-14"
        }
    ]

if "current_user" not in st.session_state:
    st.session_state.current_user = "تاجر يمني"

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
    return True

# ========== وظيفة إضافة إعجاب ==========
def like_post(post_id):
    for post in st.session_state.posts:
        if post["id"] == post_id:
            post["likes"] += 1
            break

# ========== وظيفة إضافة تعليق ==========
def add_comment(post_id, comment_text):
    for post in st.session_state.posts:
        if post["id"] == post_id:
            post["comments"].append({"user": st.session_state.current_user, "text": comment_text})
            break

# ========== قراءة الروابط ==========
def extract_product_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        product_info = {'title': 'غير معروف', 'price': 'غير معروف', 'platform': 'غير معروف', 'url': url}
        
        if 'noon.com' in url:
            product_info['platform'] = 'Noon'
        elif 'aliexpress' in url:
            product_info['platform'] = 'AliExpress'
        elif 'shein' in url:
            product_info['platform'] = 'SHEIN'
        
        return product_info
    except:
        return {'title': 'خطأ', 'price': 'غير معروف', 'platform': 'غير معروف', 'url': url}

# ========== ردود البوت ==========
def get_bot_response(user_input):
    user_input_lower = user_input.lower().strip()
    
    # السلام
    if "السلام عليكم" in user_input_lower:
        return "وعليكم السلام ورحمة الله وبركاته، أنا Saeed DaTaBoT. كيف أقدر أساعدك في نشر منتجاتك؟"
    
    # سامسونج
    if "سامسونج" in user_input_lower or "samsung" in user_input_lower:
        return """📱 **هواتف سامسونج المتوفرة في اليمن:**

• Samsung A05 - $100
• Samsung A14 - $150  
• Samsung A34 - $250
• Samsung A54 - $350
• Samsung S23 FE - $450

📍 متوفرة في **المركز الدولي للهواتف الذكية - صنعاء**
مع ضمان لمدة سنة.

هل تريد مساعدة في اختيار هاتف مناسب لك؟"""
    
    # أفضل هاتف
    if "أفضل هاتف" in user_input_lower or "افضل هاتف" in user_input_lower:
        return """🏆 **أفضل الهواتف في اليمن حسب الفئة:**

• **اقتصادي (أقل من $100):** Samsung A05, Itel A25
• **متوسط ($100-200):** Samsung A14, LT X5, VIVO Y16
• **ممتاز ($200-350):** Samsung A54, VIVO V25
• **احترافي ($350+):** Samsung S23 FE, VIVO X90

📍 نصيحتي: إذا تبحث عن قيمة مقابل سعر، Samsung A54 خيار ممتاز.
هل تريد معرفة المزيد عن هاتف معين؟"""
    
    # هاتف
    if "هاتف" in user_input_lower:
        return """📱 **عروض الهواتف في اليمن:**

• **سامسونج (Samsung)** - متوفرة في المركز الدولي
• **LT** - هواتف اقتصادية (LT P10: $80, LT X5: $120)
• **Itel** - أداء ممتاز (Itel A25: $60, Itel P37: $90)
• **VIVO** - كاميرات احترافية (VIVO Y16: $120, VIVO V25: $250)

📍 جميعها متوفرة في **المركز الدولي للهواتف الذكية** مع ضمان.
أي ماركة تهمك؟"""
    
    # Noon
    if "noon" in user_input_lower:
        return "🛍️ متجر Noon: خصومات تصل إلى 70%. أرسل رابط المنتج وسأكتب لك منشوراً تسويقياً."
    
    # AliExpress
    if "aliexpress" in user_input_lower:
        return "🌏 AliExpress: منتجات من كل العالم. أرسل رابط المنتج لتحليلها."
    
    # SHEIN
    if "shein" in user_input_lower:
        return "👗 SHEIN: أزياء وموضة. أرسل رابط المنتج وسأكتب منشوراً."
    
    # LT
    if "lt" in user_input_lower:
        return "📱 هواتف LT: LT P10 ($80)، LT X5 ($120)، LT Pro ($200). متوفرة في المركز الدولي."
    
    # Itel
    if "itel" in user_input_lower:
        return "📱 هواتف Itel: Itel A25 ($60)، Itel P37 ($90)، Itel S18 ($150)."
    
    # VIVO
    if "vivo" in user_input_lower:
        return "📱 هواتف VIVO: VIVO Y16 ($120)، VIVO V25 ($250)، VIVO X90 ($450)."
    
    # رابط
    if user_input.startswith('http'):
        info = extract_product_from_url(user_input)
        st.session_state.last_url = user_input
        return f"""✅ تم قراءة الرابط بنجاح!

📦 المنتج: {info['title']}
🏪 المتجر: {info['platform']}

هل تريد:
1. منشور تسويقي - اكتب 'منشور'
2. نشره في قسم المنشورات - اذهب إلى تبويب '🌐 النشر الاجتماعي'"""
    
    # رد افتراضي
    return f"""أنا Saeed DaTaBoT، كيف أساعدك؟

📌 **لنشر منتجك:** اذهب إلى تبويب "🌐 النشر الاجتماعي"

📌 **للتسويق:** أرسل رابط منتج من Noon, AliExpress, SHEIN

📌 **للاستفسار عن الهواتف:** اكتب "سامسونج" أو "أفضل هاتف"

كيف أقدر أخدمك اليوم؟"""

# ========== الواجهة الرئيسية ==========
st.set_page_config(page_title="Saeed DaTaBoT", page_icon="🤖", layout="wide")

# تشغيل الصوت الترحيبي
if "welcome_played" not in st.session_state:
    audio_html = play_welcome_audio()
    if audio_html:
        st.markdown(audio_html, unsafe_allow_html=True)
    st.session_state.welcome_played = True

# عنوان الصفحة
st.markdown("""
<div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px;">
    <h1 style="color: white;">🤖 Saeed DaTaBoT</h1>
    <p style="color: #e0e0e0;">صنع بواسطة سعيد المسوري | منصة لنشر المنتجات والتسويق بالعمولة</p>
    <p style="color: #ffd700;">✨ أنشر منتجك الآن - تواصل مع العملاء في اليمن ✨</p>
</div>
""", unsafe_allow_html=True)

# إنشاء التبويبات
tab1, tab2, tab3, tab4 = st.tabs(["🌐 النشر الاجتماعي", "📱 عروض الهواتف", "🤖 محادثة البوت", "🛍️ التسويق بالعمولة"])

# ========== TAB 1: النشر الاجتماعي (مثل فيسبوك) ==========
with tab1:
    st.markdown("### 📝 أنشر منتجك الآن")
    st.markdown("---")
    
    # نموذج نشر منتج جديد
    with st.expander("➕ إنشاء منشور جديد", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            product_name = st.text_input("اسم المنتج", placeholder="مثال: هاتف Samsung A54")
            product_price = st.text_input("السعر", placeholder="مثال: $350 أو 70,000 ريال")
            product_desc = st.text_area("وصف المنتج", placeholder="اكتب مميزات المنتج هنا...")
            platform_choice = st.selectbox("منصة النشر", ["Facebook", "Instagram", "Twitter", "TikTok", "WhatsApp", "Telegram"])
        
        with col2:
            st.markdown("### 🖼️ صورة المنتج")
            product_image = st.file_uploader("اختر صورة", type=["jpg", "png", "jpeg"])
            if product_image:
                st.image(product_image, width=150)
        
        if st.button("🚀 نشر المنتج", use_container_width=True):
            if product_name and product_price:
                add_new_post(product_name, product_price, product_desc, platform_choice, product_image)
                st.success("✅ تم نشر منتجك بنجاح!")
                st.balloons()
                st.rerun()
            else:
                st.error("يرجى إدخال اسم المنتج والسعر")
    
    st.markdown("---")
    st.markdown("### 📱 آخر المنشورات")
    
    # عرض المنشورات مثل فيسبوك
    for post in st.session_state.posts:
        with st.container():
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 15px; background-color: #f9f9f9;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="background-color: #667eea; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <span style="color: white;">👤</span>
                    </div>
                    <div>
                        <strong>{post['user']}</strong>
                        <small style="color: gray;"> • {post['date']} • على {post['platform']}</small>
                    </div>
                </div>
                <h4 style="margin-top: 10px;">📦 {post['product']}</h4>
                <p style="color: #28a745; font-size: 18px;"><strong>{post['price']}</strong></p>
                <p>{post['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # أزرار التفاعل
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button(f"❤️ {post['likes']}", key=f"like_{post['id']}"):
                    like_post(post['id'])
                    st.rerun()
            with col2:
                st.button(f"💬 {len(post['comments'])} تعليق", key=f"comment_btn_{post['id']}")
            
            # عرض التعليقات
            if post['comments']:
                with st.expander(f"💬 عرض التعليقات ({len(post['comments'])})"):
                    for comment in post['comments']:
                        st.markdown(f"**{comment['user']}:** {comment['text']}")
            
            # إضافة تعليق جديد
            new_comment = st.text_input("اكتب تعليقاً...", key=f"new_comment_{post['id']}")
            if st.button("إرسال تعليق", key=f"submit_comment_{post['id']}"):
                if new_comment:
                    add_comment(post['id'], new_comment)
                    st.rerun()
            
            st.markdown("---")

# ========== TAB 2: عروض الهواتف ==========
with tab2:
    st.markdown("### 📱 عروض الهواتف في اليمن")
    
    # سامسونج
    st.markdown("#### 🇰🇷 سامسونج (Samsung)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="border: 1px solid #667eea; border-radius: 10px; padding: 10px; text-align: center;">
            <h4>Samsung A05</h4>
            <p>💰 $100</p>
            <p>📱 6.5 إنش، 50MP</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="border: 1px solid #667eea; border-radius: 10px; padding: 10px; text-align: center;">
            <h4>Samsung A14</h4>
            <p>💰 $150</p>
            <p>📱 6.6 إنش، 50MP</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="border: 1px solid #667eea; border-radius: 10px; padding: 10px; text-align: center;">
            <h4>Samsung A54</h4>
            <p>💰 $350</p>
            <p>📱 6.4 إنش، 50MP OIS</p>
        </div>
        """, unsafe_allow_html=True)
    
    # LT, Itel, VIVO
    st.markdown("#### 📱 ماركات أخرى")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="border: 1px solid #764ba2; border-radius: 10px; padding: 10px; text-align: center;">
            <h4>📱 LT</h4>
            <p>LT P10: $80</p>
            <p>LT X5: $120</p>
            <p>LT Pro: $200</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="border: 1px solid #ff6b6b; border-radius: 10px; padding: 10px; text-align: center;">
            <h4>📱 Itel</h4>
            <p>Itel A25: $60</p>
            <p>Itel P37: $90</p>
            <p>Itel S18: $150</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="border: 1px solid #20c997; border-radius: 10px; padding: 10px; text-align: center;">
            <h4>📱 VIVO</h4>
            <p>VIVO Y16: $120</p>
            <p>VIVO V25: $250</p>
            <p>VIVO X90: $450</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("📍 **المركز الدولي للهواتف الذكية - صنعاء**\nجميع الهواتف متوفرة مع ضمان لمدة سنة.")

# ========== TAB 3: محادثة البوت ==========
with tab3:
    st.markdown("### 💬 تحدث مع Saeed DaTaBoT")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "السلام عليكم ورحمة الله وبركاته، أنا Saeed DaTaBoT. كيف أقدر أساعدك في نشر منتجاتك أو الاستفسار عن الهواتف؟"})
    
    if "bot_response" in st.session_state and st.session_state.bot_response:
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.bot_response})
        st.session_state.bot_response = None
    
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
        
        audio_html = text_to_speech(response)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
        
        st.rerun()

# ========== TAB 4: التسويق بالعمولة ==========
with tab4:
    st.markdown("### 🛍️ التسويق بالعمولة")
    st.markdown("أرسل رابط منتج من المتاجر العالمية وسأكتب لك منشوراً تسويقياً")
    
    affiliate_url = st.text_input("رابط المنتج", placeholder="https://www.noon.com/...")
    
    if affiliate_url:
        if st.button("📊 تحليل الرابط"):
            with st.spinner("جاري التحليل..."):
                info = extract_product_from_url(affiliate_url)
                st.success(f"✅ المتجر: {info['platform']}")
                
                # توليد منشور
                prompt = f"""اكتب منشور تسويقي قصير وجذاب لهذا المنتج من {info['platform']} بالعربية، مع إيموجيات وهاشتاجات."""
                try:
                    post = model.generate_content(prompt)
                    st.markdown("### 📝 المنشور المقترح:")
                    st.info(post.text)
                except:
                    st.info("منتج ممتاز بجودة عالية وسعر رائع! اطلبه الآن قبل نفاد الكمية 🛍️ #تسوق #عروض")

# ========== الشريط الجانبي ==========
with st.sidebar:
    st.markdown("### 👤 حسابي")
    st.session_state.current_user = st.text_input("اسم الناشر", value=st.session_state.current_user)
    
    st.markdown("---")
    st.markdown("### 📊 إحصائيات")
    st.metric("إجمالي المنشورات", len(st.session_state.posts))
    total_likes = sum(p["likes"] for p in st.session_state.posts)
    st.metric("إجمالي الإعجابات", total_likes)
    total_comments = sum(len(p["comments"]) for p in st.session_state.posts)
    st.metric("إجمالي التعليقات", total_comments)
    
    st.markdown("---")
    st.markdown("### 🔗 روابط سريعة")
    st.markdown("- [المركز الدولي للهواتف](https://example.com)")
    st.markdown("- [Noon](https://www.noon.com)")
    st.markdown("- [AliExpress](https://www.aliexpress.com)")
    st.markdown("- [SHEIN](https://www.shein.com)")
    
    st.markdown("---")
    st.markdown(f"**المطور:** {OWNER_NAME} ({SMART_SAEED})")
    
    if st.button("🎵 تشغيل الترحيب"):
        audio_html = play_welcome_audio()
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
