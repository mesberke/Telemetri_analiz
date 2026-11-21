import re
from datetime import datetime

# dosyadan veri okur
sensor_values = {} # sensordan alınan verilerin yazildigi dict
keys = [] # Sensor_valuesin anahtar degerleri
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
    global keys
    logs = load_data()
    for id, data in enumerate(logs):
        if id == 0:
            keys = re.split(r",", data.strip())
            continue
        values = []
        split_data = re.split(r",", data.strip())
        for value in split_data:
            values.append(value)  # noqa: PERF402
        if not control_data(values=values):
            continue
        append_sensor_values(values=values, id=id) # noqa: PERF40
    return sensor_values
def append_sensor_values(values, id): # ayrilan veriyi sensor_values adlı dicte atar
    global sensor_values, keys  # noqa: PLW0602
    try:
        sensor_values[id] = dict(zip(keys, values))
    except KeyError as e:
        sensor_values[id] = {}
        sensor_values[id] = dict(zip(keys, values))
        print(e)
        return
    return True


def control_data(values): # verilerin sayısal olarak dogrulugunu kontrol eder
    global invalid_data,corrupted_data

    if values is None or len(values) != 4:
        corrupted_data += 1
        return False
    time = 0
    date = 0
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
    if (
        date.year > datetime.now().year
        or date.month > 12
        or date.day > 31
        or any(x < 0 for x in (date.year, date.month, date.day))
    ):
        print("Date hatasi")
        corrupted_data += 1
        return False
    
    if (
        time.hour > 24
        or time.minute > 60
        or time.second > 60
        or any(x < 0 for x in (time.hour, time.minute, time.second))
    ):
        print("time hatasi")
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
    

