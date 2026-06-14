import os
import telebot
import subprocess
import google.generativeai as genai

# ========== جلب المفاتيح من متغيرات البيئة ==========
# تأكد من إضافة TOKEN و GEMINI_API في إعدادات المنصة (Render)
BOT_TOKEN = os.environ.get("TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API")

if not BOT_TOKEN or not GEMINI_API_KEY:
    print("❌ خطأ: يرجى التأكد من إضافة TOKEN و GEMINI_API في متغيرات البيئة")
    exit()

# ========== إعداد البوت ==========
bot = telebot.TeleBot(BOT_TOKEN)

# ========== إعداد Gemini ==========
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3.5-flash') 

# ========== الدوال ==========
def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ خطأ في الاتصال بـ Gemini: {e}"

def send_shein_store(chat_id):
    try:
        with open('shein_store.html', 'rb') as doc:
            bot.send_document(
                chat_id, 
                doc, 
                caption="🛍️ **متجر SHEIN - أحدث المنتجات**\n\n🎁 **كود الخصم: WL7KA**\n💰 خصم 60% للمستخدمين الجدد",
                parse_mode='Markdown'
            )
        return True
    except Exception:
        return False

# ========== الأوامر ==========
@bot.message_handler(commands=['start', 'about', 'coupon'])
def main_commands(message):
    if message.text == '/start':
        bot.reply_to(message, "مرحباً بك في متجر سعيد! استخدم /shein لعرض المتجر.")
    elif message.text == '/about':
        bot.reply_to(message, "🤖 بوت Saeed Market Ads\n✅ مدعوم بـ Gemini 1.5 Flash")
    elif message.text == '/coupon':
        bot.reply_to(message, "🎁 كود الخصم الحصري: `WL7KA`", parse_mode='Markdown')

@bot.message_handler(commands=['ask'])
def ask_ai(message):
    question = message.text.replace('/ask', '').strip()
    if not question:
        bot.reply_to(message, "يرجى كتابة سؤال بعد /ask")
        return
    msg = bot.reply_to(message, "🤖 جاري التفكير...")
    answer = ask_gemini(question)
    bot.edit_message_text(f"🤖 **Gemini يقول:**\n\n{answer}", chat_id=message.chat.id, message_id=msg.message_id, parse_mode='Markdown')

@bot.message_handler(commands=['shein'])
def cmd_shein(message):
    bot.send_message(message.chat.id, "🛍️ جاري تجهيز المتجر...")
    # تشغيل ملف توليد المتجر
    subprocess.run(['python', 'shein_products.py'])
    if not send_shein_store(message.chat.id):
        bot.send_message(message.chat.id, "❌ حدث خطأ أثناء إرسال الملف.")

@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def chat_with_ai(message):
    bot.send_chat_action(message.chat.id, 'typing')
    response = ask_gemini(message.text)
    bot.reply_to(message, response)

# ========== تشغيل البوت ==========
print("🤖 بوت SaeedMarket يعمل الآن...")
bot.infinity_polling()
