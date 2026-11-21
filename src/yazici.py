import json
from pathlib import Path


def write_file(data, path):
    try:
        txt = rapor(data=data)
        root = Path(__file__).resolve().parent.parent  # projenin kök klasörü
        path_txt = root / path / "output.txt"
        with open(path_txt, encoding="utf-8", mode="at") as f:
            f.write(txt)
    except TypeError as e:
        raise IsADirectoryError(f"verilen adres bir dosya yolu : {e}")
    except IsADirectoryError as e:
        raise IsADirectoryError(e)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Dosya bulunamadı : {e}")

    try:
        root = Path(__file__).resolve().parent.parent  # projenin kök klasörü
        path_json = root / path / "output.json"

        with open(path_json, encoding="utf-8", mode="wt") as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    except TypeError as e:
        raise TypeError(f"json olarak yazilamadi : {e}")
    except IsADirectoryError as e:
        raise IsADirectoryError(f"verilen adres bir dosya yolu : {e}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Dosya bulunamadı : {e}")
    print("Islem basarili oldu dosyaya veri yazildi")
    return True


def rapor(data):
    top = data["top_values"]
    satirlar = ["TELEMETRİ ANALİZ RAPORU", "=" * 40]

    bolumler = (
        ("Maksimum değerler", "max_values"),
        ("Minimum değerler", "min_values"),
        ("Ortalama değerler", "mean_values"),
    )
    for baslik, anahtar in bolumler:
        satirlar.append(baslik)
        for sutun, deger in top[anahtar].items():
            satirlar.append(f"  {sutun:<10}: {deger}")
        satirlar.append("-" * 40)

    satirlar.append(f"Batarya %20 altına ilk düştüğü zaman: {data['low_battery_time']}")
    satirlar.append(f"Hız eşiğini aşan satır sayısı: {len(data['over_speed_time'])}")
    satirlar.append(f"Atlanan satır sayısı: {data['undefined']}")

    return "\n".join(satirlar) + "\n"


# git commit -m "feat: rapor şablonnu eklendi ve yazdırıldı" -m "json ekleme modundan yazma oduna alındı"
