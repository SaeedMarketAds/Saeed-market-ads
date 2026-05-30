import streamlit as st
import google.generativeai as genai
import os
from st_audiorec import st_audiorec

# إعداد الصفحة
st.set_page_config(page_title="Saeed DataBot", page_icon="🚀")

# تحميل المفتاح السري من Streamlit Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# واجهة التطبيق
st.title("🚀 Saeed DataBot")
if os.path.exists("saeed.jpg"):
    st.image("saeed.jpg", width=200)
st.subheader("مساعدك الذكي للتفاعل مع السوق")

user_input = st.text_input("اطرح سؤالك هنا:")

# إعداد الميكروفون
audio_bytes = st_audiorec()
if audio_bytes:
    st.audio(audio_bytes)

if st.button("تفاعل مع البوت"):
    if user_input:
        if not API_KEY:
            st.error("مفتاح API غير موجود. تأكد من إضافته في إعدادات Streamlit.")
        else:
            try:
                genai.configure(api_key=API_KEY)
                
                # إعداد النموذج مع التعليمات الجديدة
                model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash',
                    system_instruction="أنت Saeed DataBot، مساعد ذكي متخصص للتفاعل مع السوق والتسويق بالعمولة، تم تطويرك بواسطة سعيد المسوري. مهمتك هي مساعدة العملاء في استفساراتهم المتعلقة بمجال التسويق بالعمولة والخدمات الذكية بكل احترافية، لطف، ومعرفة واسعة."
                )
                
                with st.spinner('جاري التحليل...'):
                    response = model.generate_content(user_input)
                
                st.success("الرد:")
                st.write(response.text)
                
                # التحقق من وجود ملف الصوت
                if os.path.exists("welcome_voice.mp3"):
                    st.audio("welcome_voice.mp3")
                    
            except Exception as e:
                st.error(f"حدث خطأ تقني: {e}")
    else:
        st.warning("الرجاء كتابة سؤال!")

# تذييل الصفحة
st.sidebar.info("مشروع saeedmarketads - 1.0")
