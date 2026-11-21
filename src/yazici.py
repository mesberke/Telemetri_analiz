import json


def write_file(data):
    try:
        with open("output.txt", "at") as f:
            f.write("-" * 40 + "\n")
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
            return True
    except ValueError as e:
        raise ValueError(f"json olarak yazilamadi : {e}")
