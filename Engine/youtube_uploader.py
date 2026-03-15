import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Botun YouTube üzerindeki yetki sınırı (Sadece video yükleme ve yönetme)
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def youtube_baglantisi_kur():
    creds = None
    # token.json dosyası botun seni her seferinde tarayıcıya yönlendirmesini engeller
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Geçerli bir kimlik yoksa kullanıcıdan (senden) izin isteyecek
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Gelecekteki otomatik yüklemeler için şifreyi/tokeni kaydet
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return build('youtube', 'v3', credentials=creds)

def youtube_a_yukle(video_yolu, baslik, aciklama, etiketler):
    print(f"\n[YOUTUBE] '{baslik}' kanala gönderiliyor...")
    try:
        youtube = youtube_baglantisi_kur()

        # Videonun YouTube'daki ayarları
        body = {
            'snippet': {
                'title': baslik,
                'description': aciklama,
                'tags': etiketler,
                'categoryId': '27' # 27 = Eğitim kategorisi (Tonga Felsefe için uygun)
            },
            'status': {
                'privacyStatus': 'private' # İLK TESTİMİZ GİZLİ OLACAK. Sonra 'public' (herkese açık) yapacağız.
            }
        }

        # Videoyu parçalar halinde (chunk) yükleme ayarı
        media = MediaFileUpload(video_yolu, chunksize=1024*1024, resumable=True)
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )

        # Yükleme sürecini ekrana yazdırma
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Yükleniyor... %{int(status.progress() * 100)}")

        print(f"\n[BAŞARILI] Video kanala uçtu! Video ID: {response['id']}")
        print(f"Linki: https://youtu.be/{response['id']}")
        return response['id']
    except Exception as e:
        print(f"\n[HATA] YouTube yükleme işlemi başarısız oldu!")
        print(f"Hata Detayı: {e}")
        # Token süresi dolmuş veya bozulmuş olabilir, bir dahaki sefere yeniden izin istesin diye siliyoruz.
        if os.path.exists('token.json'):
            try:
                os.remove('token.json')
                print("[BİLGİ] Geçersiz token.json silindi. Bir sonraki yüklemede tarayıcıdan Google izni istenecek.")
            except:
                pass
        return None

# SADECE BU DOSYAYI ÇALIŞTIRIRSAK TEST ETMEK İÇİN:
if __name__ == '__main__':
    # ciktilar klasöründe daha önce ürettiğimiz bir videonun tam adını buraya yaz
    # Örneğin: 'ciktilar/test_ses_hazir.mp4' gibi. Sende adı neyse onu gir.
    test_video = "ciktilar/Engin Nurşani - Verin Benim Sevdiğimi_hazir.mp4" 
    
    if os.path.exists(test_video):
        youtube_a_yukle(
            video_yolu=test_video,
            baslik="Tonga Felsefe - Bot Testi #1",
            aciklama="Bu video Python otomasyon botu tarafından arka planda oluşturulup yüklenmiştir.\n\n#felsefe #otomasyon",
            etiketler=["felsefe", "yazılım", "yapay zeka"]
        )
    else:
        print(f"[HATA] Test videosu bulunamadı: {test_video}. Lütfen dosya adını düzelt.")