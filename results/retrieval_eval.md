## Yöntem karşılaştırması — havuz: tüm ligler

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

## Yöntem karşılaştırması — havuz: sadece hedefin ligi

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

## Eşleştirilmiş farklar — havuz: sadece hedefin ligi

MRR farkı a − b ve %95 eşleştirilmiş bootstrap güven aralığı (aynı sorgular, 10 000 tekrar).

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

## Kırılım: mevcut yöntem (Ortak − kaleci alanları · Log per-90 + PAdj, lig farkı ½ · Cosine)

| Kesit | n | R@1 | R@5 | R@10 | MRR | Medyan sıra | Havuz | Rastgele R@10 | MRR (lig içi havuz) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tümü | 1961 | 24.9% | 49.0% | 59.8% | 0.365 | 6 | 350 | 3.3% | 0.585 |
| Forvet | 193 | 31.1% | 63.2% | 70.5% | 0.452 | 3 | 207 | 4.8% | 0.696 |
| Kanat | 284 | 31.3% | 58.8% | 70.1% | 0.438 | 4 | 269 | 3.7% | 0.656 |
| Merkez orta saha | 582 | 27.5% | 52.1% | 63.2% | 0.396 | 4 | 515 | 1.9% | 0.616 |
| Bek | 361 | 21.9% | 48.2% | 59.6% | 0.342 | 6 | 317 | 3.2% | 0.576 |
| Stoper | 386 | 19.9% | 38.3% | 49.0% | 0.297 | 11 | 348 | 2.9% | 0.490 |
| Kaleci | 155 | 14.8% | 29.7% | 42.6% | 0.234 | 15 | 146 | 6.9% | 0.455 |
| Aynı lig | 1743 | 26.3% | 50.9% | 61.7% | 0.381 | 5 | 352 | 3.3% | 0.599 |
| Lig değiştirdi | 218 | 13.3% | 33.5% | 45.0% | 0.239 | 18 | 336 | 3.4% | 0.468 |
| Aynı takım | 1456 | 28.8% | 53.0% | 63.4% | 0.404 | 5 | 352 | 3.3% | 0.617 |
| Takım değiştirdi | 505 | 13.7% | 37.2% | 49.5% | 0.255 | 11 | 345 | 3.3% | 0.492 |

## Kırılım: en iyi yöntem (Ortak (tüm alanlar) · Log per-90 + PAdj, lig farkı ½ · Pearson)

| Kesit | n | R@1 | R@5 | R@10 | MRR | Medyan sıra | Havuz | Rastgele R@10 | MRR (lig içi havuz) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tümü | 1961 | 26.9% | 49.0% | 59.7% | 0.378 | 6 | 350 | 3.3% | 0.590 |
| Forvet | 193 | 36.8% | 64.2% | 74.1% | 0.489 | 3 | 207 | 4.8% | 0.715 |
| Kanat | 284 | 32.4% | 60.2% | 70.4% | 0.453 | 3 | 269 | 3.7% | 0.668 |
| Merkez orta saha | 582 | 30.2% | 52.2% | 63.2% | 0.409 | 5 | 515 | 1.9% | 0.608 |
| Bek | 361 | 24.1% | 48.8% | 58.7% | 0.361 | 6 | 317 | 3.2% | 0.591 |
| Stoper | 386 | 20.2% | 37.6% | 48.4% | 0.295 | 12 | 348 | 2.9% | 0.501 |
| Kaleci | 155 | 15.5% | 25.8% | 39.4% | 0.226 | 16 | 146 | 6.9% | 0.444 |
| Aynı lig | 1743 | 28.6% | 50.7% | 61.8% | 0.395 | 5 | 352 | 3.3% | 0.605 |
| Lig değiştirdi | 218 | 13.8% | 35.3% | 42.7% | 0.238 | 16 | 336 | 3.4% | 0.471 |
| Aynı takım | 1456 | 30.4% | 52.7% | 64.0% | 0.414 | 5 | 352 | 3.3% | 0.626 |
| Takım değiştirdi | 505 | 17.0% | 38.2% | 47.3% | 0.272 | 12 | 345 | 3.3% | 0.486 |
