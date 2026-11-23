import argparse
import logging
import tracemalloc
from pathlib import Path

from .analiz import get_data
from .okuyucu import read_data ,load_data_all , load_data
from .yazici import write_file, write_json

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Telemetri log analizcisi")
    parser.add_argument("--input", required=True, help="CSV dosyasının yolu")
    parser.add_argument("--max", type=float, default=6.7, help="Hız esigi")
    parser.add_argument("--output", required=True, help="Cikti klasoru")
    args = parser.parse_args()

    input = Path(args.input)
    output = Path(args.output)

    path = output / "program.log"
    path.parent.mkdir(parents=True,exist_ok=True)

    if test(path=input):
        return

    logging.basicConfig(
        filename=output / "program.log",
        level=logging.INFO,
        filemode="w",
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        encoding="utf-8",
    )
    logger.info("Hız eşiği: %s", args.max)

    try:
        logger.info("Okunan dosya: %s", input)
        data, undefined_data = read_data(path=input)
        
    except (FileNotFoundError, ValueError) as e:
        logger.error("Dosya acilirken hata ile karsilasildi  Hata :  %s",e)
        return False

    if args.max < 0:
        print("esik deger 0 dan kucuk olamaz")
        logger.error("Esik deger 0 dan kucuk girildi. Esik Deger : %s",args.max)
        return False
    

    output_data = get_data(sensor_values=data, esik_deger=args.max)
    output_data.update({"undefined": undefined_data})
    logger.info("Okunan satır: %d, atlanan satır: %d", len(data["zaman"]), undefined_data)

    write_file(data=output_data, path=output / "output.txt")
    write_json(data=output_data, path=output / "output.json")
    logger.info("Çıktı yazıldı: %s", output)

    return True

def trace_memory(fonc,path):
    tracemalloc.start()
    data = fonc(path)
    _,peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return data,peak / 1024 / 1024

def test(path):
    d1,p1 = trace_memory(fonc=load_data,path=path)
    d2,p2 = trace_memory(fonc=load_data_all,path=path)
    print(f"satır satır : sonuç={d1}, tepe bellek={p1:.1f} MB")
    print(f"readLines : sonuç={d2}, tepe bellek={p2:.1f} MB")
    print(f"Fark: yaklaşık {p2 / p1:.0f} kat")
    return False

if __name__ == "__main__":
    main()
