import json
from pathlib import Path


def write_file(data, path):
    try:
        txt = report(data=data)
        root = Path(__file__).resolve().parent.parent  # projenin kök klasörü
        path_txt = root / path / "output.txt"
        with open(path_txt, encoding="utf-8", mode="at") as f:
            f.write(txt)
    except IsADirectoryError as e:
        raise IsADirectoryError(f"verilen adres bir dosya yolu : {e}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Dosya bulunamadı : {e}")

    try:
        root = Path(__file__).resolve().parent.parent  # projenin kök klasörü
        path_json = root / path / "output.json"

        with open(path_json, encoding="utf-8", mode="wt") as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    except IsADirectoryError as e:
        raise IsADirectoryError(f"verilen adres bir dosya yolu : {e}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Dosya bulunamadı : {e}")
    print("Islem basarili oldu dosyaya veri yazildi")
    return write_json(data=data,path=path)


def write_json(data, path):
    try:
        root = Path(__file__).resolve().parent.parent  # projenin kök klasörü
        path_json = root / path / "output.json"

        with open(path_json, encoding="utf-8", mode="wt") as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    except IsADirectoryError as e:
        raise IsADirectoryError(f"verilen adres bir dosya yolu : {e}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Dosya bulunamadı : {e}")
    
    print("Islem basarili oldu dosyaya veri yazildi")
    return True


def report(data):
    top = data["top_values"]
    lines = ["TELEMETRİ ANALİZ RAPORU", "=" * 40]

    sections = (
        ("Maksimum değerler", "max_values"),
        ("Minimum değerler", "min_values"),
        ("Ortalama değerler", "mean_values"),
    )
    for head, key in sections:
        lines.append(head)
        for row, value in top[key].items():
            lines.append(f"  {row:<10}: {value}")
        lines.append("-" * 40)

    lines.append(f"Batarya %20 altına ilk düştüğü zaman: {data['low_battery_time']}")
    lines.append(f"Hız eşiğini aşan satır sayısı: {len(data['over_speed_time'])}")
    lines.append(f"Atlanan satır sayısı: {data['undefined']}")

    return "\n".join(lines) + "\n"
