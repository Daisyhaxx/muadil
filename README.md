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

## Değerlendirme

Hazır bir "doğru cevap" yok. Bu yüzden şu test kullanılıyor: oyuncunun **sezon N** profiliyle arama yapılır ve
aynı oyuncunun **sezon N+1** kaydının kaçıncı sırada çıktığına bakılır.

- Sorgu: iki sezonda da 900+ dk oynamış oyuncu. 23/24 → 24/25 ve 24/25 → 25/26 çiftlerinde toplam 1961 sorgu var.
- Aday havuzu: N+1'deki aynı mevki grubundaki herkes (ortalama ~350 oyuncu). Sorgunun N kaydı havuzda yok.
- Metrikler: recall@k (hedef ilk k içinde mi), MRR (1/sıra ortalaması).
- Karşılaştırılan boyutlar: feature seti (mevkiye özel / 45 alanın tamamı) × normalizasyon (lig içi percentile /
  ligler arası percentile / per-90 z-skor) × metrik (cosine / Pearson / Öklid). Toplam 18 yöntem.

**Neden iki ayrı havuz?** Ligler arası percentile ve per-90 z-skor, ligin genel seviyesini vektörün içinde tutuyor.
Örneğin TFF 1. Lig'de xG verisi yok; TFF oyuncusunun xG'si 0 olduğu için otomatik olarak yalnızca TFF'lilere yakın
düşüyor. Oyuncuların %89'u ligini değiştirmediğinden, tüm-lig havuzu bu "lig parmak izini" oyun tarzı benzerliği
gibi ödüllendiriyor. Havuzu hedefin ligiyle sınırlamak bu etkiyi ortadan kaldırıyor, bu yüzden adil karşılaştırma
o tablo.

### Havuz: sadece hedefin ligi (adil karşılaştırma)

| Feature seti | Normalizasyon | Metrik | R@1 | R@5 | R@10 | MRR | MRR 23/24 → 24/25 | MRR 24/25 → 25/26 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Ortak (tüm alanlar) | Lig içi percentile | Öklid | 43.9% | 73.9% | 85.6% | 0.577 | 0.598 | 0.556 |
| Ortak (tüm alanlar) | Ligler arası percentile | Öklid | 43.6% | 74.1% | 86.1% | 0.576 | 0.596 | 0.555 |
| Ortak (tüm alanlar) | Per-90 z-skor | Cosine | 44.0% | 73.4% | 85.5% | 0.575 | 0.583 | 0.567 |
| Ortak (tüm alanlar) | Per-90 z-skor | Pearson | 43.8% | 73.0% | 85.4% | 0.571 | 0.583 | 0.560 |
| Ortak (tüm alanlar) | Ligler arası percentile | Cosine | 43.2% | 73.2% | 84.2% | 0.566 | 0.580 | 0.552 |
| Ortak (tüm alanlar) | Lig içi percentile | Cosine | 42.5% | 72.3% | 84.0% | 0.563 | 0.577 | 0.550 |
| Ortak (tüm alanlar) | Per-90 z-skor | Öklid | 42.3% | 71.6% | 82.3% | 0.554 | 0.575 | 0.534 |
| Ortak (tüm alanlar) | Lig içi percentile | Pearson | 40.7% | 72.3% | 84.1% | 0.550 | 0.563 | 0.537 |
| Ortak (tüm alanlar) | Ligler arası percentile | Pearson | 41.1% | 71.7% | 83.9% | 0.550 | 0.563 | 0.537 |
| Mevkiye özel | Per-90 z-skor | Cosine | 39.7% | 72.1% | 84.5% | 0.541 | 0.549 | 0.532 |
| Mevkiye özel | Lig içi percentile | Öklid | 38.4% | 71.7% | 84.1% | 0.534 | 0.542 | 0.525 |
| Mevkiye özel | Ligler arası percentile | Öklid | 38.2% | 72.1% | 84.4% | 0.534 | 0.544 | 0.523 |
| Mevkiye özel | Per-90 z-skor | Öklid | 38.5% | 70.4% | 82.3% | 0.529 | 0.533 | 0.525 |
| Mevkiye özel | Ligler arası percentile | Cosine | 37.6% | 70.1% | 83.7% | 0.524 | 0.534 | 0.514 |
| Mevkiye özel | Per-90 z-skor | Pearson | 38.1% | 69.5% | 82.4% | 0.523 | 0.535 | 0.510 |
| Mevkiye özel (mevcut) | Lig içi percentile | Cosine | 36.9% | 70.0% | 82.8% | 0.517 | 0.527 | 0.507 |
| Mevkiye özel | Ligler arası percentile | Pearson | 35.8% | 67.6% | 82.1% | 0.506 | 0.520 | 0.492 |
| Mevkiye özel | Lig içi percentile | Pearson | 35.4% | 67.8% | 82.0% | 0.500 | 0.512 | 0.488 |
| Rastgele sıralama |  |  | 2.0% | 9.8% | 19.6% | 0.087 | 0.086 | 0.088 |

### Havuz: tüm ligler

| Feature seti | Normalizasyon | Metrik | R@1 | R@5 | R@10 | MRR | MRR 23/24 → 24/25 | MRR 24/25 → 25/26 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Ortak (tüm alanlar) | Per-90 z-skor | Cosine | 28.3% | 51.3% | 61.8% | 0.395 | 0.411 | 0.379 |
| Ortak (tüm alanlar) | Per-90 z-skor | Pearson | 28.4% | 50.9% | 62.0% | 0.393 | 0.405 | 0.382 |
| Ortak (tüm alanlar) | Ligler arası percentile | Öklid | 27.4% | 51.6% | 62.4% | 0.388 | 0.411 | 0.366 |
| Ortak (tüm alanlar) | Per-90 z-skor | Öklid | 26.6% | 49.3% | 59.9% | 0.376 | 0.395 | 0.357 |
| Ortak (tüm alanlar) | Ligler arası percentile | Cosine | 25.1% | 49.1% | 61.0% | 0.369 | 0.390 | 0.348 |
| Ortak (tüm alanlar) | Lig içi percentile | Öklid | 24.5% | 47.7% | 59.8% | 0.363 | 0.350 | 0.376 |
| Ortak (tüm alanlar) | Lig içi percentile | Cosine | 24.3% | 47.9% | 59.2% | 0.361 | 0.355 | 0.367 |
| Ortak (tüm alanlar) | Ligler arası percentile | Pearson | 24.6% | 48.3% | 60.0% | 0.360 | 0.379 | 0.341 |
| Mevkiye özel | Per-90 z-skor | Cosine | 22.6% | 46.5% | 58.6% | 0.343 | 0.357 | 0.328 |
| Ortak (tüm alanlar) | Lig içi percentile | Pearson | 22.6% | 46.5% | 57.7% | 0.341 | 0.336 | 0.346 |
| Mevkiye özel | Per-90 z-skor | Öklid | 22.1% | 45.7% | 57.3% | 0.336 | 0.349 | 0.324 |
| Mevkiye özel | Ligler arası percentile | Öklid | 21.0% | 45.9% | 58.7% | 0.330 | 0.342 | 0.317 |
| Mevkiye özel | Per-90 z-skor | Pearson | 21.2% | 43.9% | 55.6% | 0.325 | 0.342 | 0.307 |
| Mevkiye özel | Ligler arası percentile | Cosine | 20.4% | 44.6% | 57.5% | 0.322 | 0.338 | 0.306 |
| Mevkiye özel | Ligler arası percentile | Pearson | 20.7% | 42.6% | 54.0% | 0.315 | 0.327 | 0.302 |
| Mevkiye özel | Lig içi percentile | Öklid | 19.1% | 39.7% | 52.9% | 0.298 | 0.309 | 0.288 |
| Mevkiye özel (mevcut) | Lig içi percentile | Cosine | 18.6% | 40.1% | 50.7% | 0.293 | 0.310 | 0.276 |
| Mevkiye özel | Lig içi percentile | Pearson | 18.2% | 37.5% | 48.2% | 0.281 | 0.296 | 0.267 |
| Rastgele sıralama |  |  | 0.3% | 1.6% | 3.3% | 0.020 | 0.020 | 0.021 |

### Bulgular

MRR farkları mevcut yönteme göre verilmiştir; köşeli parantezler eşleştirilmiş bootstrap ile %95 güven aralığıdır.

- **Feature seti en etkili parametre.** 45 alanın hepsini kullanmak mevkiye özel sete göre lig içi havuzda
  +0.047 [+0.032, +0.061], tüm-lig havuzunda +0.068 MRR kazandırıyor. İki sezon çiftinde de aynı yönde;
  12 mevki grubu × sezon çifti hücresinin 11'inde iyileşme var.
- **Normalizasyon, lig etkisi ayıklanınca fark yaratmıyor.** Ortak sette lig içi percentile (Öklid) ile per-90
  z-skor (cosine) arasındaki fark +0.002 [−0.011, +0.015]. Per-90'ın tüm-lig havuzundaki üstünlüğü lig parmak
  izinden geliyor. Ligler arası aramada bu bir kusur: Premier League'deki bir oyuncu için Eredivisie'de aday
  ararken lig seviyesi farkı benzerliği bozar. Bu yüzden lig içi percentile korunmalı.
- **Metrik ikincil.** Ortak sette Öklid, cosine'den biraz iyi: +0.014 [+0.004, +0.023]. Pearson her
  kombinasyonda en zayıf seçenek.
- **Rastgeleye göre çok iyi, ama zor durumlar var.** Mevcut yöntemde hedef, lig içi havuzda %83 oranla ilk 10'da
  (rastgele %20). Buna karşın lig ya da takım değiştiren oyuncularda MRR 0.52'den ~0.40'a düşüyor; profilin bir
  kısmı oyuncudan değil takımın oyun tarzından geliyor. En zor gruplar stoper ve kaleci.

Mevki grubu ve lig/takım değişikliği kırılımları: [`results/retrieval_eval.md`](results/retrieval_eval.md).

### Testin sınırları

- Test benzerliği değil **kimliğin sezonlar arası kararlılığını** ölçüyor. Daha çok alan kimliği her zaman daha
  iyi ayırt eder; bu, o alanların "benzer oyuncu" açısından anlamlı olduğunu garanti etmez.
- Mevki, çekim anındaki güncel profilden geliyor ve iki sezonda da aynı kabul ediliyor. Mevki değiştiren oyuncu
  (örn. kanattan beke geçen) yanlış grupta aranabilir.
- TFF 1. Lig'de xG/xA yok; 0 sayılıyor.
