1. Projenin Amacı :
    Sensorde gelen bozuk , geçersiz , ihtimaller dışında olan verileri ayrıştırarak gerçekçi ve doğru sonuçları ayırmayı hedeflemektedir. Bozuk verileri ve sağlam veriler ayrılarak sensör verileri düzenli hale getirilmesi amaçlanmaktadır.

    Aynı zamanda bu işlemi yaparken performansı optimize etmek hedeflenmektedir.
    Bu yüzden f.readlines() yerine csv.Dictreader kullanılarak bellek kullanımını minimumda tutmayı hedeflemektedir.

    Modüler yapı kurularak sadece anahatar kelimelerin değiştirilmesi ile programın diğer sensörler ile de uyumlu çalışması hedeflenmektedir bu doğrultuda çalışmalar sürmektedir.

2. venv kurulumu ve venv başlatımı :
    sanal makine başlatmak istediğimiz klasörde iken terminali açıyoruz
    ve python3 -m venv .venv kodunu yazıyoruz biraz bekledikten sonra kurulum tamamlanıyor
    venv active etmek için gene aynı terminalde source .venv/bin/activate yazarak venv başlatıyoruz

    yeni paketlerin kurulumu için pip install paket_adi paketlerin listesi için pip list ve çıkmak için ise deactivate
    
3. Çalıştırmak için örnek komut şöyledir : python -m src.main --input data/log.csv --output output --max 5.1 burada --max sınırının alabileceği 
    max değer iken --output ise analiz sonuçlarının yazılacağı klasörü temsil etmektedir --input ise verilerin nereden çekileceğini belirtmektedir.

4. TraceMalloc ile bellek takibi ve nihai sonuçlar : 
    1 milyon satırlık CSV için readlines() ile tüm dosyayı belleğe alan sürüm tepe noktada yaklaşık 77.8 MB kullandı. Dosyayı satır satır okuyan sürüm ise yaklaşık 0.2 MB kullandı. Bu, satır satır okumanın bellekte yaklaşık 479 kat daha verimli olduğunu gösteriyor, çünkü dosyanın tamamı değil, aynı anda yalnızca tek satır bellekte tutuluyor.

5. Java ve C den iki fark:
    söz dizimi olarak çok daha rahatlık sunması c de satırlarca süren kod satırları burada sadece 4-5 tane fonk ile çözülebilir hale geliyor
    boşluk kolaylığı böylece parantez arama derdi bitiyor eklentiler ile renklere bakarak hangi blok içerisinde olduğunu anlayabiliyorsunuz
    
6. Test başlatmak için:
    öncelikle 2. adım ile venvyi başlatıyoruz sonra python -m pytest -v yazınca testimiz başlıyor ve sonuçlar ekrana geliyor
7. Son commit hariç tüm commitler : 
    8d8365b (HEAD -> main) style: verilerin none gelmesi durumunda dosyaya logging error yazan hata giderildi
        5cc26e0 style: gereksiz import edilen fonk kaldırıldı
        e5f1315 (origin/main, origin/HEAD) test başlatma yönergesi eklendi yazım hataları düzeltildi
        c56f605 style: gereksiz print satırı kaldırıldı
        c4cb7e1 style: kullanılmayan değişkenler kaldırıldı
        0f3eda5 feat: verilerin kontrolü güncelledi çökmeye neden olan len(veriler) kısmı kaldırıldı
        2f51759  kullanılmayan test importu kaldırıldı
        5029bb0 Yeni bozuk satırlar eklendi (nan,inf,eksik saat) dan dolayı bozuk satırlar bundan dolayı undefined data 11 yapıldı(8'di)
        1f2d7da feat: verilerin none gelmesi durumunda len(veriler) satırı çöktüğü için kaldırıldı
        099b2eb feat: işlem başarılı satırı artık logging ile dosyaya yazılıcak
        c2435ba style: kullanılmayan import satırı silindi
        de0ea0c çakışma çözüldü gereksiz çağırılan fonk kaldırıldı
        07a6ce4 feat: fonksiyonlar maindeki eski haline getirildi
        fb9f0ec feat:ayrı bir fonk ile bellek ölçümü ayrıldı
        74d82b3 feat:tüm bellek karşılaştırmaları karsilastir.py a taşındı kullanılmayan importlar silindi
        970b1f6 feat:bellek takibi ayrı bir fonk devredildi devredilen komutlar silindi
        2a4c6c6 style: veri havuzu genişletildi
        72fbb7d readme düzenlendi java ve c den farkı ve çalıştırma komutu eklendi
        0f61e54 style: boşluk - format düzenlemesi
        ec616e5 g Merge branch 'feat/csv_reader'
        6ce960e README.md düzenlendi
        01935b0 (origin/test/malloc) test: satır satır okuma ve direk olarak hepsini belleğe alma arasındaki farkı gösteriyor
        7979be6 test: trace memory fonk eklendi
        19cc007 style:kullanılmayan line_count satırları kaldırıldı
        d3b8e8c feat/invalid_data artık yerel değişken olarak tutuluyor
        79b140a feat: empty lines durumunu test eden kod eklendi
        bd1a01a style: kullanılmayan importlar silindi , görüntüyü düzenlemek için bazı düzenlemeler yapıldı
        5bb8c41 fix:logging.wrning olarak düzeltildi,hata verirken args.max için +d yerine %s kullanıldı
        bb5f8e1 feat: nan,inf gibi durumlarda yanlış ölçüm sorunu giderildi
        8097058 style: kullanılmayan importlar silindi
        a81aa12 style: print(sensor_values) silindi encoding= utf-8 eklendi
        82781b5 fix: logging errorda değişken verilmediği için hataya yol açan sorun giderildi
        e18c766 (origin/chore/temizlik) chore: kullanılmayan output1 klasörü ve control_file.py silindi
        6faf810 style:yanlis hataya sebep olan test kodu silindi
        5a558cf (origin/feat/csv_reader) feat: eski csv_data ve data adları ve içeriği değiştirildi
        9e47694 feat: csv.DictReader kullanılarak kod sadeleştirildi ve dinamik hale getirildi
        583de8f (origin/feat/logging) fix: output klasörü olmaması durumunda çökmeye sebep olan hata giderildi
        ab632a0 style: esik değerin 0 dan küçük girilmesi durumunda dosyaya loglanması sağlandı
        dc3c84c Merge branch 'fix/main_py'
        c3f9460 Merge branch 'feat/tests'
        7495445 (origin/feat/tests) feat: geri kalan tüm kontroller eklendi
        2cdf57f (origin/fix/main_py) fix:dosyada output klasörü olmaması duruunda çökmeye neden olan hata giderildi
        a68b20d Merge branch 'refactor/write_data'
        6c7853c style: warning ve print e olan bazı uyarılar error yapıldı
        43f312c (origin/refactor/write_data) refactor: jsona yazılan ham veri analiz edilmiş ver olarak değiştirildi
        1d00242 feat: logging import edilerek hataların düzenli bir şekilde program.log dosyasına yazılması sağlandı
        3a179d6 style: daha düzenli hale getirildi
        a74fe6b test: test_corrupted_data fonk eklendi ve test edildi
        8bd867c feat: read_data nın da kontrol edilmesi sağlandı
        30955f4 test: boş-olmayan data ile kontrol fonk eklendi
        a03985e test: normal data ile test fonk eklendi
        f5d1ad2 style: log1.csv düzeldildi
        8f3c331 fix: kullanılmayan file.exists() satırı kaldırıldı path.mkdir kullanıldı
        fb97294 style: path > input yapıldı aynı zamanda dosya yolu direkt olarak gönderildi
        2575f15 gMerge branch 'feat/control_files'
        301c3f7 fix:dosya yolu olmaması durumunda çıkan hata giderildi
        5b843cc fix: bozuk veri sonucu veri olmaması durumunda çökerten sorun giderildi
        ce4f361 çakışma giderildi
        04d04de style: valueeror ve filenotfounerror aynı exceptte birleştirildi
        854fea3 fix:dosya boş olması durumunda StopIteratıon hatasına neden olan sorun giderildi
        d444153 refactor: yanlış yazılan root değişkeni yerine path yerleştirildi
        179f4f2 refactor: kullanılmayan root,id ve if root,path none satırı kaldırıldı
        fbdd5b0 refactor: gereksiz args satırı kaldırıldı
        bedf0ed refactor: gereksiz path ve root satırları kaldırıldı
        c76351b Merge branch 'feat/dinamik_path'
        f4d36cb fix: invalid_data = x[..] kodunun yanlış yere konmasından dolayı oluşan sorun giderildi
        dbb0cae feat: dönüş değerleri dict yapıldı
        93df733 refactor: import len metodu eklendi
        d54116b feat: control metodu eklendi
        e8f92ff feat:path kullanılarak root kullanımı kaldırıldı
        674d96e (origin/chore/gitignore-txt-sil) chore: gereksiz gitignore.txt silindi
        9179f19 feat:write_json ve write_file birbirinden ayrıldı iki farklı fonk yapıldı
        e8bb5c8 feat: global invalid_data ve cprrupted_data kaldırıldı
        6483b83 feat: type errora düşünce İsAdirectory error veren kod düzeltildi
        f2b1620 style: değişken isimleri ve fonk isimleri ing yapıldı
        afcf0ff style: gereksiz importlar kaldırıldı
        05100e3 conflikt(çakışma) çözüldü
        50bab98 (origin/feat/write_txt) feat: rapor şablonnu eklendi ve yazdırıldı
        030e681 (origin/feat/rapor) feat: rapor sablonu eklendi
        b1a413f (origin/feat/write_json) feat: dosya olmamas halinde uyarı verildi
        b67eaf2 (origin/feat/write_file_with_path) feat: statik dosya yolu düzeltildi
        7963009 feat: utf8 formatı eklendi jsonlar ayrıldı
        cd2e193 (origin/style/main) style: f_max çıkarıldı gereksiz float kontrolü silindi
        14673e0 style: aynı ada farklı dilde sahip hiz-esigi çıkarıldı
        48984f1 (origin/feat/write_file, origin/feat/path) feat: esik deger alma  eklendi ve kontrol edildi
        21226a1 feat: write file fonk yazıldı
        4f5dd65 (origin/feat/fonk_import_ekle) feat: args path ve root seçenekleri eklendi adres konsoldan verilecek
        2524822 style: split_logs > read_data olarak değişti
        fd36bed (origin/feat/arg_pars) feat: fonk ve importlar main dosyasına eklendi
        4f996dc (origin/refactor/analiz) refactor: gereksiz tanımlamalar kaldırıldı koşullar return içine kondu
        26b5dce style: gereksiz importlar silindi
        1b17ce0 feat: logsun hatalı dönmesi halinde false döndürerek çökmeye sebep olan hata giderildi
        a104d4b feat: next(f) ile ilk satırın atlanması saglandı
        b213520 (origin/refactor/okuyucu) refactor: gereksiz enumrate ve id kaldırıldı -m id 0 olması durumunda ilk satırı atlayan gereksiz if kaldırıldı
        cfb9030 (origin/feat/load_data) feat:Dosya olmaması durumunda güvenlik önlemi eklendi -m kod sadeleştirildi
        087d9cc feat: dönen veriler için kontrol eklendi
        ccb3965 feat: invalid_data ve corrupted_data değişkenleri program yeniden başlatınca sıfırlanıcak şekilde düzenlendi
        3e099fe refactor:veriler çekilirken static olan root ve path dinamik hale getirildi
        c11abc3 refactor: import path yolu düzeltildi -m sensor.values.keys de unutulan parantezler eklendi -m
        fe13bed feat: statik olan yol dinamik hale getirildi
        f3b0c17 (origin/refactor/split_logs) refactor: global keyler silindi -m sensor_values split_logs icine tasindi
        ed1936c (origin/feat/append_sensor_values) feat: gereksiz try except metodu kaldırıldı daha modern kullanım tercih edildi
        292303b (origin/refactor/control_data) refactor: datetime dönüşürken zaten kontrol ettiği için gereksiz kontroller silindi
        96a4ce2 style:. importlar organize edildi stil düzene sokuldu test printleri silindi
        fd5d17f feat: getdata fonknunda diğer fonklardan gelen veriler dict yardımıyla return edildi
        ac8ba86 (origin/feat/find_over_speed) feat: find_over_speed fonk eklendi
        7531465 (origin/feat/find_low_battery_time) feat:. find low battery fonk eklend
        69d3999 fix: eski koddan kalan returndeki max value değişkeni top values olarak değiştirildi
        3276a71 refactor:. fonk adı değiştirildi -m gereksiz fonklar kaldırıldı
        19318e1 feat: veriler artık ondalıklı kısımları 3 basamaga gore yuvarlanıyor test satırları silindi
        83c6178 fix : verilerin floata donusmesini engelleyen hata giderildi
        184eb3f feat: top values fonk eklendi top values fonk dolduruldu veriler float gelmedigi icin hata veriyor veriler float olarak gonderilmeli
        04007d6 test : test sat irlari silindi
        c7ce80f feat: id sütünu silindei iç ice dict yapisi kaldirildi dict keyleri static yapıldı
        fdc2f9f feat: main fonk donus degeri split_logs yapilmistir dict fonk tur atamasi yapilmistir
        7ef2d63 feat : okuyucu classi import edildi main fpnk eklendi
        83619d7 feat : main fonk eklendi split logs fonk ile sensor values dictini donduruyor
        bffafd3 feat : fonklar eklend i
        878df79 feat : split_logs donus degeri eklendi > sensor_values
        fe4285b refactor : test satırları silindi , aciklamalar eklendi
        d95eaa9 feat :  invalid data ve corrupted data sutunları eklendi speed ve temp kontrolı eklendi
        088bd00 feat : battery,temp,speed kontrolü eklendi
        4a6c7ae feat : battery,temp,speed kontrolü eklendi
        cb1f4f0 fix :  date ve timea baslangic degeri eklendi timeın veri aldığı index 1 den 0 a çekildi
        8f13aca feat : eski tek atama yerine zip ile toplu atama yapılıyor
        45f790e fix : cakisma çözüldü
        c805345 feat : \n karakteri kaldırıldı split yerine re.split yapıldı > kod sadelestirildi
        401dac5 feat : control data fonk için date ve time kontrolleri eklendi
        a5c93da feat: gelen veri parcalarina ayrildi append_sensor_values fonk gonderildi
        ea4bf40 feat : append_sensor_values fonk eklendi
        d54a71e style : bosluk duzenlemesi
        fddad0e feat : load data fonk eklendi
        9453375 feat : fonklar eklendi
        456282c license eklendi
        a73dec5 projenin dosya iskeleti olusturuldu
        55da3bf Gorevler eklend i
        74e336b Initial commit

