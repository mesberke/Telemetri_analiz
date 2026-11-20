# =============================================================================
# ÖDEV: Telemetri Log Analizcisi  (Dosya İşlemleri + Python Proje Yapısı)
# =============================================================================
# Bir araç sensör verilerini CSV olarak kaydediyor. Bu dosyaları okuyup analiz
# eden, sonuçları JSON ve metin raporu olarak yazan bir komut satırı programı
# yazacaksın. Her görevin altına kendi kodunu yaz.
# =============================================================================


# -----------------------------------------------------------------------------
# 1. PROJE KURULUMU
# -----------------------------------------------------------------------------
# [ ] "telemetri-analiz" adında yeni bir klasör aç ve içinde `git init` yap.
# [ ] `python3 -m venv .venv` ile sanal ortam oluştur ve aktive et.
# [ ] .gitignore dosyasına şunları ekle: .venv/  __pycache__/  output/
# [ ] requirements.txt oluştur (pytest kullanırsan `pip freeze > requirements.txt`).
# [ ] Klasör yapısı şöyle olsun:
#
#     telemetri-analiz/
#     ├── README.md
#     ├── requirements.txt
#     ├── .gitignore
#     ├── data/
#     │   └── ornek_log.csv
#     ├── output/
#     ├── src/
#     │   ├── __init__.py
#     │   ├── okuyucu.py
#     │   ├── analiz.py
#     │   ├── yazici.py
#     │   └── main.py
#     └── tests/
#         └── test_analiz.py


# -----------------------------------------------------------------------------
# 2. ÖRNEK VERİ  (data/ornek_log.csv)
# -----------------------------------------------------------------------------
# [ ] En az 50 satırlık bir CSV oluştur (elle ya da küçük bir script ile).
#     Başlık satırı şöyle olsun:
#         zaman,sicaklik,hiz,batarya
#         2026-11-20 10:00:00,24.5,3.2,98
# [ ] Dosyaya bilerek 2-3 bozuk satır ekle:
#       - boş değer olan satır
#       - sayı yerine harf içeren satır
#       - eksik sütunlu satır


# -----------------------------------------------------------------------------
# 3. MODÜLLER
# -----------------------------------------------------------------------------

# ---- src/okuyucu.py ---------------------------------------------------------
# [ ] log_oku(yol) fonksiyonu yaz:
#       - CSV'yi csv.DictReader ile oku, sözlük listesi döndür.
#       - Dosyayı `with open(..., encoding="utf-8")` ile aç.
#       - Yolları pathlib.Path ile ver ("data/" + ad gibi string birleştirme YOK).
#       - Dosya yoksa FileNotFoundError yakala.
#       - Bozuk satırda ValueError yakala, satırı atla.
#       - Kaç satır atlandığını say ve (veri_listesi, atlanan_sayisi) döndür.

# ---- src/analiz.py ----------------------------------------------------------
# NOT: Bu modül dosyaya hiç dokunmasın; sadece veri alıp veri döndürsün.
# [ ] Her sayısal sütun için min, max ve ortalama hesaplayan bir fonksiyon yaz.
# [ ] Bataryanın %20'nin altına düştüğü ilk zamanı bulan bir fonksiyon yaz.
# [ ] Hızı verilen eşik değerini aşan satırları filtreleyen bir fonksiyon yaz
#     (list comprehension kullan).

# ---- src/yazici.py ----------------------------------------------------------
# [ ] json_yaz(sonuc, yol):
#       json.dump(..., indent=2, ensure_ascii=False) kullan.
# [ ] rapor_yaz(sonuc, yol):
#       Okunabilir bir .txt rapor yaz.
# [ ] output/ klasörü yoksa Path.mkdir(parents=True, exist_ok=True) ile oluştur.

# ---- src/main.py ------------------------------------------------------------
# [ ] argparse ile şu parametreleri al: --girdi, --cikti, --hiz-esik
# [ ] Dosyanın sonuna `if __name__ == "__main__":` bloğu ekle.
# [ ] Şu şekilde çalışmalı:
#         python -m src.main --girdi data/ornek_log.csv --cikti output/


# -----------------------------------------------------------------------------
# 4. EK GÖREVLER
# -----------------------------------------------------------------------------
# [ ] LOGGING: Program, ne yaptığını output/program.log dosyasına logging
#     modülüyle yazsın (hangi dosya okundu, kaç satır atlandı, vb.).
#
# [ ] TEST: tests/test_analiz.py içinde en az 3 test yaz:
#       1) normal veri
#       2) boş liste
#       3) bozuk veri
#     Geçici dosya için pytest'in `tmp_path` fixture'ını kullan.
#
# [ ] BÜYÜK DOSYA: 1 milyon satırlık sahte bir CSV üret.
#     readlines() ile tamamını belleğe alan versiyonla, satır satır okuyan
#     versiyonun bellek kullanımını karşılaştır (tracemalloc kullanabilirsin).
#     Sonucu README'ye 2-3 cümleyle yaz.


# -----------------------------------------------------------------------------
# 5. GIT ŞARTLARI
# -----------------------------------------------------------------------------
# [ ] En az 5 anlamlı commit at. Örnek mesajlar:
#       "proje iskeleti", "csv okuyucu", "analiz fonksiyonları",
#       "json/rapor yazıcı", "testler"
# [ ] `git log --oneline` çıktısını README'ye yapıştır.
# [ ] "feature/logging" adında bir dal aç, logging'i orada yap, sonra main'e merge et.


# -----------------------------------------------------------------------------
# 6. TESLİM  (README.md içeriği)
# -----------------------------------------------------------------------------
# [ ] Projenin ne yaptığı ve nasıl çalıştırıldığı.
# [ ] Venv'i sıfırdan kurma adımları.
# [ ] Dosya işlemlerinde Java/C'ye göre gördüğün 2 fark
#     (örn. `with` bloğu ve otomatik kapanma; fgets/BufferedReader yerine
#     doğrudan satır satır iterasyon).


# -----------------------------------------------------------------------------
# DEĞERLENDİRME  (toplam 100 puan)
# -----------------------------------------------------------------------------
# Proje yapısı, venv, .gitignore ............ 15
# Dosya okuma/yazma (csv, json, txt) ........ 25
# Hata yönetimi ............................. 15
# Modüler yapı ve argparse .................. 15
# Test ve logging ........................... 15
# Git geçmişi ve README ..................... 15

