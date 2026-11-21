import argparse
from pathlib import Path

from .analiz import get_data
from .okuyucu import read_data


def main():
    parser = argparse.ArgumentParser(description="Telemetri log analizcisi")
    parser.add_argument("--root", required=True, help="CSV dosyasının kök dosyası")
    parser.add_argument("--path", required=True, help="CSV dosyasının yolu")
    parser.add_argument("--cikti", default="output", help="Cikti klasoru")
    parser.add_argument("--hiz-esik", type=float, default=5.0, help="Hız esigi")
    args = parser.parse_args()

    try:
        data,undefind = read_data(root=args.girdi,path=args.path)
    except FileNotFoundError as e:
        print(e)
        return False
    return True
if __name__ == "__main__":
    main()
