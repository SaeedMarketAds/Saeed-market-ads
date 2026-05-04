import os
import json
from google import genai
from gtts import gTTS

# تحديد المسار التلقائي لمكان وجود الملف
current_dir = os.path.dirname(os.path.abspath(__file__))

# البحث عن ملف saeed_key.json في المجلد الحالي أو في مجلد assets
key_path = os.path.join(current_dir, "saeed_key.json")
if not os.path.exists(key_path):
    key_path = os.path.join(current_dir, "assets", "saeed_key.json")

# تحميل المفتاح السري
api_key = None
try:
    if os.path.exists(key_path):
        with open(key_path, 'r') as f:
            key_data = json.load(f)
            api_key = key_data.get("api_key")
    else:
        raise FileNotFoundError("ملف المفتاح السري غير موجود.")
except Exception as e:
    print(f"خطأ في قراءة ملف المفتاح السري: {e}")

# تهيئة العميل
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    client = None
    print(f"خطأ في تهيئة العميل: {e}")

def speak_response(text, filename="response.mp3"):
    """دالة لتحويل رد البوت إلى ملف صوتي"""
    try:
        tts = gTTS(text=text, lang='ar', slow=False)
        file_path = os.path.join(current_dir, filename)
        tts.save(file_path)
        print(f"\n🔊 [تم حفظ الصوت]: {file_path}")
    except Exception as e:
        print(f"تعذر توليد الصوت: {e}")

def main():
    if not api_key:
        print("⚠️ توقف: لم يتم العثور على API Key. تأكد من وضعه في الملف.")
        return
        
    print("=== بدء تشغيل Saeed DataBot التفاعلي ===")
    
    while True:
        user_input = input("\nأدخل سؤالك أو المهمة المطلوبة (أو اكتب 'خروج' للإنهاء): ")
        
        if user_input.strip().lower() == 'خروج':
            print("إلى اللقاء! مع تحيات Saeed MarketAds.")
            break
            
        if not user_input.strip():
            continue
            
        try:
            # استخدام نموذج gemini-2.5-flash لتجنب استهلاك الحصة المجانية
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_input,
            )
            
            bot_text = response.text
            print(f"\n[Saeed DataBot]: {bot_text}")
            
            speak_response(bot_text)
            
        except Exception as e:
            print(f"\nحدث خطأ أثناء الاتصال: {e}")
            break

if __name__ == "__main__":
    main()
