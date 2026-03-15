import os
import json
import time
from google import genai
from google.genai import types

# ==========================================
# BURAYA KENDİ GEMINI API ŞİFRENİ YAPIŞTIR
GEMINI_API_KEY = "AIzaSyC1J-MNudLfzfXsRD5aQSEyfbdMFwETtDk"
# ==========================================

client = genai.Client(api_key=GEMINI_API_KEY)

def sesi_analiz_et(ses_yolu, maksimum_deneme=4): 
    print(f"\n[BEYİN] '{ses_yolu}' dosyası Gemini'ye yükleniyor. Kulaklar açıldı...")
    
    for deneme in range(maksimum_deneme):
        try:
            # 1. Sesi Google sunucularına yüklüyoruz
            print(f"[BEYİN] Dosya yükleniyor... (Deneme {deneme + 1}/{maksimum_deneme})")
            ses_dosyasi = client.files.upload(file=ses_yolu)
            print("[BEYİN] Yükleme tamam. Gemini 2.5 podcasti dinliyor...")
            
            # 2. Yapay zekaya verdiğimiz kesin emir
            prompt = """
            Sen Tonga Ai adlı teknoloji ve felsefe kanalının profesyonel podcast yapımcısı ve sanat yönetmenisin. 
            Sana verdiğim bu ses dosyasını dinle. İçeriğine ve anlattığı felsefi konuya uygun olarak bana geçerli bir JSON çıktısı ver.
            
            JSON şablonu tam olarak şu şekilde olmalıdır:
            {
                "youtube_baslik": "Videonun YouTube başlığı (Çarpıcı ve felsefi)",
                "youtube_aciklama": "YouTube için SEO uyumlu, felsefi ve hashtag içeren uzun açıklama",
                "reels_aciklama": "Instagram Reels için kısa, merak uyandırıcı açıklama ve hashtagler",
                "resim_komutlari": [
                    "Sahne 1 için İngilizce Stable Diffusion promptu (cinematic, dark atmospheric, highly detailed 8k, philosophy theme)",
                    "Sahne 2 için İngilizce prompt..."
                ]
            }
            
            Not: resim_komutlari dizisi tam olarak 15 elemanlı (15 farklı sahne) olmalıdır.
            """
            
            ayar = types.GenerateContentConfig(
                response_mime_type="application/json",
            )
            
            # 3. İsteği Yolluyoruz
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[ses_dosyasi, prompt],
                config=ayar
            )
            
            # 4. JSON Çıktısını Alıyoruz
            analiz_sonucu = json.loads(response.text)
            print("[BAŞARILI] Gemini podcasti anladı ve tüm yayın planını çıkardı!")
            
            # Sunucuda yer kaplamaması için dosyayı siliyoruz
            try:
                client.files.delete(name=ses_dosyasi.name)
            except:
                pass # Silinemezse çok da önemli değil
                
            return analiz_sonucu
            
        except Exception as e:
            # HATA NE OLURSA OLSUN YAKALAYIP BEKLİYORUZ (10060 Bağlantı Hatası Dahil)
            print(f"[UYARI] Bir bağlantı sorunu veya hata oluştu: {e}")
            
            if deneme < maksimum_deneme - 1:
                bekleme_suresi = 15 * (deneme + 1) # Her denemede bekleme süresi artar (15s, 30s, 45s)
                print(f"[UYARI] İnternet kopmuş veya sunucu meşgul olabilir. {bekleme_suresi} saniye beklenip tekrar denenecek...\n")
                time.sleep(bekleme_suresi)
            else:
                print("\n[BAŞARISIZ] 4 deneme yapıldı ama Google'a bağlanılamadı. Lütfen modemi kapatıp açmayı veya VPN açmayı/kapatmayı dene.")
                return None

# SADECE BU DOSYAYI ÇALIŞTIRIRSAK TEST ETMEK İÇİN:
if __name__ == "__main__":
    test_ses = "girdiler/test_ses.mp3" 
    if os.path.exists(test_ses):
        sesi_analiz_et(test_ses)
    else:
        print(f"[HATA] Test dosyası bulunamadı: {test_ses}")