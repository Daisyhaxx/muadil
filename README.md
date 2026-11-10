# Muadil

Bir futbolcunun muadilini istatistikle bulur: oyun profiline en çok benzeyen oyuncuları, tercihen daha genç ya da
daha ucuz olanları. Filtreler: yaş, lig, piyasa değeri, sözleşme, ayak.
Örnek: "Süper Lig'de şu forvete en benzer 23 yaş altı oyuncu kim?"

Veri: Sofascore'un oyuncu sezon istatistikleri. 6 lig (Süper Lig, TFF 1. Lig, Premier League, Eredivisie,
Primeira Liga, Belçika Pro League) × 3 sezon (23/24, 24/25, 25/26). Lig-sezon başına ~400–500 oyuncu var, bunların
450+ dakika oynayanları aranıyor; 900 dakikanın altındakiler düzeltilerek giriyor ve sonuçta "az veri" diye işaretleniyor.
**Veri ve veri çekme kodu bu repoda yok**; burada modelleme, değerlendirme,
API ve arayüz kodu ile türetilmiş sonuçlar (değerlendirme tabloları) paylaşılıyor. Beklenen veri formatı aşağıda.

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
python -m src.eval.league_eval --out results/league_eval.md     # lig farkı düzeltmesi (α)
python -m src.eval.team_eval --out results/team_eval.md         # topa sahip olma düzeltmesi (β)
python -m src.eval.shrinkage_eval --out results/shrinkage_eval.md  # az dakikalı oyuncular
```

### Veri formatı

Kod, lig-sezon başına bir parquet dosyası bekler: `~/player-data/processed/sofascore/<lig>_<yy-yy>.parquet`
(örn. `super_lig_25-26.parquet`; kök dizin `PLAYER_DATA_DIR` ortam değişkeniyle değişir, `src/paths.py`).
Oyuncu başına bir satır, sezon toplamları:

| Sütun | Açıklama |
|---|---|
| `league`, `season_year` | Kısa lig adı (`src/leagues.py`), sezon (`"25/26"`) |
| `player_id`, `player_name`, `team_id`, `team_name` | Kimlikler; takım = sezondaki takım |
| `position`, `positions_detailed` | Kaba mevki (G/D/M/F) ve detaylı mevki listesi (örn. `["MC", "DM"]`) |
| `date_of_birth`, `preferred_foot`, `market_value`, `contract_until` | Profil (filtreler için) |
| `minutesPlayed` | Sezon dakikası |
| 43 stil alanı | Sayımlar sezon toplamı, `*Percentage` alanları yüzde (`STYLE_FIELDS`, `src/features/feature_sets.py`) |

Takım tablosu, aynı adla `~/player-data/processed/sofascore_teams/` altında: takım başına bir satır, `league`,
`season_year`, `team_id` ve `averageBallPossession` (sezon ortalaması topa sahip olma, %). Oyuncu tablosuna
`league` + `season_year` + `team_id` ile bağlanır (`load_season`, `src/features/dataset.py`).

## Yöntem

1. Sayım istatistikleri 90 dakikaya bölünür (oran alanları olduğu gibi kalır). 450 dakikanın altı elenir; 450–899 dk
   oynayanların değerleri mevki ortalamasına doğru çekilir (`src/features/shrinkage.py`; aşağıda, Az dakikalı oyuncular).
   Ölçek hep 900+ dk oynayanlardan gelir, onların değerleri değişmez. **Savunma aksiyonları takımın topa sahip olma oranına göre düzeltilir:** müdahale, pas arası, uzaklaştırma,
   top kazanma vb. × (0,5 / (1 − p))^0,3 (p = takımın topa sahip olma oranı). Rakibi topu çok tutan takımın
   oyuncusu sırf bu yüzden daha çok müdahale eder. Üs 0,3 veriden ölçüldü; standart düzeltme (üs 1) etkiyi ~3 kat
   abartıyor (`src/features/team_adjust.py`; aşağıda, Takım etkisi).
2. **Lig farkı yarıya indirilir.** Sayım alanları log ölçeğine alınır (log(1 + x)). Sonra her alandan, oyuncunun
   liginin ortalaması ile tüm liglerin ortalaması arasındaki farkın yarısı çıkarılır (aynı sezon + mevki grubu içinde,
   `src/features/league_adjust.py`). Örneğin bir ligde herkes daha çok pas yapıyorsa bunun yarısı lig etkisi sayılıp
   silinir, yarısı oyuncunun profilinde kalır. Neden yarısı: aşağıda, Ligler arası arama.
3. Arama aynı mevki grubundaki oyuncular arasında, 43 stil alanının tamamıyla yapılır. Saha oyuncularında kaleciye
   özgü 8 alan çıkarılır, geriye 35 alan kalır (`search_fields_for`, `src/features/feature_sets.py`).
4. Vektörler her sezonun kendi mevki grubunda standardize edilir. **Profil iki sezonluktur**: güncel sezon ve bir
   önceki sezonun dakika ağırlıklı ortalaması, önceki sezon yarım ağırlıkla (ağırlık = dakika × 0,5). Önceki sezonda
   aynı mevki grubunda 900+ dk'sı olmayanın profili sadece güncel sezondur (`src/similarity/profile.py`).
5. **Benzerlik = cosine.** Her vektör birim uzunluğa (RMS = 1) ölçeklenir, sonra
   **benzerlik = 1 − d² / (2n)** (d = Öklid uzaklığı, n = alan sayısı); birim vektörlerde bu tam olarak cosine.
   Rastgele iki oyuncu için ≈ 0, aynı yönde profil için 1. Profilin büyüklüğü (oyuncunun ortalamadan genel olarak ne
   kadar ayrıştığı) değil yönü (tarzı) karşılaştırılır. Lig değiştiren oyuncuda büyüklük değişiyor, yön daha kararlı.
6. Benzerlik istatistik bazında katkılara ayrılır (katkılar toplamı = benzerlik). "Ortak yönler" ikisinin de
   ortalamadan aynı yöne belirgin şekilde ayrıştığı istatistikler, "farklar" aralarındaki açığın en büyük olduğu
   istatistikler. Radar, mevkiye özel 12–20 alanlık seti gösterir (`fields_for`).
   **Gösterilen sayılar lig içi percentile'dır** (aynı lig-sezon + mevki grubu, iki sezonun aynı ağırlıklı
   ortalaması); arama vektöründen ayrı, okunması kolay olsun diye.

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
  (lig içi percentile / ligler arası percentile / per-90 z-skor / log per-90, lig farkı ½) × metrik
  (cosine / Pearson / Öklid). Toplam 36 yöntem. Her normalizasyondan sonra sezon + mevki grubu içinde z-skor alınır.

**Neden iki ayrı havuz?** Ligler arası percentile ve per-90 z-skor, ligin genel seviyesini vektörün içinde tutuyor
(log per-90, lig farkı ½ yarısını tutuyor). Örneğin bir ligde oyuncular genel olarak daha çok pas yapıyorsa, o ligin
bütün oyuncuları pas eksenlerinde yüksek görünür ve birbirine yakın düşer. Oyuncuların %89'u ligini
değiştirmediğinden, tüm-lig havuzu bu "lig parmak izini" oyun tarzı benzerliği gibi ödüllendiriyor. Havuzu hedefin
ligiyle sınırlamak bu etkiyi ortadan kaldırıyor, bu yüzden adil karşılaştırma o tablo.

### Havuz: sadece hedefin ligi (adil karşılaştırma)

| Feature seti | Normalizasyon | Metrik | R@1 | R@5 | R@10 | MRR | MRR 23/24 → 24/25 | MRR 24/25 → 25/26 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Ortak (tüm alanlar) | Log per-90 + PAdj, lig farkı ½ | Pearson | 46.0% | 75.0% | 85.9% | 0.590 | 0.601 | 0.579 |
| Ortak (tüm alanlar) | Log per-90 + PAdj, lig farkı ½ | Cosine | 45.3% | 74.3% | 86.4% | 0.588 | 0.596 | 0.581 |
| Ortak − kaleci alanları (mevcut) | Log per-90 + PAdj, lig farkı ½ | Cosine | 45.1% | 73.8% | 85.8% | 0.585 | 0.589 | 0.580 |
| Ortak (tüm alanlar) | Lig içi percentile | Öklid | 44.3% | 74.1% | 86.0% | 0.581 | 0.598 | 0.564 |
| Ortak (tüm alanlar) | Log per-90 + PAdj, lig farkı ½ | Öklid | 44.8% | 74.3% | 85.0% | 0.581 | 0.601 | 0.561 |
| Ortak − kaleci alanları | Log per-90 + PAdj, lig farkı ½ | Pearson | 45.0% | 73.0% | 85.4% | 0.579 | 0.592 | 0.566 |
| Ortak (tüm alanlar) | Ligler arası percentile | Öklid | 43.7% | 74.5% | 86.0% | 0.577 | 0.597 | 0.558 |
| Ortak − kaleci alanları | Lig içi percentile | Öklid | 43.2% | 73.9% | 85.7% | 0.573 | 0.590 | 0.556 |
| Ortak (tüm alanlar) | Per-90 z-skor | Cosine | 43.7% | 73.2% | 85.3% | 0.572 | 0.583 | 0.561 |
| Ortak − kaleci alanları | Ligler arası percentile | Öklid | 43.1% | 74.2% | 85.5% | 0.572 | 0.587 | 0.557 |
| Ortak − kaleci alanları | Log per-90 + PAdj, lig farkı ½ | Öklid | 43.4% | 73.7% | 84.9% | 0.572 | 0.591 | 0.553 |
| Ortak − kaleci alanları | Per-90 z-skor | Cosine | 43.8% | 72.2% | 85.1% | 0.571 | 0.580 | 0.562 |
| Ortak (tüm alanlar) | Lig içi percentile | Cosine | 43.3% | 72.4% | 84.1% | 0.570 | 0.577 | 0.563 |
| Ortak (tüm alanlar) | Per-90 z-skor | Pearson | 43.7% | 72.8% | 84.9% | 0.570 | 0.582 | 0.559 |
| Ortak − kaleci alanları | Per-90 z-skor | Pearson | 43.5% | 72.0% | 83.8% | 0.566 | 0.578 | 0.555 |
| Ortak (tüm alanlar) | Ligler arası percentile | Cosine | 43.0% | 73.0% | 84.0% | 0.565 | 0.578 | 0.553 |
| Ortak − kaleci alanları | Ligler arası percentile | Cosine | 42.8% | 72.8% | 84.1% | 0.565 | 0.575 | 0.555 |
| Ortak − kaleci alanları | Lig içi percentile | Cosine | 42.7% | 72.4% | 83.8% | 0.564 | 0.572 | 0.556 |
| Ortak (tüm alanlar) | Lig içi percentile | Pearson | 41.6% | 72.5% | 84.2% | 0.557 | 0.563 | 0.551 |
| Mevkiye özel | Log per-90 + PAdj, lig farkı ½ | Öklid | 40.9% | 73.0% | 84.6% | 0.554 | 0.557 | 0.550 |
| Ortak (tüm alanlar) | Per-90 z-skor | Öklid | 42.2% | 71.8% | 82.8% | 0.554 | 0.574 | 0.534 |
| Mevkiye özel | Log per-90 + PAdj, lig farkı ½ | Cosine | 41.1% | 72.7% | 85.4% | 0.553 | 0.561 | 0.545 |
| Ortak (tüm alanlar) | Ligler arası percentile | Pearson | 41.1% | 72.1% | 83.7% | 0.552 | 0.560 | 0.544 |
| Ortak − kaleci alanları | Ligler arası percentile | Pearson | 40.9% | 71.6% | 83.2% | 0.550 | 0.562 | 0.538 |
| Ortak − kaleci alanları | Per-90 z-skor | Öklid | 41.2% | 71.6% | 82.5% | 0.547 | 0.563 | 0.531 |
| Ortak − kaleci alanları | Lig içi percentile | Pearson | 40.1% | 72.7% | 84.1% | 0.546 | 0.554 | 0.539 |
| Mevkiye özel | Ligler arası percentile | Öklid | 38.9% | 72.3% | 85.0% | 0.538 | 0.547 | 0.528 |
| Mevkiye özel | Per-90 z-skor | Cosine | 39.8% | 71.2% | 84.3% | 0.538 | 0.544 | 0.533 |
| Mevkiye özel | Lig içi percentile | Öklid | 38.6% | 72.1% | 84.2% | 0.537 | 0.544 | 0.531 |
| Mevkiye özel | Log per-90 + PAdj, lig farkı ½ | Pearson | 38.8% | 70.0% | 83.3% | 0.532 | 0.546 | 0.518 |
| Mevkiye özel | Per-90 z-skor | Öklid | 38.6% | 70.3% | 82.4% | 0.529 | 0.535 | 0.523 |
| Mevkiye özel | Ligler arası percentile | Cosine | 38.3% | 69.3% | 83.6% | 0.526 | 0.535 | 0.517 |
| Mevkiye özel | Lig içi percentile | Cosine | 37.2% | 69.3% | 83.1% | 0.519 | 0.528 | 0.510 |
| Mevkiye özel | Per-90 z-skor | Pearson | 37.8% | 68.3% | 82.2% | 0.519 | 0.528 | 0.511 |
| Mevkiye özel | Ligler arası percentile | Pearson | 35.9% | 67.3% | 81.8% | 0.505 | 0.520 | 0.491 |
| Mevkiye özel | Lig içi percentile | Pearson | 35.3% | 67.9% | 82.0% | 0.501 | 0.514 | 0.488 |
| Rastgele sıralama |  |  | 2.0% | 9.8% | 19.6% | 0.087 | 0.086 | 0.088 |

### Havuz: tüm ligler

| Feature seti | Normalizasyon | Metrik | R@1 | R@5 | R@10 | MRR | MRR 23/24 → 24/25 | MRR 24/25 → 25/26 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Ortak (tüm alanlar) | Per-90 z-skor | Cosine | 27.3% | 49.3% | 59.7% | 0.380 | 0.399 | 0.361 |
| Ortak (tüm alanlar) | Log per-90 + PAdj, lig farkı ½ | Pearson | 26.9% | 49.0% | 59.7% | 0.378 | 0.391 | 0.364 |
| Ortak (tüm alanlar) | Per-90 z-skor | Pearson | 26.9% | 49.0% | 60.5% | 0.376 | 0.391 | 0.361 |
| Ortak (tüm alanlar) | Log per-90 + PAdj, lig farkı ½ | Cosine | 26.1% | 49.6% | 60.1% | 0.374 | 0.389 | 0.359 |
| Ortak − kaleci alanları | Per-90 z-skor | Cosine | 26.2% | 48.5% | 59.2% | 0.372 | 0.388 | 0.357 |
| Ortak (tüm alanlar) | Ligler arası percentile | Öklid | 25.8% | 48.4% | 60.8% | 0.371 | 0.393 | 0.349 |
| Ortak − kaleci alanları | Per-90 z-skor | Pearson | 25.9% | 47.6% | 58.7% | 0.366 | 0.383 | 0.349 |
| Ortak − kaleci alanları (mevcut) | Log per-90 + PAdj, lig farkı ½ | Cosine | 24.9% | 49.0% | 59.8% | 0.365 | 0.379 | 0.352 |
| Ortak (tüm alanlar) | Log per-90 + PAdj, lig farkı ½ | Öklid | 26.1% | 46.5% | 58.0% | 0.364 | 0.382 | 0.347 |
| Ortak (tüm alanlar) | Lig içi percentile | Cosine | 24.8% | 48.3% | 58.7% | 0.363 | 0.351 | 0.374 |
| Ortak (tüm alanlar) | Per-90 z-skor | Öklid | 25.8% | 47.1% | 56.6% | 0.362 | 0.382 | 0.342 |
| Ortak (tüm alanlar) | Lig içi percentile | Öklid | 24.1% | 48.4% | 60.2% | 0.361 | 0.352 | 0.370 |
| Ortak − kaleci alanları | Log per-90 + PAdj, lig farkı ½ | Pearson | 24.9% | 47.5% | 58.2% | 0.358 | 0.377 | 0.340 |
| Ortak − kaleci alanları | Ligler arası percentile | Öklid | 24.2% | 47.7% | 60.1% | 0.357 | 0.375 | 0.340 |
| Ortak − kaleci alanları | Log per-90 + PAdj, lig farkı ½ | Öklid | 24.8% | 46.4% | 57.8% | 0.355 | 0.373 | 0.337 |
| Ortak (tüm alanlar) | Ligler arası percentile | Cosine | 23.7% | 47.2% | 58.9% | 0.352 | 0.375 | 0.329 |
| Ortak − kaleci alanları | Per-90 z-skor | Öklid | 24.3% | 46.7% | 55.7% | 0.351 | 0.368 | 0.334 |
| Ortak − kaleci alanları | Ligler arası percentile | Cosine | 23.0% | 46.7% | 58.1% | 0.346 | 0.360 | 0.332 |
| Ortak (tüm alanlar) | Lig içi percentile | Pearson | 23.3% | 46.3% | 57.6% | 0.344 | 0.334 | 0.355 |
| Ortak − kaleci alanları | Ligler arası percentile | Pearson | 22.6% | 45.9% | 57.2% | 0.340 | 0.356 | 0.324 |
| Ortak (tüm alanlar) | Ligler arası percentile | Pearson | 22.4% | 45.8% | 57.2% | 0.338 | 0.354 | 0.322 |
| Ortak − kaleci alanları | Lig içi percentile | Öklid | 21.5% | 45.0% | 57.2% | 0.332 | 0.351 | 0.312 |
| Ortak − kaleci alanları | Lig içi percentile | Cosine | 20.8% | 44.4% | 56.3% | 0.324 | 0.339 | 0.309 |
| Mevkiye özel | Log per-90 + PAdj, lig farkı ½ | Cosine | 20.9% | 43.7% | 55.5% | 0.322 | 0.338 | 0.306 |
| Mevkiye özel | Per-90 z-skor | Cosine | 21.1% | 43.3% | 55.4% | 0.321 | 0.338 | 0.305 |
| Mevkiye özel | Log per-90 + PAdj, lig farkı ½ | Öklid | 20.7% | 42.9% | 55.4% | 0.319 | 0.332 | 0.307 |
| Mevkiye özel | Per-90 z-skor | Öklid | 20.3% | 43.0% | 55.2% | 0.316 | 0.331 | 0.301 |
| Ortak − kaleci alanları | Lig içi percentile | Pearson | 20.0% | 41.8% | 54.8% | 0.313 | 0.326 | 0.300 |
| Mevkiye özel | Ligler arası percentile | Öklid | 19.6% | 42.2% | 56.0% | 0.310 | 0.324 | 0.296 |
| Mevkiye özel | Ligler arası percentile | Cosine | 19.4% | 41.5% | 54.3% | 0.304 | 0.318 | 0.289 |
| Mevkiye özel | Log per-90 + PAdj, lig farkı ½ | Pearson | 19.1% | 41.4% | 52.8% | 0.304 | 0.323 | 0.284 |
| Mevkiye özel | Per-90 z-skor | Pearson | 19.1% | 41.7% | 52.7% | 0.303 | 0.320 | 0.285 |
| Mevkiye özel | Ligler arası percentile | Pearson | 18.8% | 39.5% | 50.9% | 0.295 | 0.307 | 0.282 |
| Mevkiye özel | Lig içi percentile | Öklid | 18.5% | 39.4% | 52.6% | 0.294 | 0.304 | 0.285 |
| Mevkiye özel | Lig içi percentile | Cosine | 18.3% | 38.9% | 50.2% | 0.288 | 0.305 | 0.272 |
| Mevkiye özel | Lig içi percentile | Pearson | 16.8% | 36.7% | 48.1% | 0.272 | 0.285 | 0.258 |
| Rastgele sıralama |  |  | 0.3% | 1.6% | 3.3% | 0.020 | 0.020 | 0.021 |

### Bulgular

Farklar lig içi havuzda MRR farkıdır; köşeli parantezler eşleştirilmiş bootstrap ile %95 güven aralığıdır
(`run_eval` çıktısında da var).

| Karşılaştırma | Tümü (n=1961) | Aynı lig (n=1743) | Lig değiştirdi (n=218) | Aynı takım (n=1456) | Takım değiştirdi (n=505) |
|---|---:|---:|---:|---:|---:|
| Mevcut − önceki (lig içi percentile · Öklid) | +0.011 [-0.001, +0.024] | +0.007 [-0.007, +0.021] | +0.044 [+0.010, +0.079] | -0.003 [-0.017, +0.012] | +0.052 [+0.028, +0.077] |
| Mevcut − ilk sürüm (mevkiye özel · lig içi percentile · cosine) | +0.066 [+0.051, +0.081] | +0.065 [+0.050, +0.081] | +0.069 [+0.028, +0.111] | +0.060 [+0.043, +0.077] | +0.082 [+0.052, +0.112] |
| Normalizasyon: log lig farkı ½ − lig içi percentile (cosine) | +0.020 [+0.010, +0.031] | +0.020 [+0.009, +0.031] | +0.021 [-0.007, +0.049] | +0.015 [+0.003, +0.027] | +0.036 [+0.017, +0.055] |
| Normalizasyon: log lig farkı ½ − per-90 z (cosine) | +0.014 [+0.007, +0.021] | +0.015 [+0.007, +0.023] | +0.005 [-0.017, +0.027] | +0.017 [+0.009, +0.025] | +0.006 [-0.009, +0.020] |
| Metrik: cosine − Öklid (log lig farkı ½) | +0.013 [+0.001, +0.024] | +0.010 [-0.003, +0.023] | +0.032 [+0.000, +0.064] | +0.004 [-0.010, +0.017] | +0.038 [+0.015, +0.063] |
| Metrik: cosine − Öklid (lig içi percentile) | -0.009 [-0.019, +0.001] | -0.013 [-0.023, -0.002] | +0.023 [-0.003, +0.049] | -0.018 [-0.030, -0.006] | +0.016 [-0.002, +0.035] |
| Feature seti: 35 alan − mevkiye özel (log lig farkı ½ · cosine) | +0.032 [+0.018, +0.045] | +0.029 [+0.014, +0.044] | +0.052 [+0.016, +0.090] | +0.029 [+0.013, +0.044] | +0.039 [+0.013, +0.066] |
| Kaleci alanlarını tutmak: tüm alanlar − mevcut | +0.004 [-0.001, +0.008] | +0.006 [+0.001, +0.010] | -0.011 [-0.024, -0.001] | +0.007 [+0.002, +0.012] | -0.006 [-0.015, +0.003] |

- **Mevcut yöntem (log per-90 + PAdj, lig farkı ½ · cosine) lig ve takım değiştirenlerde belirgin şekilde iyi,
  genelde kayıp yok.** Önceki yönteme (lig içi percentile · Öklid) göre lig değiştirenlerde +0.044 [+0.010, +0.079]
  (0.424 → 0.468), takım değiştirenlerde +0.052 [+0.028, +0.077] (0.440 → 0.492). Tüm sorgularda +0.011
  (0.573 → 0.585); aynı takımda kalanlarda fark yok. İlk sürüme (mevkiye özel · cosine) göre toplam +0.066.
- **Eski "lig değiştirende per-90 daha iyi" bulgusunun yarısı metrikten.** Eski karşılaştırma (per-90 cosine vs lig
  içi Öklid) normalizasyonla metriği birlikte değiştiriyordu. Ayrılınca: lig içi percentile'da sadece metriği
  cosine'e çevirmek lig değiştirenlerde +0.023 kazandırıyor ama aynı ligde −0.013 kaybettiriyor. Log per-90 ile
  cosine aynı ligde kayıp vermiyor (+0.010), lig değiştirenlerde +0.032, takım değiştirenlerde +0.038.
- **Normalizasyon, cosine altında:** log per-90 + PAdj, lig farkı ½, lig içi percentile'dan +0.020 [+0.010, +0.031],
  per-90 z-skordan +0.014 [+0.007, +0.021] iyi. Lig değiştirenlerde per-90 z-skorla fark yok (+0.005); oradaki
  kazanç per-90 ölçeği + cosine'den.
- **Feature seti hâlâ önemli.** 35 alan, mevkiye özel sete göre +0.032; lig değiştirenlerde +0.052.
- **En yüksek skor, arama için doğru seçim değil.** Kaleci alanlarını saha oyuncusunda da tutmak aynı takımda
  kalanlarda +0.007 kazandırıyor ama takım değiştirenlerde −0.006, lig değiştirenlerde −0.011 kaybettiriyor. Bu
  alanlar oyuncuyu değil takımı tanıyor (`goalsConceded`), bu yüzden aramada kullanılmıyor.
- **Zor durumlar.** Lig değiştirenlerde MRR 0.468, takım değiştirenlerde 0.492 (aynı takımda kalanlarda 0.617).
  Topa sahip olma bu açığı açıklamıyor (aşağıda, Takım etkisi). En zor gruplar stoper (0.49) ve kaleci (0.46).

### Ligler arası arama: lig farkının ne kadarı çıkarılsın?

Lig farkının çıkarılan payı α (0 = ham per-90 seviyesi korunur, 1 = ligin seviyesi tamamen silinir). Hepsi log
per-90 · 35 alan · cosine. Son sütun ürün açısından önemli: lig filtresi olmadan aranınca ilk 10 sonucun ne kadarı
sorgunun liginden geliyor. Yansız bir arama için bu oran ligin havuzdaki payı kadar olmalı (25/26: %16,6).
Çıktı: [`results/league_eval.md`](results/league_eval.md).

| Yöntem | Tümü | Aynı lig | Lig değiştirdi | Takım değiştirdi | Lig değiştirdi 23/24 → 24/25 | Lig değiştirdi 24/25 → 25/26 | Lig değiştirdi · tüm-lig havuzu | Fark: lig değiştirdi | İlk 10'da kendi ligi |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Önceki: Lig içi percentile · Öklid | 0.573 | 0.592 | 0.424 | 0.440 | 0.463 | 0.385 | 0.235 | — | 15.8% |
| α = 0 | 0.576 | 0.591 | 0.456 | 0.487 | 0.477 | 0.436 | 0.248 | +0.032 [-0.005, +0.070] | 22.3% |
| α = 0.25 | 0.581 | 0.596 | 0.463 | 0.495 | 0.485 | 0.441 | 0.243 | +0.039 [+0.004, +0.075] | 19.2% |
| α = 0.5 (mevcut) | 0.585 | 0.599 | 0.468 | 0.492 | 0.480 | 0.455 | 0.239 | +0.044 [+0.010, +0.079] | 17.1% |
| α = 0.75 | 0.585 | 0.601 | 0.459 | 0.488 | 0.476 | 0.442 | 0.233 | +0.035 [+0.002, +0.068] | 15.8% |
| α = 1 | 0.583 | 0.599 | 0.456 | 0.482 | 0.469 | 0.444 | 0.228 | +0.032 [-0.002, +0.067] | 15.5% |

- α = 0,25 ile 1 arasında genel MRR neredeyse aynı (0.581–0.585), α = 0'da 0.576. Lig değiştirenlerde en iyi
  α = 0,5 (0.468; diğerleri 0.456–0.463), ama farklar gürültü düzeyinde (218 sorgu, aralık ±0,035).
- **α = 0,5 lig yanlılığını sıfırlıyor:** filtresiz aramada ilk 10'un %17,1'i sorgunun liginden (yansız: %16,6).
  α = 0'da %22,3: aynı ligin oyuncuları sırf lig seviyesi yüzünden öne çıkıyor. α = 1'de lig değiştirenler
  tüm-lig havuzunda en kötü (0.228).
- Seçim sağlam: α'yı bir sezon çiftinde seçip diğerinde test etmek de 0,25–0,5 veriyor, ikisi de önceki yöntemden
  iyi.

### Takım etkisi: topa sahip olma düzeltmesi

Takım değiştiren oyuncular, aynı takımda kalanlardan belirgin şekilde daha zor bulunuyor (MRR 0.49'a karşı 0.62).
İlk akla gelen açıklama topa sahip olma: rakibi topu çok tutan takımın oyuncusu daha çok müdahale eder. Standart
düzeltme (PAdj) savunma istatistiklerini 0,5 / (1 − p) ile çarpar (p = takımın topa sahip olma oranı). Önce bu
varsayım veriden test edildi: aynı ligde takım değiştiren bir oyuncunun savunma istatistikleri, yeni takımının topa
sahip olma oranı değişince ne kadar değişiyor? Eğim 1 ise standart düzeltme doğru, 0 ise hiç etki yok.
Çıktı: [`results/team_eval.md`](results/team_eval.md).

| Alan | n | Eğim | 23/24 → 24/25 | 24/25 → 25/26 |
|---|---:|---:|---:|---:|
| tackles | 338 | 0.29 [0.04, 0.56] | 0.26 | 0.27 |
| interceptions | 338 | 0.21 [-0.19, 0.63] | 0.31 | 0.11 |
| clearances | 338 | 0.62 [0.25, 0.99] | 0.58 | 0.55 |
| ballRecovery | 338 | 0.22 [0.03, 0.41] | 0.29 | 0.23 |
| possessionWonAttThird | 338 | 0.16 [-0.32, 0.63] | 0.05 | 0.28 |
| dribbledPast | 338 | 0.44 [0.08, 0.82] | 0.66 | 0.26 |

| Düzeltme | Tümü (n=1961) | Aynı takım (n=1456) | Takım değiştirdi (n=505) | Takım değiştirdi · aynı lig (n=354) | Fark: Tümü | Fark: Takım değiştirdi |
|---|---:|---:|---:|---:|---:|---:|
| β = 0 (düzeltme yok) | 0.583 | 0.617 | 0.485 | 0.507 | — | — |
| β = 0.3 (mevcut) | 0.585 | 0.617 | 0.492 | 0.512 | +0.002 [-0.001, +0.005] | +0.007 [-0.000, +0.014] |
| β = 0.5 | 0.583 | 0.614 | 0.492 | 0.513 | +0.000 [-0.004, +0.004] | +0.007 [-0.002, +0.015] |
| β = 1 (standart PAdj) | 0.581 | 0.614 | 0.486 | 0.512 | -0.002 [-0.007, +0.003] | +0.001 [-0.011, +0.012] |

- **Esneklik 1 değil, ~0,3.** Müdahale 0.29, top kazanma 0.22, pas arası 0.21; sadece uzaklaştırma (0.62) ve
  çalım yeme (0.44) daha yüksek. Değerler iki sezon çiftinde benzer. Standart PAdj etkiyi ~3 kat abartıyor ve
  aramaya katkısı yok (β = 1: −0.002).
- **β = 0,3 ile** takım değiştirenlerde +0.007 [−0.000, +0.014], genelde +0.002; kayıp yok. Kazanç küçük ama yönü
  tutarlı, en çok stoper ve merkez orta sahada. Arama β = 0,3 ile çalışıyor.
- **Topla oynanan alanlar düzeltilmiyor.** Pas hacmi topa sahip olmayla artıyor (pas sayısında eğim ~0,5), ama
  orta, uzun top ve çalım azalıyor (eğim negatif). Bu alanlarda topa sahip olma hacmi değil oyun tarzını
  değiştiriyor. Pas hacmini de düzeltmek denendi, ek kazanç getirmedi.
- **Takım değiştirenlerdeki açığın sebebi topa sahip olma değil.** Takım değiştirenlerde topa sahip olma ortalama
  sadece 5,2 puan değişiyor; bu da savunma istatistiklerinde yalnızca ~%3–5'lik bir fark yaratıyor. Açığın asıl
  kaynağı büyük ihtimalle yeni takımdaki rol değişimi.

### Çok sezonlu profil

Sorgu profili sezon N ile N−1'in ağırlıklı ortalaması, hedef N+1 (tek sezon; hedefin profiline N girmez, sızıntı
olmasın diye). 3 sezon verisiyle test edilebilen tek çift 24/25 → 25/26 (geçmiş: 23/24). Çıktı:
[`results/history_eval.md`](results/history_eval.md).

| Profil | R@1 | R@5 | R@10 | MRR | Fark: Tümü (n=983) | Fark: Geçmişi olan (n=592) | Fark: Geçmişi olan · takım değiştirdi (n=171) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Tek sezon (mevcut) | 44.9% | 72.9% | 85.9% | 0.580 | — | — | — |
| Çok sezon · sadece dakika ağırlıklı | 46.4% | 76.8% | 87.8% | 0.600 | +0.019 [+0.006, +0.032] | +0.032 [+0.011, +0.054] | +0.039 [+0.002, +0.078] |
| Çok sezon · önceki sezon ×0.5 | 46.9% | 76.0% | 88.5% | 0.601 | +0.020 [+0.010, +0.030] | +0.034 [+0.017, +0.050] | +0.028 [-0.003, +0.059] |
| Çok sezon · önceki sezon ×0.25 | 45.3% | 75.4% | 87.5% | 0.588 | +0.008 [+0.001, +0.015] | +0.013 [+0.001, +0.025] | +0.009 [-0.016, +0.032] |

- İki sezonluk profil tek sezondan iyi: önceki sezon ×0,5 ile +0.020 [+0.010, +0.030]; geçmişi olan oyuncularda
  +0.034. Arama bu ayarla çalışıyor. (Lig içi percentile · Öklid ile kazanç +0.030'du; yeni normalizasyon tek
  sezonluk profili zaten 0.556'dan 0.580'e çıkardığı için ek kazanç biraz küçüldü. İkisi birlikte: 0.556 → 0.601.)
- ×1 ile ×0,5 aynı (0.600 / 0.601). ×0,5 seçildi çünkü güncel formu daha çok yansıtıyor; takım değiştirenlerde ×1
  biraz daha iyi (+0.039).
- 3 sezonluk profil test edilmedi (22/23 verisi yok).
- Kullanımda adayların profili de iki sezonluk. Test sadece sorgu tarafını ölçüyor (aday tarafında N+1'in
  geçmişi N olurdu, bu da sızıntı demek). Aday tarafında da aynı kazancın olduğu varsayılıyor.

### Az dakikalı oyuncular

900 dakika eşiği aranan gençleri eliyordu: 25/26'da 450–899 dk oynayan 513 oyuncunun 184'ü 23 yaş ve altı. Bu oyuncular
gürültülü olduğu için değerleri mevki ortalamasına doğru çekiliyor: x̂ = w·x + (1 − w)·μ, w = m / (m + c·k). k alanın
kararlılık noktası: 900+ dk oyuncuların iki sezon arasındaki korelasyondan (r = m / (m + k)). Hava topu ~500 dk'da
otururken gol ~2300 dk ister. c = ¼. Çıktı: [`results/shrinkage_eval.md`](results/shrinkage_eval.md).

| Test (havuz: hedefin ligi) | n | Düzeltme yok (MRR) | Tek k (fark) | Alan bazlı k × ¼ (MRR) | Alan bazlı k × ¼ (fark) |
|---|---:|---:|---:|---:|---:|
| A · Sorgu 450–899 dk → hedef 900+ | 296 | 0.398 | -0.017 [-0.039, +0.005] | 0.436 | +0.038 [+0.017, +0.058] |
| B · Sorgu 900+ → hedef 450–899 dk | 295 | 0.328 | +0.004 [-0.014, +0.022] | 0.406 | +0.078 [+0.055, +0.101] |
| C · Sorgu 900+ → hedef 900+, havuz 450+ | 1961 | 0.564 | -0.009 [-0.013, -0.005] | 0.558 | -0.007 [-0.010, -0.004] |
| A2 · Sorgu 300–449 dk → hedef 900+ | 62 | 0.366 | -0.122 [-0.191, -0.061] | 0.374 | +0.008 [-0.040, +0.054] |
| B2 · Sorgu 900+ → hedef 300–449 dk | 88 | 0.300 | -0.025 [-0.060, +0.010] | 0.365 | +0.065 [+0.025, +0.110] |

- Asıl kullanım B: az oynamış adayı bulmak. Düzeltme MRR'ı 0.328'den 0.406'ya çıkarıyor.
- **Tek k işe yaramıyor.** Bütün vektörü aynı oranda küçültür, cosine de ölçeği sildiği için yön değişmez. Kazanç,
  gürültülü alanların (gol) kararlı alanlara (hava topu) göre daha çok bastırılmasından geliyor.
- k × ¼, k × ½ ve k × 1 A ve B'de birbirine yakın; ¼ seçildi çünkü C'de en az zararı veriyor. Sezonlar arası korelasyon
  oyuncunun gerçek değişimini de içerdiği için k gürültüyü olduğundan büyük gösteriyor.
- C: Havuza 513 oyuncu daha girince 900+ oyuncuları bulmak doğal olarak biraz zorlaşıyor (0.585 → 0.558). 900+ oyuncuların
  kendi vektörleri ve percentile'ları değişmedi. Az dakikalılar ilk sıraları haksız doldurmuyor: havuzun %22'si, ilk
  10'un %18,5'i.
- Alt eşik 450: 300–449 dk için örnek az (62 ve 88) ve sorgu tarafında kazanç yok.
- Örneklem seçilmiş: A'da az oynadıktan sonra sıradaki sezon 900+ oynayanlar var, B'de tersi. Hiç şans bulamayanlar test dışı.

Sonuçtaki güven göstergesi efektif dakikaya (güncel + önceki sezon × 0,5) bağlı. Eşikler bu tablodan (sorgu 24/25, iki
sezonlu profil, hedef 25/26, havuz 900+): **düşük** < 900, **orta** 900–1799, **yüksek** 1800+.

| Efektif dakika | n | MRR | R@10 |
|---|---:|---:|---:|
| 450–699 | 60 | 0.431 | 75.0% |
| 700–899 | 37 | 0.467 | 78.4% |
| 900–1199 | 67 | 0.493 | 80.6% |
| 1200–1799 | 187 | 0.519 | 82.9% |
| 1800–2699 | 285 | 0.583 | 86.7% |
| 2700+ | 493 | 0.646 | 92.1% |

### Testin sınırları

- Test benzerliği değil **kimliğin sezonlar arası kararlılığını** ölçüyor. Daha çok alan kimliği her zaman daha
  iyi ayırt eder; bu, o alanların "benzer oyuncu" açısından anlamlı olduğunu garanti etmez.
- Mevki, çekim anındaki güncel profilden geliyor ve iki sezonda da aynı kabul ediliyor. Mevki değiştiren oyuncu
  (örn. kanattan beke geçen) yanlış grupta aranabilir.
- TFF 1. Lig'de xG/xA yok. TFF oyuncusu içeren karşılaştırmalarda bu iki alan atlanıyor; profil iki alan eksik
  bilgiyle kuruluyor.
- Lig değiştiren sorgu az (218). Bu kesitteki farkların güven aralığı geniş (±0,035); lig değiştirenlere göre
  yapılan seçimler (α) ayrıca lig yanlılığı gibi ürün ölçütleriyle desteklenmeli.
