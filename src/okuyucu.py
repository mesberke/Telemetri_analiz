
from datetime import datetime
import logging
import csv
import math


logger = logging.getLogger(__name__)


def load_data(path):

    try:
        with open(path,encoding="utf-8", mode="r") as csv_file:
            rows = []
            csv_reader = csv.DictReader(csv_file)
            line_count = 0

            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                rows.append(row)
        return rows
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
        if not (
            x := control_data(values=data, invalid_data=invalid_data, index=index + 2)
        )["status"]:  # return status or return invalid_data
            invalid_data = x["invalid_data"]
            continue
        append_sensor_values(sensor_values=sensor_values, values=data)  # noqa: PERF40
    return sensor_values, (invalid_data)  # sensor verileri + atlanan satır sayısı


def append_sensor_values(
    sensor_values, values
):  # ayrilan veriyi sensor_values adlı dicte atar
    for key, value in zip(sensor_values.keys(), values.values()):
        sensor_values[key].append(value if key == "zaman" else float(value))

    return sensor_values


def control_data(
    values, invalid_data, index
):  # verilerin sayısal olarak dogrulugunu kontrol eder

    if (values is None) or (len(values) != 4):
        logger.warning("Satir : %d  Beklenen 4 gelen: %d", index, len(values))
        invalid_data += 1
        return {"status": False, "invalid_data": invalid_data}

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
        invalid_data += 1
        return {"status": False, "invalid_data": invalid_data}

    if any(x is None  for x in (battery, speed, temp)):
        logger.warning(
            "Satir : %d  batarya,hiz,sicaklıktan herhangi biri boş olamaz batarya : %s , sicaklik : %s , hiz : %s",
            index,
            battery,
            temp,
            speed,
        )
        invalid_data += 1
        return {"status": False, "invalid_data": invalid_data}

    try:
        f_battery = float(battery)
        f_speed = float(speed)
        f_temp = float(temp)
    except ValueError as error:
        logger.warning(
            "Satir : %d  batarya,hiz,sicaklik degerlerinden biri veya birkaci floata donusturulemiyor batarya : %s , sicaklik : %s , hiz : %s",
            index,
            battery,
            temp,
            speed,
        )
        invalid_data += 1
        return {"status": False, "invalid_data": invalid_data}

    if any(not math.isfinite(x) for x in (f_battery, f_speed, f_temp)):
        logger.warning("Degerler sadece sayi olmalidir : batarya : %s , sicaklik : %s , hiz : %s",f_battery,f_temp,f_speed)
        invalid_data += 1
        return {"status": False, "invalid_data": invalid_data}
    if f_battery < 0:
        logger.warning(
            "Satir : %d  Batarya degeri negatif  Batarya : %d", index, f_battery
        )
        invalid_data += 1
        return {"status": False, "invalid_data": invalid_data}

    return {"status": True, "invalid_data": invalid_data}
