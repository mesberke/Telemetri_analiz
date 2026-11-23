import re
from datetime import datetime
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


def load_data(path):
    
    try:
        with open(path, encoding="utf-8") as f:
            if next(f, None) is None:    
                raise ValueError("Dosya boş: başlık satırı yok")
            return f.readlines() 
    except FileNotFoundError as e:
        logger.warning("dosya yolu bulunamadı",e)
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {path}") from e


def read_data(path): # veriyi parcalarına ayırır ve kontrole hazir hale getirir
    
    if not (logs := load_data(path=path)):
        raise ValueError("Dosyada veri yok")
    
    sensor_values: dict[str, list[float]]= {
        "zaman" : [],
        "sicaklik": [],
        "hiz": [],
        "batarya": [],
        }
    invalid_data = 0
    for index,data in enumerate(logs):
        values = []
        split_data = re.split(r",", data.strip())

        for value in split_data:
            values.append(value)  # noqa: PERF402

        if not (x := control_data(values=values,invalid_data=invalid_data,index=index+2))["status"]:# return status or return invalid_data
            invalid_data = x["invalid_data"]
            continue

        append_sensor_values(sensor_values=sensor_values,values=values) # noqa: PERF40

    return sensor_values,(invalid_data) # sensor verileri + atlanan satır sayısı

def append_sensor_values(sensor_values,values): # ayrilan veriyi sensor_values adlı dicte atar
    for key,value in zip(sensor_values.keys(),values):
        sensor_values[key].append(value if key == "zaman" else float(value))  
        
    return sensor_values


def control_data(values,invalid_data,index): # verilerin sayısal olarak dogrulugunu kontrol eder

    if values is None or len(values) != 4:
        logger.warning("Satir : %d  Beklenen 4 gelen: %d",index,len(values))
        invalid_data += 1
        return {"status":False,"invalid_data":invalid_data}
    temp = values[1]
    speed = values[2]
    battery = values[3]
    try:
        date = datetime.strptime(values[0].split()[0], "%Y-%m-%d")
        time = datetime.strptime(values[0].split()[1], "%H:%M:%S")

    except ValueError as error:
        logger.warning("Satir : %d  date veya time hatalı data: %s error  : %s",index,values[0],error)
        invalid_data += 1
        return {"status":False,"invalid_data":invalid_data}
    
    if any(x is None for x in (battery, speed, temp)):
        logger.warning("Satir : %d  batarya,hiz,sicaklıktan herhangi biri boş olamaz batarya : %s , sicaklik : %s , hiz : %s",index,battery,temp,speed)
        invalid_data += 1
        return {"status":False,"invalid_data":invalid_data}
    
    try:
        f_battery = float(battery)
        f_speed = float(speed)
        f_temp = float(temp)
    except ValueError as error:
        logger.warning("Satir : %d  batarya,hiz,sicaklik degerlerinden biri veya birkaci floata donusturulemiyor batarya : %s , sicaklik : %s , hiz : %s",index,battery,temp,speed)
        invalid_data += 1
        return {"status":False,"invalid_data":invalid_data}
    
    if f_battery < 0:
        logger.warning("Satir : %d  Batarya degeri negatif  Batarya : %d",index,f_battery)
        invalid_data += 1
        return {"status":False,"invalid_data":invalid_data}
    
    return {"status":True,"invalid_data":invalid_data}
    
