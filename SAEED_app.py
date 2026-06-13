def send_shein_store(bot, chat_id):
    """إرسال متجر SHEIN عبر Telegram"""
    with open('shein_store.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # إرسال كملف أو معاينة
    with open('shein_store.html', 'rb') as doc:
        bot.send_document(chat_id, doc, caption="🛍️ متجر SHEIN - أحدث المنتجات\n🎁 كود الخصم: WL7KA")
# أضف هذا في بداية الملف مع المكتبات الأخرى
import os
from telebot import types

# ثم أضف أمراً جديداً للبوت
@bot.message_handler(commands=['shein'])
def cmd_shein(message):
    """إرسال متجر SHEIN عند استخدام الأمر /shein"""
    chat_id = message.chat.id
    
    # أولاً: تأكد من وجود ملف المتجر
    if not os.path.exists('shein_store.html'):
        bot.send_message(chat_id, "⚠️ جاري تجهيز المتجر... يرجى المحاولة مرة أخرى بعد لحظة")
        # يمكنك تشغيل shein_products.py هنا تلقائياً
        os.system('python shein_products.py')
    
    # إرسال المتجر
    try:
        with open('shein_store.html', 'rb') as doc:
            bot.send_document(
                chat_id, 
                doc, 
                caption="🛍️ **متجر SHEIN - أحدث المنتجات**\n\n🎁 **كود الخصم: WL7KA**\n💰 خصم 60% للمستخدمين الجدد\n\n@SaeedMarketAds",
                parse_mode='Markdown'
            )
    except Exception as e:
        bot.send_message(chat_id, f"❌ حدث خطأ: {e}")
        # توليد المتجر من جديد
        os.system('python shein_products.py')
        with open('shein_store.html', 'rb') as doc:
            bot.send_document(chat_id, doc, caption="🛍️ متجر SHEIN - أحدث المنتجات\n🎁 كود الخصم: WL7KA")
