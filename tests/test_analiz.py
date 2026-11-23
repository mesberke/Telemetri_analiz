import pytest  # noqa: F401, I001
from src.analiz import calc_top_values, find_low_battery_time, find_over_speed # type: ignore
from src.okuyucu import read_data  # type: ignore

VERI = {
    "zaman": [
        "2026-11-22 10:00:00", "2026-11-22 10:00:30", "2026-11-22 10:01:00",
        "2026-11-22 10:01:30", "2026-11-22 10:02:00", "2026-11-22 10:02:30",
        "2026-11-22 10:03:00", "2026-11-22 10:03:30", "2026-11-22 10:04:00",
        "2026-11-22 10:04:30",
    ],
    "sicaklik": [24.5, 24.8, 25.1, 25.6, 26.0, 26.3, 26.9, 27.2, 27.5, 27.1],
    "hiz": [3.2, 4.1, 5.0, 6.9, 7.4, 5.8, 4.4, 3.9, 2.5, 1.2],
    "batarya": [98, 90, 80, 70, 55, 40, 30, 21, 18, 15],
}

def test_normal_data():
    
    top_values = calc_top_values(VERI)
    assert top_values["max_values"]["hiz"] == 7.4
    assert top_values["max_values"]["batarya"] == 98
    assert top_values["max_values"]["sicaklik"] == 27.5
    assert top_values["min_values"]["hiz"] == 1.2
    assert top_values["min_values"]["batarya"] == 15
    assert top_values["min_values"]["sicaklik"] == 24.5
    assert find_low_battery_time(VERI) == "2026-11-22 10:04:00"
    assert find_over_speed(VERI,6.7) == [ "2026-11-22 10:01:30", "2026-11-22 10:02:00"]

def test_corrupted_data(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text(
        "zaman,sicaklik,hiz,batarya\n"
        "2026-11-22 10:00:00,24.5,3.2,98\n"      # geçerli
        "2026-11-22 10:00:30,25.1,4.0,97\n"      # geçerli
        "2026-11-22 10:01:00,25.4,,96\n"         # boş hız
        "2026-11-22 10:01:30,abc,5.0,95\n"       # sayı yerine harf
        "2026-11-22 10:02:00,26.0,3.3\n"         # eksik sütun
        "2026-11-22 10:02:30,26.2,3.5,94,7\n"    # fazla sütun
        "2026-11-22 10:03:00,26.4,3.1,-5\n"      # negatif batarya
        "bozuk-tarih,26.5,3.0,93\n"              # geçersiz tarih
        "2026-13-45 10:04:00,26.5,3.0,93\n"      # imkansız tarih
        "\n"                                     # boş satır
        "2026-11-22 10:05:30,27.0,3.4,92\n",     # geçerli
        encoding="utf-8",
    )
    data,undefined = read_data(file)
    assert undefined == 8
    assert len(data["zaman"]) == 3
    assert data["zaman"] == [
        "2026-11-22 10:00:00",
        "2026-11-22 10:00:30",
        "2026-11-22 10:05:30",
    ]
    assert data["batarya"] == [98, 97, 92]
    
def test_empty_data(tmp_path):
    empty_data = {"zaman" : [],"sicaklik":[],"hiz":[],"batarya":[]}
    top_values = calc_top_values(empty_data)
    assert top_values["max_values"]["hiz"] == 0
    assert top_values["max_values"]["batarya"] == 0
    assert top_values["max_values"]["sicaklik"] ==0
    assert top_values["min_values"]["hiz"] == 0
    assert top_values["min_values"]["batarya"] == 0     
    assert top_values["min_values"]["sicaklik"] == 0
    assert find_low_battery_time(empty_data) == None
    assert find_over_speed(empty_data,6.7) == []

    with_only_head =tmp_path/ "data.csv"
    with_only_head.write_text("zaman,sicaklik,hiz,batarya")
    with pytest.raises(ValueError):
        read_data(with_only_head)
    