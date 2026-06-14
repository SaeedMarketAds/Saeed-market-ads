import os
import telebot
import subprocess
import google.generativeai as genai

# ========== جلب المفاتيح من متغيرات البيئة ==========
BOT_TOKEN = os.environ.get("TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API")

# ========== إعداد البوت ==========
bot = telebot.TeleBot(BOT_TOKEN)

# ========== إعداد نموذج Gemini 3.5 Flash ==========
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3.5-flash')

# ========== دالة للتواصل مع Gemini ==========
def ask_gemini(prompt):
    """إرسال سؤال إلى Gemini والحصول على رد"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ خطأ في الاتصال بـ Gemini: {e}"

# ========== دالة إرسال متجر SHEIN ==========
def send_shein_store(chat_id):
    """إرسال متجر SHEIN عبر Telegram"""
    try:
        with open('shein_store.html', 'rb') as doc:
            bot.send_document(
                chat_id, 
                doc, 
                caption="🛍️ **متجر SHEIN - أحدث المنتجات**\n\n🎁 **كود الخصم: WL7KA**\n💰 خصم 60% للمستخدمين الجدد\n\n@SaeedMarketAds",
                parse_mode='Markdown'
            )
        return True
    except Exception as e:
        return False

# ========== أمر /start ==========
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message, 
        "مرحباً بك في متجر سعيد! 🎉\n\n"
        "📌 **الأوامر المتاحة:**\n"
        "/shein - لعرض متجر SHEIN\n"
        "/coupon - للحصول على كود الخصم\n"
        "/ask [سؤالك] - اسأل الذكاء الاصطناعي Gemini\n"
        "/about - معلومات عن البوت\n\n"
        "✨ البوت مدعوم بـ **Gemini 3.5 Flash** من Google"
    )

# ========== أمر /about ==========
@bot.message_handler(commands=['about'])
def about(message):
    bot.reply_to(
        message,
        "🤖 **بوت Saeed Market Ads**\n\n"
        "✅ متجر منتجات SHEIN\n"
        "✅ كود خصم حصري WL7KA\n"
        "✅ ذكاء اصطناعي Gemini 3.5 Flash\n"
        "✅ دعم منتجات نون وعلي إكسبرس قريباً\n\n"
        "👨‍💻 المطور: Saeed\n"
        "📧 للتواصل: @SaeedMarketAds",
        parse_mode='Markdown'
    )

# ========== أمر /coupon ==========
@bot.message_handler(commands=['coupon'])
def send_coupon(message):
    bot.reply_to(
        message,
        "🎁 **كود الخصم الحصري:** `WL7KA`\n\n"
        "💰 خصم 60% للمستخدمين الجدد\n"
        "📱 استخدم الكود عند الدفع في تطبيق SHEIN\n\n"
        "رابط التحميل: https://onelink.shein.com",
        parse_mode='Markdown'
    )

# ========== أمر /ask (الذكاء الاصطناعي) ==========
@bot.message_handler(commands=['ask'])
def ask_ai(message):
    question = message.text.replace('/ask', '').strip()
    
    if not question:
        bot.reply_to(
            message,
            "🤖 **كيف تستخدم أمر /ask:**\n\n"
            "اكتب: `/ask ما هو أفضل هاتف؟`\n"
            "أو: `/ask اشرح لي الذكاء الاصطناعي`\n\n"
            "سأجيبك باستخدام Gemini 3.5 Flash",
            parse_mode='Markdown'
        )
        return
    
    bot.send_message(message.chat.id, "🤖 جاري التفكير... لحظة من فضلك")
    answer = ask_gemini(question)
    
    if len(answer) > 4000:
        for i in range(0, len(answer), 4000):
            bot.send_message(message.chat.id, answer[i:i+4000])
    else:
        bot.reply_to(message, f"🤖 **Gemini 3.5 Flash يقول:**\n\n{answer}", parse_mode='Markdown')

# ========== معالجة الرسائل النصية العادية ==========
@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    user_text = message.text
    
    if user_text.startswith('/'):
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    response = ask_gemini(user_text)
    
    if len(response) > 4000:
        for i in range(0, len(response), 4000):
            bot.send_message(message.chat.id, response[i:i+4000])
    else:
        bot.reply_to(message, response)

# ========== أمر /shein ==========
@bot.message_handler(commands=['shein'])
def cmd_shein(message):
    chat_id = message.chat.id
    
    bot.send_message(chat_id, "🛍️ جاري تجهيز متجر SHEIN... لحظة من فضلك")
    
    if not os.path.exists('shein_store.html'):
        bot.send_message(chat_id, "⚠️ هذا أول تشغيل... جاري توليد المتجر")
        try:
            subprocess.run(['python', 'shein_products.py'], timeout=30)
        except Exception as e:
            bot.send_message(chat_id, f"❌ خطأ في التوليد: {e}")
            return
    
    if send_shein_store(chat_id):
        print(f"✅ تم إرسال المتجر للمستخدم {chat_id}")
    else:
        bot.send_message(chat_id, "🔄 جاري إعادة تجهيز المتجر...")
        try:
            subprocess.run(['python', 'shein_products.py'], timeout=30)
            if send_shein_store(chat_id):
                bot.send_message(chat_id, "✅ تم بنجاح!")
            else:
                bot.send_message(chat_id, "❌ فشل إرسال المتجر، حاول مرة أخرى")
        except Exception as e:
            bot.send_message(chat_id, f"❌ خطأ: {e}")

# ========== تشغيل البوت ==========
print("=" * 40)
print("🤖 بوت SaeedMarket يعمل الآن...")
print("📌 الأوامر المتاحة:")
print("   /start  - الترحيب والأوامر")
print("   /shein  - متجر SHEIN")
print("   /coupon - كود الخصم")
print("   /ask    - اسأل Gemini AI")
print("   /about  - معلومات عن البوت")
print("✨ مدعوم بـ Google Gemini 1.5 Flash")
print("=" * 40)

bot.infinity_polling()
