import re
from datetime import datetime

# dosyadan veri okur
sensor_values = {}
keys = []


def load_data():
    log_lines = []
    with open(
        "/home/desktoptamirin/projects_python/telemetri_analiz/data/log.csv"
    ) as f:
        for line in f:
            log_lines.append(line)  # noqa: PERF402
    f.close()
    return log_lines


def split_logs():
    global keys
    logs = load_data()
    for id, data in enumerate(logs):
        if id == 0:
            keys =re.split(r",",data.strip())
            continue
        values = []
        split_data = re.split(r",",data.strip())
        for value in split_data:
            values.append(value)  # noqa: PERF402
        append_sensor_values(values=values, id=id)  # noqa: PERF40
    print(sensor_values)
def append_sensor_values(values, id):
    global sensor_values, keys  # noqa: PLW0602
    try:
        for index,value in enumerate(values):
            sensor_values[id] = {}
            sensor_values[id][keys[index]] = value
    except KeyError as e:
        print(e)
        return False
    return True


def control_data(values):
    if(values is None):
        return False
    try : 
        date = datetime.strptime(values[0].split()[0],"%Y-%m-%d")
        time = datetime.strptime(values[1].split()[1],"%H:M:S")
        print(date.hour())
    except ValueError as error:
        print(error)
        return False
    if date.year() > datetime.now().year() or   date.month > 12   or date.day > 31 or any( x < 0 for x in (date.year,date.month,date.day)):
        return False
    if time.hour < 24 or  time.minute > 60  or time.second > 60 or  any( x < 0 for x in (time.hour ,time.minute,time.second)):
        return False
    
def dict_telemetri():
    pass


split_logs()
