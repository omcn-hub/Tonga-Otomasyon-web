import mysql.connector

# DB Ayarları
DB_AYARLARI = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'automation_web'
}

try:
    db = mysql.connector.connect(**DB_AYARLARI)
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, status, error_log FROM videos WHERE status = 'hata' ORDER BY id DESC LIMIT 1")
    hata_kaydi = cursor.fetchone()
    
    if hata_kaydi:
        print(f"--- HATA DETAYI (ID: {hata_kaydi['id']}) ---")
        print(hata_kaydi['error_log'])
    else:
        print("Hata statüsünde kayıt bulunamadı.")
        
    cursor.close()
    db.close()
except Exception as e:
    print(f"Bağlantı Hatası: {e}")
