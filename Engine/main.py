import os
import time
import shutil

# YAZDIĞIMIZ TÜM SÜPER GÜÇLERİ (MODÜLLERİ) İÇERİ AKTARIYORUZ
from beyin import sesi_analiz_et
from gorsel_uretici import gorsel_olustur_ve_indir
from montaj_yapici import videoyu_birlestir
from youtube_uploader import youtube_a_yukle
from reels_yapici import reels_olustur
from instagram_uploader import instagrama_yukle

# KLASÖR YOLLARI VE HESAP BİLGİLERİ (Girdi klasörünü sildik, Laravel veriyor!)
CIKTI_KLASORU = "ciktilar"
ARKAPLAN_KLASORU = "arkaplanlar"

IG_USERNAME = "tongafelsefesi@gmail.com"
IG_PASSWORD = "Tongafelsefesi123456"

def temizlik_yap():
    if os.path.exists(ARKAPLAN_KLASORU):
        shutil.rmtree(ARKAPLAN_KLASORU)
    os.makedirs(ARKAPLAN_KLASORU)

    if not os.path.exists(CIKTI_KLASORU):
        os.makedirs(CIKTI_KLASORU)

    if not os.path.exists("stok_gorseller"):
        os.makedirs("stok_gorseller")

# PANEL'DEN GELEN BAŞLIĞI DA ALABİLMESİ İÇİN PARAMETRE EKLEDİK
def tonga_motorunu_calistir(ses_yolu, ozel_baslik=None):
    dosya_adi = os.path.splitext(os.path.basename(ses_yolu))[0]
    
    print(f"\n{'='*70}")
    print(f"🚀 [YAPAY ZEKA MOTORU ATEŞLENDİ] Dosya: {os.path.basename(ses_yolu)}")
    print(f"{'='*70}")
    
    temizlik_yap()
    
    # --- ADIM 1: BEYİN ---
    print("\n▶️ ADIM 1: Gemini 2.5 podcasti dinliyor ve plan yapıyor...")
    plan = sesi_analiz_et(ses_yolu)
    
    if not plan:
        raise Exception("Beyin modülü planı çıkaramadı!") # Return yerine hata fırlatıyoruz ki İşçi Bot bunu panelde göstersin
        
    resim_komutlari = plan.get('resim_komutlari', [])
    
    # Admin panelinden başlık girilmişse onu kullan, girilmemişse yapay zekanınkini kullan
    if ozel_baslik and str(ozel_baslik).strip() != "":
        youtube_baslik = ozel_baslik
    else:
        youtube_baslik = plan.get('youtube_baslik', f"Tonga Ai - {dosya_adi}")
        
    youtube_aciklama = plan.get('youtube_aciklama', "Felsefe üzerine derin düşünceler...")
    reels_aciklama = plan.get('reels_aciklama', "Yeni bölüm yayında! #felsefe")

    # --- ADIM 2: GÖZ ---
    print(f"\n▶️ ADIM 2: {len(resim_komutlari)} adet sahne yapay zekaya çizdiriliyor...")
    indirilen_resimler = []
    
    for i, komut in enumerate(resim_komutlari):
        resim_yolu = gorsel_olustur_ve_indir(komut, f"sahne_{i+1}", ARKAPLAN_KLASORU, sahne_no=i)
        if resim_yolu:
            indirilen_resimler.append(resim_yolu)
        time.sleep(3) 
        
    if len(indirilen_resimler) == 0:
        raise Exception("Hiç resim çizilemedi, montaj yapılamaz.")

    # --- ADIM 3: MONTAJ ---
    print("\n▶️ ADIM 3: Yönetmen koltuğuna geçildi, video kurgulanıyor...")
    yatay_video_yolu = os.path.join(CIKTI_KLASORU, f"{dosya_adi}_ana_video.mp4")
    
    montajli_video = videoyu_birlestir(ses_yolu, indirilen_resimler, yatay_video_yolu)
    
    if not montajli_video:
        raise Exception("Montaj motoru çöktü, video oluşturulamadı.")

    # --- ADIM 4: YOUTUBE YÜKLEMESİ ---
    print("\n▶️ ADIM 4: YouTube Kuryesi çağrıldı, yatay video yükleniyor...")
    try:
        youtube_a_yukle(yatay_video_yolu, youtube_baslik, youtube_aciklama, ["yapayzeka", "felsefe"])
    except Exception as e:
        print(f"⚠️ YouTube yükleme hatası (Ana süreç devam ediyor): {e}")

    # --- ADIM 5 & 6: REELS VE INSTAGRAM ---
    print("\n▶️ ADIM 5: Instagram için videonun ilk 90 saniyesi kesiliyor...")
    dikey_video_yolu = os.path.join(CIKTI_KLASORU, f"{dosya_adi}_reels.mp4")
    try:
        reels_olustur(yatay_video_yolu, dikey_video_yolu, baslangic_sn=0, sure_sn=90)
        if os.path.exists(dikey_video_yolu):
            print("▶️ ADIM 6: Instagram hesabına giriş yapılıp Reels ateşleniyor...")
            instagrama_yukle(dikey_video_yolu, reels_aciklama, IG_USERNAME, IG_PASSWORD)
    except Exception as e:
        print(f"⚠️ Instagram/Reels hatası: {e}")

    # --- ADIM 7: YOUTUBE SHORTS ---
    shorts_video_yolu = os.path.join(CIKTI_KLASORU, f"{dosya_adi}_shorts.mp4")
    try:
        print("\n▶️ ADIM 7: YouTube Shorts için kesim yapılıp yükleniyor...")
        reels_olustur(yatay_video_yolu, shorts_video_yolu, baslangic_sn=0, sure_sn=60)
        if os.path.exists(shorts_video_yolu):
            shorts_baslik = youtube_baslik[:55] + " #shorts"
            youtube_a_yukle(shorts_video_yolu, shorts_baslik, reels_aciklama, ["shorts", "felsefe"])
    except Exception as e:
        print(f"⚠️ YouTube Shorts hatası: {e}")

    print(f"\n{'='*70}")
    print(f"🎉 YAPAY ZEKA MOTORU GÖREVİNİ KUSURSUZ BİTİRDİ!")
    print(f"{'='*70}\n")
    
    # EN KRİTİK YER: Web sitesine (işçi bota) çıkan MP4 dosyasının tam yerini veriyoruz
    return os.path.abspath(yatay_video_yolu)