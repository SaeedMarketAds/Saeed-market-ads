# ========== المكتبات ==========
import telebot
import os
import subprocess

# ========== إعداد البوت ==========
TOKEN = "ضع_توكن_البوت_هنا"  # 🔴 غير هذا إلى توكن البوت الحقيقي
bot = telebot.TeleBot(TOKEN)

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
        "📌 الأوامر المتاحة:\n"
        "/shein - لعرض متجر SHEIN\n"
        "/coupon - للحصول على كود الخصم"
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

# ========== أمر /shein (الرئيسي) ==========
@bot.message_handler(commands=['shein'])
def cmd_shein(message):
    chat_id = message.chat.id
    
    # إعلام المستخدم بالبدء
    bot.send_message(chat_id, "🛍️ جاري تجهيز متجر SHEIN... لحظة من فضلك")
    
    # التأكد من وجود ملف المتجر
    if not os.path.exists('shein_store.html'):
        bot.send_message(chat_id, "⚠️ هذا أول تشغيل... جاري توليد المتجر")
        try:
            subprocess.run(['python', 'shein_products.py'], timeout=30)
        except Exception as e:
            bot.send_message(chat_id, f"❌ خطأ في التوليد: {e}")
            return
    
    # إرسال المتجر
    if send_shein_store(chat_id):
        print(f"✅ تم إرسال المتجر للمستخدم {chat_id}")
    else:
        # محاولة إعادة التوليد
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
print("🤖 بوت SaeedMarket يعمل الآن...")
print("📌 انتظر الأوامر: /start , /shein , /coupon")
print("=" * 40)

bot.infinity_polling()
