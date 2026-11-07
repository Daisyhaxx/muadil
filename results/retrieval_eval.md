## Yöntem karşılaştırması — havuz: tüm ligler

| Feature seti | Normalizasyon | Metrik | R@1 | R@5 | R@10 | MRR | MRR 23/24 → 24/25 | MRR 24/25 → 25/26 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Ortak (tüm alanlar) | Log per-90, lig farkı ½ | Pearson | 27.5% | 48.9% | 59.6% | 0.381 | 0.394 | 0.368 |
| Ortak (tüm alanlar) | Per-90 z-skor | Cosine | 27.3% | 49.3% | 59.7% | 0.380 | 0.399 | 0.361 |
| Ortak (tüm alanlar) | Per-90 z-skor | Pearson | 26.9% | 49.0% | 60.5% | 0.376 | 0.391 | 0.361 |
| Ortak (tüm alanlar) | Log per-90, lig farkı ½ | Cosine | 26.1% | 49.7% | 60.1% | 0.374 | 0.393 | 0.355 |
| Ortak − kaleci alanları | Per-90 z-skor | Cosine | 26.2% | 48.5% | 59.2% | 0.372 | 0.388 | 0.357 |
| Ortak (tüm alanlar) | Ligler arası percentile | Öklid | 25.8% | 48.4% | 60.8% | 0.371 | 0.393 | 0.349 |
| Ortak − kaleci alanları | Per-90 z-skor | Pearson | 25.9% | 47.6% | 58.7% | 0.366 | 0.383 | 0.349 |
| Ortak − kaleci alanları (mevcut) | Log per-90, lig farkı ½ | Cosine | 25.0% | 48.7% | 60.0% | 0.365 | 0.380 | 0.351 |
| Ortak (tüm alanlar) | Log per-90, lig farkı ½ | Öklid | 26.1% | 46.9% | 57.6% | 0.364 | 0.382 | 0.347 |
| Ortak (tüm alanlar) | Lig içi percentile | Cosine | 24.8% | 48.3% | 58.7% | 0.363 | 0.351 | 0.374 |
| Ortak (tüm alanlar) | Per-90 z-skor | Öklid | 25.8% | 47.1% | 56.6% | 0.362 | 0.382 | 0.342 |
| Ortak (tüm alanlar) | Lig içi percentile | Öklid | 24.1% | 48.4% | 60.2% | 0.361 | 0.352 | 0.370 |
| Ortak − kaleci alanları | Ligler arası percentile | Öklid | 24.2% | 47.7% | 60.1% | 0.357 | 0.375 | 0.340 |
| Ortak − kaleci alanları | Log per-90, lig farkı ½ | Pearson | 24.7% | 47.3% | 58.6% | 0.357 | 0.374 | 0.341 |
| Ortak − kaleci alanları | Log per-90, lig farkı ½ | Öklid | 24.9% | 46.4% | 57.5% | 0.356 | 0.375 | 0.336 |
| Ortak (tüm alanlar) | Ligler arası percentile | Cosine | 23.7% | 47.2% | 58.9% | 0.352 | 0.375 | 0.329 |
| Ortak − kaleci alanları | Per-90 z-skor | Öklid | 24.3% | 46.7% | 55.7% | 0.351 | 0.368 | 0.334 |
| Ortak − kaleci alanları | Ligler arası percentile | Cosine | 23.0% | 46.7% | 58.1% | 0.346 | 0.360 | 0.332 |
| Ortak (tüm alanlar) | Lig içi percentile | Pearson | 23.3% | 46.3% | 57.6% | 0.344 | 0.334 | 0.355 |
| Ortak − kaleci alanları | Ligler arası percentile | Pearson | 22.6% | 45.9% | 57.2% | 0.340 | 0.356 | 0.324 |
| Ortak (tüm alanlar) | Ligler arası percentile | Pearson | 22.4% | 45.8% | 57.2% | 0.338 | 0.354 | 0.322 |
| Ortak − kaleci alanları | Lig içi percentile | Öklid | 21.5% | 45.0% | 57.2% | 0.332 | 0.351 | 0.312 |
| Ortak − kaleci alanları | Lig içi percentile | Cosine | 20.8% | 44.4% | 56.3% | 0.324 | 0.339 | 0.309 |
| Mevkiye özel | Log per-90, lig farkı ½ | Cosine | 21.0% | 43.5% | 55.3% | 0.322 | 0.337 | 0.306 |
| Mevkiye özel | Per-90 z-skor | Cosine | 21.1% | 43.3% | 55.4% | 0.321 | 0.338 | 0.305 |
| Mevkiye özel | Log per-90, lig farkı ½ | Öklid | 20.9% | 43.2% | 55.2% | 0.319 | 0.330 | 0.307 |
| Mevkiye özel | Per-90 z-skor | Öklid | 20.3% | 43.0% | 55.2% | 0.316 | 0.331 | 0.301 |
| Ortak − kaleci alanları | Lig içi percentile | Pearson | 20.0% | 41.8% | 54.8% | 0.313 | 0.326 | 0.300 |
| Mevkiye özel | Ligler arası percentile | Öklid | 19.6% | 42.2% | 56.0% | 0.310 | 0.324 | 0.296 |
| Mevkiye özel | Log per-90, lig farkı ½ | Pearson | 19.8% | 41.3% | 52.9% | 0.307 | 0.325 | 0.289 |
| Mevkiye özel | Ligler arası percentile | Cosine | 19.4% | 41.5% | 54.3% | 0.304 | 0.318 | 0.289 |
| Mevkiye özel | Per-90 z-skor | Pearson | 19.1% | 41.7% | 52.7% | 0.303 | 0.320 | 0.285 |
| Mevkiye özel | Ligler arası percentile | Pearson | 18.8% | 39.5% | 50.9% | 0.295 | 0.307 | 0.282 |
| Mevkiye özel | Lig içi percentile | Öklid | 18.5% | 39.4% | 52.6% | 0.294 | 0.304 | 0.285 |
| Mevkiye özel | Lig içi percentile | Cosine | 18.3% | 38.9% | 50.2% | 0.288 | 0.305 | 0.272 |
| Mevkiye özel | Lig içi percentile | Pearson | 16.8% | 36.7% | 48.1% | 0.272 | 0.285 | 0.258 |
| Rastgele sıralama |  |  | 0.3% | 1.6% | 3.3% | 0.020 | 0.020 | 0.021 |

## Yöntem karşılaştırması — havuz: sadece hedefin ligi

| Feature seti | Normalizasyon | Metrik | R@1 | R@5 | R@10 | MRR | MRR 23/24 → 24/25 | MRR 24/25 → 25/26 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Ortak (tüm alanlar) | Log per-90, lig farkı ½ | Cosine | 45.7% | 74.4% | 86.2% | 0.590 | 0.598 | 0.582 |
| Ortak (tüm alanlar) | Log per-90, lig farkı ½ | Pearson | 45.9% | 75.0% | 86.0% | 0.590 | 0.601 | 0.579 |
| Ortak − kaleci alanları (mevcut) | Log per-90, lig farkı ½ | Cosine | 44.7% | 74.2% | 85.9% | 0.583 | 0.587 | 0.579 |
| Ortak (tüm alanlar) | Lig içi percentile | Öklid | 44.3% | 74.1% | 86.0% | 0.581 | 0.598 | 0.564 |
| Ortak (tüm alanlar) | Log per-90, lig farkı ½ | Öklid | 44.9% | 74.6% | 85.2% | 0.581 | 0.599 | 0.563 |
| Ortak − kaleci alanları | Log per-90, lig farkı ½ | Pearson | 44.8% | 73.0% | 85.1% | 0.578 | 0.592 | 0.565 |
| Ortak (tüm alanlar) | Ligler arası percentile | Öklid | 43.7% | 74.5% | 86.0% | 0.577 | 0.597 | 0.558 |
| Ortak − kaleci alanları | Lig içi percentile | Öklid | 43.2% | 73.9% | 85.7% | 0.573 | 0.590 | 0.556 |
| Ortak − kaleci alanları | Log per-90, lig farkı ½ | Öklid | 43.6% | 73.9% | 85.1% | 0.573 | 0.592 | 0.554 |
| Ortak (tüm alanlar) | Per-90 z-skor | Cosine | 43.7% | 73.2% | 85.3% | 0.572 | 0.583 | 0.561 |
| Ortak − kaleci alanları | Ligler arası percentile | Öklid | 43.1% | 74.2% | 85.5% | 0.572 | 0.587 | 0.557 |
| Ortak − kaleci alanları | Per-90 z-skor | Cosine | 43.8% | 72.2% | 85.1% | 0.571 | 0.580 | 0.562 |
| Ortak (tüm alanlar) | Lig içi percentile | Cosine | 43.3% | 72.4% | 84.1% | 0.570 | 0.577 | 0.563 |
| Ortak (tüm alanlar) | Per-90 z-skor | Pearson | 43.7% | 72.8% | 84.9% | 0.570 | 0.582 | 0.559 |
| Ortak − kaleci alanları | Per-90 z-skor | Pearson | 43.5% | 72.0% | 83.8% | 0.566 | 0.578 | 0.555 |
| Ortak (tüm alanlar) | Ligler arası percentile | Cosine | 43.0% | 73.0% | 84.0% | 0.565 | 0.578 | 0.553 |
| Ortak − kaleci alanları | Ligler arası percentile | Cosine | 42.8% | 72.8% | 84.1% | 0.565 | 0.575 | 0.555 |
| Ortak − kaleci alanları | Lig içi percentile | Cosine | 42.7% | 72.4% | 83.8% | 0.564 | 0.572 | 0.556 |
| Ortak (tüm alanlar) | Lig içi percentile | Pearson | 41.6% | 72.5% | 84.2% | 0.557 | 0.563 | 0.551 |
| Ortak (tüm alanlar) | Per-90 z-skor | Öklid | 42.2% | 71.8% | 82.8% | 0.554 | 0.574 | 0.534 |
| Ortak (tüm alanlar) | Ligler arası percentile | Pearson | 41.1% | 72.1% | 83.7% | 0.552 | 0.560 | 0.544 |
| Mevkiye özel | Log per-90, lig farkı ½ | Cosine | 40.6% | 72.8% | 85.2% | 0.550 | 0.557 | 0.543 |
| Ortak − kaleci alanları | Ligler arası percentile | Pearson | 40.9% | 71.6% | 83.2% | 0.550 | 0.562 | 0.538 |
| Mevkiye özel | Log per-90, lig farkı ½ | Öklid | 40.5% | 72.3% | 84.3% | 0.549 | 0.549 | 0.550 |
| Ortak − kaleci alanları | Per-90 z-skor | Öklid | 41.2% | 71.6% | 82.5% | 0.547 | 0.563 | 0.531 |
| Ortak − kaleci alanları | Lig içi percentile | Pearson | 40.1% | 72.7% | 84.1% | 0.546 | 0.554 | 0.539 |
| Mevkiye özel | Ligler arası percentile | Öklid | 38.9% | 72.3% | 85.0% | 0.538 | 0.547 | 0.528 |
| Mevkiye özel | Per-90 z-skor | Cosine | 39.8% | 71.2% | 84.3% | 0.538 | 0.544 | 0.533 |
| Mevkiye özel | Lig içi percentile | Öklid | 38.6% | 72.1% | 84.2% | 0.537 | 0.544 | 0.531 |
| Mevkiye özel | Log per-90, lig farkı ½ | Pearson | 38.7% | 70.1% | 83.4% | 0.532 | 0.544 | 0.520 |
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
| Mevcut − önceki (lig içi percentile · Öklid) | +0.010 [-0.003, +0.022] | +0.006 [-0.007, +0.020] | +0.036 [+0.000, +0.072] | -0.003 [-0.017, +0.012] | +0.046 [+0.021, +0.070] |
| Mevcut − ilk sürüm (mevkiye özel · lig içi percentile · cosine) | +0.064 [+0.050, +0.078] | +0.064 [+0.049, +0.079] | +0.062 [+0.022, +0.102] | +0.060 [+0.043, +0.076] | +0.075 [+0.047, +0.104] |
| Normalizasyon: log lig farkı ½ − lig içi percentile (cosine) | +0.019 [+0.008, +0.029] | +0.019 [+0.008, +0.030] | +0.013 [-0.017, +0.043] | +0.015 [+0.003, +0.027] | +0.029 [+0.010, +0.049] |
| Normalizasyon: log lig farkı ½ − per-90 z (cosine) | +0.012 [+0.005, +0.019] | +0.014 [+0.007, +0.021] | -0.003 [-0.023, +0.017] | +0.016 [+0.009, +0.024] | -0.001 [-0.015, +0.013] |
| Metrik: cosine − Öklid (log lig farkı ½) | +0.010 [-0.002, +0.021] | +0.008 [-0.005, +0.021] | +0.022 [-0.010, +0.054] | +0.001 [-0.013, +0.014] | +0.036 [+0.013, +0.060] |
| Metrik: cosine − Öklid (lig içi percentile) | -0.009 [-0.019, +0.001] | -0.013 [-0.023, -0.002] | +0.023 [-0.003, +0.049] | -0.018 [-0.030, -0.006] | +0.016 [-0.002, +0.035] |
| Feature seti: 35 alan − mevkiye özel (log lig farkı ½ · cosine) | +0.033 [+0.019, +0.046] | +0.031 [+0.016, +0.045] | +0.048 [+0.013, +0.083] | +0.032 [+0.016, +0.047] | +0.035 [+0.009, +0.061] |
| Kaleci alanlarını tutmak: tüm alanlar − mevcut | +0.007 [+0.002, +0.012] | +0.008 [+0.003, +0.013] | -0.002 [-0.011, +0.008] | +0.010 [+0.005, +0.016] | -0.003 [-0.012, +0.007] |

## Kırılım: mevcut yöntem (Ortak − kaleci alanları · Log per-90, lig farkı ½ · Cosine)

| Kesit | n | R@1 | R@5 | R@10 | MRR | Medyan sıra | Havuz | Rastgele R@10 | MRR (lig içi havuz) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tümü | 1961 | 25.0% | 48.7% | 60.0% | 0.365 | 6 | 350 | 3.3% | 0.583 |
| Forvet | 193 | 31.1% | 63.7% | 71.0% | 0.452 | 3 | 207 | 4.8% | 0.703 |
| Kanat | 284 | 31.3% | 57.4% | 69.4% | 0.436 | 4 | 269 | 3.7% | 0.646 |
| Merkez orta saha | 582 | 27.7% | 52.2% | 63.7% | 0.397 | 5 | 515 | 1.9% | 0.610 |
| Bek | 361 | 22.4% | 48.2% | 60.1% | 0.345 | 6 | 317 | 3.2% | 0.581 |
| Stoper | 386 | 20.2% | 37.6% | 49.0% | 0.296 | 12 | 348 | 2.9% | 0.488 |
| Kaleci | 155 | 14.2% | 29.7% | 42.6% | 0.230 | 15 | 146 | 6.9% | 0.453 |
| Aynı lig | 1743 | 26.5% | 50.7% | 62.0% | 0.381 | 5 | 352 | 3.3% | 0.598 |
| Lig değiştirdi | 218 | 13.3% | 33.0% | 44.0% | 0.237 | 18 | 336 | 3.4% | 0.460 |
| Aynı takım | 1456 | 29.1% | 52.8% | 63.7% | 0.405 | 5 | 352 | 3.3% | 0.617 |
| Takım değiştirdi | 505 | 13.5% | 36.8% | 49.3% | 0.251 | 11 | 345 | 3.3% | 0.485 |

## Kırılım: en iyi yöntem (Ortak (tüm alanlar) · Log per-90, lig farkı ½ · Pearson)

| Kesit | n | R@1 | R@5 | R@10 | MRR | Medyan sıra | Havuz | Rastgele R@10 | MRR (lig içi havuz) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tümü | 1961 | 27.5% | 48.9% | 59.6% | 0.381 | 6 | 350 | 3.3% | 0.590 |
| Forvet | 193 | 37.8% | 64.8% | 74.6% | 0.500 | 3 | 207 | 4.8% | 0.722 |
| Kanat | 284 | 33.8% | 59.9% | 69.4% | 0.457 | 4 | 269 | 3.7% | 0.671 |
| Merkez orta saha | 582 | 30.4% | 51.7% | 62.9% | 0.410 | 5 | 515 | 1.9% | 0.606 |
| Bek | 361 | 24.9% | 48.8% | 59.6% | 0.366 | 6 | 317 | 3.2% | 0.594 |
| Stoper | 386 | 20.5% | 38.1% | 48.4% | 0.297 | 12 | 348 | 2.9% | 0.497 |
| Kaleci | 155 | 15.5% | 25.8% | 38.7% | 0.225 | 15 | 146 | 6.9% | 0.441 |
| Aynı lig | 1743 | 29.0% | 50.7% | 62.0% | 0.398 | 5 | 352 | 3.3% | 0.605 |
| Lig değiştirdi | 218 | 15.1% | 34.4% | 40.8% | 0.241 | 16 | 336 | 3.4% | 0.468 |
| Aynı takım | 1456 | 31.1% | 52.7% | 64.1% | 0.419 | 5 | 352 | 3.3% | 0.627 |
| Takım değiştirdi | 505 | 17.0% | 37.8% | 46.5% | 0.271 | 12 | 345 | 3.3% | 0.485 |
