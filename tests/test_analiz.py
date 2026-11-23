import pytest  # noqa: F401, I001
import json
from src.analiz import calc_top_values, find_low_battery_time, find_over_speed , get_data # type: ignore
from src.okuyucu import read_data
from src.yazici import write_json,write_file  # type: ignore

VERI = {
    "zaman": [
        "2026-11-22 10:00:00",
        "2026-11-22 10:00:30",
        "2026-11-22 10:01:00",
        "2026-11-22 10:01:30",
        "2026-11-22 10:02:00",
        "2026-11-22 10:02:30",
        "2026-11-22 10:03:00",
        "2026-11-22 10:03:30",
        "2026-11-22 10:04:00",
        "2026-11-22 10:04:30",
    ],
    "sicaklik": [24.5, 24.8, 25.1, 25.6, 26.0, 26.3, 26.9, 27.2, 27.5, 27.1],
    "hiz": [3.2, 4.1, 5.0, 6.9, 7.4, 5.8, 4.4, 3.9, 2.5, 1.2],
    "batarya": [98, 90, 80, 70, 55, 40, 30, 21, 18, 15],
}


def test_normal_data(tmp_path):

    # --- min / max / ortalama Kontrolu
    top_values = calc_top_values(VERI)
    assert top_values["max_values"]["zaman"] == "2026-11-22 10:04:30"
    assert top_values["max_values"]["hiz"] == 7.4
    assert top_values["max_values"]["batarya"] == 98
    assert top_values["max_values"]["sicaklik"] == 27.5

    assert top_values["min_values"]["zaman"] == "2026-11-22 10:00:00"
    assert top_values["min_values"]["hiz"] == 1.2
    assert top_values["min_values"]["batarya"] == 15
    assert top_values["min_values"]["sicaklik"] == 24.5

    assert top_values["mean_values"]["sicaklik"] == 26.1
    assert top_values["mean_values"]["hiz"] == 4.44
    assert top_values["mean_values"]["batarya"] == 51.7

    # --- batarya ve hız ---
    assert find_low_battery_time(VERI) == "2026-11-22 10:04:00"
    assert find_over_speed(VERI, 6.7) == ["2026-11-22 10:01:30", "2026-11-22 10:02:00"]

    # sınır durumları
    assert find_over_speed(VERI, 7.4) == []              # eşiğin kendisi aşmış sayılmaz (>)
    assert len(find_over_speed(VERI, 0)) == 10           # hepsi 0'dan büyük
    assert find_over_speed(VERI, 100) == []
    assert find_low_battery_time({**VERI, "batarya": [98] * 10}) is None
    assert find_low_battery_time({**VERI, "batarya": [20] * 10}) is None   # tam 20, %20 altı değil

    # --- get_data hepsini birleştiriyor mu ---
    output_data = get_data(esik_deger=6.7, sensor_values=VERI)
    assert output_data["top_values"] == top_values
    assert output_data["over_speed_time"] == ["2026-11-22 10:01:30", "2026-11-22 10:02:00"]
    assert output_data["low_battery_time"] == "2026-11-22 10:04:00"

    # --- geçerli bir CSV'yi read_data ile okuma ---
    lines = ["zaman,sicaklik,hiz,batarya"] + [
        f"{z},{t},{h},{b}"
        for z, t, h, b in zip(
            VERI["zaman"], VERI["sicaklik"], VERI["hiz"], VERI["batarya"]
        )
    ]
    csv_file = tmp_path / "normal.csv"
    csv_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    data, undefined = read_data(csv_file)
    assert undefined == 0
    assert data == VERI

    # --- yazıcılar ---
    output_data["undefined"] = undefined
    txt_path = tmp_path / "output" / "output.txt"        # klasör yok, kendisi oluşturmalı
    json_path = tmp_path / "output" / "output.json"
    write_file(data=output_data, path=txt_path)
    write_json(data=output_data, path=json_path)

    report = txt_path.read_text(encoding="utf-8")
    assert "TELEMETRİ ANALİZ RAPORU" in report
    assert "Batarya %20 altına ilk düştüğü zaman: 2026-11-22 10:04:00" in report
    assert "Hız eşiğini aşan satır sayısı: 2" in report
    assert "Atlanan satır sayısı: 0" in report

    assert json.loads(json_path.read_text(encoding="utf-8")) == output_data


def test_corrupted_data(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text(
        "zaman,sicaklik,hiz,batarya\n"
        "2026-11-22 10:00:00,24.5,3.2,98\n"  # geçerli
        "2026-11-22 10:00:30,25.1,4.0,97\n"  # geçerli
        "2026-11-22 10:01:00,25.4,,96\n"  # boş hız
        "2026-11-22 10:01:30,abc,5.0,95\n"  # sayı yerine harf
        "2026-11-22 10:02:00,26.0,3.3\n"  # eksik sütun
        "2026-11-22 10:02:30,26.2,3.5,94,7\n"  # fazla sütun
        "2026-11-22 10:03:00,26.4,3.1,-5\n"  # negatif batarya
        "bozuk-tarih,26.5,3.0,93\n"  # geçersiz tarih
        "2026-13-45 10:04:00,26.5,3.0,93\n"  # imkansız tarih
        "\n"  # boş satır
        "2026-11-22 10:05:30,27.0,3.4,92\n",  # geçerli
        encoding="utf-8",
    )
    data, undefined = read_data(file)

    # sayılar
    assert undefined == 8
    assert len(data["zaman"]) == 3

    # tüm sütunlar aynı uzunlukta olmalı
    assert (
        len(data["zaman"])
        == len(data["sicaklik"])
        == len(data["hiz"])
        == len(data["batarya"])
        == 3
    )

    # geçerli satırların değerleri
    assert data["zaman"] == [
        "2026-11-22 10:00:00",
        "2026-11-22 10:00:30",
        "2026-11-22 10:05:30",
    ]
    assert data["sicaklik"] == [24.5, 25.1, 27.0]
    assert data["hiz"] == [3.2, 4.0, 3.4]
    assert data["batarya"] == [98, 97, 92]

    # bozuk satırların değerleri listelere girmemiş olmalı
    assert "bozuk-tarih" not in data["zaman"]
    assert "abc" not in data["sicaklik"]
    assert -5 not in data["batarya"]

    # bozuk satırlar atlandıktan sonra analiz sonuçları
    top_values = calc_top_values(data)
    assert top_values["max_values"]["sicaklik"] == 27.0
    assert top_values["max_values"]["hiz"] == 4.0
    assert top_values["max_values"]["batarya"] == 98
    assert top_values["min_values"]["sicaklik"] == 24.5
    assert top_values["min_values"]["hiz"] == 3.2
    assert top_values["min_values"]["batarya"] == 92
    assert top_values["mean_values"]["sicaklik"] == 25.533
    assert top_values["mean_values"]["hiz"] == 3.533
    assert top_values["mean_values"]["batarya"] == 95.667

    assert find_low_battery_time(data) is None          # batarya hiç %20 altına düşmüyor
    assert find_over_speed(data, 3.3) == [
        "2026-11-22 10:00:30",
        "2026-11-22 10:05:30",
    ]
    assert find_over_speed(data, 6.7) == [] 

def test_empty_data(tmp_path):
    empty_data = {"zaman": [], "sicaklik": [], "hiz": [], "batarya": []}

    # analiz fonksiyonları boş listede çökmeden varsayılan değer döndürmeli
    top_values = calc_top_values(empty_data)
    assert top_values["max_values"]["zaman"] == 0
    assert top_values["max_values"]["hiz"] == 0
    assert top_values["max_values"]["batarya"] == 0
    assert top_values["max_values"]["sicaklik"] == 0
    assert top_values["min_values"]["zaman"] == 0
    assert top_values["min_values"]["hiz"] == 0
    assert top_values["min_values"]["batarya"] == 0
    assert top_values["min_values"]["sicaklik"] == 0
    assert top_values["mean_values"]["hiz"] == 0
    assert top_values["mean_values"]["batarya"] == 0
    assert top_values["mean_values"]["sicaklik"] == 0
    assert find_low_battery_time(empty_data) is None
    assert find_over_speed(empty_data, 6.7) == []

    output_data = get_data(esik_deger=6.7, sensor_values=empty_data)

    assert output_data["top_values"] == top_values
    assert output_data["over_speed_time"] == []
    assert output_data["low_battery_time"] is None

    # sadece başlık satırı (sonunda \n yok)
    with_only_head = tmp_path / "data.csv"
    with_only_head.write_text("zaman,sicaklik,hiz,batarya")
    with pytest.raises(ValueError):
        read_data(with_only_head)

    # tamamen boş dosya (0 byte)
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")
    with pytest.raises(ValueError):
        read_data(empty_file)

    # başlık + sadece boş satırlar: hata vermez, hepsi atlanır
    empty_lines = tmp_path / "empty_lines.csv"
    empty_lines.write_text("zaman,sicaklik,hiz,batarya\n\n\n")
    data, undefined = read_data(empty_lines)
    assert undefined == 2
    assert data == empty_data

    # tüm satırlar bozuk: yine boş veri ve atlanan sayısı
    corrupted = tmp_path / "corrupted.csv"
    corrupted.write_text(
        "zaman,sicaklik,hiz,batarya\n"
        "bozuk-tarih,abc,abc,abc\n"
        "2026-11-22 10:00:00,24.5,,98\n"
    )
    data, undefined = read_data(corrupted)
    assert undefined == 2
    assert data == empty_data

    # olmayan dosya
    with pytest.raises(FileNotFoundError):
        read_data(tmp_path / "not_exist.csv")