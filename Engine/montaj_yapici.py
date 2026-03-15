import os
import json
import subprocess
import imageio_ffmpeg
from mutagen import File

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def ses_suresi_bul(dosya_yolu):
    print("\n[MONTAJ] Dosya süresi deşifre ediliyor...")

    # 1. YÖNTEM: FFprobe JSON — m4a dahil her format için en güvenilir yöntem
    try:
        ffprobe_exe = FFMPEG_EXE.replace('ffmpeg.exe', 'ffprobe.exe').replace('ffmpeg', 'ffprobe')
        sonuc = subprocess.run(
            [ffprobe_exe, '-v', 'quiet', '-print_format', 'json', '-show_format', dosya_yolu],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, errors='ignore'
        )
        data = json.loads(sonuc.stdout)
        sure = float(data['format']['duration'])
        if sure > 0:
            print(f"[MONTAJ] Süre ffprobe ile kesin olarak bulundu: {sure:.1f} saniye")
            return sure
    except: pass

    # 2. YÖNTEM: M4A formatına özel mutagen taraması
    try:
        from mutagen.mp4 import MP4
        ses = MP4(dosya_yolu)
        if ses is not None and getattr(ses.info, 'length', 0) > 0:
            print(f"[MONTAJ] Süre MP4 modülüyle bulundu: {ses.info.length:.1f} saniye")
            return ses.info.length
    except: pass

    # 3. YÖNTEM: Genel ses taraması
    try:
        ses = File(dosya_yolu)
        if ses is not None and getattr(ses.info, 'length', 0) > 0:
            print(f"[MONTAJ] Süre File modülüyle bulundu: {ses.info.length:.1f} saniye")
            return ses.info.length
    except: pass

    # 4. YÖNTEM: FFmpeg stderr parse (yedek)
    try:
        sonuc = subprocess.run(
            [FFMPEG_EXE, '-i', dosya_yolu],
            stderr=subprocess.PIPE, stdout=subprocess.PIPE,
            text=True, errors='ignore'
        )
        for satir in sonuc.stderr.split('\n'):
            if 'Duration:' in satir and 'N/A' not in satir:
                zaman_metni = satir.split('Duration:')[1].split(',')[0].strip()
                saat, dakika, saniye = zaman_metni.split(':')
                toplam = int(saat) * 3600 + int(dakika) * 60 + float(saniye)
                print(f"[MONTAJ] Süre FFmpeg ile söküp alındı: {toplam:.1f} saniye")
                return toplam
    except: pass

    print("[UYARI] Süre hiçbir yöntemle okunamadı! Lütfen ses dosyasını kontrol et.")
    return 300.0

def videoyu_birlestir(ses_yolu, resim_yollari, cikti_yolu, abone_logosu="abone.png", fon_muzigi="fon_muzigi.mp3"):
    print("\n[MONTAJ] Yönetmen koltuğuna geçildi. Görseller ve ses 1080p Ultra HD birleştiriliyor...")
    
    toplam_sure = ses_suresi_bul(ses_yolu)
    
    if toplam_sure <= 0:
        print(f"[HATA] '{ses_yolu}' süresi 0 hesaplandı. İşlem iptal.")
        return None
        
    resim_sayisi = len(resim_yollari)
    if resim_sayisi == 0:
        return None
        
    resim_basina_sure = toplam_sure / resim_sayisi
    
    liste_dosyasi = "yayin_akisi.txt"
    with open(liste_dosyasi, "w", encoding="utf-8") as f:
        for resim in resim_yollari:
            temiz_yol = resim.replace("\\", "/")
            f.write(f"file '{temiz_yol}'\n")
            f.write(f"duration {resim_basina_sure}\n")
            
        son_resim = resim_yollari[-1].replace("\\", "/")
        f.write(f"file '{son_resim}'\n")
        f.write(f"duration {resim_basina_sure}\n")
        # FFmpeg concat requires the last file to be repeated without a duration to ensure the last duration is actually applied
        f.write(f"file '{son_resim}'\n")
    komut = [
        FFMPEG_EXE, "-y",
        "-f", "concat", "-safe", "0", "-i", liste_dosyasi,
        "-i", ses_yolu
    ]

    filtre_komutlari = []
    girdi_index = 2
    ses_ciktisi = "[1:a]"

    # Görseller zaten 1920x1080 — sadece SAR'i standartlaştır
    filtre_komutlari.append("[0:v]setsar=1[v_scaled]")
    goruntu_ciktisi = "[v_scaled]"

    if os.path.exists(abone_logosu):
        komut.extend(["-i", abone_logosu])
        filtre_komutlari.append(f"{goruntu_ciktisi}[{girdi_index}:v]overlay=W-w-30:H-h-30:enable='lt(mod(t\\,45)\\,7)'[logolu]")
        goruntu_ciktisi = "[logolu]"
        girdi_index += 1

    filtre_komutlari.append(f"{goruntu_ciktisi}fps=25,fade=t=out:st={toplam_sure-2}:d=2[nihai_goruntu]")
    goruntu_ciktisi = "[nihai_goruntu]"

    if os.path.exists(fon_muzigi):
        komut.extend(["-stream_loop", "-1", "-i", fon_muzigi])
        filtre_komutlari.append(f"[1:a]volume=1.0[ana_ses];[{girdi_index}:a]volume=0.08[fon_ses];[ana_ses][fon_ses]amix=inputs=2:duration=first:dropout_transition=2[nihai_ses]")
        ses_ciktisi = "[nihai_ses]"
        girdi_index += 1

    tam_filtre = ";".join(filtre_komutlari)
    komut.extend(["-filter_complex", tam_filtre, "-map", goruntu_ciktisi, "-map", ses_ciktisi])
    
    komut.extend([
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "fast",
        "-s", "1920x1080",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        cikti_yolu
    ])
    
    try:
        sonuc = subprocess.run(komut, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if os.path.exists(liste_dosyasi):
            os.remove(liste_dosyasi)
        print(f"[BAŞARILI] Tonga Ai 1080p Sinematik videosu hazırlandı: {cikti_yolu}")
        return cikti_yolu
    except subprocess.CalledProcessError as e:
        print(f"\n[HATA] Montaj çöktü: {e}")
        print(f"[FFMPEG ÇIKTISI]: {e.stderr}")
        return None
    except Exception as e:
        print(f"\n[HATA] Beklenmeyen Montaj Hatası: {e}")
        return None

# --- MANUEL KURTARMA TESTİ (KREDİ HARCAMAMAK İÇİN) ---
if __name__ == '__main__':
    print("\n--- YARIM KALAN PROJEYİ KURTARMA MODU ---")
    ses = "girdiler/Gerceklik_Madde_mi_Yoksa_Bir_Kod_mu.m4a"
    
    # Sadece var olan resimleri sırasıyla al
    resimler = []
    for i in range(1, 16):
        yol = f"arkaplanlar/sahne_{i}.jpg"
        if os.path.exists(yol):
            resimler.append(yol)
    
    if os.path.exists(ses) and len(resimler) > 0:
        videoyu_birlestir(ses, resimler, "ciktilar/kurtarilan_ana_video.mp4")
    else:
        print("[HATA] Ses veya resim dosyaları eksik. İsimleri kontrol et.")