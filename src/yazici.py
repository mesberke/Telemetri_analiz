import json


def write_file(data):
    try:
        with open("output.txt",encoding="utf-8", mode = "at") as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            return True
    except TypeError as e:
        raise TypeError(f"json olarak yazilamadi : {e}")
