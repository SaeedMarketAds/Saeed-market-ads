import streamlit as st
import google.generativeai as genai
from PIL import Imageimport streamlit as st
import google.generativeai as genai
import os  # أضف هذا السطر


# إعداد مفتاح API
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# إعداد النموذج - استخدم 3.5-flash
model = genai.GenerativeModel(model_name="gemini-3.5-flash")

# إعداد الواجهة
st.set_page_config(page_title="سعيد ماركت", layout="wide")
# ... (الكود السابق كما هو)
# السطر 16: # الشريط الجانبي للتبديل بين الأوضاع
with st.sidebar:
    st.header("إعدادات سعيد")
    mode = st.radio("اختر الوضع:", ["سعيد ماركت", "سعيد داتابوت"])
    
    # التحقق من وجود الملف قبل عرضه لتجنب الانهيار
    if mode == "سعيد ماركت":
        if os.path.exists("SAEED.jpg"):
            st.image("SAEED.jpg", caption="سعيد ماركت")
        else:
            st.warning("صورة SAEED.jpg غير موجودة")
    else:
        if os.path.exists("ROBOT.jpg"):
            st.image("ROBOT.jpg", caption="سعيد داتابوت")
        else:
            st.warning("صورة ROBOT.jpg غير موجودة")

# السطر 27: # تهيئة الجلسة (تابع بقية الكود من هنا)
if 'chat_session' not in st.session_state:
# ...

    else:
        st.image("ROBOT.jpg", caption="سعيد داتابوت")

# تهيئة الجلسة
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if 'messages' not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المستخدم
if prompt := st.chat_input("ما الذي تحتاجه؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("سعيد يجيب..."):
            try:
                # إرسال سياق إضافي بناءً على الوضع المختار
                context = f"أنت تعمل الآن في وضع: {mode}. "
                response = st.session_state.chat_session.send_message(context + prompt)
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"حدث خطأ تقني: {e}")
                st.info("تأكد من استخدام اسم نموذج صحيح مثل: gemini-1.5-flash")
