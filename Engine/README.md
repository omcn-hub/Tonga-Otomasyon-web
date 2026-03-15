# 🤖 Tonga AI - Tam Otomatik Felsefe & Podcast Medya Otomasyonu

Tonga AI, baştan uca çalışan tam otomatik bir yapay zeka medya şirketidir. Sisteme sadece bir ses dosyası (MP3/M4A) verilir; geriye kalan dinleme, anlama, hayal etme, görselleştirme, sinematik montaj ve sosyal medya dağıtımı tamamen otonom olarak gerçekleşir.

## 🚀 Özellikler ve Akış (Pipeline)
1. **İşitsel Analiz (Gemini 2.5 Flash):** Verilen ses dosyasını dinler, felsefi derinliğini analiz eder ve SEO uyumlu başlık, açıklama ve 15 adet İngilizce görsel prompt'u (JSON formatında) üretir.
2. **Görsel Üretim (Hugging Face SDXL):** Gemini'nin ürettiği promptları kullanarak 1080p çözünürlüğünde 15 adet sinematik, felsefi ve karanlık temalı görsel çizer.
3. **Sinematik Montaj Motoru (FFmpeg):** Görselleri ve sesi birleştirir.
   - **Ken Burns & Fade:** Sahnelere sinematik kararma/aydınlanma (Fade in/out) uygular.
   - **Audio Ducking:** Telifsiz mistik bir fon müziğini, ana sesin altına %8 seviyesinde dinamik olarak miksler.
   - **Logo Entegrasyonu:** Belirli saniye aralıklarıyla ekranda "Abone Ol" filigranı gösterir.
4. **Çoklu Çıktı Üretimi:** 1920x1080 (Yatay Ana Video) ve 1080x1920 (Reels/Shorts için dikey kesit) formatlarında kayıpsız (CRF 18) render alır.
5. **Sosyal Medya Kuryeleri:** - Yatay videoyu YouTube'a ana video olarak yükler.
   - Dikey videoyu Instagram'a Reels olarak ateşler.
   - Aynı dikey videoyu YouTube'a `#shorts` etiketiyle yükler.

## 🛠️ Kullanılan Teknolojiler
* **Python 3.x** (Core Backend)
* **Google Gemini API** (NLP & Planlama)
* **Hugging Face Inference API** (Text-to-Image)
* **FFmpeg & imageio_ffmpeg** (Video Render & Audio Mixing)
* **Watchdog** (Klasör Dinleme Otomasyonu)
* **Instagrapi & Google API Client** (Sosyal Medya Otomasyonu)

## 💻 Nasıl Çalıştırılır?
1. Repoyu klonlayın ve kütüphaneleri kurun.
2. `main.py`, `beyin.py` ve `gorsel_uretici.py` içindeki API Key ve hesap bilgilerinizi girin.
3. Ana dizine `abone.png` ve `fon_muzigi.mp3` dosyalarınızı ekleyin.
4. Terminalde `python main.py` komutunu çalıştırın.
5. `girdiler/` klasörüne herhangi bir `.m4a` veya `.mp3` atın ve arkanıza yaslanın!