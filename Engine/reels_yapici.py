import subprocess
import imageio_ffmpeg

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def reels_olustur(girdi_video, cikti_video, baslangic_sn=0, sure_sn=90):
    print(f"\n[REELS/SHORTS] '{girdi_video}' dosyasından 1080p dikey (9:16) kesit alınıyor...")
    
    komut = [
        FFMPEG_EXE, "-y",
        "-i", girdi_video,
        "-ss", str(baslangic_sn),
        "-t", str(sure_sn),
        # trunc(ih*9/16/2)*2 → libx264'ün gerektirdiği çift sayılı piksel boyutu (607.5 sorunu giderildi)
        "-vf", "crop=trunc(ih*9/16/2)*2:ih,scale=1080:1920",
        "-map", "0:v",   # Görüntüyü al
        "-map", "0:a?",  # Sesi al (varsa)
        "-c:v", "libx264",
        "-crf", "18",            # Yüksek görüntü kalitesi
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",          # Yüksek ses kalitesi
        cikti_video
    ]
    
    try:
        sonuc = subprocess.run(
            komut, check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,   # Hata mesajını yakala, gizleme!
            text=True, errors='ignore'
        )
        print(f"[BAŞARILI] Yüksek kalite Reels/Shorts kesildi: {cikti_video}")
    except subprocess.CalledProcessError as e:
        print(f"[HATA] Reels/Shorts kesilemedi!")
        print(f"[FFmpeg Hatası]:\n{e.stderr[-600:] if e.stderr else 'Hata mesajı yok'}")

if __name__ == '__main__':
    print("Bu modül ana sistem tarafından çağrılmalıdır.")