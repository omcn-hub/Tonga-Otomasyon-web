import sys
import mysql.connector
import os
import json
import traceback

# Laravel'in Engine klasörü içindeyiz, main.py ile aynı dizin
import main

# LARAGON VERİTABANI AYARLARI
DB_AYARLARI = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'automation_web' # isci_bot.py'deki veritabanı adı
}

class DBLogger:
    def __init__(self, db_conn, video_id):
        self.db = db_conn
        self.video_id = video_id
        self.cursor = self.db.cursor()
        self.logs = []
        
        # Orijinal stdout'u sakla
        self.original_stdout = sys.stdout

    def write(self, message):
        # Konsola da yaz (eğer terminalden çalıştırılırsa görmek için)
        try:
            self.original_stdout.write(message)
        except UnicodeEncodeError:
            # Windows terminali (cp1254 vb.) emojileri (🚀, vb.) basamazsa hatayı yut
            pass
        
        # Boş satırları loglama
        msg = message.strip()
        if not msg:
            return
            
        # Log array'ine ekle (son 20 logu tutalım, DB şişmesin)
        self.logs.append(msg)
        if len(self.logs) > 20:
            self.logs.pop(0)
            
        # Veritabanına JSON formatında veya alt alta yaz
        log_text = "\n".join(self.logs)
        
        try:
            self.cursor.execute("UPDATE videos SET error_log = %s WHERE id = %s", (log_text, self.video_id))
            self.db.commit()
        except Exception as e:
            self.original_stdout.write(f"\n[Veritabanı Log Hatası]: {e}\n")

    def flush(self):
        self.original_stdout.flush()

def calistir(video_id):
    try:
        db = mysql.connector.connect(**DB_AYARLARI)
        cursor = db.cursor(dictionary=True)

        # Video kaydını al
        cursor.execute("SELECT * FROM videos WHERE id = %s", (video_id,))
        is_kaydi = cursor.fetchone()

        if not is_kaydi:
            print(f"Hata: Veritabanında ID {video_id} bulunamadı.")
            return

        # Durumu işleniyor yap
        cursor.execute("UPDATE videos SET status = 'isleniyor', error_log = 'Araçlar hazırlanıyor...' WHERE id = %s", (video_id,))
        db.commit()

        # DOSYA YOLU
        ses_yolu = is_kaydi['audio_path'].replace("\\", "/")
        ozel_baslik = is_kaydi.get('title')

        # SYSOUT'u kendi logger'ımıza yönlendir (print'leri yakalamak için)
        db_logger = DBLogger(db, video_id)
        sys.stdout = db_logger

        try:
            # === YAPAY ZEKA MOTORU BAŞLATILIYOR ===
            cikti_video_yolu, donen_baslik = main.tonga_motorunu_calistir(ses_yolu, ozel_baslik=ozel_baslik)
            cikti_video_yolu = cikti_video_yolu.replace("\\", "/")

            # İş bitti, durumu güncelle
            # Stdout'u geri al ki sql update sırasında gereksiz log yazılmasın
            sys.stdout = db_logger.original_stdout
            cursor.execute("UPDATE videos SET status = 'tamamlandı', video_path = %s, title = %s, error_log = 'Tamamlandı.' WHERE id = %s", (cikti_video_yolu, donen_baslik, video_id))
            db.commit()

        except Exception as e:
            sys.stdout = db_logger.original_stdout
            
            # Eski logları al ve hatayı altına ekle ki panelde neyden sonra çöktüğü anlaşılsın
            mevcut_log = "\n".join(db_logger.logs)
            hata_mesaji = f"{mevcut_log}\n\n[KRİTİK HATA]: {str(e)}\n\nTeknik Detay:\n{traceback.format_exc()}"
            
            # DB boyutunu şişirmemek için son 1000 karakteri alabiliriz
            if len(hata_mesaji) > 2000:
                hata_mesaji = "..." + hata_mesaji[-1997:]
                
            cursor.execute("UPDATE videos SET status = 'hata', error_log = %s WHERE id = %s", (hata_mesaji, video_id))
            db.commit()

        finally:
            cursor.close()
            db.close()

    except Exception as general_e:
        print(f"Kritik Hata: Python veritabanına bağlanamadı veya başlatılamadı.\n{general_e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python run_task.py <video_id>")
        sys.exit(1)
        
    v_id = sys.argv[1]
    calistir(v_id)
