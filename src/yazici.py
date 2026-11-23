import json
from pathlib import Path


def write_file(data, path: Path):

    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        txt = report(data=data)
        with open(path, encoding="utf-8", mode="w") as f:
            f.write(txt)
        print("Islem basarili oldu dosyaya veri yazildi")
    except IsADirectoryError as e:
        raise IsADirectoryError(f"verilen adres bir dosya yolu : {e}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Dosya bulunamadı : {e}")


def write_json(data, path : Path):

    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, encoding="utf-8", mode="w") as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
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
