1. Projenin Amacı :
    Sensorde gelen bozuk , geçersiz , ihtimaller dışında olan verileri ayrıştırarak gerçekçi ve doğru sonuçları ayırmayı hedeflemektedir. Bozuk verileri ve sağlam veriler ayrılarak sensör verileri düzenli hale getirilmesi amaçlanmaktadır.

    Aynı zamanda bu işlemi yaparken performansı optimize etmek hedeflenmektedir.
    Bu yüzden f.readlines() yerine csv.Dictreader kullanılarak bellek kullanımını minimumda tutmayı hedeflemektedir.

    Modüler yapı kurularak sadece anahatar kelimelerin değiştirilmesi ile programın diğer sensörler ile de uyumlu çalışması hedeflenmektedir bu doğrultuda çalışmalar sürmektedir.
2. venv kurulumu ve venv başlatımı :
    sanal makine başlatmak istediğimiz klasörde iken terminali açıyoruz
    ve python3 -m venv venv kodunu yazıyoruz biraz bekledikten sonra kurulum tamamlanıyor
    vevn active etmek için gene aynı terminalde sourc .venv/bin/activate yazarak venv başlatıyoruz

    yeni paketlerin kurulumu için pip install paket_adi paketlerin listesi için pip list ve çıkmak için ise deactivate
3.
TraceMalloc ile bellek takibi ve nihai sonuçlar : 
    1 milyon satırlık CSV için readlines() ile tüm dosyayı belleğe alan sürüm tepe noktada yaklaşık 77.8 MB kullandı. Dosyayı satır satır okuyan sürüm ise yaklaşık 0.2 MB kullandı. Bu, satır satır okumanın bellekte yaklaşık 479 kat daha verimli olduğunu gösteriyor, çünkü dosyanın tamamı değil, aynı anda yalnızca tek satır bellekte tutuluyor.
