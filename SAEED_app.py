import streamlit as st
import pandas as pd
import requests
from io import StringIO
import os
import base64
import edge_tts
import asyncio
import tempfile
import re

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(page_title="سوق سعيد | Saeed Market", layout="wide")

# ==========================================
# 2. جلب المنتجات من جيت هاب
# ==========================================
@st.cache_data(ttl=600) # تحديث البيانات كل 10 دقائق
def load_products_from_csv():
    try:
        url = 'https://raw.githubusercontent.com/SaeedMarketAds/Saeed-market-ads/main/products.csv'
        r = requests.get(url)
        if r.status_code == 200:
            return pd.read_csv(StringIO(r.text))
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")
    return None

# ==========================================
# 3. التصميم (CSS)
# ==========================================
st.markdown("""
<style>
.product-card { border-radius: 20px; padding: 20px; background: white; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
.product-name { font-weight: bold; font-size: 16px; margin-bottom: 10px; }
.product-price { color: #ff4757; font-weight: bold; font-size: 20px; }
.product-btn { background: #667eea; color: white; padding: 10px; border-radius: 20px; text-align: center; text-decoration: none; display: block; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. الواجهة الرئيسية
# ==========================================
st.title("🛍️ سوق سعيد")
st.markdown("---")

# جلب البيانات
df = load_products_from_csv()

# الأزرار العلوية للفلترة
col1, col2, col3, col4 = st.columns(4)
store_filter = None
if col1.button("عرض الكل"): store_filter = "ALL"
if col2.button("SHEIN"): store_filter = "SH"
if col3.button("AliExpress/SM"): store_filter = "SM"
if col4.button("Noon"): store_filter = "N"

# ==========================================
# 5. عرض المنتجات (هنا يكمن الحل)
# ==========================================
if df is not None:
    # فلترة المنتجات بناءً على بداية كود SKU
    if store_filter and store_filter != "ALL":
        display_df = df[df['SKU'].astype(str).str.startswith(store_filter)]
    else:
        display_df = df

    # عرض المنتجات في شبكة
    cols = st.columns(4)
    for index, row in enumerate(display_df.itertuples()):
        with cols[index % 4]:
            st.markdown(f"""
            <div class='product-card'>
                <div class='product-name'>{row.name}</div>
                <div class='product-price'>{row.price} $</div>
                <div style='color:green;'>خصم: {row.discount}%</div>
                <a href='{row.link}' target='_blank' class='product-btn'>تسوق الآن</a>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("جاري تحميل المنتجات، تأكد من اتصالك بالإنترنت.")

# ==========================================
# 6. قسم الأداة (بدون سكرابينج تلقائي)
# ==========================================
st.markdown("---")
st.subheader("🛠️ أداة فحص الروابط (يدوي فقط)")
link_input = st.text_input("ضع الرابط للفحص:")
if st.button("افحص الرابط الآن"):
    st.info("جاري فحص الرابط... (سيظهر التقرير هنا)")
    # يمكنك وضع كود الفحص البسيط هنا فقط عند الضغط على الزر

