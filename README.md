# Benzer Oyuncu Bulucu

Bir futbolcunun istatistik profiline en çok benzeyen oyuncuları bulur. Filtreler: yaş, lig, piyasa değeri, sözleşme, ayak.
Örnek: "Süper Lig'de şu forvete en benzer 23 yaş altı oyuncu kim?"

Veri: Sofascore. 6 lig (Süper Lig, TFF 1. Lig, Premier League, Eredivisie, Primeira Liga, Belçika Pro League) ×
3 sezon (23/24, 24/25, 25/26). Lig-sezon başına ~400–500 oyuncu var, bunların 900+ dakika oynayanları kullanılıyor.
Ham veri repoda yok; burada sadece kod ve türetilmiş sonuçlar paylaşılıyor.

Yol haritası ve ilerleme: [`ROADMAP.md`](ROADMAP.md).

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
3. Arama aynı mevki grubundaki oyuncular arasında, 43 stil alanının tamamıyla yapılır. Saha oyuncularında kaleciye
   özgü 8 alan çıkarılır, geriye 35 alan kalır (`search_fields_for`, `src/features/feature_sets.py`).
4. Vektörler standardize edilir, benzerlik Öklid uzaklığından hesaplanır: **benzerlik = 1 − d² / (2n)**
   (n = alan sayısı). Rastgele iki oyuncu için ≈ 0, aynı profil için 1; ölçek cosine'e yakın.
5. Benzerlik istatistik bazında katkılara ayrılır (katkılar toplamı = benzerlik). "Ortak yönler" ikisinin de
   ortalamadan aynı yöne belirgin şekilde ayrıştığı istatistikler, "farklar" aralarındaki açığın en büyük olduğu
   istatistikler. Radar, mevkiye özel 12–20 alanlık seti gösterir (`fields_for`).

Bir alan lig-sezonda hiç gelmiyorsa (TFF 1. Lig'de xG/xA) "veri yok" sayılır: percentile'ı boş kalır, o oyuncu
çifti için benzerlik hesabında atlanır (n o kadar küçülür), radarda çizilmez. Oyuncu bazında gelmeyen sayım alanı
ise 0'dır (örn. şutu olmayanın xG'si).

**Neden saha oyuncusunda kaleci alanları yok?** `goalsConceded` saha oyuncusu için "sahadayken yenen gol" demek;
oyun tarzını değil takımın savunmasını ölçer. Değerlendirmede aynı takımda kalanları bulmayı kolaylaştırıyor ama
takım değiştirenlerde işe yaramıyor (aşağıda, Bulgular). Diğer kaleci alanları saha oyuncusunda neredeyse hep 0.

## Değerlendirme

Hazır bir "doğru cevap" yok. Bu yüzden şu test kullanılıyor: oyuncunun **sezon N** profiliyle arama yapılır ve
aynı oyuncunun **sezon N+1** kaydının kaçıncı sırada çıktığına bakılır.

- Sorgu: iki sezonda da 900+ dk oynamış oyuncu. 23/24 → 24/25 ve 24/25 → 25/26 çiftlerinde toplam 1961 sorgu var.
- Aday havuzu: N+1'deki aynı mevki grubundaki herkes (ortalama ~350 oyuncu). Sorgunun N kaydı havuzda yok.
- Metrikler: recall@k (hedef ilk k içinde mi), MRR (1/sıra ortalaması).
- Karşılaştırılan boyutlar: feature seti (mevkiye özel / 43 alanın tamamı / 43 − kaleci alanları) × normalizasyon
  (lig içi percentile / ligler arası percentile / per-90 z-skor) × metrik (cosine / Pearson / Öklid). Toplam 27 yöntem.

**Neden iki ayrı havuz?** Ligler arası percentile ve per-90 z-skor, ligin genel seviyesini vektörün içinde tutuyor.
Örneğin bir ligde oyuncular genel olarak daha çok pas yapıyorsa, o ligin bütün oyuncuları pas eksenlerinde yüksek
görünür ve birbirine yakın düşer. Oyuncuların %89'u ligini değiştirmediğinden, tüm-lig havuzu bu "lig parmak izini"
oyun tarzı benzerliği gibi ödüllendiriyor. Havuzu hedefin ligiyle sınırlamak bu etkiyi ortadan kaldırıyor, bu yüzden adil karşılaştırma
o tablo.

### Havuz: sadece hedefin ligi (adil karşılaştırma)

| Feature seti | Normalizasyon | Metrik | R@1 | R@5 | R@10 | MRR | MRR 23/24 → 24/25 | MRR 24/25 → 25/26 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Ortak (tüm alanlar) | Lig içi percentile | Öklid | 44.3% | 74.0% | 86.2% | 0.580 | 0.598 | 0.562 |
| Ortak (tüm alanlar) | Ligler arası percentile | Öklid | 43.5% | 74.1% | 85.9% | 0.575 | 0.597 | 0.553 |
| Ortak (tüm alanlar) | Per-90 z-skor | Cosine | 44.0% | 73.2% | 85.4% | 0.575 | 0.583 | 0.566 |
| Ortak − kaleci alanları (mevcut) | Lig içi percentile | Öklid | 43.2% | 74.0% | 85.7% | 0.573 | 0.590 | 0.555 |
| Ortak − kaleci alanları | Ligler arası percentile | Öklid | 43.0% | 73.9% | 85.7% | 0.571 | 0.587 | 0.554 |
| Ortak (tüm alanlar) | Per-90 z-skor | Pearson | 43.5% | 72.6% | 85.1% | 0.570 | 0.581 | 0.559 |
| Ortak (tüm alanlar) | Lig içi percentile | Cosine | 43.3% | 72.3% | 84.3% | 0.569 | 0.577 | 0.561 |
| Ortak − kaleci alanları | Per-90 z-skor | Cosine | 43.4% | 72.4% | 85.2% | 0.569 | 0.581 | 0.558 |
| Ortak (tüm alanlar) | Ligler arası percentile | Cosine | 43.3% | 72.8% | 84.1% | 0.566 | 0.579 | 0.552 |
| Ortak − kaleci alanları | Per-90 z-skor | Pearson | 43.1% | 72.2% | 84.0% | 0.565 | 0.578 | 0.553 |
| Ortak − kaleci alanları | Lig içi percentile | Cosine | 42.4% | 72.2% | 83.7% | 0.562 | 0.572 | 0.551 |
| Ortak − kaleci alanları | Ligler arası percentile | Cosine | 42.4% | 72.5% | 84.3% | 0.562 | 0.575 | 0.549 |
| Ortak (tüm alanlar) | Lig içi percentile | Pearson | 42.0% | 72.7% | 84.5% | 0.559 | 0.568 | 0.550 |
| Ortak (tüm alanlar) | Per-90 z-skor | Öklid | 42.1% | 71.9% | 82.3% | 0.553 | 0.574 | 0.533 |
| Ortak (tüm alanlar) | Ligler arası percentile | Pearson | 41.4% | 72.2% | 83.8% | 0.552 | 0.562 | 0.542 |
| Ortak − kaleci alanları | Ligler arası percentile | Pearson | 40.7% | 72.1% | 83.3% | 0.550 | 0.565 | 0.535 |
| Ortak − kaleci alanları | Lig içi percentile | Pearson | 40.0% | 72.8% | 84.0% | 0.546 | 0.555 | 0.537 |
| Ortak − kaleci alanları | Per-90 z-skor | Öklid | 41.1% | 71.2% | 82.0% | 0.546 | 0.563 | 0.529 |
| Mevkiye özel | Per-90 z-skor | Cosine | 39.7% | 71.2% | 84.2% | 0.538 | 0.543 | 0.533 |
| Mevkiye özel | Lig içi percentile | Öklid | 38.7% | 72.2% | 84.3% | 0.537 | 0.544 | 0.531 |
| Mevkiye özel | Ligler arası percentile | Öklid | 38.8% | 72.3% | 84.7% | 0.537 | 0.547 | 0.527 |
| Mevkiye özel | Per-90 z-skor | Öklid | 38.4% | 70.2% | 82.2% | 0.528 | 0.535 | 0.521 |
| Mevkiye özel | Ligler arası percentile | Cosine | 38.3% | 69.2% | 83.6% | 0.526 | 0.536 | 0.517 |
| Mevkiye özel | Lig içi percentile | Cosine | 37.2% | 69.4% | 83.3% | 0.519 | 0.529 | 0.510 |
| Mevkiye özel | Per-90 z-skor | Pearson | 37.6% | 68.7% | 82.6% | 0.519 | 0.527 | 0.510 |
| Mevkiye özel | Ligler arası percentile | Pearson | 36.1% | 67.4% | 82.0% | 0.507 | 0.520 | 0.494 |
| Mevkiye özel | Lig içi percentile | Pearson | 35.5% | 68.0% | 82.4% | 0.503 | 0.516 | 0.490 |
| Rastgele sıralama |  |  | 2.0% | 9.8% | 19.6% | 0.087 | 0.086 | 0.088 |

### Havuz: tüm ligler

| Feature seti | Normalizasyon | Metrik | R@1 | R@5 | R@10 | MRR | MRR 23/24 → 24/25 | MRR 24/25 → 25/26 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Ortak (tüm alanlar) | Per-90 z-skor | Cosine | 27.6% | 49.9% | 60.2% | 0.384 | 0.403 | 0.365 |
| Ortak (tüm alanlar) | Per-90 z-skor | Pearson | 27.4% | 49.2% | 60.4% | 0.382 | 0.395 | 0.368 |
| Ortak − kaleci alanları | Per-90 z-skor | Cosine | 26.7% | 48.9% | 59.9% | 0.376 | 0.392 | 0.360 |
| Ortak − kaleci alanları | Per-90 z-skor | Pearson | 25.9% | 48.3% | 59.2% | 0.369 | 0.386 | 0.353 |
| Ortak (tüm alanlar) | Ligler arası percentile | Öklid | 25.3% | 48.5% | 59.9% | 0.367 | 0.393 | 0.342 |
| Ortak (tüm alanlar) | Lig içi percentile | Cosine | 25.0% | 48.4% | 59.1% | 0.365 | 0.354 | 0.376 |
| Ortak (tüm alanlar) | Lig içi percentile | Öklid | 24.2% | 48.0% | 60.0% | 0.362 | 0.352 | 0.371 |
| Ortak (tüm alanlar) | Per-90 z-skor | Öklid | 25.5% | 46.9% | 56.6% | 0.359 | 0.382 | 0.336 |
| Ortak − kaleci alanları | Ligler arası percentile | Öklid | 23.9% | 47.3% | 59.4% | 0.356 | 0.375 | 0.337 |
| Ortak (tüm alanlar) | Ligler arası percentile | Cosine | 24.1% | 47.3% | 58.9% | 0.355 | 0.380 | 0.331 |
| Ortak − kaleci alanları | Per-90 z-skor | Öklid | 24.4% | 46.3% | 55.7% | 0.350 | 0.368 | 0.333 |
| Ortak (tüm alanlar) | Lig içi percentile | Pearson | 23.6% | 47.2% | 57.7% | 0.348 | 0.338 | 0.358 |
| Ortak − kaleci alanları | Ligler arası percentile | Cosine | 23.0% | 46.6% | 58.4% | 0.348 | 0.362 | 0.333 |
| Ortak − kaleci alanları | Ligler arası percentile | Pearson | 23.3% | 46.4% | 58.3% | 0.346 | 0.362 | 0.330 |
| Ortak (tüm alanlar) | Ligler arası percentile | Pearson | 23.0% | 46.1% | 58.0% | 0.344 | 0.362 | 0.326 |
| Ortak − kaleci alanları | Lig içi percentile | Cosine | 21.9% | 45.1% | 56.0% | 0.333 | 0.347 | 0.319 |
| Mevkiye özel | Per-90 z-skor | Cosine | 21.9% | 44.1% | 56.6% | 0.329 | 0.343 | 0.315 |
| Ortak − kaleci alanları (mevcut) | Lig içi percentile | Öklid | 21.1% | 45.2% | 57.2% | 0.329 | 0.351 | 0.308 |
| Ortak − kaleci alanları | Lig içi percentile | Pearson | 20.9% | 43.0% | 55.6% | 0.321 | 0.335 | 0.308 |
| Mevkiye özel | Per-90 z-skor | Öklid | 20.4% | 42.8% | 55.2% | 0.315 | 0.331 | 0.300 |
| Mevkiye özel | Ligler arası percentile | Cosine | 20.0% | 42.7% | 55.1% | 0.310 | 0.324 | 0.297 |
| Mevkiye özel | Ligler arası percentile | Öklid | 19.7% | 42.3% | 56.0% | 0.310 | 0.324 | 0.297 |
| Mevkiye özel | Per-90 z-skor | Pearson | 19.6% | 42.0% | 53.6% | 0.309 | 0.326 | 0.292 |
| Mevkiye özel | Ligler arası percentile | Pearson | 19.5% | 40.2% | 51.4% | 0.302 | 0.312 | 0.291 |
| Mevkiye özel | Lig içi percentile | Cosine | 18.9% | 40.2% | 51.4% | 0.297 | 0.314 | 0.279 |
| Mevkiye özel | Lig içi percentile | Öklid | 18.3% | 39.3% | 52.8% | 0.292 | 0.304 | 0.281 |
| Mevkiye özel | Lig içi percentile | Pearson | 18.2% | 38.0% | 49.0% | 0.284 | 0.297 | 0.271 |
| Rastgele sıralama |  |  | 0.3% | 1.6% | 3.3% | 0.020 | 0.020 | 0.021 |

### Bulgular

MRR farkları lig içi havuzdadır; köşeli parantezler eşleştirilmiş bootstrap ile %95 güven aralığıdır.

- **Yeni yöntem eskisinden belirgin şekilde iyi.** Mevkiye özel set + cosine yerine 35 alan + Öklid: lig içi MRR
  0.519 → 0.573, fark +0.053 [+0.039, +0.068]; R@10 %83 → %86. Takım değiştirenlerde +0.025 [−0.002, +0.051],
  lig değiştirenlerde +0.017 [−0.017, +0.052]: yön aynı ama örneklem küçük, anlamlı değil.
- **Feature seti en etkili parametre.** 43 alanın hepsini kullanmak mevkiye özel sete göre (lig içi percentile,
  cosine) +0.049 [+0.035, +0.064], tüm-lig havuzunda +0.068 MRR kazandırıyor. 12 mevki grubu × sezon çifti
  hücresinin 10'unda iyileşme var.
- **En yüksek skor, arama için doğru seçim değil.** Kaleci alanlarını saha oyuncusunda da tutmak (43 alan · Öklid)
  MRR'ı +0.007 [+0.002, +0.013] daha artırıyor. Ama kazanç sadece aynı takımda kalanlarda: +0.012 [+0.006, +0.019];
  takım değiştirenlerde −0.007 [−0.018, +0.003]. Bu alanlar oyuncuyu değil takımı tanıyor (`goalsConceded`),
  bu yüzden aramada kullanılmıyor.
- **Normalizasyon, lig etkisi ayıklanınca fark yaratmıyor.** Ortak sette lig içi percentile (Öklid) ile per-90
  z-skor (cosine) arasındaki fark +0.005 [−0.008, +0.019]. Per-90'ın tüm-lig havuzundaki üstünlüğü lig parmak
  izinden geliyor. Ligler arası aramada bu bir kusur: Premier League'deki bir oyuncu için Eredivisie'de aday
  ararken lig seviyesi farkı benzerliği bozar. Bu yüzden lig içi percentile korunmalı.
- **Metrik ikincil.** Ortak sette Öklid, cosine'den biraz iyi: +0.011 [+0.002, +0.021]. Pearson, 9 feature seti ×
  normalizasyon kombinasyonunun 7'sinde en zayıf seçenek.
- **Zor durumlar.** Lig ya da takım değiştiren oyuncularda MRR 0.57'den ~0.43'e düşüyor; profilin bir kısmı
  oyuncudan değil takımın oyun tarzından geliyor. En zor gruplar stoper (0.49) ve kaleci (0.46).

Mevki grubu ve lig/takım değişikliği kırılımları: [`results/retrieval_eval.md`](results/retrieval_eval.md).

### Testin sınırları

- Test benzerliği değil **kimliğin sezonlar arası kararlılığını** ölçüyor. Daha çok alan kimliği her zaman daha
  iyi ayırt eder; bu, o alanların "benzer oyuncu" açısından anlamlı olduğunu garanti etmez.
- Mevki, çekim anındaki güncel profilden geliyor ve iki sezonda da aynı kabul ediliyor. Mevki değiştiren oyuncu
  (örn. kanattan beke geçen) yanlış grupta aranabilir.
- TFF 1. Lig'de xG/xA yok. TFF oyuncusu içeren karşılaştırmalarda bu iki alan atlanıyor; profil iki alan eksik
  bilgiyle kuruluyor.
