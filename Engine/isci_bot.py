import mysql.connector
import time
import os
import main

# LARAGON VERİTABANI AYARLARIN
DB_AYARLARI = {
    'host': 'localhost',
    'user': 'root', # Laragon varsayılan kullanıcısı
    'password': '', # Laragon'da şifre genelde boştur
    'database': 'automation_web' # Kendi veritabanı adını buraya yaz (tonga_db veya ne koyduysan)
}

def is_var_mi_kontrol_et():
    try:
        # Veritabanına sız
        db = mysql.connector.connect(**DB_AYARLARI)
        cursor = db.cursor(dictionary=True)

        # "bekliyor" statüsündeki İLK İŞİ al
        cursor.execute("SELECT * FROM videos WHERE status = 'bekliyor' ORDER BY id ASC LIMIT 1")
        is_kaydi = cursor.fetchone()

        if is_kaydi:
            is_id = is_kaydi['id']
            ses_yolu = is_kaydi['audio_path']
            
            # Eğer Windows yolunda ters slash varsa düzeltelim
            ses_yolu = ses_yolu.replace("\\", "/")

            print(f"\n[İŞÇİ] 🚨 YENİ GÖREV YAKALANDI! ID: {is_id}")
            print(f"[İŞÇİ] Hedef Dosya: {ses_yolu}")

            # 1. Panele Haber Ver: "Ben bunu işlemeye başladım, sarı ikon yak!"
            cursor.execute("UPDATE videos SET status = 'isleniyor' WHERE id = %s", (is_id,))
            db.commit()

            try:
                # =====================================================================
                # 🚀 SİMÜLASYON BİTTİ, GERÇEK YAPAY ZEKA MOTORU ATEŞLENİYOR!
                # =====================================================================
                print(f"[İŞÇİ] {ses_yolu} dosyası Yapay Zeka Motoruna gönderiliyor...")
                
                # Hem sesi veriyoruz, hem de eğer panelden girildiyse o özel başlığı veriyoruz
                cikti_video_yolu = main.tonga_motorunu_calistir(ses_yolu, ozel_baslik=is_kaydi.get('title'))
                
                # Yollardaki \ işaretlerini / ile değiştirelim (Windows Laravel sorunu olmasın)
                cikti_video_yolu = cikti_video_yolu.replace("\\", "/")

                # 2. İş Bitti! Panele Haber Ver: "Videoyu Jilet Gibi Teslim Ettim!"
                cursor.execute("UPDATE videos SET status = 'tamamlandı', video_path = %s WHERE id = %s", (cikti_video_yolu, is_id))
                db.commit()
                print(f"[BAŞARILI] Görev {is_id} tamamlandı! Panelde yeşil ışık yandı.")

            except Exception as e:
                # 3. Motor Çökerse Panele Haber Ver: "Abi Hata Var!"
                hata_mesaji = str(e)
                cursor.execute("UPDATE videos SET status = 'hata', error_log = %s WHERE id = %s", (hata_mesaji, is_id))
                db.commit()
                print(f"[HATA] Görev {is_id} başarısız oldu: {hata_mesaji}")

        cursor.close()
        db.close()

    except Exception as e:
        print(f"[VERİTABANI HATASI] MySQL'e ulaşılamıyor: {e}")

# ==========================================
# İŞÇİ NÖBETE BAŞLIYOR (SONSUZ DÖNGÜ)
# ==========================================
if __name__ == "__main__":
    print("🤖 Tonga AI İşçi Botu Uyandı. Bekleyen işler dinleniyor...")
    while True:
        is_var_mi_kontrol_et()
        time.sleep(5) # Veritabanını yormamak için 5 saniyede bir sor