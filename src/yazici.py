import json
from pathlib import Path


def write_file(data, path):
    try:
        root = Path(__file__).resolve().parent.parent  # projenin kök klasörü
        path_txt = root / path / "output.txt"
        with open(path_txt, encoding="utf-8", mode="at") as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    except TypeError as e:
        raise IsADirectoryError(f"verilen adres bir dosya yolu : {e}")
    except IsADirectoryError as e:
        raise IsADirectoryError(e)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Dosya bulunamadı : {e}")

    try:
        root = Path(__file__).resolve().parent.parent  # projenin kök klasörü
        path_json = root / path / "output.json"

        with open(path_json, encoding="utf-8", mode="at") as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    except TypeError as e:
        raise TypeError(f"json olarak yazilamadi : {e}")
    except IsADirectoryError as e:
        raise IsADirectoryError(f"verilen adres bir dosya yolu : {e}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Dosya bulunamadı : {e}")
    
    print("Islem basarili oldu dosyaya veri yazildi")
    return True
