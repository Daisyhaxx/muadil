## Yöntem karşılaştırması — havuz: tüm ligler

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

## Yöntem karşılaştırması — havuz: sadece hedefin ligi

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

## Kırılım: mevcut yöntem (Mevkiye özel · Lig içi percentile · Cosine)

| Kesit | n | R@1 | R@5 | R@10 | MRR | Medyan sıra | Havuz | Rastgele R@10 | MRR (lig içi havuz) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tümü | 1961 | 18.6% | 40.1% | 50.7% | 0.293 | 10 | 350 | 3.3% | 0.517 |
| Forvet | 193 | 18.7% | 41.5% | 53.9% | 0.304 | 9 | 207 | 4.8% | 0.538 |
| Kanat | 284 | 17.6% | 36.3% | 49.3% | 0.273 | 12 | 269 | 3.7% | 0.481 |
| Merkez orta saha | 582 | 25.9% | 49.5% | 59.6% | 0.371 | 6 | 515 | 1.9% | 0.593 |
| Bek | 361 | 15.2% | 42.7% | 53.7% | 0.280 | 8 | 317 | 3.2% | 0.529 |
| Stoper | 386 | 14.2% | 31.6% | 39.9% | 0.231 | 16 | 348 | 2.9% | 0.443 |
| Kaleci | 155 | 11.0% | 25.2% | 36.1% | 0.206 | 20 | 146 | 6.9% | 0.426 |
| Aynı lig | 1743 | 19.7% | 42.1% | 52.8% | 0.307 | 9 | 352 | 3.3% | 0.531 |
| Lig değiştirdi | 218 | 9.6% | 24.3% | 34.4% | 0.179 | 26 | 336 | 3.4% | 0.400 |
| Aynı takım | 1456 | 22.0% | 44.3% | 54.9% | 0.330 | 8 | 352 | 3.3% | 0.556 |
| Takım değiştirdi | 505 | 8.7% | 27.9% | 38.6% | 0.186 | 18 | 345 | 3.3% | 0.405 |

## Kırılım: en iyi yöntem (Ortak (tüm alanlar) · Lig içi percentile · Öklid)

| Kesit | n | R@1 | R@5 | R@10 | MRR | Medyan sıra | Havuz | Rastgele R@10 | MRR (lig içi havuz) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tümü | 1961 | 24.5% | 47.7% | 59.8% | 0.363 | 6 | 350 | 3.3% | 0.577 |
| Forvet | 193 | 25.9% | 47.7% | 61.1% | 0.374 | 6 | 207 | 4.8% | 0.673 |
| Kanat | 284 | 26.8% | 53.5% | 63.7% | 0.395 | 4 | 269 | 3.7% | 0.639 |
| Merkez orta saha | 582 | 32.5% | 56.5% | 67.7% | 0.444 | 4 | 515 | 1.9% | 0.607 |
| Bek | 361 | 20.8% | 44.0% | 57.9% | 0.332 | 7 | 317 | 3.2% | 0.571 |
| Stoper | 386 | 17.9% | 39.6% | 51.8% | 0.291 | 9 | 348 | 2.9% | 0.489 |
| Kaleci | 155 | 13.5% | 32.3% | 45.8% | 0.236 | 14 | 146 | 6.9% | 0.463 |
| Aynı lig | 1743 | 25.9% | 50.5% | 63.1% | 0.383 | 5 | 352 | 3.3% | 0.598 |
| Lig değiştirdi | 218 | 12.8% | 24.8% | 33.5% | 0.202 | 28 | 336 | 3.4% | 0.411 |
| Aynı takım | 1456 | 28.9% | 53.9% | 66.1% | 0.412 | 4 | 352 | 3.3% | 0.628 |
| Takım değiştirdi | 505 | 11.7% | 29.7% | 41.6% | 0.221 | 17 | 345 | 3.3% | 0.430 |
