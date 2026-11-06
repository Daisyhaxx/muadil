## Yöntem karşılaştırması — havuz: tüm ligler

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

## Yöntem karşılaştırması — havuz: sadece hedefin ligi

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

## Eşleştirilmiş farklar — havuz: sadece hedefin ligi

MRR farkı a − b ve %95 eşleştirilmiş bootstrap güven aralığı (aynı sorgular, 10 000 tekrar).

| Karşılaştırma | Tümü (n=1961) | Aynı lig (n=1743) | Lig değiştirdi (n=218) | Aynı takım (n=1456) | Takım değiştirdi (n=505) |
|---|---:|---:|---:|---:|---:|
| Mevcut − eski (mevkiye özel · cosine) | +0.054 [+0.039, +0.069] | +0.058 [+0.043, +0.074] | +0.017 [-0.019, +0.053] | +0.063 [+0.046, +0.081] | +0.026 [-0.001, +0.053] |
| Feature seti: tüm alanlar − mevkiye özel (lig içi · cosine) | +0.049 [+0.036, +0.064] | +0.053 [+0.038, +0.067] | +0.025 [-0.016, +0.068] | +0.056 [+0.040, +0.072] | +0.031 [+0.003, +0.059] |
| Kaleci alanlarını tutmak: tüm alanlar − mevcut (Öklid) | +0.008 [+0.002, +0.013] | +0.010 [+0.004, +0.016] | -0.013 [-0.028, +0.003] | +0.013 [+0.006, +0.019] | -0.007 [-0.017, +0.004] |
| Normalizasyon: lig içi (Öklid) − per-90 z (cosine), tüm alanlar | +0.006 [-0.008, +0.020] | +0.013 [-0.002, +0.028] | -0.050 [-0.088, -0.011] | +0.021 [+0.005, +0.038] | -0.038 [-0.064, -0.011] |
| Metrik: Öklid − cosine (tüm alanlar, lig içi) | +0.012 [+0.002, +0.022] | +0.016 [+0.005, +0.026] | -0.021 [-0.047, +0.005] | +0.020 [+0.009, +0.031] | -0.012 [-0.031, +0.007] |

## Kırılım: mevcut yöntem (Ortak − kaleci alanları · Lig içi percentile · Öklid)

| Kesit | n | R@1 | R@5 | R@10 | MRR | Medyan sıra | Havuz | Rastgele R@10 | MRR (lig içi havuz) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tümü | 1961 | 21.5% | 45.0% | 57.2% | 0.332 | 7 | 350 | 3.3% | 0.573 |
| Forvet | 193 | 32.6% | 53.9% | 68.4% | 0.434 | 4 | 207 | 4.8% | 0.668 |
| Kanat | 284 | 24.3% | 53.9% | 64.4% | 0.376 | 5 | 269 | 3.7% | 0.626 |
| Merkez orta saha | 582 | 22.5% | 47.4% | 60.1% | 0.348 | 7 | 515 | 1.9% | 0.604 |
| Bek | 361 | 20.5% | 44.9% | 56.2% | 0.324 | 8 | 317 | 3.2% | 0.569 |
| Stoper | 386 | 16.8% | 36.5% | 47.9% | 0.272 | 11 | 348 | 2.9% | 0.491 |
| Kaleci | 155 | 12.9% | 30.3% | 43.9% | 0.229 | 14 | 146 | 6.9% | 0.459 |
| Aynı lig | 1743 | 22.1% | 47.2% | 59.6% | 0.344 | 7 | 352 | 3.3% | 0.592 |
| Lig değiştirdi | 218 | 16.5% | 28.0% | 37.6% | 0.235 | 21 | 336 | 3.4% | 0.424 |
| Aynı takım | 1456 | 25.0% | 50.1% | 62.2% | 0.372 | 5 | 352 | 3.3% | 0.619 |
| Takım değiştirdi | 505 | 11.5% | 30.5% | 42.6% | 0.214 | 16 | 345 | 3.3% | 0.440 |

## Kırılım: en iyi yöntem (Ortak (tüm alanlar) · Lig içi percentile · Öklid)

| Kesit | n | R@1 | R@5 | R@10 | MRR | Medyan sıra | Havuz | Rastgele R@10 | MRR (lig içi havuz) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tümü | 1961 | 24.1% | 48.4% | 60.2% | 0.361 | 6 | 350 | 3.3% | 0.581 |
| Forvet | 193 | 27.5% | 49.2% | 61.7% | 0.382 | 6 | 207 | 4.8% | 0.677 |
| Kanat | 284 | 25.4% | 53.9% | 64.8% | 0.390 | 4 | 269 | 3.7% | 0.645 |
| Merkez orta saha | 582 | 30.6% | 57.7% | 68.4% | 0.434 | 4 | 515 | 1.9% | 0.610 |
| Bek | 361 | 21.1% | 45.4% | 57.9% | 0.333 | 7 | 317 | 3.2% | 0.576 |
| Stoper | 386 | 18.9% | 39.9% | 52.6% | 0.299 | 9 | 348 | 2.9% | 0.494 |
| Kaleci | 155 | 12.9% | 30.3% | 43.9% | 0.229 | 14 | 146 | 6.9% | 0.459 |
| Aynı lig | 1743 | 25.5% | 51.3% | 63.6% | 0.381 | 5 | 352 | 3.3% | 0.602 |
| Lig değiştirdi | 218 | 12.8% | 24.8% | 33.5% | 0.205 | 28 | 336 | 3.4% | 0.411 |
| Aynı takım | 1456 | 28.3% | 54.9% | 67.0% | 0.411 | 4 | 352 | 3.3% | 0.632 |
| Takım değiştirdi | 505 | 11.9% | 29.5% | 40.6% | 0.218 | 17 | 345 | 3.3% | 0.433 |
