#!/usr/bin/env python3
"""index.html dosyasını üretir.

Her örnek burada gerçekten çalıştırılır; çıktılar HTML içine statik metin olarak yazılır.
Site açıldığında tarayıcıda Python çalışmaz. Kullanım:  python3 tools/build.py
"""
import contextlib
import html
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from basics import BASICS  # noqa: E402
NB, NEW = "Notebook örneği", "Yeni örnek"

TOPICS = [
    # ------------------------------------------------------------------ 1
    dict(
        id="asal-carpan", title="Asal çarpan bulma",
        short="Bir sayıyı bölen farklı asal sayılar",
        lead="Bir sayının asal çarpanlarını bulun. Notebook testleri her çarpanı yalnızca bir kez bekler: "
             "2025 = 3⁴ · 5² için sonuç [3, 5] olmalıdır.",
        points=[
            "d değerini 2'den başlatın ve d·d ≤ n olduğu sürece deneyin; √n'den büyük iki ayrı çarpan bulunamaz.",
            "d, n'yi bölüyorsa listeye ekleyin ve n'yi d'ye tamamen bölün. Böylece çarpan tekrar etmez ve sıradaki d her zaman asal olur.",
            "Döngü bittiğinde n > 1 ise kalan değerin kendisi de asal bir çarpandır.",
        ],
        solution=r'''from typing import List

def prime_factors(n: int) -> List[int]:
    """n sayısının farklı asal çarpanlarını döndürür."""
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors''',
        examples=[
            (NB, "Notebook test değerleri",
             "Kontrol fonksiyonundaki beş sayının asal çarpanlarını bulun.",
             r'''for n in [75, 919191, 2025, 512, 9699690]:
    print(f"{n} -> {prime_factors(n)}")'''),
            (NEW, "Asal sayılar ve küçük girdiler",
             "Asal bir sayının tek çarpanı kendisidir. 1 sayısının asal çarpanı yoktur.",
             r'''for n in [1, 2, 97, 360, 1001]:
    print(f"{n:>5} -> {prime_factors(n)}")'''),
            (NEW, "Büyük bir sayı",
             "600851475143 sayısının asal çarpanlarını ve en büyüğünü bulun. √n kuralı sayesinde yalnızca birkaç yüz bin deneme yapılır.",
             r'''n = 600851475143
factors = prime_factors(n)
print("Çarpanlar:", factors)
print("En büyüğü:", max(factors))'''),
            (NEW, "Üslerle gösterim",
             "Bulunan çarpanların kaçar kez geçtiğini sayarak sayıyı çarpım olarak yazın.",
             r'''n = 2025
parts = []
for p in prime_factors(n):
    k, m = 0, n
    while m % p == 0:
        m //= p
        k += 1
    parts.append(f"{p}^{k}")
print(f"{n} = " + " x ".join(parts))'''),
        ]),
    # ------------------------------------------------------------------ 2
    dict(
        id="permutasyon", title="Permütasyon bulma",
        short="Rakamların tüm farklı dizilişleri",
        lead="Rakamlardan oluşan bir string verildiğinde, rakamların yerleri değiştirilerek elde edilebilecek tüm dizilişleri "
             "listeleyin. Tekrarlı rakamlarda aynı yazım yalnızca bir kez yer almalıdır.",
        points=[
            "itertools.permutations tekrar eden rakamlarda aynı dizilişi birden çok kez üretir. Sonuçları bir küme (set) içinde toplayarak tekilleştirin.",
            "Girdi string olduğu için baştaki sıfırlar korunur: \"1020\" için \"0012\" de geçerli bir sonuçtur.",
            "Farklı diziliş sayısı n! / (tekrar eden her rakamın faktöriyelinin çarpımı) formülüyle hesaplanır.",
        ],
        solution=r'''from itertools import permutations
from typing import List

def digit_permutations(n: str) -> List[str]:
    """Rakamların tüm farklı dizilişlerini sıralı liste olarak döndürür."""
    return sorted({"".join(p) for p in permutations(n)})''',
        examples=[
            (NB, "Notebook test değerleri",
             "\"123\", \"999\", \"989\" ve \"3578\" için tüm farklı dizilişleri bulun.",
             r'''for n in ["123", "999", "989", "3578"]:
    result = digit_permutations(n)
    print(f"{n} -> {len(result)} diziliş")
    print(result)'''),
            (NEW, "Tekrarlı rakamlar",
             "\"112\" içinde iki tane 1 vardır. 3! = 6 yerine yalnızca 3 farklı diziliş vardır.",
             r'''print(digit_permutations("112"))
print(digit_permutations("5"))'''),
            (NEW, "Baştaki sıfır",
             "Girdi string olduğundan \"0012\" gibi sonuçlar da listede yer alır.",
             r'''result = digit_permutations("1020")
print(len(result), "diziliş")
print(result)'''),
            (NEW, "Sonuç sayısını formülle doğrulama",
             "\"112233\" için üretilen liste uzunluğunu n! / (2! · 2! · 2!) formülüyle karşılaştırın.",
             r'''from math import factorial
from collections import Counter

n = "112233"
expected = factorial(len(n))
for count in Counter(n).values():
    expected //= factorial(count)

print("Üretilen:", len(digit_permutations(n)))
print("Formül  :", expected)'''),
        ]),
    # ------------------------------------------------------------------ 3
    dict(
        id="flatten", title="Liste düzleştirme",
        short="İç içe listeleri tek listeye çevirme",
        lead="İç içe geçmiş listelerdeki tüm elemanları, sırasını koruyarak düz bir listeye dönüştürün. "
             "Örneğin [1, [2], [[3, 4]]] listesi [1, 2, 3, 4] olur.",
        points=[
            "Eleman bir liste ise aynı fonksiyonu onun için çağırın (özyineleme); değilse sonuca ekleyin.",
            "Boş iç listeler sonuca bir şey eklemez: [[[[[]]]]] için sonuç [] olur.",
            "Yalnızca list türü açılır. Metinler (string) parçalanmaz, tek eleman olarak kalır.",
            "Çok derin yapılarda Python'un özyineleme sınırı (varsayılan 1000) aşılabilir. Yığın kullanan yinelemeli çözüm bu sınırdan etkilenmez.",
        ],
        solution=r'''def flatten_list(nested_list):
    """İç içe listeyi sırayı koruyarak düz listeye çevirir."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result''',
        examples=[
            (NB, "Notebook test değerleri",
             "Kontrol fonksiyonundaki dört iç içe liste yapısını düzleştirin.",
             r'''cases = [
    [1, [2, 3], [4, [5, 6]], 7],
    [[[1, 2], 3], 4],
    [1, [2, [3, [4]]]],
    [[[[[]]]]],
]
for data in cases:
    print(f"{data} -> {flatten_list(data)}")'''),
            (NEW, "Metinler parçalanmaz",
             "Liste içindeki stringler karakterlerine ayrılmamalı, sayılarla karışık yapılar da düzleşmelidir.",
             r'''data = ["a", ["bc", ["d", [2.5]]], "efg", [[], True]]
print(flatten_list(data))'''),
            (NEW, "Sınıflara göre notlar",
             "Sınıf şubelerine göre gruplanmış notları tek listeye çevirip toplam ve ortalamayı hesaplayın.",
             r'''grades = [[70, 80], [90, [60, 100]], [50]]
flat = flatten_list(grades)
print("Notlar  :", flat)
print("Toplam  :", sum(flat))
print("Ortalama:", sum(flat) / len(flat))'''),
            (NEW, "Çok derin liste ve yinelemeli çözüm",
             "2000 katman derinliğindeki bir listede özyinelemeli çözüm hata verir. Yığın kullanan çözüm sorunsuz çalışır.",
             r'''def flatten_iterative(nested_list):
    stack = list(reversed(nested_list))
    result = []
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(reversed(item))
        else:
            result.append(item)
    return result

deep = 0
for i in range(1, 2001):
    deep = [i, deep]

try:
    flatten_list(deep)
except RecursionError:
    print("Özyinelemeli: RecursionError")

result = flatten_iterative(deep)
print("Yinelemeli  :", len(result), "eleman, ilk üçü", result[:3])'''),
        ]),
    # ------------------------------------------------------------------ 4
    dict(
        id="ortalama-liste", title="Verilen ortalamada liste oluşturma",
        short="Eleman sayısı, ortalama ve açıklık verilir",
        lead="Eleman sayısı n, hedef ortalama ve açıklık (max − min) verilen bir liste üretin. Tek bir doğru yanıt yoktur; "
             "üç koşulu sağlayan her liste geçerlidir.",
        points=[
            "En küçük ve en büyük değeri ortalamanın iki yanına simetrik koyun: mean − r/2 ve mean + r/2. Bu ikisinin ortalaması tam olarak mean'dir.",
            "Kalan n − 2 elemanı mean'e eşitleyin. Ortalama bozulmaz, açıklık da r olarak kalır.",
            "n = 1 iken açıklık 0'dan farklı olamaz. Bu durum ValueError ile bildirilir.",
            "Notebook'taki kontrol fonksiyonu numpy kullanır. Buradaki doğrulamalar yalnızca standart kütüphaneyle yapılır, ek kurulum gerekmez.",
        ],
        solution=r'''def generate_mean_list(n, mean, range_width):
    """n elemanlı, ortalaması mean, açıklığı range_width olan bir liste üretir."""
    if n < 1:
        raise ValueError("n en az 1 olmalı")
    if range_width < 0:
        raise ValueError("açıklık negatif olamaz")
    if n == 1:
        if range_width != 0:
            raise ValueError("Tek elemanlı listenin açıklığı 0 olmalı")
        return [mean]
    half = range_width / 2
    return [mean - half, mean + half] + [mean] * (n - 2)''',
        examples=[
            (NB, "Notebook test değerleri",
             "(10, 50, 25), (5, 0, 0) ve (100, 55, 100) için üretilen listelerin uzunluk, ortalama ve açıklığını kontrol edin.",
             r'''from statistics import fmean

for n, mean, r in [(10, 50, 25), (5, 0, 0), (100, 55, 100)]:
    values = generate_mean_list(n, mean, r)
    print(f"n={n}: uzunluk={len(values)}, ortalama={fmean(values)}, açıklık={max(values) - min(values)}")'''),
            (NEW, "Küçük bir liste",
             "4 elemanlı, ortalaması 10 ve açıklığı 6 olan bir liste üretin.",
             r'''values = generate_mean_list(4, 10, 6)
print(values)
print("Ortalama:", sum(values) / len(values))
print("Açıklık :", max(values) - min(values))'''),
            (NEW, "Negatif ve ondalıklı ortalama",
             "6 elemanlı, ortalaması -2.5 ve açıklığı 9 olan bir liste üretin; sonucu math.isclose ile doğrulayın.",
             r'''from math import isclose

values = generate_mean_list(6, -2.5, 9)
print(values)
print(isclose(sum(values) / 6, -2.5), isclose(max(values) - min(values), 9))'''),
            (NEW, "Sınır durumları",
             "Tek elemanlı bir listede açıklık yalnızca 0 olabilir. Mümkün olmayan istek hata verir.",
             r'''print(generate_mean_list(1, 7, 0))

try:
    generate_mean_list(1, 7, 3)
except ValueError as error:
    print("Hata:", error)'''),
        ]),
    # ------------------------------------------------------------------ 5
    dict(
        id="sinif-ortalamasi", title="Sınıf ortalaması hesaplama",
        short="Geçersiz ve aykırı notları eleyerek ortalama",
        lead="Not listesinden geçersiz değerleri ve aykırı uçları ayıklayarak \"stabil ortalamayı\" hesaplayın.",
        points=[
            "Önce [0, 100] aralığı dışındaki notları atın.",
            "Kalan notların ortalamasını ve standart sapmasını bulun. Burada popülasyon standart sapması (pstdev) kullanılır.",
            "[ortalama − sapma, ortalama + sapma] dışında kalan notları da atın ve geriye kalanların ortalamasını float olarak döndürün.",
            "Hiç geçerli not yoksa 0.0 döndürülür.",
        ],
        solution=r'''from statistics import mean, pstdev

def calculate_mean(l: list[int]) -> float:
    """Geçersiz ve aykırı notlar dışarıda bırakılarak stabil ortalamayı döndürür."""
    valid = [x for x in l if 0 <= x <= 100]
    if not valid:
        return 0.0
    m, s = mean(valid), pstdev(valid)
    stable = [x for x in valid if m - s <= x <= m + s]
    return float(mean(stable))''',
        examples=[
            (NB, "Notebook test değerleri",
             "Kontrol fonksiyonundaki beş not listesini ve beklenen ortalamaları karşılaştırın.",
             r'''cases = [
    ([40, 50, 60, 55, 45], 50.0),
    ([10, 20, -5, 105, 30], 20.0),
    ([50, 52, 48, 49, 100], 49.75),
    ([80, 85, 82, 84, 10], 82.75),
    ([70, 72, 68, 69, 0], 69.75),
]
for grades, expected in cases:
    print(f"{grades} -> {calculate_mean(grades)} (beklenen {expected})")'''),
            (NEW, "Adım adım hesaplama",
             "[90, 92, 88, 91, 30, 150] listesinde her aşamayı yazdırın. 150 geçersizdir, 30 ise aykırı değerdir.",
             r'''from statistics import mean, pstdev

grades = [90, 92, 88, 91, 30, 150]
valid = [x for x in grades if 0 <= x <= 100]
m, s = mean(valid), pstdev(valid)
stable = [x for x in valid if m - s <= x <= m + s]

print("Geçerli notlar:", valid)
print(f"Ortalama={m:.2f}, sapma={s:.2f}")
print(f"Kabul aralığı: [{m - s:.2f}, {m + s:.2f}]")
print("Kalan notlar  :", stable)
print("Stabil ortalama:", calculate_mean(grades))'''),
            (NEW, "Hiç geçerli not yok",
             "Tüm notlar aralık dışındaysa fonksiyon 0.0 döndürmelidir. Boş liste için de aynısı geçerlidir.",
             r'''print(calculate_mean([-3, 120, 101]))
print(calculate_mean([]))'''),
            (NEW, "Sınır durumları",
             "Tüm notlar eşitse sapma 0'dır ve hiçbir not elenmez. 0 ve 100 geçerli uç değerlerdir.",
             r'''print(calculate_mean([60, 60, 60, 60]))
print(calculate_mean([0, 100]))
print(calculate_mean([0, 100, 50, 51, 49]))'''),
        ]),
    # ------------------------------------------------------------------ 6
    dict(
        id="zaman-farki", title="Zaman farkı",
        short="İki saat arasındaki dakika farkı",
        lead="Saat ve dakika olarak verilen iki zaman arasındaki süreyi (örneğin 08:30 ve 17:15) dakika cinsinden hesaplayın. Notebook açıklaması \"mutlak değer\" der, ancak testler (23:50 → 00:20 = 30, 18:00 → 07:00 = 780) time1'den time2'ye ileri doğru geçen süreyi bekler; time2 daha erkense gece yarısı geçilmiş sayılır.",
        points=[
            "Notebook'taki açıklama \"mutlak değer\" der, ancak testler 23:50 → 00:20 için 30 ve 18:00 → 07:00 için 780 bekler. "
            "Bu değerler time1'den time2'ye ileri doğru geçen süreye uyar. time2 daha erkense gece yarısı geçilmiş sayılır.",
            "Her saati dakikaya çevirin: saat × 60 + dakika.",
            "Farkı % 1440 ile alın. Negatif fark otomatik olarak ertesi güne sarar.",
            "Aynı saat 0 dakika verir (24 saat değil).",
        ],
        solution=r'''def time_diff(time1: str, time2: str) -> int:
    """time1'den time2'ye ileri doğru geçen dakika (gece yarısını aşabilir)."""
    h1, m1 = map(int, time1.split(":"))
    h2, m2 = map(int, time2.split(":"))
    return ((h2 * 60 + m2) - (h1 * 60 + m1)) % 1440''',
        examples=[
            (NB, "Notebook test değerleri",
             "Kontrol fonksiyonundaki beş saat çiftini hesaplayın.",
             r'''pairs = [("08:30", "17:15"), ("12:00", "12:30"), ("23:50", "00:20"),
         ("09:15", "09:15"), ("18:00", "07:00")]
for a, b in pairs:
    print(f"{a} -> {b}: {time_diff(a, b)} dk")'''),
            (NEW, "Gece yarısını aşan süreler",
             "Geceye uzanan süreler ve günün en uzun aralığı.",
             r'''print(time_diff("22:10", "01:40"))
print(time_diff("00:00", "23:59"))
print(time_diff("06:00", "06:01"))'''),
            (NEW, "Yön önemlidir",
             "Saatlerin sırası değişince sonuç da değişir. İki yönün toplamı her zaman 1440 dakikadır (aynı saat hariç).",
             r'''forward = time_diff("08:30", "17:15")
backward = time_diff("17:15", "08:30")
print(forward, backward, forward + backward)'''),
            (NEW, "Vardiya süreleri",
             "Üç vardiyanın süresini saat ve dakika olarak yazdırın. Toplamları bir günü verir.",
             r'''shifts = [("06:00", "14:00"), ("14:00", "22:00"), ("22:00", "06:00")]
total = 0
for start, end in shifts:
    minutes = time_diff(start, end)
    hours, rest = divmod(minutes, 60)
    total += minutes
    print(f"{start}-{end}: {hours} sa {rest} dk")
print("Toplam:", total, "dk")'''),
        ]),
]

# --------------------------------------------------------------------------
# Notebook'taki kontrol fonksiyonlarındaki beklentiler: çözümleri doğrulamak için.
NB_CHECKS = {
    "asal-carpan": lambda f: all(sorted(f(k)) == v for k, v in {
        75: [3, 5], 919191: [3, 7, 13, 37], 2025: [3, 5], 512: [2],
        9699690: [2, 3, 5, 7, 11, 13, 17, 19]}.items()),
    "permutasyon": lambda f: f("123") == ['123', '132', '213', '231', '312', '321'] and f("999") == ['999']
    and f("989") == ['899', '989', '998'] and len(f("3578")) == 24,
    "flatten": lambda f: f([1, [2, 3], [4, [5, 6]], 7]) == [1, 2, 3, 4, 5, 6, 7] and f([[[1, 2], 3], 4]) == [1, 2, 3, 4]
    and f([1, [2, [3, [4]]]]) == [1, 2, 3, 4] and f([[[[[]]]]]) == [],
    "ortalama-liste": lambda f: all(
        len(f(n, m, r)) == n and abs(sum(f(n, m, r)) / n - m) < 1e-6 and abs(max(f(n, m, r)) - min(f(n, m, r)) - r) < 1e-6
        for n, m, r in [(10, 50, 25), (5, 0, 0), (100, 55, 100)]),
    "sinif-ortalamasi": lambda f: all(abs(f(g) - e) < 1e-6 for g, e in [
        ([40, 50, 60, 55, 45], 50.0), ([10, 20, -5, 105, 30], 20.0), ([50, 52, 48, 49, 100], 49.75),
        ([80, 85, 82, 84, 10], 82.75), ([70, 72, 68, 69, 0], 69.75)]),
    "zaman-farki": lambda f: all(f(a, b) == e for a, b, e in [
        ("08:30", "17:15", 525), ("12:00", "12:30", 30), ("23:50", "00:20", 30),
        ("09:15", "09:15", 0), ("18:00", "07:00", 780)]),
}
FUNC_NAMES = {"asal-carpan": "prime_factors", "permutasyon": "digit_permutations", "flatten": "flatten_list",
              "ortalama-liste": "generate_mean_list", "sinif-ortalamasi": "calculate_mean", "zaman-farki": "time_diff"}


# Her problem için önce bakılması önerilen temel konular.
NEEDS = {
    "asal-carpan": ["operatorler", "listeler", "while-dongusu", "fonksiyonlar"],
    "permutasyon": ["string", "tuple-set", "comprehension", "hata-import"],
    "flatten": ["ic-ice-listeler", "if-else", "for-dongusu", "fonksiyonlar"],
    "ortalama-liste": ["listeler", "fonksiyonlar", "hata-import"],
    "sinif-ortalamasi": ["listeler", "comprehension", "if-else", "hata-import"],
    "zaman-farki": ["string", "operatorler", "fonksiyonlar"],
}
GROUPS = [("Temelden başla", "Konu", BASICS), ("Alıştırma problemleri", "Problem", TOPICS)]


def run(code, ns, expect_error=False):
    buf = io.StringIO()
    err = None
    with contextlib.redirect_stdout(buf):
        try:
            exec(code, ns)
        except Exception as e:  # noqa: BLE001
            err = f"{type(e).__name__}: {e}"
    if err and not expect_error:
        raise RuntimeError(f"Beklenmeyen hata: {err}\n{code}")
    if expect_error and not err:
        raise RuntimeError(f"Hata bekleniyordu:\n{code}")
    out = buf.getvalue().rstrip("\n")
    if err:
        out = (out + "\n" if out else "") + "Traceback (most recent call last):\n  ...\n" + err
    return out, bool(err)


def esc(s):
    return html.escape(s, quote=False)


def example_html(ex_id, ex, ns):
    kind, title, problem, code = ex[:4]
    out, is_err = run(code, ns, expect_error=len(ex) > 4)
    tag = "tag-nb" if kind == NB else "tag-new"
    label = "Çıktı (hata)" if is_err else "Çıktı"
    cls = "output err" if is_err else "output"
    return f'''<article class="example" data-ex="{ex_id}">
  <header><h3>{esc(title)}</h3><span class="tag {tag}">{kind}</span></header>
  <p class="problem">{esc(problem)}</p>
  <div class="run">
    <pre class="code"><code>{esc(code)}</code></pre>
    <div class="{cls}">
      <div class="output-head">
        <span class="output-label">{label}</span>
        <button class="reveal" type="button" aria-expanded="false">Cevabı göster</button>
      </div>
      <p class="out-placeholder">Çıktıyı görmek için &ldquo;Cevabı göster&rdquo; düğmesine basın.</p>
      <pre class="out-body">{esc(out)}</pre>
    </div>
  </div>
  <button class="ex-mark" type="button" data-ex="{ex_id}" aria-pressed="false">Örneği tamamladım</button>
</article>'''


def build():
    order = [t for _, _, ts in GROUPS for t in ts]
    titles = {t["id"]: t["title"] for t in order}
    nav, home, views = [], [], []
    for g_title, g_word, topics in GROUPS:
        nav.append(f'<p class="nav-group">{esc(g_title)}</p>')
        home.append(f'<li class="home-group">{esc(g_title)}</li>')
        for i, t in enumerate(topics):
            gi = order.index(t)
            nav.append(f'<a class="nav-link" href="#{t["id"]}" data-topic="{t["id"]}"><span class="num">{i + 1}</span>{esc(t["title"])}</a>')
            home.append(f'<li><a class="home-item" href="#{t["id"]}" data-topic="{t["id"]}"><span class="num">{i + 1}</span>'
                        f'<span><strong>{esc(t["title"])}</strong><small>{esc(t["short"])}</small></span></a></li>')
            is_problem = "solution" in t
            ns = {}
            if is_problem:
                exec(t["solution"], ns)
                assert NB_CHECKS[t["id"]](ns[FUNC_NAMES[t["id"]]]), f"Notebook testi başarısız: {t['id']}"
            ex_html = []
            for j, ex in enumerate(t["examples"], 1):
                ex_ns = ns if is_problem else {}
                ex_html.append(example_html(f'{t["id"]}-{j}', ex, ex_ns))

            prev_l = (f'<a href="#{order[gi - 1]["id"]}">&larr; {esc(order[gi - 1]["title"])}</a>' if gi > 0
                      else '<a href="#baslangic">&larr; Başlangıç</a>')
            next_l = (f'<a href="#{order[gi + 1]["id"]}">{esc(order[gi + 1]["title"])} &rarr;</a>' if gi < len(order) - 1
                      else '<span></span>')
            needs = ""
            if is_problem:
                links = ", ".join(f'<a href="#{n}">{esc(titles[n])}</a>' for n in NEEDS[t["id"]])
                needs = f'<p class="needs">Zorlanırsanız önce şu temel konulara bakın: {links}.</p>'
            solution = ""
            if is_problem:
                solution = (f'<h3 class="sub">Çözüm</h3>\n'
                            f'  <div class="run"><pre class="code"><code>{esc(t["solution"])}</code></pre></div>')
            views.append(f'''<section class="view" id="view-{t["id"]}" aria-labelledby="h-{t["id"]}">
  <p class="crumb">{g_word} {i + 1} / {len(topics)}</p>
  <h2 id="h-{t["id"]}">{esc(t["title"])}</h2>
  <p class="lead">{esc(t["lead"])}</p>
  {needs}
  {solution}
  <h3 class="sub">Örnekler</h3>
  {"".join(ex_html)}
  <div class="topic-bar">
    <span class="topic-count" data-count="{t["id"]}" data-total="{len(t["examples"])}">0 / {len(t["examples"])} örnek</span>
    <button class="mark" type="button" data-topic="{t["id"]}" aria-pressed="false">Konuyu tamamlandı olarak işaretle</button>
  </div>
  <nav class="pager" aria-label="Konu gezinme">{prev_l}{next_l}</nav>
</section>''')

    page = (ROOT / "tools" / "template.html").read_text(encoding="utf-8")
    page = (page.replace("%%NAV%%", "\n".join(nav)).replace("%%HOME%%", "\n".join(home))
            .replace("%%VIEWS%%", "\n".join(views)).replace("%%TOTAL%%", str(len(order))))
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    n_ex = sum(len(t["examples"]) for t in order)
    print(f"index.html üretildi: {len(order)} konu, {n_ex} örnek; tüm notebook testleri geçti.")


if __name__ == "__main__":
    build()
