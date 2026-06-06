import streamlit as st
import base64
import json
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="Saeed DataBot Dashboard", layout="wide")

# وظيفة لتحميل الإعدادات (تعريفها في البداية)
def load_config():
    try:
        with open('saeed_databot_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"username": "admin", "password": "123"} # افتراضي إذا لم يوجد الملف

# وظيفة تشغيل الصوت
def autoplay_audio(file_path: str):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>"""
            st.markdown(md, unsafe_allow_html=True)

# 2. نظام تسجيل الدخول
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("Saeed DataBot | منصة إدارة Saeed MarketAds")
    st.subheader("تسجيل الدخول للوصول إلى الأدوات")
    
    username_input = st.text_input("اسم المستخدم أو البريد الإلكتروني")
    password_input = st.text_input("كلمة السر", type='password')
    
    if st.button("تسجيل الدخول"):
        config = load_config()
        if username_input == config.get('username') and password_input == config.get('password'):
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("اسم المستخدم أو كلمة السر غير صحيحة.")
else:
    # 3. محتوى التطبيق بعد الدخول
    st.title("Saeed DataBot | لوحة التحكم")
    st.caption("صنع بواسطة: سعيد المسوري")
    
    # الترحيب الصوتي
    autoplay_audio("welcome_voice.mp3") 
    
    with st.sidebar:
        st.header("القائمة الرئيسية")
        st.info("مرحباً بك يا سعيد!")
        if st.button("🔒 سياسة الخصوصية"):
            st.write("جميع البيانات محمية بموجب سياسة خصوصية Saeed MarketAds.")
    
    tab1, tab2 = st.tabs(["🚀 قسم التسويق والعروض", "📱 قسم الهواتف والمودم"])

    with tab1:
        st.header("تحليل وعروض المتاجر")
        cols = st.columns(3)
        cols[0].button("Noon")
        cols[1].button("AliExpress")
        cols[2].button("SHEIN")
        
        user_prompt = st.text_area("اكتب طلبك لـ SaeeD DaTaBoT:")
        if st.button("تنفيذ الطلب"):
            st.write("... جارٍ المعالجة بواسطة SaeeD DaTaBoT ...")

    with tab2:
        st.header("إدارة الأجهزة")
        st.subheader("أجهزة LT أيتل")
        st.text_input("موديل الهاتف:")
        st.number_input("الكمية:", min_value=0)
        st.button("حفظ بيانات الهاتف")

    st.markdown("---")
    st.caption("جميع الحقوق محفوظة © سعيد المسوري - Saeed MarketAds")
