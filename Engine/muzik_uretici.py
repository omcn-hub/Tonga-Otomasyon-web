"""
FON MUZİGİ ÜRETİCİ — Tonga Felsefe için Felsefi Ambient Müzik
=============================================================
Bu script numpy kullanarak meditasyon/felsefe videolarına uygun,
derin ve sakin bir ambient dron sesi üretir, ardından ffmpeg ile
MP3'e dönüştürür.

Üretilen ses özellikleri:
  - C minör pentatonik dizi (mistik atmosfer için ideal)
  - Derin bass dron (C2, G2, C3) + harmonikler
  - Yavaş LFO "nefes" efekti (20 sn'de bir tam döngü)
  - Pentatonik notalar her 30 saniyede yavaşça değişir
  - Yumuşak fade-in (3 sn) / fade-out (4 sn)
  - Toplam süre: 6 dakika (döngüde kullanılacak)
"""

import os
import wave
import subprocess
import numpy as np
import imageio_ffmpeg

FFMPEG_EXE  = imageio_ffmpeg.get_ffmpeg_exe()
SAMPLE_RATE = 44100
DURATION    = 360          # 6 dakika
OUTPUT_WAV  = "fon_temp.wav"
OUTPUT_MP3  = "fon_muzigi.mp3"


def ton_olustur(frekans, n_orneklem, amplitude=0.15):
    """Verilen frekans için harmonik zengin sinyal üretir."""
    t = np.linspace(0, n_orneklem / SAMPLE_RATE, n_orneklem, dtype=np.float32)
    sinyal = (
        0.50 * np.sin(2 * np.pi * frekans       * t) +
        0.25 * np.sin(2 * np.pi * frekans * 2.0 * t) +
        0.12 * np.sin(2 * np.pi * frekans * 3.0 * t) +
        0.08 * np.sin(2 * np.pi * frekans * 0.5 * t) +
        0.05 * np.sin(2 * np.pi * frekans * 4.0 * t)
    )
    return sinyal * amplitude


def zarf_uygula(sinyal, attack_sn=2.0, release_sn=2.0):
    """Sinyal başı ve sonuna yumuşak fade uygular."""
    a = min(int(attack_sn  * SAMPLE_RATE), len(sinyal) // 3)
    r = min(int(release_sn * SAMPLE_RATE), len(sinyal) // 3)
    sinyal = sinyal.copy()
    sinyal[:a]  *= np.linspace(0.0, 1.0, a, dtype=np.float32)
    sinyal[-r:] *= np.linspace(1.0, 0.0, r, dtype=np.float32)
    return sinyal


def muzik_olustur():
    N = int(SAMPLE_RATE * DURATION)
    t = np.linspace(0, DURATION, N, dtype=np.float32)

    # ── Katman 1: Derin bass dron (C2=65.41, G2=98.00, C3=130.81) ──────────
    dron = np.zeros(N, dtype=np.float32)
    for frekans in [65.41, 98.00, 130.81]:
        dron += ton_olustur(frekans, N, amplitude=0.13)

    # LFO: 20 sn periyotlu yavaş "nefes" efekti
    lfo  = 0.65 + 0.35 * np.sin(2 * np.pi * (1.0 / 20.0) * t)
    dron = dron * lfo

    # ── Katman 2: Pentatonik melodi (her 30 sn'de biri) ─────────────────────
    # C minör pentatonik: C3, Eb3, F3, G3, Bb3
    NOTALAR = [130.81, 155.56, 174.61, 196.00, 233.08, 261.63, 196.00, 155.56,
               130.81, 174.61, 233.08, 196.00]
    melodi  = np.zeros(N, dtype=np.float32)
    nota_sn = 30  # her nota 30 saniye sürer

    for i, nota_hz in enumerate(NOTALAR):
        bas = int(i * nota_sn * SAMPLE_RATE)
        bit = min(int((i + 1) * nota_sn * SAMPLE_RATE), N)
        if bas >= N:
            break
        n   = bit - bas
        seg = ton_olustur(nota_hz, n, amplitude=0.06)
        seg = zarf_uygula(seg, attack_sn=4.0, release_sn=4.0)
        melodi[bas:bit] += seg

    # ── Karıştır ve normalize et ─────────────────────────────────────────────
    karisim = dron + melodi

    # Yumuşak alçak-geçiren filtre (pencereleme konvolüsyonu)
    pencere_boyutu = int(SAMPLE_RATE * 0.004)   # 4 ms pencere
    kernel  = np.ones(pencere_boyutu, dtype=np.float32) / pencere_boyutu
    karisim = np.convolve(karisim, kernel, mode='same').astype(np.float32)

    # Normalize
    karisim = karisim / (np.max(np.abs(karisim)) + 1e-6) * 0.82

    # Global fade-in / fade-out
    karisim = zarf_uygula(karisim, attack_sn=3.0, release_sn=5.0)

    return karisim


def wav_yaz(sinyal, dosya):
    sinyal_int16 = (sinyal * 32767).astype(np.int16)
    with wave.open(dosya, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(sinyal_int16.tobytes())
    print(f"[FON MÜZİĞİ] WAV oluşturuldu: {dosya}")


def mp3_cevir(wav_dosya, mp3_dosya):
    komut = [
        FFMPEG_EXE, "-y",
        "-i", wav_dosya,
        "-codec:a", "libmp3lame",
        "-b:a", "192k",
        mp3_dosya
    ]
    subprocess.run(komut, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(wav_dosya)
    print(f"[FON MÜZİĞİ] MP3 hazırlandı: {mp3_dosya}")


if __name__ == "__main__":
    print("\n🎵 Felsefi ambient fon müziği üretiliyor...")
    print("   Stil: C minör pentatonik dron | Süre: 6 dakika\n")

    sinyal = muzik_olustur()
    wav_yaz(sinyal, OUTPUT_WAV)
    mp3_cevir(OUTPUT_WAV, OUTPUT_MP3)

    print("\n✅ fon_muzigi.mp3 başarıyla güncellendi!")
    print("   Derin, felsefi ve sakin bir ambient müzik hazır.\n")
