## Yöntem karşılaştırması — havuz: tüm ligler

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

## Yöntem karşılaştırması — havuz: sadece hedefin ligi

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

## Kırılım: mevcut yöntem (Ortak − kaleci alanları · Lig içi percentile · Öklid)

| Kesit | n | R@1 | R@5 | R@10 | MRR | Medyan sıra | Havuz | Rastgele R@10 | MRR (lig içi havuz) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tümü | 1961 | 21.1% | 45.2% | 57.2% | 0.329 | 7 | 350 | 3.3% | 0.573 |
| Forvet | 193 | 30.6% | 56.0% | 66.8% | 0.424 | 4 | 207 | 4.8% | 0.666 |
| Kanat | 284 | 24.6% | 53.2% | 64.1% | 0.376 | 5 | 269 | 3.7% | 0.627 |
| Merkez orta saha | 582 | 22.2% | 47.1% | 60.5% | 0.348 | 6 | 515 | 1.9% | 0.603 |
| Bek | 361 | 19.9% | 45.2% | 56.8% | 0.320 | 8 | 317 | 3.2% | 0.568 |
| Stoper | 386 | 16.3% | 37.0% | 47.9% | 0.270 | 11 | 348 | 2.9% | 0.491 |
| Kaleci | 155 | 12.9% | 30.3% | 43.9% | 0.228 | 15 | 146 | 6.9% | 0.459 |
| Aynı lig | 1743 | 21.7% | 47.3% | 59.7% | 0.342 | 6 | 352 | 3.3% | 0.591 |
| Lig değiştirdi | 218 | 15.6% | 28.0% | 37.2% | 0.231 | 22 | 336 | 3.4% | 0.424 |
| Aynı takım | 1456 | 24.4% | 50.3% | 62.3% | 0.370 | 5 | 352 | 3.3% | 0.619 |
| Takım değiştirdi | 505 | 11.5% | 30.5% | 42.4% | 0.214 | 16 | 345 | 3.3% | 0.438 |

## Kırılım: en iyi yöntem (Ortak (tüm alanlar) · Lig içi percentile · Öklid)

| Kesit | n | R@1 | R@5 | R@10 | MRR | Medyan sıra | Havuz | Rastgele R@10 | MRR (lig içi havuz) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tümü | 1961 | 24.2% | 48.0% | 60.0% | 0.362 | 6 | 350 | 3.3% | 0.580 |
| Forvet | 193 | 26.9% | 48.2% | 60.6% | 0.379 | 6 | 207 | 4.8% | 0.681 |
| Kanat | 284 | 26.1% | 53.2% | 64.8% | 0.392 | 4 | 269 | 3.7% | 0.636 |
| Merkez orta saha | 582 | 31.1% | 57.7% | 67.4% | 0.437 | 4 | 515 | 1.9% | 0.610 |
| Bek | 361 | 21.3% | 44.0% | 58.4% | 0.333 | 7 | 317 | 3.2% | 0.574 |
| Stoper | 386 | 18.4% | 40.4% | 52.8% | 0.298 | 9 | 348 | 2.9% | 0.498 |
| Kaleci | 155 | 12.9% | 30.3% | 43.9% | 0.228 | 15 | 146 | 6.9% | 0.459 |
| Aynı lig | 1743 | 25.6% | 50.9% | 63.3% | 0.381 | 5 | 352 | 3.3% | 0.601 |
| Lig değiştirdi | 218 | 13.3% | 24.8% | 33.0% | 0.207 | 30 | 336 | 3.4% | 0.415 |
| Aynı takım | 1456 | 28.5% | 54.4% | 66.9% | 0.412 | 4 | 352 | 3.3% | 0.632 |
| Takım değiştirdi | 505 | 11.9% | 29.7% | 40.0% | 0.217 | 17 | 345 | 3.3% | 0.431 |
