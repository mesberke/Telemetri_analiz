
from pathlib import Path


def control(path : Path):
    if path.exists():
        print(f"Boyle bir yol bulunmaktadır {path}")
        return False
    if path.is_file():
        print(f"Bu bir dosya yolu {path}")
        return False
    return True
    