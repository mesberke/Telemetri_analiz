import re
from datetime import datetime
from pathlib import Path

invalid_data = 0
corrupted_data = 0

def load_data(path):
    global invalid_data,corrupted_data
    invalid_data = 0 
    corrupted_data = 0   # veriyi dosyadan ceker 
    try:
        with open(path, encoding="utf-8") as f:
            return f.readlines() 
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {path}") from e


def split_logs(root,path): # veriyi parcalarına ayırır ve kontrole hazir hale getirir
    
    if root is None or path is None:
        root = Path(__file__).resolve().parent.parent      # projenin kök klasörü
        path = root /"data" / "lo.csv"
    if not (logs := load_data(path=path)):
        return False
    
    sensor_values: dict[str, list[float]]= {
        "zaman" : [],
        "sicaklik": [],
        "hiz": [],
        "batarya": [],
        }

    for data in logs:
        values = []
        split_data = re.split(r",", data.strip())

        for value in split_data:
            values.append(value)  # noqa: PERF402

        if not control_data(values=values):
            continue

        append_sensor_values(sensor_values=sensor_values,values=values, id=id) # noqa: PERF40
    return sensor_values,(invalid_data + corrupted_data) # sensor verileri + atlanan satır sayısı
def append_sensor_values(sensor_values,values, id): # ayrilan veriyi sensor_values adlı dicte atar
    for key,value in zip(sensor_values.keys(),values):
        sensor_values[key].append(value if key == "zaman" else float(value))    
    return True


def control_data(values): # verilerin sayısal olarak dogrulugunu kontrol eder
    global invalid_data,corrupted_data

    if values is None or len(values) != 4:
        corrupted_data += 1
        return False
    temp = values[1]
    speed = values[2]
    battery = values[3]
    try:
        date = datetime.strptime(values[0].split()[0], "%Y-%m-%d")
        time = datetime.strptime(values[0].split()[1], "%H:%M:%S")

    except ValueError as error:
        print(error)
        corrupted_data += 1
        return False
    
    if any(x is None for x in (battery, speed, temp)):
        print("Keys degerlerinden biri veya birkaci None")
        corrupted_data += 1
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
    
    return True
    
def main():
    return split_logs(root=None,path=None)
print(main())
