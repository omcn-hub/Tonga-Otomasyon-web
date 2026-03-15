import os
import random
from PIL import Image, ImageDraw, ImageFilter

# Stok görsellerin saklandığı sabit klasör
STOK_KLASOR = "stok_gorseller"

# Renk paletleri (stok görsel de yoksa kullanılır)
FELSEFI_PALETLER = [
    [(20, 10, 50),  (80,  40, 120)],   # Derin mor
    [(10, 20, 60),  (40,  80, 150)],   # Lacivert
    [(35, 15, 10),  (100, 50,  30)],   # Koyu kırmızı
    [(10, 30, 15),  (30,  90,  50)],   # Koyu yeşil
    [(20, 18, 12),  (70,  60,  35)],   # Antrasit-kehribar
    [(10, 12, 45),  (40,  45, 120)],   # İndigo
    [(25, 15, 5),   (90,  60,  20)],   # Kehribar
    [(12, 12, 40),  (45,  42, 110)],   # Gece mavisi
]


def stok_gorsel_aktar(cikti_yolu):
    """stok_gorseller klasöründen rastgele bir görseli seçip 1920x1080 olarak kaydeder."""
    resimler = []
    if os.path.exists(STOK_KLASOR):
        resimler = [
            os.path.join(STOK_KLASOR, f)
            for f in os.listdir(STOK_KLASOR)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]

    if resimler:
        kaynak = random.choice(resimler)
        img = Image.open(kaynak).convert('RGB').resize((1920, 1080), Image.LANCZOS)
        img.save(cikti_yolu, quality=92)
        print(f"[GÖRSEL] Stok görsel seçildi → {os.path.basename(kaynak)}")
        return cikti_yolu
    return None


def gradient_gorsel_olustur(cikti_yolu, sahne_no=0):
    """Hiç stok görsel yoksa koyu felsefi gradient oluşturur."""
    palette = FELSEFI_PALETLER[sahne_no % len(FELSEFI_PALETLER)]
    (r1, g1, b1), (r2, g2, b2) = palette

    img = Image.new('RGB', (1920, 1080))
    draw = ImageDraw.Draw(img)
    for y in range(1080):
        ratio = y / 1080
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (1920, y)], fill=(r, g, b))

    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    img.save(cikti_yolu, quality=92)
    print(f"[YEDEK] Gradient görsel oluşturuldu (stok_gorseller boş): {cikti_yolu}")
    return cikti_yolu


def gorsel_olustur_ve_indir(prompt, dosya_adi, klasor="arkaplanlar", sahne_no=0):
    """Artık API kullanmıyoruz, sadece stok görsellerden seçiyoruz."""
    if not os.path.exists(klasor):
        os.makedirs(klasor)

    dosya_yolu = os.path.join(klasor, f"{dosya_adi}.jpg")
    print(f"\n[GÖRSEL] Stoktan görsel aranıyor (Sahne {sahne_no+1})...")

    sonuc = stok_gorsel_aktar(dosya_yolu)
    if sonuc:
        return sonuc

    print("[UYARI] stok_gorseller klasörü boş veya resim yok. Yedek plana (gradient) geçiliyor...")
    return gradient_gorsel_olustur(dosya_yolu, sahne_no=sahne_no)


if __name__ == '__main__':
    print("Test: 3 farklı stok görsel kopyalanıyor...")
    for i in range(3):
        gorsel_olustur_ve_indir("", dosya_adi=f"test_{i+1}", sahne_no=i)