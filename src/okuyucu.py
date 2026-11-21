import re
from datetime import datetime

invalid_data = 0
corrupted_data = 0

def load_data():   # veriyi dosyadan ceker
    log_lines = []
    with open(
        "/home/desktoptamirin/projects_python/telemetri_analiz/data/log.csv"
    ) as f:
        for line in f:
            log_lines.append(line)  # noqa: PERF402
    f.close()
    return log_lines


def split_logs(): # veriyi parcalarına ayırır ve kontrole hazir hale getirir

    logs = load_data()
    sensor_values: dict[str, list[float]]= {
        "zaman" : [],
        "sicaklik": [],
        "hiz": [],
        "batarya": [],
        }

    for id, data in enumerate(logs):
        values = []
        if id == 0:
            continue
        split_data = re.split(r",", data.strip())

        for value in split_data:
            values.append(value)  # noqa: PERF402

        if not control_data(values=values):
            continue

        append_sensor_values(sensor_values=sensor_values,values=values, id=id) # noqa: PERF40
    return sensor_values,(invalid_data + corrupted_data) # sensor verileri + atlanan satır sayısı
def append_sensor_values(sensor_values,values, id): # ayrilan veriyi sensor_values adlı dicte atar
    global sensor_values, keys  # noqa: PLW0602
    for key,value in zip(keys,values):
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
    return split_logs()