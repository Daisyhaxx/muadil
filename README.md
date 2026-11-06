# Benzer Oyuncu Bulucu

Bir futbolcunun istatistik profiline en çok benzeyen oyuncuları bulur. Filtreler: yaş, lig, piyasa değeri, sözleşme, ayak.
Örnek: "Süper Lig'de şu forvete en benzer 23 yaş altı oyuncu kim?"

Veri: Sofascore. 6 lig (Süper Lig, TFF 1. Lig, Premier League, Eredivisie, Primeira Liga, Belçika Pro League) ×
3 sezon (23/24, 24/25, 25/26). Lig-sezon başına ~400–500 oyuncu var, bunların 900+ dakika oynayanları kullanılıyor.
Ham veri repoda yok; burada sadece kod ve türetilmiş sonuçlar paylaşılıyor.

## Çalıştırma

```
pip install -r requirements.txt


# Arama
python -m src.similarity.find_similar "Orkun Kökçü" --max-age 23 --max-value 5 --league eredivisie

# Web arayüzü → http://127.0.0.1:8000
uvicorn api.main:app --reload

# Değerlendirme
python -m src.eval.run_eval --out results/retrieval_eval.md
```

## Yöntem

1. Sayım istatistikleri 90 dakikaya bölünür (oran alanları olduğu gibi kalır). 900 dakikanın altı elenir.
2. Her istatistik aynı lig-sezon + mevki grubu içinde percentile'a çevrilir.
3. Mevki grubuna özel 12–20 alanlık feature seti seçilir (`src/features/feature_sets.py`).
4. Aynı mevki grubundaki oyuncular arasında, standardize vektörler üstünde cosine benzerliği hesaplanır.
5. Benzerlik istatistik bazında katkılara ayrılır, radar grafiğiyle gösterilir.

Bir alan lig-sezonda hiç gelmiyorsa (TFF 1. Lig'de xG/xA) "veri yok" sayılır: percentile'ı boş kalır, benzerliğe
katkısı olmaz, radarda çizilmez. Oyuncu bazında gelmeyen sayım alanı ise 0'dır (örn. şutu olmayanın xG'si).

## Değerlendirme

Hazır bir "doğru cevap" yok. Bu yüzden şu test kullanılıyor: oyuncunun **sezon N** profiliyle arama yapılır ve
aynı oyuncunun **sezon N+1** kaydının kaçıncı sırada çıktığına bakılır.

- Sorgu: iki sezonda da 900+ dk oynamış oyuncu. 23/24 → 24/25 ve 24/25 → 25/26 çiftlerinde toplam 1961 sorgu var.
- Aday havuzu: N+1'deki aynı mevki grubundaki herkes (ortalama ~350 oyuncu). Sorgunun N kaydı havuzda yok.
- Metrikler: recall@k (hedef ilk k içinde mi), MRR (1/sıra ortalaması).
- Karşılaştırılan boyutlar: feature seti (mevkiye özel / 45 alanın tamamı) × normalizasyon (lig içi percentile /
  ligler arası percentile / per-90 z-skor) × metrik (cosine / Pearson / Öklid). Toplam 18 yöntem.

**Neden iki ayrı havuz?** Ligler arası percentile ve per-90 z-skor, ligin genel seviyesini vektörün içinde tutuyor.
Örneğin bir ligde oyuncular genel olarak daha çok pas yapıyorsa, o ligin bütün oyuncuları pas eksenlerinde yüksek
görünür ve birbirine yakın düşer. Oyuncuların %89'u ligini değiştirmediğinden, tüm-lig havuzu bu "lig parmak izini"
oyun tarzı benzerliği gibi ödüllendiriyor. Havuzu hedefin ligiyle sınırlamak bu etkiyi ortadan kaldırıyor, bu yüzden adil karşılaştırma
o tablo.

### Havuz: sadece hedefin ligi (adil karşılaştırma)

| Feature seti | Normalizasyon | Metrik | R@1 | R@5 | R@10 | MRR | MRR 23/24 → 24/25 | MRR 24/25 → 25/26 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Ortak (tüm alanlar) | Lig içi percentile | Öklid | 44.5% | 74.1% | 85.8% | 0.580 | 0.598 | 0.562 |
| Ortak (tüm alanlar) | Ligler arası percentile | Öklid | 44.1% | 73.7% | 85.5% | 0.577 | 0.598 | 0.556 |
| Ortak (tüm alanlar) | Per-90 z-skor | Cosine | 43.8% | 72.9% | 85.4% | 0.573 | 0.583 | 0.564 |
| Ortak (tüm alanlar) | Per-90 z-skor | Pearson | 43.6% | 72.6% | 85.2% | 0.570 | 0.580 | 0.560 |
| Ortak (tüm alanlar) | Lig içi percentile | Cosine | 43.2% | 72.4% | 84.2% | 0.567 | 0.577 | 0.558 |
| Ortak (tüm alanlar) | Ligler arası percentile | Cosine | 43.2% | 72.3% | 84.0% | 0.565 | 0.579 | 0.551 |
| Ortak (tüm alanlar) | Lig içi percentile | Pearson | 41.8% | 72.7% | 84.4% | 0.557 | 0.566 | 0.549 |
| Ortak (tüm alanlar) | Ligler arası percentile | Pearson | 41.3% | 72.1% | 83.6% | 0.551 | 0.561 | 0.541 |
| Ortak (tüm alanlar) | Per-90 z-skor | Öklid | 41.9% | 71.7% | 82.3% | 0.551 | 0.573 | 0.530 |
| Mevkiye özel | Per-90 z-skor | Cosine | 39.5% | 70.8% | 84.1% | 0.537 | 0.542 | 0.532 |
| Mevkiye özel | Lig içi percentile | Öklid | 38.4% | 72.0% | 84.1% | 0.534 | 0.542 | 0.526 |
| Mevkiye özel | Ligler arası percentile | Öklid | 38.3% | 72.3% | 84.7% | 0.534 | 0.543 | 0.525 |
| Mevkiye özel | Per-90 z-skor | Öklid | 38.4% | 70.1% | 82.0% | 0.528 | 0.534 | 0.521 |
| Mevkiye özel | Ligler arası percentile | Cosine | 38.1% | 69.2% | 83.4% | 0.525 | 0.536 | 0.514 |
| Mevkiye özel (mevcut) | Lig içi percentile | Cosine | 37.2% | 69.6% | 83.1% | 0.519 | 0.529 | 0.510 |
| Mevkiye özel | Per-90 z-skor | Pearson | 37.2% | 68.7% | 82.4% | 0.516 | 0.525 | 0.507 |
| Mevkiye özel | Ligler arası percentile | Pearson | 35.8% | 67.1% | 81.8% | 0.503 | 0.516 | 0.490 |
| Mevkiye özel | Lig içi percentile | Pearson | 35.6% | 67.8% | 82.0% | 0.502 | 0.514 | 0.491 |
| Rastgele sıralama |  |  | 2.0% | 9.8% | 19.6% | 0.087 | 0.086 | 0.088 |

### Havuz: tüm ligler

| Feature seti | Normalizasyon | Metrik | R@1 | R@5 | R@10 | MRR | MRR 23/24 → 24/25 | MRR 24/25 → 25/26 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Ortak (tüm alanlar) | Per-90 z-skor | Cosine | 27.5% | 49.9% | 60.1% | 0.384 | 0.402 | 0.365 |
| Ortak (tüm alanlar) | Per-90 z-skor | Pearson | 27.4% | 49.4% | 60.3% | 0.382 | 0.395 | 0.370 |
| Ortak (tüm alanlar) | Ligler arası percentile | Öklid | 26.0% | 49.3% | 59.7% | 0.374 | 0.397 | 0.351 |
| Ortak (tüm alanlar) | Lig içi percentile | Öklid | 24.5% | 48.8% | 60.3% | 0.366 | 0.355 | 0.376 |
| Ortak (tüm alanlar) | Lig içi percentile | Cosine | 24.8% | 48.5% | 59.2% | 0.364 | 0.353 | 0.375 |
| Ortak (tüm alanlar) | Per-90 z-skor | Öklid | 25.7% | 47.4% | 57.8% | 0.362 | 0.382 | 0.342 |
| Ortak (tüm alanlar) | Ligler arası percentile | Cosine | 24.1% | 47.3% | 58.8% | 0.356 | 0.380 | 0.333 |
| Ortak (tüm alanlar) | Lig içi percentile | Pearson | 23.4% | 47.4% | 57.9% | 0.347 | 0.337 | 0.358 |
| Ortak (tüm alanlar) | Ligler arası percentile | Pearson | 23.4% | 46.1% | 57.7% | 0.346 | 0.364 | 0.328 |
| Mevkiye özel | Per-90 z-skor | Cosine | 21.8% | 44.5% | 56.0% | 0.329 | 0.343 | 0.314 |
| Mevkiye özel | Per-90 z-skor | Öklid | 20.9% | 43.9% | 55.4% | 0.323 | 0.337 | 0.308 |
| Mevkiye özel | Ligler arası percentile | Öklid | 20.3% | 43.3% | 57.1% | 0.317 | 0.329 | 0.305 |
| Mevkiye özel | Ligler arası percentile | Cosine | 20.2% | 42.7% | 54.7% | 0.311 | 0.325 | 0.297 |
| Mevkiye özel | Per-90 z-skor | Pearson | 19.8% | 42.4% | 53.3% | 0.309 | 0.328 | 0.291 |
| Mevkiye özel | Lig içi percentile | Öklid | 19.1% | 40.2% | 53.9% | 0.301 | 0.312 | 0.291 |
| Mevkiye özel | Ligler arası percentile | Pearson | 19.3% | 40.1% | 51.5% | 0.300 | 0.311 | 0.290 |
| Mevkiye özel (mevcut) | Lig içi percentile | Cosine | 18.6% | 40.5% | 51.4% | 0.295 | 0.312 | 0.279 |
| Mevkiye özel | Lig içi percentile | Pearson | 18.1% | 38.3% | 48.9% | 0.283 | 0.296 | 0.271 |
| Rastgele sıralama |  |  | 0.3% | 1.6% | 3.3% | 0.020 | 0.020 | 0.021 |

### Bulgular

MRR farkları mevcut yönteme göre verilmiştir; köşeli parantezler eşleştirilmiş bootstrap ile %95 güven aralığıdır.

- **Feature seti en etkili parametre.** 45 alanın hepsini kullanmak mevkiye özel sete göre lig içi havuzda
  +0.048 [+0.034, +0.062], tüm-lig havuzunda +0.069 MRR kazandırıyor. İki sezon çiftinde de aynı yönde;
  12 mevki grubu × sezon çifti hücresinin 11'inde iyileşme var.
- **Normalizasyon, lig etkisi ayıklanınca fark yaratmıyor.** Ortak sette lig içi percentile (Öklid) ile per-90
  z-skor (cosine) arasındaki fark +0.007 [−0.007, +0.020]. Per-90'ın tüm-lig havuzundaki üstünlüğü lig parmak
  izinden geliyor. Ligler arası aramada bu bir kusur: Premier League'deki bir oyuncu için Eredivisie'de aday
  ararken lig seviyesi farkı benzerliği bozar. Bu yüzden lig içi percentile korunmalı.
- **Metrik ikincil.** Ortak sette Öklid, cosine'den biraz iyi: +0.012 [+0.002, +0.022]. Pearson, 6
  feature seti × normalizasyon kombinasyonunun 5'inde en zayıf seçenek.
- **Rastgeleye göre çok iyi, ama zor durumlar var.** Mevcut yöntemde hedef, lig içi havuzda %83 oranla ilk 10'da
  (rastgele %20). Buna karşın lig ya da takım değiştiren oyuncularda MRR 0.52'den ~0.40'a düşüyor; profilin bir
  kısmı oyuncudan değil takımın oyun tarzından geliyor. En zor gruplar stoper ve kaleci.

Mevki grubu ve lig/takım değişikliği kırılımları: [`results/retrieval_eval.md`](results/retrieval_eval.md).

### Testin sınırları

- Test benzerliği değil **kimliğin sezonlar arası kararlılığını** ölçüyor. Daha çok alan kimliği her zaman daha
  iyi ayırt eder; bu, o alanların "benzer oyuncu" açısından anlamlı olduğunu garanti etmez.
- Mevki, çekim anındaki güncel profilden geliyor ve iki sezonda da aynı kabul ediliyor. Mevki değiştiren oyuncu
  (örn. kanattan beke geçen) yanlış grupta aranabilir.
- TFF 1. Lig'de xG/xA yok. Bu iki alan TFF oyuncuları için nötr sayılıyor; TFF oyuncusu bu iki istatistikte
  başka liglerle karşılaştırılamıyor.
