import argparse
from builtins import float
from pathlib import Path

from .analiz import get_data
from .okuyucu import read_data
from .yazici import write_file
from .yazici import write_json


def main():
    parser = argparse.ArgumentParser(description="Telemetri log analizcisi")
    parser.add_argument("--input", required=True, help="CSV dosyasının yolu")
    parser.add_argument("--max", type=float, default=6.7, help="Hız esigi")
    parser.add_argument("--output", required=True, help="Cikti klasoru")
    args = parser.parse_args()

    input = Path(args.input)
    output = Path(args.output)

    try:
        data, undefined_data = read_data(path=input)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        return False

    if args.max < 0:
        print("esik deger 0 dan kucuk olamaz")
        return False

    output_data = get_data(sensor_values=data, esik_deger=args.max)
    output_data.update({"undefined": undefined_data})
    write_file(data=output_data, path=output / "output.txt")
    write_json(data=data, path=output / "output.json")

    return True


if __name__ == "__main__":
    main()
