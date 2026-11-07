## Ligler arası arama: lig farkı düzeltmesi (α) · Ortak − kaleci alanları · Log per-90, lig farkı ½ · Cosine

Lig içi havuz MRR (sütunlar kesit). "Tüm-lig havuzu" = filtresiz arama, hedef lig değiştirmiş. Fark = önceki yönteme göre MRR farkı ve %95 bootstrap aralığı.
Son sütun: 25/26'da filtresiz arama, ilk 10 sonucun sorgunun liginden olan payı; havuzdaki pay (yansız arama) 16.6%.

| Yöntem | Tümü | Aynı lig | Lig değiştirdi | Takım değiştirdi | Lig değiştirdi 23/24 → 24/25 | Lig değiştirdi 24/25 → 25/26 | Lig değiştirdi · tüm-lig havuzu | Fark: lig değiştirdi | İlk 10'da kendi ligi |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Önceki: Lig içi percentile · Öklid | 0.573 | 0.592 | 0.424 | 0.440 | 0.463 | 0.385 | 0.235 | — | 15.8% |
| α = 0 | 0.577 | 0.592 | 0.457 | 0.487 | 0.475 | 0.438 | 0.246 | +0.033 [-0.005, +0.069] | 22.4% |
| α = 0.25 | 0.582 | 0.597 | 0.461 | 0.488 | 0.479 | 0.443 | 0.243 | +0.037 [+0.000, +0.073] | 19.3% |
| α = 0.5 (mevcut) | 0.583 | 0.598 | 0.460 | 0.485 | 0.472 | 0.449 | 0.237 | +0.036 [+0.000, +0.072] | 16.9% |
| α = 0.75 | 0.582 | 0.598 | 0.452 | 0.480 | 0.467 | 0.437 | 0.231 | +0.028 [-0.006, +0.061] | 15.8% |
| α = 1 | 0.582 | 0.598 | 0.453 | 0.479 | 0.463 | 0.442 | 0.221 | +0.029 [-0.006, +0.063] | 15.4% |
