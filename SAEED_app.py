import streamlit as st
import time

# ==========================================
# 1. إعدادات الصفحة وحالة جلسة الصوت
# ==========================================
st.set_page_config(page_title="مساعد الصوت الذكي", layout="wide")

# حالات الجلسة للتحكم في البث الصوتي وظهور القائمة
if "audio_streaming" not in st.session_state:
    st.session_state.audio_streaming = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "أنظمة الصوت جاهزة. اضغط على الزر الأزرق لبدء البث أو الإيقاف المباشر."}]

# ==========================================
# 2. حقن واجهة تصميم الصوت (Gemini Audio UI)
# ==========================================
audio_ui_style = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
/* تهيئة الخلفية الداكنة العميقة */
[data-testid="stAppViewContainer"] {
    background: #09090b;
    color: #f4f4f5;
}

/* شريط إدخال الصوت السفلي المطور */
.audio-footer {
    position: fixed;
    bottom: 20px; left: 0; right: 0;
    z-index: 999;
    padding: 0 20px;
}
.audio-input-container {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #18181b;
    border: 1px solid #27272a;
    border-radius: 9999px;
    padding: 8px 16px;
    max-width: 650px;
    margin: 0 auto;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

/* زر البث/الإيقاف الأزرق الدائري (كما في الصورة تماماً) */
.btn-audio-core {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: #2563eb;
    color: white;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(37,99,235,0.4);
    transition: transform 0.2s, background 0.2s;
}
.btn-audio-core:hover { background: #1d4ed8; transform: scale(1.05); }
.btn-audio-core.active {
    background: #dc2626; /* يتحول للأحمر عند البث النشط */
    box-shadow: 0 4px 15px rgba(220,38,38,0.4);
}

/* باقي أزرار التحكم في الشريط */
.icon-btn {
    background: transparent;
    border: none;
    color: #a1a1aa;
    font-size: 1.3rem;
    cursor: pointer;
    transition: color 0.2s;
}
.icon-btn:hover { color: #f4f4f5; }

.audio-text-field {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: white;
    font-size: 15px;
    text-align: right;
    direction: rtl;
}

/* القائمة المنبثقة الذكية الخاصة بعلامة (+) */
.audio-sheet {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: #111113;
    border-top: 1px solid #27272a;
    border-top-left-radius: 24px;
    border-top-right-radius: 24px;
    z-index: 9999;
    padding: 24px;
    transform: translateY(100%);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.audio-sheet.show { transform: translateY(0); }
.audio-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.7);
    z-index: 9998;
    display: none;
}
.audio-overlay.show { display: block; }
</style>
"""
st.markdown(audio_ui_style, unsafe_allow_html=True)

# ==========================================
# 3. معالجة أحداث وتغيير حالة البث المباشر
# ==========================================
# استقبال إشارات التحكم بالصوت من أزرار الواجهة المخصصة
params = st.query_params
if "toggle_stream" in params:
    st.session_state.audio_streaming = not st.session_state.audio_streaming
    st.query_params.clear()
    st.rerun()

# ==========================================
# 4. عرض ساحة الردود والمحادثة الصوتية
# ==========================================
st.markdown("<h3 style='text-align: center; color: #a1a1aa;'>🎙️ نظام معالجة الصوت المباشر</h3>", unsafe_allow_html=True)

chat_area = st.container()
with chat_area:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<div style='text-align:right; margin:12px;'><span style='background:#2563eb; color:white; padding:10px 16px; border-radius:18px 18px 0 18px; display:inline-block; max-width:75%;'>{msg['content']}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left; margin:12px;'><span style='background:#1c1c1e; color:#e4e4e7; padding:10px 16px; border-radius:18px 18px 18px 0; display:inline-block; max-width:75%; border:1px solid #27272a;'>{msg['content']}</span></div>", unsafe_allow_html=True)

# ==========================================
# 5. منطقة المعالجة البرمجية للصوت (المحرك الخاص بك)
# ==========================================
if st.session_state.audio_streaming:
    st.markdown("<p style='text-align:center; color:#10b981;'><i class='fa-solid fa-spinner fa-spin'></i> جاري التقاط دفق الصوت وبث البيانات الحية...</p>", unsafe_allow_html=True)
    
    # ⬇️ ضع كود معالجة بث الصوت أو التقاط الميكروفون الخاص بك هنا ⬇️
    # مثال: معالجة الإطارات الصوتية (Audio Chunks) وتمريرها للموديل
    # chunks = your_audio_stream.read()
    # pass
    
else:
    st.markdown("<p style='text-align:center; color:#71717a;'>البث الصوتي متوقف حالياً.</p>", unsafe_allow_html=True)


# ==========================================
# 6. حقن شريط التحكم الصوتي التفاعلي الثابت
# ==========================================
is_active_class = "active" if st.session_state.audio_streaming else ""
audio_icon = '<i class="fa-solid fa-pause"></i>' if st.session_state.audio_streaming else '<i class="fa-solid fa-waveform"></i>'

st.markdown(f"""
<!-- خلفية القائمة المنبثقة للـ (+) -->
<div id="audioOverlay" class="audio-overlay" onclick="toggleAudioSheet(false)"></div>

<!-- القائمة المنبثقة الذكية للخلفية المكس (+) -->
<div id="audioSheet" class="audio-sheet">
    <div style="width:50px; height:5px; background:#3f3f46; border-radius:999px; margin:0 auto 20px auto; cursor:pointer;" onclick="toggleAudioSheet(false)"></div>
    <h4 style="color:#a1a1aa; margin-bottom:15px; font-size:14px;">أدوات فلاش المتقدمة للصوت</h4>
    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:12px;">
        <div style="background:#18181b; border:1px solid #27272a; padding:15px; border-radius:16px; text-align:center; cursor:pointer;">
            <i class="fa-solid fa-microphone-lines" style="color:#a855f7; font-size:1.5rem; margin-bottom:6px;"></i>
            <div style="font-size:12px; color:white;">تنقية الصوت</div>
        </div>
        <div style="background:#18181b; border:1px solid #27272a; padding:15px; border-radius:16px; text-align:center; cursor:pointer;">
            <i class="fa-solid fa-file-audio" style="color:#3b82f6; font-size:1.5rem; margin-bottom:6px;"></i>
            <div style="font-size:12px; color:white;">رفع ملف صوتي</div>
        </div>
        <div style="background:#18181b; border:1px solid #27272a; padding:15px; border-radius:16px; text-align:center; cursor:pointer;">
            <i class="fa-solid fa-language" style="color:#10b981; font-size:1.5rem; margin-bottom:6px;"></i>
            <div style="font-size:12px; color:white;">ترجمة فورية</div>
        </div>
    </div>
</div>

<!-- شريط الصوت المخصص السفلي (المطابق تماماً للصورة) -->
<div class="audio-footer">
    <div class="audio-input-container">
        
        <!-- 1. زر البث والإيقاف الدائري الأزرق (يتحول لأحمر عند التشغيل) -->
        <button class="btn-audio-core {is_active_class}" onclick="triggerAudioStream()">
            {audio_icon}
        </button>
        
        <!-- 2. أيقونة الميكروفون الجانبية -->
        <button class="icon-btn" style="margin-left: 5px;"><i class="fa-solid fa-microphone"></i></button>
        
        <!-- 3. خانة نص الذكاء الاصطناعي -->
        <input type="text" id="audioInputField" placeholder="اسأل Gemini أو ابدأ التحدث..." class="audio-text-field" onkeypress="handleAudioSend(event)">
        
        <!-- 4. زر الـ (+) لفتح قائمة المتطلبات الموسعة -->
        <button class="icon-btn" onclick="toggleAudioSheet(true)"><i class="fa-solid fa-plus"></i></button>
        
    </div>
</div>

<script>
// التحكم في ظهور وإغلاق قائمة الخيارات المتقدمة (+)
function toggleAudioSheet(show) {{
    const sheet = document.getElementById('audioSheet');
    const overlay = document.getElementById('audioOverlay');
    if(show) {{
        sheet.classList.add('show');
        overlay.classList.add('show');
    }} else {{
        sheet.classList.remove('show');
        overlay.classList.remove('show');
    }}
}}

// إطلاق وتبديل حالة البث الصوتي في نظام ستريمليت
function triggerAudioStream() {{
    const url = new URL(window.location.href);
    url.searchParams.set('toggle_stream', '1');
    window.location.href = url.toString();
}}

// معالجة إرسال النصوص من داخل الشريط الصوتي
function handleAudioSend(e) {{
    if(e.key === 'Enter') {{
        const val = document.getElementById('audioInputField').value;
        if(!val) return;
        alert('جاري إرسال النص معالجة مع تيار الصوت المعين: ' + val);
        document.getElementById('audioInputField').value = '';
    }}
}}
</script>
""", unsafe_allow_html=True)

