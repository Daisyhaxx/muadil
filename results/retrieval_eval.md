## Yöntem karşılaştırması — havuz: tüm ligler

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

## Yöntem karşılaştırması — havuz: sadece hedefin ligi

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

## Kırılım: mevcut yöntem (Mevkiye özel · Lig içi percentile · Cosine)

| Kesit | n | R@1 | R@5 | R@10 | MRR | Medyan sıra | Havuz | Rastgele R@10 | MRR (lig içi havuz) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tümü | 1961 | 18.6% | 40.5% | 51.4% | 0.295 | 10 | 350 | 3.3% | 0.519 |
| Forvet | 193 | 18.7% | 41.5% | 53.9% | 0.304 | 9 | 207 | 4.8% | 0.539 |
| Kanat | 284 | 17.6% | 36.3% | 49.3% | 0.273 | 12 | 269 | 3.7% | 0.481 |
| Merkez orta saha | 582 | 25.9% | 49.5% | 59.6% | 0.371 | 6 | 515 | 1.9% | 0.593 |
| Bek | 361 | 15.2% | 42.7% | 53.7% | 0.280 | 8 | 317 | 3.2% | 0.529 |
| Stoper | 386 | 14.2% | 33.7% | 43.3% | 0.242 | 14 | 348 | 2.9% | 0.455 |
| Kaleci | 155 | 11.0% | 25.2% | 36.1% | 0.206 | 20 | 146 | 6.9% | 0.426 |
| Aynı lig | 1743 | 19.7% | 42.5% | 53.5% | 0.309 | 9 | 352 | 3.3% | 0.534 |
| Lig değiştirdi | 218 | 9.6% | 24.8% | 34.4% | 0.181 | 26 | 336 | 3.4% | 0.403 |
| Aynı takım | 1456 | 22.0% | 44.5% | 55.7% | 0.332 | 8 | 352 | 3.3% | 0.558 |
| Takım değiştirdi | 505 | 8.5% | 28.9% | 39.0% | 0.188 | 18 | 345 | 3.3% | 0.408 |

## Kırılım: en iyi yöntem (Ortak (tüm alanlar) · Lig içi percentile · Öklid)

| Kesit | n | R@1 | R@5 | R@10 | MRR | Medyan sıra | Havuz | Rastgele R@10 | MRR (lig içi havuz) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tümü | 1961 | 24.5% | 48.8% | 60.3% | 0.366 | 6 | 350 | 3.3% | 0.580 |
| Forvet | 193 | 26.4% | 47.7% | 60.1% | 0.378 | 6 | 207 | 4.8% | 0.680 |
| Kanat | 284 | 26.4% | 53.9% | 63.4% | 0.394 | 4 | 269 | 3.7% | 0.639 |
| Merkez orta saha | 582 | 32.5% | 58.9% | 68.7% | 0.449 | 3 | 515 | 1.9% | 0.610 |
| Bek | 361 | 20.8% | 44.9% | 58.4% | 0.331 | 7 | 317 | 3.2% | 0.571 |
| Stoper | 386 | 18.7% | 41.5% | 53.6% | 0.300 | 9 | 348 | 2.9% | 0.495 |
| Kaleci | 155 | 12.3% | 30.3% | 43.9% | 0.225 | 14 | 146 | 6.9% | 0.463 |
| Aynı lig | 1743 | 26.0% | 51.7% | 63.8% | 0.386 | 5 | 352 | 3.3% | 0.600 |
| Lig değiştirdi | 218 | 12.4% | 25.2% | 32.1% | 0.200 | 31 | 336 | 3.4% | 0.414 |
| Aynı takım | 1456 | 29.0% | 55.4% | 67.0% | 0.416 | 4 | 352 | 3.3% | 0.632 |
| Takım değiştirdi | 505 | 11.7% | 29.9% | 40.8% | 0.220 | 17 | 345 | 3.3% | 0.431 |
