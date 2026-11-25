# Python alıştırmaları

Python'u sıfırdan öğreten, statik bir Türkçe eğitim sitesi. İki bölümden oluşur:

1. **Temelden başla** (17 konu): print, değişkenler, veri tipleri, operatörler, listeler, iç içe listeler, tuple ve set, sözlükler,
   metin işlemleri, f-string, hazır fonksiyonlar, if/elif/else, for, comprehension/enumerate/zip, while/break/continue,
   fonksiyonlar, hata yakalama ve import.
2. **Alıştırma problemleri** (6 konu): asal çarpan bulma, permütasyon, liste düzleştirme, verilen ortalamada liste oluşturma,
   sınıf ortalaması, zaman farkı. Her problemde "önce şu temel konulara bakın" bağlantıları vardır.

Her konuda anlatım, notebook'tan alınan örnekler ve yeni örnekler bulunur. Her örnekte problem açıklaması, Python kodu ve çıktı vardır.

- Çıktılar önceden gerçekten çalıştırılarak HTML'e statik olarak yazıldı; her örnekte "Cevabı göster" düğmesiyle açılır.
  Sitede Python çalışmaz; kurulum, kütüphane veya backend gerekmez.
- Örnek ve konu tamamlama işaretleri ile ilerleme çubuğu tarayıcının `localStorage` alanında saklanır.

## Dosyalar

```
index.html          Üretilmiş sayfa (tüm içerik ve çıktılar içinde)
style.css           Tasarım
script.js           Konu geçişi, ilerleme kaydı, cevap gösterme, sözdizimi renklendirme
tools/build.py      index.html'i üretir; örnekleri çalıştırıp çıktıları kaydeder
tools/basics.py     "Temelden başla" konularının metinleri ve örnekleri
tools/template.html Sayfa iskeleti
```

## Yerelde açma

`index.html` dosyasına çift tıklamanız yeterlidir.

## GitHub Pages ile yayımlama (normal web sitesi gibi)

1. github.com'da hesap açın veya giriş yapın.
2. Sağ üstte **+ → New repository**'ye tıklayın.
3. **Repository name** alanına `kullaniciadiniz.github.io` yazın (kullaniciadiniz yerine GitHub kullanıcı adınız).
4. **Public** seçili olsun, **Create repository**'ye tıklayın.
5. Açılan sayfada **uploading an existing file** bağlantısına tıklayın.
6. `index.html`, `style.css`, `script.js` dosyalarını (isterseniz `tools` klasörünü de) sürükleyip bırakın. Dosyalar doğrudan ana dizinde olmalı; zip yüklemeyin.
7. En altta **Commit changes**'e tıklayın.
8. **Settings → Pages** bölümünde **Source** olarak `Deploy from a branch`, **Branch** olarak `main` ve `/ (root)` seçip **Save**'e tıklayın.
9. 1-2 dakika sonra site `https://kullaniciadiniz.github.io` adresinde açılır. Bu bağlantıyı paylaşabilirsiniz.

Siteyi güncellemek için aynı depoda **Add file → Upload files** ile değişen dosyaları yükleyin.

## İçeriği değiştirmek

Temel konular `tools/basics.py` içindeki `BASICS`, problemler `tools/build.py` içindeki `TOPICS` listesindedir. Düzenledikten sonra:

```
python3 tools/build.py
```

Komut her örneği çalıştırır, çıktıları `index.html` içine yazar ve problem çözümlerini notebook'taki test değerleriyle doğrular
(biri başarısız olursa hata verir). Kasıtlı hata gösteren örnekler (ör. `int("5a")`) örneğe `"hata"` işareti eklenerek tanımlanır.
Bu adım yalnızca siteyi güncellerken gerekir; ziyaretçiler için hiçbir şey çalıştırılmaz.

## Notlar

- Problem notebook'unda fonksiyonlar boş bırakılmıştı. Buradaki çözümler çalışma amaçlı olarak bu proje için yazıldı.
- **Zaman farkı:** Notebook'taki açıklama "mutlak değer" der, fakat testler (`23:50 → 00:20 = 30`, `18:00 → 07:00 = 780`)
  `time1`'den `time2`'ye ileri doğru geçen süreyi bekler. Çözüm testlere göre yazıldı.
- **Ortalamada liste:** Kontrol fonksiyonu `numpy` ister; sitedeki doğrulamalar yalnızca standart kütüphaneyi kullanır.
- **Sınıf ortalaması:** Standart sapma olarak popülasyon sapması (`statistics.pstdev`) kullanıldı.
- Temel bölümde `input()` ve dosya işlemleri çalıştırılmaz (tarayıcıda anlamlı değil); `input()` davranışı sabit bir değerle gösterilir.
