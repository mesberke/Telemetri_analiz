import json
from pathlib import Path


def write_file(data,path):
    try:
        root = Path(__file__).resolve().parent.parent      # projenin kök klasörü
        path = root / path
        with open(path,encoding="utf-8", mode = "at") as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            return True
    except TypeError as e:
        raise TypeError(f"json olarak yazilamadi : {e}")
    
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