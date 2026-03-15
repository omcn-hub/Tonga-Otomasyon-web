import os

# FFmpeg "concat" demuxer behavior check
# Let's inspect yayin_akisi.txt if it exists to see if the durations are written correctly
if os.path.exists("yayin_akisi.txt"):
    with open("yayin_akisi.txt", "r", encoding="utf-8") as f:
        print("--- yayin_akisi.txt icerigi ---")
        print(f.read())
else:
    print("yayin_akisi.txt bulunamadi.")
