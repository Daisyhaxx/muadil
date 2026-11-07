# Yol Haritası

İş bitince `[x]` yap ve tarihi yaz. Sıradaki işler öncelik sırasıyla.

## Sıradaki

1. [ ] **Model · Takım etkisini ayıkla.** Takım değiştirenlerde MRR 0.62 → 0.49, lig değiştirenlerde 0.46
   (aynı takımda kalanlara göre); profilin bir kısmı takımın oyun tarzından geliyor. Savunma/pas istatistiklerini
   topa sahip olma oranına göre düzelt. Önce takım istatistiği verisi (topa sahip olma) bulunmalı.
   *Bitti sayılır:* "Takım değiştirdi" kesitinde MRR iyileşmesi ölçüldü.
2. [ ] **Model · Az dakikalı genç oyuncular.** 900 dk eşiği aradığımız gençleri eliyor. Az oynayanları mevki
   ortalamasına doğru çek (shrinkage), sonuçta güven göstergesi göster.
3. [ ] **Model · Rol kümeleme.** KMeans/GMM ile rol etiketleri ("derin oyun kurucu", "box-to-box" ...), rol içi arama.
4. [ ] **Veri · Sezon bazlı mevki.** Mevki şu an çekim anındaki profilden geliyor; sezon içinde mevki değiştiren
   oyuncu yanlış grupta aranabiliyor.
5. [ ] **Mühendislik · Birim testleri.** Per-90, percentile, "katkılar toplamı = benzerlik", NaN (veri yok) davranışı,
   arama servisi ile eval'in aynı sıralamayı vermesi.
6. [ ] **Ürün · Shortlist + CSV dışa aktarma.**
7. [ ] **Ürün · Supabase'e arama logu** (hangi oyuncular, hangi filtrelerle aranıyor).
8. [ ] **Ürün · Sezonlar arası gelişim.** Oyuncunun 23/24 → 25/26 percentile değişimini gösteren sayfa.
9. [ ] **Mühendislik · GitHub'a gönder.** Remote yok; ham veri `.gitignore`'da, sadece kod + türetilmiş sonuçlar.
10. [ ] **Veri · 22/23 sezonu.** 3 sezonluk profili test etmek için. 6 lig; çekimi 2 güne böl.

## Tamamlananlar

- [x] Ligler arası arama: log per-90, lig farkı ½ (α = 0,5) + cosine. Önceki yönteme (lig içi percentile · Öklid)
  göre lig değiştirenlerde MRR 0.424 → 0.460 (+0.036 [+0.000, +0.072]), takım değiştirenlerde 0.440 → 0.485
  (+0.046), genelde 0.573 → 0.583, kayıp yok. Eski "per-90 daha iyi" bulgusunun yarısı metrikten (cosine) çıktı.
  α = 0,5'te filtresiz aramanın lig yanlılığı sıfır (`src.eval.league_eval`) (07.11.2026)
- [x] Çok sezonlu profil: güncel + önceki sezon, dakika ağırlıklı, önceki sezon ×0,5. Sorgu tarafında lig içi MRR
  +0.030 [+0.019, +0.041], geçmişi olan oyuncularda +0.050. Radar ve percentile'lar da iki sezonluk (07.11.2026)
- [x] Arama yöntemi güncellendi: 35 alan (saha oyuncusunda kaleci alanları hariç) + Öklid. Lig içi MRR
  0.519 → 0.573, R@10 %83 → %86. Radar mevkiye özel seti göstermeye devam ediyor (06.11.2026)
- [x] TFF 1. Lig'de xG/xA "veri yok" (NaN) olarak işaretlendi; radarda gösterilmiyor (06.11.2026)
- [x] Git: ilk commit (06.11.2026)
- [x] Geçmiş sezonlar (23/24, 24/25) + sezonlar arası retrieval değerlendirmesi (21.10.2026)
- [x] FastAPI + web arayüzü (radar, karşılaştırma, paylaşılabilir link)
- [x] Mevkiye özel feature setleri + benzerlik açıklaması + radar PNG
- [x] 6 ligin 25/26 sezonu (17.10.2026)
- [x] Per-90 + mevki içi percentile + cosine + filtreler, CLI
- [x] Süper Lig 25/26 tam çekim, cache'li (15.10.2026)
- [x] Veri erişimi doğrulandı (15.10.2026)
