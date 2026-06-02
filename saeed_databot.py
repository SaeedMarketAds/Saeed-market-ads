import os
import json
import random
from pathlib import Path

# تحميل الإعدادات
CONFIG_PATH = Path(__file__).parent / "bot_config.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

class SaeedDataBot:
    def __init__(self):
        self.name = config.get('name', 'SaeedDataBot')
        self.owner = config.get('owner', 'سعيد المسوري')
        self.expertise = config.get('expertise', [])
        self.voice_path = Path(__file__).parent.parent / "static/audio/founder_voice.m4a"
        
    def get_welcome_message(self):
        """رسالة ترحيبية تعرف بنفسها"""
        return f"🎙️ أهلاً بك! أنا {self.name}، مساعدك الذكي المعتمد من خبرة {self.owner}. أسواق العالم بين يديك. كيف أخدمك اليوم؟"
    
    def get_voice_greeting(self):
        """إرجاع مسار ملف الصوت الترحيبي (صوتك الحقيقي)"""
        if self.voice_path.exists():
            return f"/static/audio/founder_voice.m4a"
        return None
    
    def generate_response(self, user_message):
        """توليد رد ذكي (يمكن ربطه بـ Gemini API لاحقاً)"""
        msg = user_message.lower()
        
        # ردود ذكية حسب السياق
        if any(word in msg for word in ['aliexpress', 'علي', 'اكسبريس']):
            return {
                'text': '🔍 AliExpress وجهتك المثالية للإلكترونيات والإكسسوارات بأسعار تنافسية. هل تبحث عن منتج محدد؟',
                'suggestions': ['هواتف', 'سماعات', 'ساعات ذكية']
            }
        elif any(word in msg for word in ['noon', 'نون']):
            return {
                'text': '🇦🇪 Noon يتميز بالتوصيل السريع في الإمارات والسعودية. يمكنني البحث عن كوبونات خصم حصرية لك!',
                'suggestions': ['تخفيضات', 'توصيل مجاني', 'عروض اليوم']
            }
        elif any(word in msg for word in ['shein', 'شين']):
            return {
                'text': '👗 Shein أحدث صيحات الموضة والأزياء بأسعار لا تُقارن. هل تبحث عن فستان، حقيبة، أو إكسسوارات؟',
                'suggestions': ['فساتين', 'حقائب', 'أحذية']
            }
        elif any(word in msg for word in ['يمن', 'يمني', 'محلي', 'ريال']):
            return {
                'text': '🇾🇪 السوق اليمني قادم قريباً جداً! سندعم المحافظ الإلكترونية اليمنية. شكراً لدعمك الاقتصاد المحلي ❤️',
                'suggestions': ['متى الإطلاق؟', 'كيف أنضم كتاجر؟']
            }
        elif any(word in msg for word in ['شكر', 'جزاك']):
            return {
                'text': 'العفو! شكر الله لك. أنا هنا لخدمتك ولخدمة أطفالك. لا تتردد أبداً في طلب المساعدة 🙏',
                'suggestions': []
            }
        elif any(word in msg for word in ['سعر', 'غالي', 'رخيص', 'عرض', 'خصم']):
            return {
                'text': '📊 كخبير في تحليل الأسواق، أنصحك بمقارنة الأسعار بين AliExpress و Noon. هل تريد مني البحث عن أفضل عرض لمنتج معين؟',
                'suggestions': ['أبحث عن هاتف', 'أبحث عن لابتوب']
            }
        else:
            return {
                'text': f'أنا {self.name}، خبير {", ".join(self.expertise)}. أخبرني ما الذي تبحث عنه وسأجد لك أفضل العروض في AliExpress، Noon، و Shein.',
                'suggestions': ['عروض AliExpress', 'تخفيضات Noon', 'أزياء Shein', 'السوق اليمني']
            }
    
    def connect_gemini(self, api_key):
        """ربط البوت بـ Gemini API (التفعيل لاحقاً)"""
        self.gemini_api_key = api_key
        # هنا سيتم إضافة كود ربط Gemini الفعلي
        return True
