# dosyadan veri okur
def load_data():
    log_lines =[]
    with open("log.csv") as f:
        for line in f:
            log_lines.append(line)  # noqa: PERF402
    f.close()
    return log_lines  
def split_logs():
    pass
def control_data():
    pass
def dict_telemetri():
    pass
