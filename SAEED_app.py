import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="SAEED DATABOT", layout="wide")
st.title("🚀 SAEED DATABOT - منصة التسويق الذكية")

# دالة عرض المنتج (تستقبل البيانات وتعرضها)
def display_product(title, price, link, image_url, description=""):
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(image_url, width=150)
        with col2:
            st.subheader(title)
            st.write(f"💰 **السعر:** {price}")
            if description:
                st.write(f"📝 {description}")
            st.link_button("🛒 تسوق الآن", link)
        st.divider()

# الألسنة (Tabs)
tab1, tab2, tab3, tab4 = st.tabs(["🏠 الرئيسية", "🤖 الذكاء الاصطناعي", "🌙 نون (Noon)", "✨ شي إن (SHEIN)"])

with tab1:
    st.header("مرحباً بك في Saeed MarketAds")
    st.info("منصتك المتكاملة لأفضل العروض والخدمات الذكية.")

with tab2:
    st.header("خدمات الذكاء الاصطناعي")
    user_input = st.text_input("اسأل Saeed DataBot عن أي منتج:")
    if user_input:
        st.write(f"جاري تحليل طلبك: {user_input}...")
        # هنا يتم استدعاء نموذج Gemini 3.5

with tab3:
    st.header("عروض نون المميزة")
    # مثال لعرض منتج نون
    display_product(
        "Apple AirPods Pro (الجيل الثاني)", 
        "899 ر.س", 
        "https://www.noon.com/ar-sa/N70105592V/p/?o=ea17dfe6040c4bae",
        "https://k.nooncdn.com/t_desktop-pdp-v1/v1647432658/N50838186A_1.jpg" # استبدلها برابط الصورة الحقيقي
    )

with tab4:
    st.header("عروض شي إن (SHEIN) الحصرية")
    # مثال لعرض منتج شي إن
    display_product(
        "معطف بناتي بقلنسوة", 
        "$19.39", 
        "https://onelink.shein.com/38/5shrzfcizjmg",
        "https://img.ltwebstatic.com/images3_pi/2023/09/25/..." # استبدلها برابط الصورة
    )

