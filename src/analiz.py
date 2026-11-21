from statistics import mean

from .okuyucu import main as m


def calc_top_values(veriler):
    if veriler is None or len(veriler) <= 0:
        return False
    top_values = {
        "max_values": {"zaman": 0, "sicaklik": 0, "hiz": 0, "batarya": 0},
        "min_values": {"zaman": 0, "sicaklik": 0, "hiz": 0, "batarya": 0},
        "mean_values": {"sicaklik": 0, "hiz": 0, "batarya": 0},
    }
    for key in veriler.keys():  # noqa: SIM118
        max_value = max(veriler[key])
        min_value = min(veriler[key])

        top_values["max_values"][key] = max_value
        top_values["min_values"][key] = min_value
        if key != "zaman":
            top_values["mean_values"][key] = round(mean(veriler[key]), 3)
    return top_values


def find_low_battery_time(veriler):
    zaman = next(
        (x for x, y in zip(veriler["zaman"], veriler["batarya"]) if y < 20), None
    )
    return zaman


def find_over_speed(veriler, esik_deger):
    zaman = []
    zaman.append(  
            time
            for time, speed in zip(veriler["zaman"], veriler["hiz"])
            if speed > esik_deger 
    )
    return zaman


def get_data(esik_deger,sensor_values):
    
    top_values = calc_top_values(veriler=sensor_values)
    over_speed_times = find_over_speed(veriler=sensor_values, esik_deger=esik_deger)
    low_battery_time = find_low_battery_time(sensor_values)

    return {
        "top_values": top_values,
        "over_speed_time": over_speed_times,
        "low_battery_time": low_battery_time,
    }

