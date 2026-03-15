import os
import sys
import time
import threading
from pathlib import Path
from instagrapi import Client

yukleme_aktif = False

def yukleniyor_animasyonu():
    semboller = ['|', '/', '-', '\\']
    i = 0
    while yukleme_aktif:
        sys.stdout.write(f"\r[INSTAGRAM] Video yükleniyor, lütfen bekle... {semboller[i % 4]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * 60 + "\r")

def instagrama_yukle(video_yolu, aciklama, kullanici_adi, sifre):
    global yukleme_aktif
    print(f"\n[INSTAGRAM] '{kullanici_adi}' hesabı ile giriş yapılıyor...")
    
    cl = Client()
    
    try:
        # Oturum ayarlarını yükle
        if os.path.exists("session.json"):
            cl.load_settings("session.json")
            cl.login(kullanici_adi, sifre)
        else:
            cl.login(kullanici_adi, sifre)
            cl.dump_settings("session.json")

        print("[BAŞARILI] Hesaba giriş yapıldı.\n")
        
        # --- KAPAK FOTOĞRAFI AYARI (HATA ÇÖZÜCÜ) ---
        # Yapay zekanın arkaplanlar klasörüne çizdiği ilk sahneyi kapak yapıyoruz
        kapak_yolu = Path("arkaplanlar/sahne_1.jpg")
        
        yukleme_aktif = True
        animasyon_thread = threading.Thread(target=yukleniyor_animasyonu)
        animasyon_thread.start()
        
        # EĞER KAPAK VARSA ONU KULLAN (MoviePy Bypass)
        if kapak_yolu.exists():
            media = cl.clip_upload(
                Path(video_yolu), 
                caption=aciklama,
                thumbnail=kapak_yolu # <-- İŞTE BU SATIR HATAYI ÇÖZER!
            )
        else:
            # Kapak bulunamazsa (tedbir amaçlı) eski yöntem
            media = cl.clip_upload(
                Path(video_yolu), 
                caption=aciklama
            )
        
        yukleme_aktif = False
        animasyon_thread.join()
        
        print(f"[BAŞARILI] Reels videon Instagram'a ateşlendi! Medya ID: {media.pk}")
        
    except Exception as e:
        yukleme_aktif = False 
        if 'animasyon_thread' in locals() and animasyon_thread.is_alive():
            animasyon_thread.join()
            
        print(f"\n[HATA] Instagram yüklemesinde bir sorun oluştu: {e}")
        
        if os.path.exists("session.json"):
            try:
                os.remove("session.json")
                print("[BİLGİ] Bozuk oturum dosyası (session.json) silindi.")
            except:
                pass

if __name__ == '__main__':
    print("Bu modül ana sistem tarafından çağrılmalıdır.")