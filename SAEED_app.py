def send_shein_store(bot, chat_id):
    """إرسال متجر SHEIN عبر Telegram"""
    with open('shein_store.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # إرسال كملف أو معاينة
    with open('shein_store.html', 'rb') as doc:
        bot.send_document(chat_id, doc, caption="🛍️ متجر SHEIN - أحدث المنتجات\n🎁 كود الخصم: WL7KA")
