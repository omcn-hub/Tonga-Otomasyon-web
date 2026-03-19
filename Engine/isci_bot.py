import os
import sys
import mysql.connector
import time
from dotenv import load_dotenv
import main

# .env dosyasını yükle
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# LARAGON VERİTABANI AYARLARIN
DB_AYARLARI = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USERNAME', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_DATABASE', 'automation_web')
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
                cikti = main.tonga_motorunu_calistir(ses_yolu, ozel_baslik=is_kaydi.get('title'))
                
                # main.tonga_motorunu_calistir bir tuple dönüyor olabilir (cikti_video_yolu, donen_baslik)
                if isinstance(cikti, tuple):
                    cikti_video_yolu = cikti[0]
                    donen_baslik = cikti[1]
                else:
                    cikti_video_yolu = cikti
                    donen_baslik = is_kaydi.get('title')

                # Yollardaki \ işaretlerini / ile değiştirelim (Windows Laravel sorunu olmasın)
                cikti_video_yolu = cikti_video_yolu.replace("\\", "/")

                # 2. İş Bitti! Panele Haber Ver: "Videoyu Jilet Gibi Teslim Ettim!"
                cursor.execute("UPDATE videos SET status = 'tamamlandı', video_path = %s, title = %s WHERE id = %s", (cikti_video_yolu, donen_baslik, is_id))
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