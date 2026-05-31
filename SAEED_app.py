import google.generativeai as genai
import os
from st_audiorec import st_audiorec 
import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="Saeed DataBot", page_icon="🛍️")

# تحميل المفتاح السري من Streamlit Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# واجهة التطبيق
st.title("🛍️ Saeed DataBot")
if os.path.exists("saeed.jpg"):
    st.image("saeed.jpg", width=200)
st.subheader("مساعدك الذكي للتفاعل مع السوق")

user_input = st.text_input("اطرح سؤالك هنا")

# 
# بدلاً من st_audiorec() استخدم التالي:
audio_bytes = st.audio_input("سجل صوتك هنا")

if audio_bytes:
    st.audio(audio_bytes)

if st.button("تفاعل مع البوت"):
    if user_input:
        if not API_KEY:
            st.error("Streamlit: تأكد من إضافة API Key في إعدادات التطبيق (Secrets)")
        else:
            try:
                genai.configure(api_key=API_KEY)
                
                # تحديث اسم النموذج هنا
                # ملاحظة: تأكد من أن هذا الاسم مدعوم في إصدار مكتبة                model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash', 
                    system_instruction="""
                    أنت Saeed DataBot، المساعد الذكي الخاص بـ Saeed MarketAds. 
                    مهمتك هي تقديم دعم تسويقي احترافي، ودود، وسريع للعملاء.
                    تخصصك الأساسي هو التسويق بالعمولة لمنتجات: SHEIN، AliExpress، و Noon.
                    عندما يطرح المستخدم سؤالاً عن منتج:
                    1. قدم وصفاً تسويقياً جذاباً ومقنعاً للمنتج.
                    2. استخدم لهجة تناسب الجمهور المستهدف.
                    3. إذا طلب المستخدم المساعدة في الشراء، وجهه بالطريقة الصحيحة لاستخدام الروابط الخاصة بك.
                    4. حافظ دائماً على هويتك كمساعد خبير تابع لـ Saeed MarketAds.
                    """
                )
 Google لديك
                model = genai.GenerativeModel(
                    model_name='gemini-3.5-flash', 
                    system_instruction="أنت Saeed DataBot، مساعد ذكي يقدم خدمات ومعلومات واسعة عن السوق بلطف."
                )
                
                with st.spinner("جاري التفكير..."):
                    response = model.generate_content(user_input)
                
                st.success("الرد:")
                st.write(response.text)
                
                if os.path.exists("welcome_voice.mp3"):
                    st.audio("welcome_voice.mp3")
                    
            except Exception as e:
                st.error(f"حدث خطأ في الاتصال بالنموذج: {e}")
    else:
        st.warning("الرجاء كتابة سؤال!")

# تذييل الصفحة
st.sidebar.info("مشروع saeedmarketads - 1.0")
