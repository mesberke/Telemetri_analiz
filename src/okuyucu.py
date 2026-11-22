import re
from datetime import datetime
from pathlib import Path


def load_data(path):
   
    try:
        with open(path, encoding="utf-8") as f:
            next(f)
            return f.readlines() 
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {path}") from e


def read_data(root,path): # veriyi parcalarına ayırır ve kontrole hazir hale getirir
    
    if root is None or path is None:
        root = Path(__file__).resolve().parent.parent      # projenin kök klasörü
        path = root /"data" / "log.csv"
    if not (logs := load_data(path=path)):
        raise ValueError("Dosyada veri yok")
    
    sensor_values: dict[str, list[float]]= {
        "zaman" : [],
        "sicaklik": [],
        "hiz": [],
        "batarya": [],
        }
    
    invalid_data = 0
    for data in logs:
        values = []
        split_data = re.split(r",", data.strip())

        for value in split_data:
            values.append(value)  # noqa: PERF402

        if not (invalid_data := control_data(values=values),invalid_data):# return status or return invalid_data
            continue

        append_sensor_values(sensor_values=sensor_values,values=values, id=id) # noqa: PERF40
    return sensor_values,(invalid_data) # sensor verileri + atlanan satır sayısı

def append_sensor_values(sensor_values,values, id): # ayrilan veriyi sensor_values adlı dicte atar
    for key,value in zip(sensor_values.keys(),values):
        sensor_values[key].append(value if key == "zaman" else float(value))    
    return True


def control_data(values,invalid_data): # verilerin sayısal olarak dogrulugunu kontrol eder

    if values is None or len(values) != 4:
        invalid_data += 1
        return False
    temp = values[1]
    speed = values[2]
    battery = values[3]
    try:
        date = datetime.strptime(values[0].split()[0], "%Y-%m-%d")
        time = datetime.strptime(values[0].split()[1], "%H:%M:%S")

    except ValueError as error:
        print(error)
        invalid_data += 1
        return False
    
    if any(x is None for x in (battery, speed, temp)):
        print("Keys degerlerinden biri veya birkaci None")
        invalid_data += 1
        return False
    
    try:
        f_battery = float(battery)
        f_speed = float(speed)
        f_temp = float(temp)
    except ValueError as error:
        print(error)
        print("speeed or temp or battery degerlerinden biri veya birkacı hatali")
        invalid_data += 1
        return False
    
    if f_battery < 0:
        print(f"Batarya degeri hatalidir Batarya : {battery}")
        invalid_data += 1
        return False
    
    return invalid_data
    


