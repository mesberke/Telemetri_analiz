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
    
