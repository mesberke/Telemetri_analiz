import os
from statistics import mean, median
from .okuyucu import main as m

def calc_top_values(veriler):
    if veriler is None or len(veriler) <= 0 :
        return False
    top_values = {"max_values" : {"zaman" : 0 ,"sicaklik": 0 , "hiz" : 0 ,"batarya" : 0},
                  "min_values" : {"zaman" : 0 ,"sicaklik": 0 , "hiz" : 0 ,"batarya" : 0},
                  "mean_values" : {"sicaklik": 0 , "hiz" : 0 ,"batarya" : 0}}
    for key in veriler.keys():
        
        max_value = max(veriler[key])
        min_value = min(veriler[key])

        top_values["max_values"][key] = max_value
        top_values["min_values"][key] = min_value
        if (key != "zaman"):
            top_values["mean_values"][key] =round(mean(veriler[key]),3)
    print(top_values)
    return max_value

def find_low_battery_time():
    pass    
def get_data():
    sensor_values = m()
    if sensor_values is None :
        print("sensor values fonk bos gelmistir")
        return False
    calc_top_values(veriler=sensor_values)
    return sensor_values
if __name__ == "__main__":
    get_data()
# git commit -m "feat : okuyucu classi yardimiyla veriler cekildi"