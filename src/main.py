import argparse
from pathlib import Path

from .analiz import get_data
from .okuyucu import read_data
from .yazici import write_file


def main():
    parser = argparse.ArgumentParser(description="Telemetri log analizcisi")
    parser.add_argument("--root", required=True, help="CSV dosyasının kök dosyası")
    parser.add_argument("--path", required=True, help="CSV dosyasının yolu")
    parser.add_argument("--max", type=float, default=6.7, help="Hız esigi")
    parser.add_argument("--cikti", default="output", help="Cikti klasoru")
    args = parser.parse_args()

    try:
        data, undefined_data = read_data(root=args.root, path=args.path)
    except FileNotFoundError as e:
        print(e)
        return False
    if args.max < 0 :
        raise ValueError("Esik deger 0 dan kücük olamaz")
    
    output_data = get_data(sensor_values=data, esik_deger=args.max)
    output_data.update({"undefined": undefined_data})
    write_file(data=output_data)
    return True


if __name__ == "__main__":
    main()
