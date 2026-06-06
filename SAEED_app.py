import streamlit as st
import base64
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="Saeed DataBot Dashboard", layout="wide")
st.title("Saeed DataBot | منصة إدارة Saeed MarketAds")
st.caption("صنع بواسطة: سعيد المسوري")

# 2. وظيفة لتشغيل ملفات الصوت (مثل welcome_voice.mp3)
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

# 3. التحقق من تسجيل الدخول (نظام بسيط للعرض)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.subheader("تسجيل الدخول للوصول إلى أدوات Saeed DataBot")
    username_or_email = st.text_input("اسم المستخدم أو البريد الإلكتروني")
    password = st.text_input("كلمة السر", type='password')
    
    if st.button("تسجيل الدخول"):
        # هنا يتم وضع منطق التحقق الحقيقي من GitHub
        if username_or_email == "saeed" and password == "1234":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("بيانات تسجيل الدخول غير صحيحة.")

# 4. محتوى التطبيق بعد تسجيل الدخول (الهيكل من مخطط image_4.png)
if st.session_state['logged_in']:
    # أ. تشغيل الترحيب الصوتي تلقائياً عند الدخول
    autoplay_audio("welcome_voice.mp3") 
    st.success("تم تشغيل نظام الترحيب الصوتي لـ Saeed DataBot...")

    # ب. القائمة الجانبية مع رابط الخصوصية
    with st.sidebar:
        st.header("Saeed DataBot")
        st.info("مرحباً بك، سعيد!")
        st.write("---")
        # رابط الخصوصية في آخر القائمة
        if st.button("🔒 الخصوصية وسياسة الاستخدام"):
            st.markdown("---")
            st.write("### سياسة الخصوصية لـ Saeed MarketAds")
            st.write("هنا يتم عرض نص سياسة الخصوصية والبنود والشروط...")

    # ج. تقسيم الواجهة الرئيسية (Tabs)
    tab1, tab2 = st.tabs(["🚀 قسم التسويق والعروض", "📱 قسم الهواتف والمودم"])

    with tab1:
        st.header("تحليل وعروض المتاجر القائمة")
        # هيكل من مخطط image_4.png
        cols = st.columns(3)
        cols[0].button("Noon (نون)")
        cols[1].button("AliExpress (علي إكسبريس)")
        cols[2].button("SHEIN (شي إن)")
        
        st.subheader("توليد المنشورات الذكي")
        user_prompt = st.text_area("اكتب طلبك هنا:")
        if st.button("توليد المنشور"):
            # هنا يتم استدعاء الذكاء الاصطناعي (SaeeD DaTaBoT)
            st.write("... جاري توليد النص بواسطة **SaeeD DaTaBoT** ...")

    with tab2:
        st.header("إدارة المتاجر المحلية للهواتف والمودم")
        # هيكل من مخطط image_4.png
        st.subheader("أجهزة LT أيتل")
        st.text_input("أدخل موديل الهاتف:")
        st.number_input("الكمية المتاحة:", min_value=0)
        
        st.subheader("أجهزة vivo")
        st.write("---")
        st.button("إضافة هاتف جديد")

st.markdown("---")
st.caption("جميع الحقوق محفوظة © سعيد المسوري - Saeed MarketAds")
