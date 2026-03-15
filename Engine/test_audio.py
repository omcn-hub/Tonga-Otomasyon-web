import mysql.connector

db=mysql.connector.connect(host='localhost',user='root',password='',database='automation_web')
c=db.cursor(dictionary=True)
c.execute('SELECT * FROM videos WHERE id=8')
row = c.fetchone()
print(row)
from montaj_yapici import ses_suresi_bul
print("Hesaplanan Süre:", ses_suresi_bul(row['audio_path']))
