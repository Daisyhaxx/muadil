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
python -m src.eval.history_eval --out results/history_eval.md   # çok sezonlu profil
```

## Yöntem

1. Sayım istatistikleri 90 dakikaya bölünür (oran alanları olduğu gibi kalır). 900 dakikanın altı elenir.
2. Her istatistik aynı lig-sezon + mevki grubu içinde percentile'a çevrilir.
3. Arama aynı mevki grubundaki oyuncular arasında, 43 stil alanının tamamıyla yapılır. Saha oyuncularında kaleciye
   özgü 8 alan çıkarılır, geriye 35 alan kalır (`search_fields_for`, `src/features/feature_sets.py`).
4. Vektörler her sezonun kendi mevki grubunda standardize edilir. **Profil iki sezonluktur**: güncel sezon ve bir
   önceki sezonun dakika ağırlıklı ortalaması, önceki sezon yarım ağırlıkla (ağırlık = dakika × 0,5). Önceki sezonda
   aynı mevki grubunda 900+ dk'sı olmayanın profili sadece güncel sezondur (`src/similarity/profile.py`).
5. Benzerlik Öklid uzaklığından hesaplanır: **benzerlik = 1 − d² / (2n)** (n = alan sayısı). Rastgele iki oyuncu
   için ≈ 0, aynı profil için 1; ölçek cosine'e yakın.
6. Benzerlik istatistik bazında katkılara ayrılır (katkılar toplamı = benzerlik). "Ortak yönler" ikisinin de
   ortalamadan aynı yöne belirgin şekilde ayrıştığı istatistikler, "farklar" aralarındaki açığın en büyük olduğu
   istatistikler. Radar, mevkiye özel 12–20 alanlık seti gösterir (`fields_for`); percentile'lar da iki sezonun
   aynı ağırlıklı ortalamasıdır.

Bir alan lig-sezonda hiç gelmiyorsa "veri yok" sayılır: percentile'ı boş kalır, o oyuncu çifti için benzerlik
hesabında atlanır (n o kadar küçülür), radarda çizilmez. Örnekler: TFF 1. Lig'de xG/xA hiç yok; `outfielderBlocks`
24/25'te hiçbir ligde yok. İki sezonluk profilde eksik alan diğer sezondan gelir. Oyuncu bazında gelmeyen sayım
alanı ise 0'dır (örn. şutu olmayanın xG'si).

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
| Ortak (tüm alanlar) | Lig içi percentile | Öklid | 44.3% | 74.1% | 86.0% | 0.581 | 0.598 | 0.564 |
| Ortak (tüm alanlar) | Ligler arası percentile | Öklid | 43.7% | 74.5% | 86.0% | 0.577 | 0.597 | 0.558 |
| Ortak (tüm alanlar) | Per-90 z-skor | Cosine | 44.0% | 73.2% | 85.4% | 0.575 | 0.583 | 0.566 |
| Ortak − kaleci alanları (mevcut) | Lig içi percentile | Öklid | 43.2% | 73.9% | 85.7% | 0.573 | 0.590 | 0.556 |
| Ortak − kaleci alanları | Ligler arası percentile | Öklid | 43.1% | 74.2% | 85.5% | 0.572 | 0.587 | 0.557 |
| Ortak (tüm alanlar) | Per-90 z-skor | Pearson | 43.5% | 72.6% | 85.1% | 0.570 | 0.581 | 0.559 |
| Ortak (tüm alanlar) | Lig içi percentile | Cosine | 43.3% | 72.3% | 84.3% | 0.569 | 0.577 | 0.561 |
| Ortak − kaleci alanları | Per-90 z-skor | Cosine | 43.4% | 72.4% | 85.2% | 0.569 | 0.581 | 0.558 |
| Ortak (tüm alanlar) | Ligler arası percentile | Cosine | 43.3% | 72.8% | 84.1% | 0.566 | 0.579 | 0.552 |
| Ortak − kaleci alanları | Per-90 z-skor | Pearson | 43.1% | 72.2% | 84.0% | 0.565 | 0.578 | 0.553 |
| Ortak − kaleci alanları | Lig içi percentile | Cosine | 42.4% | 72.2% | 83.7% | 0.562 | 0.572 | 0.551 |
| Ortak − kaleci alanları | Ligler arası percentile | Cosine | 42.4% | 72.5% | 84.3% | 0.562 | 0.575 | 0.549 |
| Ortak (tüm alanlar) | Lig içi percentile | Pearson | 42.0% | 72.7% | 84.5% | 0.559 | 0.568 | 0.550 |
| Ortak (tüm alanlar) | Per-90 z-skor | Öklid | 42.2% | 71.8% | 82.8% | 0.554 | 0.574 | 0.534 |
| Ortak (tüm alanlar) | Ligler arası percentile | Pearson | 41.4% | 72.2% | 83.8% | 0.552 | 0.562 | 0.542 |
| Ortak − kaleci alanları | Ligler arası percentile | Pearson | 40.7% | 72.1% | 83.3% | 0.550 | 0.565 | 0.535 |
| Ortak − kaleci alanları | Per-90 z-skor | Öklid | 41.2% | 71.6% | 82.5% | 0.547 | 0.563 | 0.531 |
| Ortak − kaleci alanları | Lig içi percentile | Pearson | 40.0% | 72.8% | 84.0% | 0.546 | 0.555 | 0.537 |
| Mevkiye özel | Ligler arası percentile | Öklid | 38.9% | 72.3% | 85.0% | 0.538 | 0.547 | 0.528 |
| Mevkiye özel | Per-90 z-skor | Cosine | 39.7% | 71.2% | 84.2% | 0.538 | 0.543 | 0.533 |
| Mevkiye özel | Lig içi percentile | Öklid | 38.6% | 72.1% | 84.2% | 0.537 | 0.544 | 0.531 |
| Mevkiye özel | Per-90 z-skor | Öklid | 38.6% | 70.3% | 82.4% | 0.529 | 0.535 | 0.523 |
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
| Ortak (tüm alanlar) | Ligler arası percentile | Öklid | 25.8% | 48.4% | 60.8% | 0.371 | 0.393 | 0.349 |
| Ortak − kaleci alanları | Per-90 z-skor | Pearson | 25.9% | 48.3% | 59.2% | 0.369 | 0.386 | 0.353 |
| Ortak (tüm alanlar) | Lig içi percentile | Cosine | 25.0% | 48.4% | 59.1% | 0.365 | 0.354 | 0.376 |
| Ortak (tüm alanlar) | Per-90 z-skor | Öklid | 25.8% | 47.1% | 56.6% | 0.362 | 0.382 | 0.342 |
| Ortak (tüm alanlar) | Lig içi percentile | Öklid | 24.1% | 48.4% | 60.2% | 0.361 | 0.352 | 0.370 |
| Ortak − kaleci alanları | Ligler arası percentile | Öklid | 24.2% | 47.7% | 60.1% | 0.357 | 0.375 | 0.340 |
| Ortak (tüm alanlar) | Ligler arası percentile | Cosine | 24.1% | 47.3% | 58.9% | 0.355 | 0.380 | 0.331 |
| Ortak − kaleci alanları | Per-90 z-skor | Öklid | 24.3% | 46.7% | 55.7% | 0.351 | 0.368 | 0.334 |
| Ortak (tüm alanlar) | Lig içi percentile | Pearson | 23.6% | 47.2% | 57.7% | 0.348 | 0.338 | 0.358 |
| Ortak − kaleci alanları | Ligler arası percentile | Cosine | 23.0% | 46.6% | 58.4% | 0.348 | 0.362 | 0.333 |
| Ortak − kaleci alanları | Ligler arası percentile | Pearson | 23.3% | 46.4% | 58.3% | 0.346 | 0.362 | 0.330 |
| Ortak (tüm alanlar) | Ligler arası percentile | Pearson | 23.0% | 46.1% | 58.0% | 0.344 | 0.362 | 0.326 |
| Ortak − kaleci alanları | Lig içi percentile | Cosine | 21.9% | 45.1% | 56.0% | 0.333 | 0.347 | 0.319 |
| Ortak − kaleci alanları (mevcut) | Lig içi percentile | Öklid | 21.5% | 45.0% | 57.2% | 0.332 | 0.351 | 0.312 |
| Mevkiye özel | Per-90 z-skor | Cosine | 21.9% | 44.1% | 56.6% | 0.329 | 0.343 | 0.315 |
| Ortak − kaleci alanları | Lig içi percentile | Pearson | 20.9% | 43.0% | 55.6% | 0.321 | 0.335 | 0.308 |
| Mevkiye özel | Per-90 z-skor | Öklid | 20.3% | 43.0% | 55.2% | 0.316 | 0.331 | 0.301 |
| Mevkiye özel | Ligler arası percentile | Cosine | 20.0% | 42.7% | 55.1% | 0.310 | 0.324 | 0.297 |
| Mevkiye özel | Ligler arası percentile | Öklid | 19.6% | 42.2% | 56.0% | 0.310 | 0.324 | 0.296 |
| Mevkiye özel | Per-90 z-skor | Pearson | 19.6% | 42.0% | 53.6% | 0.309 | 0.326 | 0.292 |
| Mevkiye özel | Ligler arası percentile | Pearson | 19.5% | 40.2% | 51.4% | 0.302 | 0.312 | 0.291 |
| Mevkiye özel | Lig içi percentile | Cosine | 18.9% | 40.2% | 51.4% | 0.297 | 0.314 | 0.279 |
| Mevkiye özel | Lig içi percentile | Öklid | 18.5% | 39.4% | 52.6% | 0.294 | 0.304 | 0.285 |
| Mevkiye özel | Lig içi percentile | Pearson | 18.2% | 38.0% | 49.0% | 0.284 | 0.297 | 0.271 |
| Rastgele sıralama |  |  | 0.3% | 1.6% | 3.3% | 0.020 | 0.020 | 0.021 |

### Bulgular

Farklar lig içi havuzda MRR farkıdır; köşeli parantezler eşleştirilmiş bootstrap ile %95 güven aralığıdır
(`run_eval` çıktısında da var).

| Karşılaştırma | Tümü (n=1961) | Aynı lig (n=1743) | Lig değiştirdi (n=218) | Aynı takım (n=1456) | Takım değiştirdi (n=505) |
|---|---:|---:|---:|---:|---:|
| Mevcut − eski (mevkiye özel · cosine) | +0.054 [+0.039, +0.069] | +0.058 [+0.043, +0.074] | +0.017 [-0.019, +0.053] | +0.063 [+0.046, +0.081] | +0.026 [-0.001, +0.053] |
| Feature seti: tüm alanlar − mevkiye özel (lig içi · cosine) | +0.049 [+0.036, +0.064] | +0.053 [+0.038, +0.067] | +0.025 [-0.016, +0.068] | +0.056 [+0.040, +0.072] | +0.031 [+0.003, +0.059] |
| Kaleci alanlarını tutmak: tüm alanlar − mevcut (Öklid) | +0.008 [+0.002, +0.013] | +0.010 [+0.004, +0.016] | -0.013 [-0.028, +0.003] | +0.013 [+0.006, +0.019] | -0.007 [-0.017, +0.004] |
| Normalizasyon: lig içi (Öklid) − per-90 z (cosine), tüm alanlar | +0.006 [-0.008, +0.020] | +0.013 [-0.002, +0.028] | -0.050 [-0.088, -0.011] | +0.021 [+0.005, +0.038] | -0.038 [-0.064, -0.011] |
| Metrik: Öklid − cosine (tüm alanlar, lig içi) | +0.012 [+0.002, +0.022] | +0.016 [+0.005, +0.026] | -0.021 [-0.047, +0.005] | +0.020 [+0.009, +0.031] | -0.012 [-0.031, +0.007] |

- **Mevcut yöntem eskisinden belirgin şekilde iyi.** Mevkiye özel set + cosine yerine 35 alan + Öklid: lig içi MRR
  0.519 → 0.573, R@10 %83 → %86. Lig/takım değiştirenlerde yön aynı ama aralık 0'ı içeriyor.
- **Feature seti en etkili parametre.** 43 alanın hepsi mevkiye özel sete göre +0.049; takım değiştirenlerde de
  anlamlı (+0.031).
- **En yüksek skor, arama için doğru seçim değil.** Kaleci alanlarını saha oyuncusunda da tutmak MRR'ı +0.008
  artırıyor, ama kazanç sadece aynı takımda kalanlarda (+0.013); takım değiştirenlerde −0.007. Bu alanlar oyuncuyu
  değil takımı tanıyor (`goalsConceded`), bu yüzden aramada kullanılmıyor.
- **Normalizasyon: genelde fark yok, ama lig değiştirenlerde per-90 daha iyi.** Tüm sorgularda lig içi percentile
  ile per-90 z-skor arasındaki fark +0.006 [−0.008, +0.020]. Fakat lig değiştirenlerde per-90 +0.050, takım
  değiştirenlerde +0.038 daha iyi; aynı takımda kalanlarda ise lig içi percentile +0.021 daha iyi. Ligler arası
  arama ürünün ana senaryolarından biri olduğu için bu ayrıca incelenecek (ROADMAP). Not: tüm-lig havuzunda
  per-90'ın öne çıkması büyük ölçüde lig parmak izinden.
- **Metrik ikincil.** Öklid cosine'den biraz iyi (+0.012), farkın tamamı aynı takımda kalanlardan geliyor. Pearson,
  9 feature seti × normalizasyon kombinasyonunun 7'sinde en zayıf seçenek.
- **Zor durumlar.** Lig ya da takım değiştiren oyuncularda MRR 0.57'den ~0.43'e düşüyor; profilin bir kısmı
  oyuncudan değil takımın oyun tarzından geliyor. En zor gruplar stoper (0.49) ve kaleci (0.46).

### Çok sezonlu profil

Sorgu profili sezon N ile N−1'in ağırlıklı ortalaması, hedef N+1 (tek sezon; hedefin profiline N girmez, sızıntı
olmasın diye). 3 sezon verisiyle test edilebilen tek çift 24/25 → 25/26 (geçmiş: 23/24). Çıktı:
[`results/history_eval.md`](results/history_eval.md).

| Profil | R@1 | R@5 | R@10 | MRR | Fark: Tümü (n=983) | Fark: Geçmişi olan (n=592) | Fark: Geçmişi olan · takım değiştirdi (n=171) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Tek sezon (mevcut) | 40.8% | 72.4% | 84.7% | 0.556 | — | — | — |
| Çok sezon · sadece dakika ağırlıklı | 43.9% | 76.0% | 86.6% | 0.584 | +0.028 [+0.014, +0.042] | +0.046 [+0.023, +0.069] | +0.070 [+0.028, +0.112] |
| Çok sezon · önceki sezon ×0.5 | 44.6% | 75.3% | 86.4% | 0.586 | +0.030 [+0.019, +0.041] | +0.050 [+0.032, +0.068] | +0.047 [+0.017, +0.077] |
| Çok sezon · önceki sezon ×0.25 | 43.4% | 74.6% | 86.0% | 0.579 | +0.023 [+0.015, +0.031] | +0.038 [+0.025, +0.052] | +0.030 [+0.011, +0.051] |

- İki sezonluk profil tek sezondan iyi: önceki sezon ×0,5 ile +0.030 [+0.019, +0.041]; geçmişi olan oyuncularda
  +0.050, geçmişi olup takım değiştirenlerde +0.047. Arama bu ayarla çalışıyor.
- ×1 ile ×0,5 arasındaki fark gürültü düzeyinde. ×0,5 seçildi çünkü genelde biraz önde ve güncel formu daha çok
  yansıtıyor; takım değiştirenlerde ×1 biraz daha iyi (+0.070).
- 3 sezonluk profil test edilmedi (22/23 verisi yok).
- Kullanımda adayların profili de iki sezonluk. Test sadece sorgu tarafını ölçüyor (aday tarafında N+1'in
  geçmişi N olurdu, bu da sızıntı demek). Aday tarafında da aynı kazancın olduğu varsayılıyor.

### Testin sınırları

- Test benzerliği değil **kimliğin sezonlar arası kararlılığını** ölçüyor. Daha çok alan kimliği her zaman daha
  iyi ayırt eder; bu, o alanların "benzer oyuncu" açısından anlamlı olduğunu garanti etmez.
- Mevki, çekim anındaki güncel profilden geliyor ve iki sezonda da aynı kabul ediliyor. Mevki değiştiren oyuncu
  (örn. kanattan beke geçen) yanlış grupta aranabilir.
- TFF 1. Lig'de xG/xA yok. TFF oyuncusu içeren karşılaştırmalarda bu iki alan atlanıyor; profil iki alan eksik
  bilgiyle kuruluyor.
