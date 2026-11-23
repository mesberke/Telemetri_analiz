
import csv
import logging
import math
from datetime import datetime

logger = logging.getLogger(__name__)

def load_data_all(path):
    try:
        with open(path,encoding="utf-8",mode="r") as csv_file:
            lines = csv_file.readlines()
            return len(lines)
    except FileNotFoundError as e:
        logger.error("Dosya yolu bulunamadı Hata :  %s", e)
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {path}") from e 

def load_data(path):

    try:
        with open(path,encoding="utf-8", mode="r") as csv_file:
            rows = []
            csv_reader = csv.DictReader(csv_file)
            sayac = 0
            for row in csv_reader:
                sayac +=1
        return sayac
    except FileNotFoundError as e:
        logger.error("Dosya yolu bulunamadı Hata :  %s", e)
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {path}") from e


def read_data(path):  # veriyi parcalarına ayırır ve kontrole hazir hale getirir

    if not (logs := load_data(path=path)):
        raise ValueError("Dosyada veri yok")
    sensor_values: dict[str, list[float]] = {
        "zaman": [],
        "sicaklik": [],
        "hiz": [],
        "batarya": [],
    }

    invalid_data = 0
    for index, data in enumerate(logs):

        if not (x := control_data(values=data, index=index + 2)):  # return status or return invalid_data
            invalid_data +=1
            continue

        append_sensor_values(sensor_values=sensor_values, values=data)  # noqa: PERF40
    return sensor_values, (invalid_data)  # sensor verileri + atlanan satır sayısı


def append_sensor_values(sensor_values, values):  # ayrilan veriyi sensor_values adlı dicte atar
    for key, value in zip(sensor_values.keys(), values.values()):
        sensor_values[key].append(value if key == "zaman" else float(value))

    return sensor_values

def control_data(values, index):  # verilerin sayısal olarak dogrulugunu kontrol eder

    if (values is None) or (len(values) != 4):
        logger.warning("Satir : %d  Beklenen 4 gelen: %d", index, len(values))
        return False

    temp = values["sicaklik"]
    speed = values["hiz"]
    battery = values["batarya"]
    try:
        date = datetime.strptime(values["zaman"].split()[0], "%Y-%m-%d")
        time = datetime.strptime(values["zaman"].split()[1], "%H:%M:%S")

    except (ValueError,IndexError) as error:
        logger.warning(
            "Satir : %d  date veya time hatalı ya da bos data: %s error  : %s",
            index,
            values["zaman"],
            error,
        )
        return False

    if any(x is None  for x in (battery, speed, temp)):
        logger.warning(
            "Satir : %d  batarya,hiz,sicaklıktan herhangi biri boş olamaz " \
            "batarya : %s , sicaklik : %s , hiz : %s",
            index,
            battery,
            temp,
            speed,
        )
        return False

    try:
        f_battery = float(battery)
        f_speed = float(speed)
        f_temp = float(temp)
    except ValueError as error:
        logger.warning(
            "Satir : %d  batarya,hiz,sicaklik degerlerinden biri veya birkaci floata donusturulemiyor " \
            "batarya : %s , sicaklik : %s , hiz : %s",
            index,
            battery,
            temp,
            speed,
        )
        return False

    if any(not math.isfinite(x) for x in (f_battery, f_speed, f_temp)):
        logger.warning("Degerler sadece sayi olmalidir :" \
        " batarya : %s , sicaklik : %s , hiz : %s",f_battery,f_temp,f_speed)
        return False
    
    if f_battery < 0:
        logger.warning(
            "Satir : %d  Batarya degeri negatif  Batarya : %d", index, f_battery
        )
        return False
    return True
