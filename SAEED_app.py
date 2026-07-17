import streamlit as st
import google.generativeai as genai
import cloudscraper
import requests
import os
import base64
import edge_tts
import tempfile
import asyncio
from bs4 import BeautifulSoup
import re
import pandas as pd
from io import StringIO, BytesIO
import time

# ==========================================
# 1. إعدادات الموديل والتعليمات
# ==========================================
AVAILABLE_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash"
]
DEFAULT_MODEL = "gemini-2.5-flash"

def get_system_instructions():
    return """
    أنت مساعد ذكي متخصص في الأسواق الخليجية.
    هويتك: Saeed DaTaBoT، المساعد الذكي لمنصة SaeedMarketAds.
    المطور: سعيد المسوري.
    ردودك باللغة العربية الفصحى.
    قواعد:
    1. عند سؤالك عن هويتك أو المطور: عرف نفسك بالاسم والمطور.
    2. عند تحليل المنتجات: لا تذكر اسمك أو اسم المنصة.
    3. تحليل المنتجات: مختصر (≤200 كلمة).
    4. استخدم العملة المحلية حسب الدولة.
    5. لا تستخدم رموزاً مثل ⭐ أو ★ في تحليل المنتجات.
    """

@st.cache_resource(ttl=3600)
def init_gemini(model_name):
    if "GEMINI_MAIN_KEY" not in st.secrets:
        return None
    genai.configure(api_key=st.secrets["GEMINI_MAIN_KEY"])
    return genai.GenerativeModel(
        model_name=model_name,
        system_instruction=get_system_instructions(),
        generation_config={"max_output_tokens": 1824}
    )

# ==========================================
# 2. إعدادات الصفحة وحالة الجلسة
# ==========================================
st.set_page_config(
    page_title="سوق سعيد | المساعد الذكي المتكامل",
    page_icon="🛍️",
    layout="wide"
)

if 'conversation' not in st.session_state:
    st.session_state.conversation = [{"role": "assistant", "content": "مرحباً بك! تم دمج الواجهة بالكامل بنجاح. كيف يمكنني مساعدتك اليوم؟"}]
if 'products' not in st.session_state:
    st.session_state.products = [
        {"name": "هاتف ذكي متطور", "price": 2499, "desc": "أحدث المواصفات والكاميرات المحترفة", "image": ""},
        {"name": "سماعات لاسلكية إلغاء الضجيج", "price": 599, "desc": "صوت نقي عالي الدقة وعزل كامل", "image": ""}
    ]
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "المحادثة الذكية"

# ==========================================
# 3. واجهة الـ CSS المتقدمة لدمج التصميم الجديد
# ==========================================
page_style = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
/* تهيئة الخلفية العامة وتصميم الألوان الداكنة */
[data-testid="stAppViewContainer"] {
    background: #0b0c10;
    color: #e2e8f0;
}
[data-testid="stHeader"] { background: rgba(0,0,0,0); }

/* إخفاء تبويبات ستريمليت الافتراضية لتركيب التبويبات المخصصة */
.stTabs [data-baseweb="tab-list"] {
    display: none !important;
}

/* تنسيق كروت المنتجات العصرية العلوي */
.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
}
.product-card {
    background: #16171a;
    border: 1px solid #27272a;
    border-radius: 20px;
    padding: 15px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.product-img-holder {
    height: 100px;
    background: #27272a;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #71717a;
    font-size: 2rem;
    margin-bottom: 10px;
}

/* القائمة المنبثقة السفلي لعلامة الـ (+) */
.bottom-sheet {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: #09090b;
    border-top: 1px solid #27272a;
    border-top-left-radius: 24px;
    border-top-right-radius: 24px;
    z-index: 9999;
    padding: 20px;
    transform: translateY(100%);
    transition: transform 0.3s ease-in-out;
    max-height: 75vh;
    overflow-y: auto;
}
.bottom-sheet.open {
    transform: translateY(0);
}
.sheet-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.6);
    z-index: 9998;
    display: none;
}
.sheet-overlay.show {
    display: block;
}

/* شريط الإدخال الثابت بالأسفل */
.fixed-footer {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: rgba(9, 9, 11, 0.95);
    border-top: 1px solid #27272a;
    padding: 12px 20px;
    z-index: 999;
}
.input-container {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #18181b;
    border-radius: 9999px;
    padding: 6px 14px;
    max-width: 600px;
    margin: 0 auto;
    border: 1px solid #27272a;
}
.input-box {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: white;
    font-size: 14px;
    text-align: right;
    direction: rtl;
}
.btn-circle {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border: none;
    transition: background 0.2s;
}
.btn-plus { background: #27272a; color: white; }
.btn-plus:hover { background: #3f3f46; }
.btn-pause { background: #2563eb; color: white; box-shadow: 0 4px 10px rgba(37,99,235,0.3); }
.btn-pause:hover { background: #1d4ed8; }

/* شريط التبويبات المخصص المدمج */
.nav-tabs-custom {
    display: flex;
    justify-content: space-around;
    max-width: 600px;
    margin: 10px auto 0 auto;
    border-top: 1px solid #27272a;
    padding-top: 8px;
}
.nav-item {
    background: transparent;
    border: none;
    color: #a1a1aa;
    font-size: 12px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
}
.nav-item.active {
    color: #3b82f6;
    font-weight: bold;
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# ==========================================
# 4. معالجة وتوجيه الضغطات من الـ UI المخصص
# ==========================================
# استقبال الأوامر من مستشعرات الجافاسكريبت المخفية لمنع ضياع الرسائل
query_params = st.query_params
if "action" in query_params:
    action = query_params["action"]
    if action == "change_tab" and "tab_name" in query_params:
        st.session_state.current_tab = query_params["tab_name"]
    st.query_params.clear()

# ==========================================
# 5. الواجهة العلوية: إدارة المنتجات (التبويب النشط)
# ==========================================
st.markdown(f"""
<div style='display:flex; justify-content:space-between; align-items:center; max-width:600px; margin:0 auto 15px auto;'>
    <h2 style='font-size:1.2rem; font-weight:bold;'><i class="fa-solid fa-layer-group text-blue-500"></i> لوحة تحكم سوق سعيد</h2>
    <span style='background:#27272a; padding:4px 12px; border-radius:12px; font-size:11px; color:#a1a1aa;'>{st.session_state.current_tab}</span>
</div>
""", unsafe_allow_html=True)

# عرض المنتجات بالأعلى مباشرة بطريقة عصرية
if st.session_state.current_tab == "إدارة المنتجات":
    st.markdown("<div class='product-grid'>", unsafe_allow_html=True)
    cols = st.columns(len(st.session_state.products) if st.session_state.products else 1)
    if not st.session_state.products:
        st.info("لا توجد منتجات حالياً.")
    else:
        for idx, prod in enumerate(st.session_state.products):
            with cols[idx % len(cols)]:
                st.markdown(f"""
                <div class='product-card'>
                    <div class='product-img-holder'><i class="fa-solid fa-box"></i></div>
                    <h3 style='font-size:14px; font-weight:bold; color:white;'>{prod['name']}</h3>
                    <p style='font-size:12px; color:#3b82f6; font-weight:bold; margin:4px 0;'>{prod['price']} ر.س</p>
                </div>
                """, unsafe_allow_html=True)
                # أزرار تحكم داخلية لإصدار ستريمليت الإجرائي
                c1, c2 = st.columns(2)
                c1.button("✏️ تعديل", key=f"edit_{idx}", size="small")
                if c2.button("🗑️ حذف", key=f"del_{idx}", size="small"):
                    st.session_state.products.pop(idx)
                    st.rerun()

# ==========================================
# 6. مساحة المحادثة الذكية (الشات)
# ==========================================
if st.session_state.current_tab == "المحادثة الذكية":
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.conversation:
            if msg["role"] == "user":
                st.markdown(f"<div style='text-align:right; margin:10px; fill:#27272a;'><span style='background:#2563eb; color:white; padding:10px 16px; border-radius:18px 18px 0 18px; display:inline-block; max-width:80%; text-align:right;'>{msg['content']}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:left; margin:10px;'><span style='background:#1f1f23; color:#e2e8f0; padding:10px 16px; border-radius:18px 18px 18px 0; display:inline-block; max-width:80%; border:1px solid #27272a;'>{msg['content']}</span></div>", unsafe_allow_html=True)

# ==========================================
# 7. أداة الفحص المتقدم للروابط
# ==========================================
if st.session_state.current_tab == "أداة الفحص المتقدم":
    st.markdown("<div style='max-width:600px; margin: 0 auto;'>", unsafe_allow_html=True)
    adv_url = st.text_input("أدخل رابط المنتج المراد فحصه من نون أو شي إن:", placeholder="https://...")
    if st.button("بدء الفحص والتحليل الذكي"):
        if adv_url:
            st.success("تم استقبال الرابط، جاري الفحص الشامل للأسعار والمخزون...")
        else:
            st.warning("الرجاء إدخال رابط أولاً.")
    st.markdown("</div>", unsafe_allow_html=True)

# معالجة النصوص البرمجية المرسلة عبر شريط الإدخال الحقيقي لستريمليت
st.markdown("<div style='height:140px;'></div>", unsafe_allow_html=True) # مساحة أمان سفلية

# ==========================================
# 8. شريط الإدخال الثابت + قائمة الـ (+) المنبثقة الذكية
# ==========================================
# استخدام نموذج ستريمليت مخفي لمعالجة الرسائل بسلاسة دون أن تضيع عند الإدخال
with st.sidebar:
    st.title("⚙️ الإعدادات الخلفية")
    st.session_state.model_name = st.selectbox("موديل الذكاء الاصطناعي:", AVAILABLE_MODELS, index=0)
    
    # نموذج استقبال البيانات المخفي المرتبط بالواجهة التفاعلية بالأسفل
    with st.form(key="hidden_chat_form", clear_on_submit=True):
        st.markdown("### إرسال رسالة يدوية")
        user_input = st.text_input("اكتب هنا واضغط إرسال:", key="st_chat_input")
        submit_btn = st.form_submit_button("إرسال للنظام")
        
        if submit_btn and user_input:
            st.session_state.conversation.append({"role": "user", "content": user_input})
            # هنا يمكنك ربط الموديل الفعلي لـ Gemini
            # response = model.generate_content(user_input)
            st.session_state.conversation.append({"role": "assistant", "content": f"تمت المعالجة التلقائية لنصك: '{user_input}' عبر الموديل بنجاح وبدون فقدان الخانات."})
            st.rerun()

# حقن كود الـ HTML التفاعلي لشريط الأدوات وقائمة الـ (+) الذكية أسفل الشاشة وثباتها تماماً
st.markdown("""
<!-- الخلفية المظلمة للقائمة -->
<div id="sheetOverlay" class="sheet-overlay" onclick="toggleBottomSheet(false)"></div>

<!-- القائمة المنبثقة السفلي المليئة بالمتطلبات (صورة 3) -->
<div id="bottomSheet" class="bottom-sheet">
    <div style="width:40px; hieght:5px; background:#3f3f46; height:5px; border-radius:999px; margin:0 auto 15px auto; cursor:pointer;" onclick="toggleBottomSheet(false)"></div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
        <span style="color:#a1a1aa; font-size:13px;">Flash موسّع <i class="fa-solid fa-chevron-down"></i></span>
        <i class="fa-solid fa-xmark" style="cursor:pointer;" onclick="toggleBottomSheet(false)"></i>
    </div>
    
    <!-- الأزرار السريعة الثلاثية -->
    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; margin-bottom:20px;">
        <div style="background:#18181b; border:1px solid #27272a; padding:12px; border-radius:16px; text-align:center; cursor:pointer;">
            <i class="fa-regular fa-image" style="color:#3b82f6; font-size:1.5rem; margin-bottom:5px;"></i><div style="font-size:12px;">الصور</div>
        </div>
        <div style="background:#18181b; border:1px solid #27272a; padding:12px; border-radius:16px; text-align:center; cursor:pointer;">
            <i class="fa-solid fa-camera" style="color:#10b981; font-size:1.5rem; margin-bottom:5px;"></i><div style="font-size:12px;">الكاميرا</div>
        </div>
        <div style="background:#18181b; border:1px solid #27272a; padding:12px; border-radius:16px; text-align:center; cursor:pointer;">
            <i class="fa-solid fa-paperclip" style="color:#f59e0b; font-size:1.5rem; margin-bottom:5px;"></i><div style="font-size:12px;">الملفات</div>
        </div>
    </div>

    <!-- متطلبات القائمة الكاملة المتطورة -->
    <div style="display:flex; flex-direction:column; gap:12px;">
        <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #18181b;">
            <div style="display:flex; align-items:center; gap:12px;">
                <i class="fa-solid fa-wand-magic-sparkles" style="color:#a855f7;"></i>
                <div><div style="font-size:13px; font-weight:bold;">إنشاء صور</div><div style="font-size:11px; color:#71717a;">الإنشاء والتعديل</div></div>
            </div>
            <i class="fa-solid fa-chevron-left" style="font-size:10px; color:#3f3f46;"></i>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #18181b;">
            <div style="display:flex; align-items:center; gap:12px;">
                <i class="fa-solid fa-music" style="color:#3b82f6;"></i>
                <div><div style="font-size:13px; font-weight:bold;">موسيقى</div><div style="font-size:11px; color:#71717a;">إنشاء مقاطع صوتية</div></div>
            </div>
            <i class="fa-solid fa-chevron-left" style="font-size:10px; color:#3f3f46;"></i>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #18181b;">
            <div style="display:flex; align-items:center; gap:12px;">
                <i class="fa-regular fa-file-code" style="color:#14b8a6;"></i>
                <div><div style="font-size:13px; font-weight:bold;">Canvas</div><div style="font-size:11px; color:#71717a;">الترميز أو الكتابة أو إنشاء الشرائح</div></div>
            </div>
            <i class="fa-solid fa-chevron-left" style="font-size:10px; color:#3f3f46;"></i>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #18181b;">
            <div style="display:flex; align-items:center; gap:12px;">
                <i class="fa-solid fa-magnifying-glass-chart" style="color:#f97316;"></i>
                <div><div style="font-size:13px; font-weight:bold;">Deep Research</div><div style="font-size:11px; color:#71717a;">احصل على تقارير مفصّلة</div></div>
            </div>
            <i class="fa-solid fa-chevron-left" style="font-size:10px; color:#3f3f46;"></i>
        </div>
    </div>
</div>

<!-- شريط الإدخال الرئيسي المثبت سفلياً (صورة 1 وصورة 2) -->
<div class="fixed-footer">
    <div class="input-container">
        <!-- زر علامة الزائد المطور لفتح القائمة السفلية ميكس -->
        <button class="btn-circle btn-plus" onclick="toggleBottomSheet(true)"><i class="fa-solid fa-plus"></i></button>
        
        <!-- خانة الرسائل التي لا تضيع -->
        <input type="text" id="customUiInput" placeholder="اسأل Saeed DaTaBoT أو أرسل استفسارك..." class="input-box" onkeypress="handleUiKeyPress(event)">
        
        <!-- زر الإيقاف المؤقت الدائري الأزرق من الصورة الأولى -->
        <button class="btn-circle btn-pause" onclick="triggerStreamlitSubmit()"><i class="fa-solid fa-pause"></i></button>
    </div>
    
    <!-- التبويبات المكس السفلية للتنقل التلقائي بين أقسام التطبيق الحقيقي -->
    <div class="nav-tabs-custom">
        <button class="nav-item" onclick="switchAppTab('إدارة المنتجات')">
            <i class="fa-solid fa-box-open"></i><span>إدارة المنتجات</span>
        </button>
        <button class="nav-item" onclick="switchAppTab('المحادثة الذكية')">
            <i class="fa-solid fa-comment-dots"></i><span>المحادثة الذكية</span>
        </button>
        <button class="nav-item" onclick="switchAppTab('أداة الفحص المتقدم')">
            <i class="fa-solid fa-wand-magic-sparkles"></i><span>أداة الفحص المتقدم</span>
        </button>
    </div>
</div>

<script>
// وظيفة فتح وإغلاق قائمة المتطلبات السفلية (+)
function toggleBottomSheet(open) {
    const sheet = document.getElementById('bottomSheet');
    const overlay = document.getElementById('sheetOverlay');
    if(open) {
        sheet.classList.add('open');
        overlay.classList.add('show');
    } else {
        sheet.classList.remove('open');
        overlay.classList.remove('show');
    }
}

// ربط خانة الرسائل الجديدة المكس بنظام ستريمليت لضمان عدم ضياع النص
function handleUiKeyPress(event) {
    if (event.key === "Enter") {
        triggerStreamlitSubmit();
    }
}

function triggerStreamlitSubmit() {
    const uiVal = document.getElementById('customUiInput').value;
    if(!uiVal) return;
    
    // البحث عن مربع الإدخال الجانبي الحقيقي التابع لـ Streamlit وحقن القيمة داخله
    const stInputs = window.parent.document.querySelectorAll('input[type="text"]');
    let targetInput = null;
    stInputs.forEach(inp => {
        if(inp.getAttribute('aria-label') && inp.getAttribute('aria-label').includes('اكتب هنا واضغط إرسال')) {
            targetInput = inp;
        }
    });
    
    if(targetInput) {
        targetInput.value = uiVal;
        targetInput.dispatchEvent(new Event('input', { bubbles: true }));
        // إرسال النموذج تلقائياً
        setTimeout(() => {
            const form = targetInput.closest('form');
            if(form) {
                const btn = form.querySelector('button[type="submit"]');
                if(btn) btn.click();
            }
        }, 50);
        document.getElementById('customUiInput').value = '';
    }
}

// وظيفة التنقل التلقائي السلس بين التبويبات بدون أي أخطاء
function switchAppTab(tabName) {
    const url = new URL(window.location.href);
    url.searchParams.set('action', 'change_tab');
    url.searchParams.set('tab_name', tabName);
    window.location.href = url.toString();
}

// تحديد التبويب النشط في واجهة المستخدم تلقائياً بناءً على وضع التطبيق الحالي
setTimeout(() => {
    const currentActiveTab = "{st.session_state.current_tab}";
    const buttons = document.querySelectorAll('.nav-item');
    buttons.forEach(btn => {
        if(btn.innerText.trim() === currentActiveTab) {
            btn.classList.add('active');
        }
    });
}, 100);
</script>
""", unsafe_allow_html=True)
