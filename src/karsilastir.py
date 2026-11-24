import argparse
import csv
import tracemalloc
from pathlib import Path


def trace_memory(fonc, path):
    tracemalloc.start()
    data = fonc(path)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return data, peak / 1024 / 1024


def test(path):
    d1, p1 = trace_memory(fonc=load_data, path=path)
    d2, p2 = trace_memory(fonc=load_data_all, path=path)
    print(f"satır satır : sonuç={d1}, tepe bellek={p1:.1f} MB")
    print(f"readLines : sonuç={d2}, tepe bellek={p2:.1f} MB")
    print(f"Fark: yaklaşık {p2 / p1:.0f} kat")

def load_data_all(path):
    try:
        with open(path,encoding="utf-8",mode="r") as csv_file:
            lines = csv_file.readlines()
            return len(lines)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {path}") from e 
def load_data(path):

    try:
        with open(path,encoding="utf-8", mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            sayac = 0
            for row in csv_reader:
                sayac +=1
        return sayac
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {path}") from e

def main():
    parser = argparse.ArgumentParser(description="Telemetri log analizcisi")
    parser.add_argument("--input", required=True, help="CSV dosyasının yolu")
    args = parser.parse_args()

    input = Path(args.input)
    test(input)


if __name__ == "__main__":
    main()