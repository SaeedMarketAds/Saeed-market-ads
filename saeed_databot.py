import json
import os
import base64
from pathlib import Path

# تحميل الإعدادات
CONFIG_PATH = Path(__file__).parent / "saeed_databot_config.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

class SaeedDataBot:
    def __init__(self):
        self.name = config.get('name', 'SaeedDataBot')
        self.owner = config.get('owner', 'سعيد المسوري')
        self.expertise = config.get('expertise', [])
        # مسار ملف صوتك
        self.voice_path = Path(__file__).parent.parent / "Saeed_Voice_01.m4a"
        
    def get_welcome_message(self):
        """رسالة ترحيبية"""
        return f"🎙️ أهلاً بك! أنا {self.name}، مساعدك الذكي. أسواق العالم بين يديك، كيف أخدمك اليوم؟"
    
    def get_voice_html(self):
        """توليد كود HTML لتشغيل صوتك"""
        if self.voice_path.exists():
            with open(self.voice_path, "rb") as f:
                audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            return f'''
            <audio autoplay="true" src="data:audio/m4a;base64,{audio_base64}">
                <source src="data:audio/m4a;base64,{audio_base64}" type="audio/mp4">
            </audio>
            '''
        return ""
    
    def generate_response(self, user_message):
        """توليد رد ذكي حسب كلام المستخدم"""
        msg = user_message.lower()
        
        responses = {
            'aliexpress': "🔍 AliExpress يقدم أفضل الأسعار للإلكترونيات. هل تبحث عن منتج محدد؟",
            'noon': "🇦🇪 Noon يتميز بالتوصيل السريع. سأبحث لك عن كوبونات خصم حصرية!",
            'shein': "👗 Shein وجهتك للأزياء العصرية. أحدث التشكيلات بأسعار رائعة.",
            'يمني': "🇾🇪 السوق اليمني قادم قريباً مع دعم المحافظ الإلكترونية. شكراً لدعمك!",
            'محلي': "🇾🇪 السوق اليمني قادم قريباً مع دعم المحافظ الإلكترونية. شكراً لدعمك!",
            'شكرا': "العفو! أنا هنا لخدمتك دائماً يا صاحب المشروع 🙏",
            'سعر': "📊 تحليل الأسعار: أنصحك بمقارنة العروض قبل الشراء.",
            'عرض': "🎁 لدينا عروض حصرية على AliExpress و Noon حالياً!"
        }
        
        for key, response in responses.items():
            if key in msg:
                return response
        
        return f"📊 كخبير في {', '.join(self.expertise)}، كيف يمكنني مساعدتك اليوم؟"
