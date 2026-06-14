import streamlit as st
import os
import google.generativeai as genai

# ========== إعداد الصفحة ==========
st.set_page_config(page_title="سوق سعيد | متجر SHEIN", page_icon="🛍️", layout="wide")

# ========== العنوان ==========
st.title("🛍️ سوق سعيد - متجر SHEIN")
st.markdown("---")

# ========== جلب المفتاح من متغيرات البيئة ==========
GEMINI_API_KEY = os.environ.get("GEMINI_API", "")

# ========== إعداد Gemini 3.5 Flash ==========
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# ========== جميع منتجات SHEIN (مترجمة للعربية) ==========
PRODUCTS = [
    {"name": "معطف مبطن بغطاء رأس للفتيات", "price": 19.39, "discount": 43, "link": "https://onelink.shein.com/38/5shrzfcizjmg", "sales": "150+"},
    {"name": "قميص أنيق بتصميم هونج كونج", "price": 14.18, "discount": 37, "link": "https://onelink.shein.com/38/5shune7n90yf", "sales": "200+"},
    {"name": "نظارات حفلات مطبوعة 6 قطع", "price": 2.70, "discount": 0, "link": "https://onelink.shein.com/38/5shujg5f2ywk", "sales": "300+"},
    {"name": "حقيبة مستلزمات سفر مقاومة للماء", "price": 3.90, "discount": 17, "link": "https://onelink.shein.com/38/5shuimjyfjt7", "sales": "100+"},
    {"name": "معطف رجالي كاجوال سادة", "price": 25.67, "discount": 24, "link": "https://onelink.shein.com/38/5shui8qqn60h", "sales": "200+"},
    {"name": "أقراط زهرية بتصميم لافت", "price": 1.44, "discount": 4, "link": "https://onelink.shein.com/38/5shtox57cemc", "sales": "300+"},
    {"name": "ربطات شعر ملونة 5 قطع", "price": 1.50, "discount": 38, "link": "https://onelink.shein.com/38/5shtobfv3sxn", "sales": "800+"},
    {"name": "أحذية رياضية نسائية كاجوال", "price": 5.00, "discount": 82, "link": "https://onelink.shein.com/38/5shtl502kmcf", "sales": "200+"},
    {"name": "مجموعة خواتم زهور وردية", "price": 2.16, "discount": 6, "link": "https://onelink.shein.com/38/5shtkl9rhh8f", "sales": "500+"},
    {"name": "دلو أرز مع كوب قياس", "price": 8.84, "discount": 70, "link": "https://onelink.shein.com/38/5shtjtnbwphj", "sales": "200+"},
    {"name": "أقراط هوب مطلية بالذهب 3 أزواج", "price": 1.43, "discount": 5, "link": "https://onelink.shein.com/38/5shti8ffmexk", "sales": "50+"},
    {"name": "شعر مستعار قصير مجعد", "price": 2.70, "discount": 33, "link": "https://onelink.shein.com/38/5shthyka1fts", "sales": "100+"},
    {"name": "حذاء تزلج بإضاءة LED للأطفال", "price": 34.72, "discount": 37, "link": "https://onelink.shein.com/38/5shthetyxlby", "sales": "50+"},
    {"name": "طقم مقص أظافر احترافي", "price": 1.40, "discount": 36, "link": "https://onelink.shein.com/38/5shtg7fahsfp", "sales": "1200+"},
    {"name": "هاتف لعبة موسيقي تعليمي", "price": 3.40, "discount": 0, "link": "https://onelink.shein.com/38/5shtfvl3s22n", "sales": "50+"},
    {"name": "شريط إضاءة RGB LED", "price": 2.27, "discount": 55, "link": "https://onelink.shein.com/38/5shtfbusmt15", "sales": "200+"},
    {"name": "طقم بيسبول للأولاد", "price": 3.28, "discount": 80, "link": "https://onelink.shein.com/38/5shtek8d4572", "sales": "100+"},
    {"name": "شريط لاصق مزدوج قوي", "price": 1.05, "discount": 30, "link": "https://onelink.shein.com/38/5shtead7hrfl", "sales": "800+"},
    {"name": "طبق طعام محكم الإغلاق 24 قطعة", "price": 7.14, "discount": 60, "link": "https://onelink.shein.com/38/5shtdonvakbf", "sales": "150+"},
    {"name": "حقيبة شاطئ كبيرة السعة", "price": 2.34, "discount": 57, "link": "https://onelink.shein.com/38/5shtcj87y44e", "sales": "100+"},
    {"name": "طقم بيجامة صيفية للأولاد", "price": 6.19, "discount": 42, "link": "https://onelink.shein.com/38/5shtc1gxxmda", "sales": "600+"},
    {"name": "أظافر صناعية فرنسية 24 قطعة", "price": 1.35, "discount": 41, "link": "https://onelink.shein.com/38/5sht8yz7kfv1", "sales": "200+"},
    {"name": "تيشيرت مدرسي بقوس وردي", "price": 4.09, "discount": 47, "link": "https://onelink.shein.com/38/5sht8r3347y5", "sales": "800+"},
    {"name": "حامل هاتف قابل للطي محمول", "price": 1.30, "discount": 24, "link": "https://onelink.shein.com/38/5sht5cr65itw", "sales": "100+"},
    {"name": "طقم مناشف مخططة سريعة الجفاف", "price": 2.34, "discount": 38, "link": "https://onelink.shein.com/38/5sht12urdy18", "sales": "200+"},
    {"name": "شريط مانع لتسرب المياه", "price": 1.70, "discount": 0, "link": "https://onelink.shein.com/38/5sht0h5f61jc", "sales": "300+"},
    {"name": "مقص دجاج متعدد الاستخدامات", "price": 2.70, "discount": 23, "link": "https://onelink.shein.com/38/5shszze54ug2", "sales": "300+"},
    {"name": "طقم قميص وبنطلون رجالي", "price": 7.77, "discount": 70, "link": "https://onelink.shein.com/38/5shsz9qqou3d", "sales": "50+"},
    {"name": "طقم موس حاجب 30 قطعة", "price": 0.75, "discount": 32, "link": "https://onelink.shein.com/38/5shsyi4b2nub", "sales": "500+"},
    {"name": "فرجار رقمي 6 بوصة", "price": 1.71, "discount": 10, "link": "https://onelink.shein.com/38/5shsxydzzinl", "sales": "200+"},
    {"name": "حزام رجالي بإبزيم أوتوماتيكي", "price": 2.93, "discount": 38, "link": "https://onelink.shein.com/38/5shsxapmkr2h", "sales": "500+"},
    {"name": "شفاطات لامعة قابلة لإعادة الاستخدام", "price": 0.99, "discount": 18, "link": "https://onelink.shein.com/38/5shswb72kgum", "sales": "600+"},
    {"name": "واقي شاشة ضد التجسس", "price": 1.63, "discount": 49, "link": "https://onelink.shein.com/38/5shsw790bnla", "sales": "800+"},
    {"name": "مشط قابل للطي مع مرآة", "price": 1.90, "discount": 32, "link": "https://onelink.shein.com/38/5shsw1bwzhq8", "sales": "800+"},
    {"name": "لعبة ضغط بيضاوية مخططة", "price": 2.97, "discount": 10, "link": "https://onelink.shein.com/38/5shsvxdus31c", "sales": "200+"},
    {"name": "حزام كلب مبطن وعاكس", "price": 3.30, "discount": 25, "link": "https://onelink.shein.com/38/5shsvrgrgmbu", "sales": "50+"},
    {"name": "غطاء حماية شاحن 3 قطع", "price": 1.13, "discount": 25, "link": "https://onelink.shein.com/38/5shsvboiirzh", "sales": "900+"},
    {"name": "طقم فرش مكياج 3 قطع", "price": 1.05, "discount": 48, "link": "https://onelink.shein.com/38/5shsv5rf6m2j", "sales": "1000+"},
    {"name": "فاتحة علب 4 في 1", "price": 1.08, "discount": 23, "link": "https://onelink.shein.com/38/5shsuk22y0h7", "sales": "200+"},
    {"name": "شارة أنمي دبوس", "price": 1.65, "discount": 21, "link": "https://onelink.shein.com/38/5shstycqq3uz", "sales": "100+"},
    {"name": "رأس دش مطري عالي الضغط", "price": 12.64, "discount": 65, "link": "https://onelink.shein.com/38/5shst4ra0l06", "sales": "200+"},
    {"name": "مكواة فرد وتجعيد شعر سيراميك", "price": 26.90, "discount": 20, "link": "https://onelink.shein.com/38/5shsrzbmou3o", "sales": "100+"},
    {"name": "زجاجة رش زيت للطبخ", "price": 1.17, "discount": 22, "link": "https://onelink.shein.com/38/5shsrvdkg0tg", "sales": "500+"},
    {"name": "مشابك تثبيت لحاف 4 قطع", "price": 3.33, "discount": 5, "link": "https://onelink.shein.com/38/5shsrnhfz3p0", "sales": "200+"},
    {"name": "نظارات حجب الضوء الأزرق", "price": 5.22, "discount": 50, "link": "https://onelink.shein.com/38/5shsqvv0f19e", "sales": "100+"},
    {"name": "أداة تقليم القدم", "price": 1.10, "discount": 8, "link": "https://onelink.shein.com/38/5shspqfd1vtf", "sales": "300+"},
    {"name": "أساور خرز خشبي", "price": 1.80, "discount": 25, "link": "https://onelink.shein.com/38/5shsp8o323az", "sales": "100+"},
    {"name": "ورق زبدة للمقلاة الهوائية", "price": 1.26, "discount": 21, "link": "https://onelink.shein.com/38/5shsof2mdyzs", "sales": "300+"},
    {"name": "أظافر فرنسية للمانيكير 48 قطعة", "price": 1.30, "discount": 35, "link": "https://onelink.shein.com/38/5shso76hvn95", "sales": "300+"},
    {"name": "سوار ساعة أبل جلد أصلي", "price": 5.89, "discount": 5, "link": "https://onelink.shein.com/38/5shs5kbzkzl4", "sales": "100+"},
    {"name": "حمالة هاتف فراشة مع كريستال", "price": 2.48, "discount": 25, "link": "https://onelink.shein.com/38/5shs5gdxezhw", "sales": "150+"},
]

# ========== عرض كود الخصم ==========
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='background: linear-gradient(90deg, #ff6b6b, #feca57); padding: 20px; border-radius: 20px; text-align: center;'>
        <h2>🎁 عرض خاص للمستخدمين الجدد 🎁</h2>
        <h1 style='background: white; display: inline-block; padding: 10px 30px; border-radius: 50px; color: #ff6b6b;'>🏷️ كود الخصم: WL7KA</h1>
        <p>🔥 خصم يصل إلى 60% على أول طلب</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ========== عرض المنتجات ==========
st.subheader(f"🛍️ منتجات SHEIN ({len(PRODUCTS)} منتج)")

# عرض المنتجات في شبكة
cols = st.columns(4)
for i, product in enumerate(PRODUCTS):
    with cols[i % 4]:
        final_price = product['price'] * (1 - product['discount']/100) if product['discount'] > 0 else product['price']
        
        st.markdown(f"""
        <div style='border: 1px solid #ddd; border-radius: 15px; padding: 15px; margin-bottom: 15px; background: white;'>
            <h4 style='font-size: 14px;'>{product['name']}</h4>
            <p style='color: #ff4757; font-size: 20px; font-weight: bold;'>
                ${final_price:.2f}
                {' ' + 'عذراً، خطأ في عرض السعر' if product['discount'] > 0 else ''}
            </p>
            <p>🛍️ {product['sales']} تم البيع</p>
            <a href='{product['link']}' target='_blank'>
                <button style='background: linear-gradient(90deg, #667eea, #764ba2); color: white; border: none; padding: 10px; width: 100%; border-radius: 10px; cursor: pointer;'>
                    🛒 تسوق الآن
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ========== قسم الذكاء الاصطناعي Gemini 3.5 Flash ==========
st.subheader("🤖 اسأل الذكاء الاصطناعي Gemini 3.5 Flash")

question = st.text_input("اكتب سؤالك هنا:")

if st.button("اسأل Gemini"):
    if question:
        if model:
            with st.spinner("🤖 جاري التفكير..."):
                try:
                    response = model.generate_content(question)
                    st.success(f"**Gemini 3.5 Flash يقول:**\n\n{response.text}")
                except Exception as e:
                    st.error(f"خطأ: {e}")
        else:
            st.warning("⚠️ مفتاح Gemini API غير موجود. أضف GEMINI_API في Secrets")
    else:
        st.warning("⚠️ الرجاء كتابة سؤال أولاً")

st.markdown("---")

# ========== معلومات التطبيق ==========
with st.expander("📌 معلومات عن سوق سعيد"):
    st.markdown(f"""
    - **عدد المنتجات:** {len(PRODUCTS)} منتج من SHEIN
    - **كود الخصم الحصري:** WL7KA (خصم 60% للمستخدمين الجدد)
    - **الذكاء الاصطناعي:** Google Gemini 3.5 Flash
    - **منتجات أخرى:** نون وعلي إكسبرس (قريباً)
    - **للتواصل:** @SaeedMarketAds
    """)

# ========== السايدبار ==========
st.sidebar.image("https://via.placeholder.com/300x100?text=Saeed+Market", use_container_width=True)
st.sidebar.title("📌 القائمة")
st.sidebar.markdown(f"""
- 🛍️ **{len(PRODUCTS)} منتج** من SHEIN
- 🎁 كود الخصم: **WL7KA**
- 🤖 **Gemini 3.5 Flash**
- 📞 @SaeedMarketAds
""")
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 سوق سعيد - جميع الحقوق محفوظة")
