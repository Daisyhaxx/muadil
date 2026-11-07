## Takım etkisi: topa sahip olma düzeltmesi · Ortak − kaleci alanları · Log per-90 + PAdj, lig farkı ½ · Cosine

### Esneklik: savunma alanı ~ rakibin topa sahip olması

Aynı ligde takım değiştiren saha oyuncuları (n = 338 oyuncu-çift; topa sahip olma değişimi ort. 5.2 puan). Eğim = Δlog(istatistik) / Δlog(1 − p); standart PAdj 1 varsayar. Köşeli parantez: %95 bootstrap aralığı. `outfielderBlocks` 24/25'te olmadığı için ölçülemiyor (düzeltme yine uygulanıyor).

| Alan | n | Eğim | 23/24 → 24/25 | 24/25 → 25/26 |
|---|---:|---:|---:|---:|
| tackles | 338 | 0.29 [0.04, 0.56] | 0.26 | 0.27 |
| interceptions | 338 | 0.21 [-0.19, 0.63] | 0.31 | 0.11 |
| clearances | 338 | 0.62 [0.25, 0.99] | 0.58 | 0.55 |
| ballRecovery | 338 | 0.22 [0.03, 0.41] | 0.29 | 0.23 |
| possessionWonAttThird | 338 | 0.16 [-0.32, 0.63] | 0.05 | 0.28 |
| dribbledPast | 338 | 0.44 [0.08, 0.82] | 0.66 | 0.26 |

### Retrieval: lig içi havuz MRR

Savunma alanları × (0,5 / (1 − p))^β. Fark = β = 0'a göre MRR farkı, %95 bootstrap aralığı.

| Düzeltme | Tümü (n=1961) | Aynı takım (n=1456) | Takım değiştirdi (n=505) | Takım değiştirdi · aynı lig (n=354) | Fark: Tümü | Fark: Takım değiştirdi |
|---|---:|---:|---:|---:|---:|---:|
| β = 0 (düzeltme yok) | 0.583 | 0.617 | 0.485 | 0.507 | — | — |
| β = 0.3 (mevcut) | 0.585 | 0.617 | 0.492 | 0.512 | +0.002 [-0.001, +0.005] | +0.007 [-0.000, +0.014] |
| β = 0.5 | 0.583 | 0.614 | 0.492 | 0.513 | +0.000 [-0.004, +0.004] | +0.007 [-0.002, +0.015] |
| β = 1 (standart PAdj) | 0.581 | 0.614 | 0.486 | 0.512 | -0.002 [-0.007, +0.003] | +0.001 [-0.011, +0.012] |
