## Ligler arası arama: lig farkı düzeltmesi (α) · Ortak − kaleci alanları · Log per-90 + PAdj, lig farkı ½ · Cosine

Lig içi havuz MRR (sütunlar kesit). "Tüm-lig havuzu" = filtresiz arama, hedef lig değiştirmiş. Fark = önceki yönteme göre MRR farkı ve %95 bootstrap aralığı.
Son sütun: 25/26'da filtresiz arama, ilk 10 sonucun sorgunun liginden olan payı; havuzdaki pay (yansız arama) 16.6%.

| Yöntem | Tümü | Aynı lig | Lig değiştirdi | Takım değiştirdi | Lig değiştirdi 23/24 → 24/25 | Lig değiştirdi 24/25 → 25/26 | Lig değiştirdi · tüm-lig havuzu | Fark: lig değiştirdi | İlk 10'da kendi ligi |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Önceki: Lig içi percentile · Öklid | 0.573 | 0.592 | 0.424 | 0.440 | 0.463 | 0.385 | 0.235 | — | 15.8% |
| α = 0 | 0.576 | 0.591 | 0.456 | 0.487 | 0.477 | 0.436 | 0.248 | +0.032 [-0.005, +0.070] | 22.3% |
| α = 0.25 | 0.581 | 0.596 | 0.463 | 0.495 | 0.485 | 0.441 | 0.243 | +0.039 [+0.004, +0.075] | 19.2% |
| α = 0.5 (mevcut) | 0.585 | 0.599 | 0.468 | 0.492 | 0.480 | 0.455 | 0.239 | +0.044 [+0.010, +0.079] | 17.1% |
| α = 0.75 | 0.585 | 0.601 | 0.459 | 0.488 | 0.476 | 0.442 | 0.233 | +0.035 [+0.002, +0.068] | 15.8% |
| α = 1 | 0.583 | 0.599 | 0.456 | 0.482 | 0.469 | 0.444 | 0.228 | +0.032 [-0.002, +0.067] | 15.5% |
