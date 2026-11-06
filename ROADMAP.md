# Yol Haritası

İş bitince `[x]` yap ve tarihi yaz. Sıradaki işler öncelik sırasıyla.

## Sıradaki

1. [ ] **Model · Çok sezonlu profil.** Son 2–3 sezonun dakikaya göre ağırlıklı ortalaması; tek sezonluk
   gürültüyü azaltır. Veri hazır (18 lig-sezon), yeni çekim gerekmiyor.
   *Bitti sayılır:* eval'de tek sezonluk profile göre MRR farkı ölçüldü.
2. [ ] **Model · Takım etkisini ayıkla.** Takım/lig değiştirenlerde MRR 0.57 → ~0.43 düşüyor; profilin bir kısmı
   takımın oyun tarzından geliyor. Savunma/pas istatistiklerini topa sahip olma oranına göre düzelt.
   Önce takım istatistiği verisi (topa sahip olma) bulunmalı.
   *Bitti sayılır:* "Takım değiştirdi" kesitinde MRR iyileşmesi ölçüldü.
3. [ ] **Model · Az dakikalı genç oyuncular.** 900 dk eşiği aradığımız gençleri eliyor. Az oynayanları mevki
   ortalamasına doğru çek (shrinkage), sonuçta güven göstergesi göster.
4. [ ] **Model · Rol kümeleme.** KMeans/GMM ile rol etiketleri ("derin oyun kurucu", "box-to-box" ...), rol içi arama.
5. [ ] **Veri · Sezon bazlı mevki.** Mevki şu an çekim anındaki profilden geliyor; sezon içinde mevki değiştiren
   oyuncu yanlış grupta aranabiliyor.
6. [ ] **Mühendislik · Birim testleri.** Per-90, percentile, "katkılar toplamı = benzerlik", NaN (veri yok) davranışı,
   arama servisi ile eval'in aynı sıralamayı vermesi.
7. [ ] **Ürün · Shortlist + CSV dışa aktarma.**
8. [ ] **Ürün · Supabase'e arama logu** (hangi oyuncular, hangi filtrelerle aranıyor).
9. [ ] **Ürün · Sezonlar arası gelişim.** Oyuncunun 23/24 → 25/26 percentile değişimini gösteren sayfa.
10. [ ] **Mühendislik · GitHub'a gönder.** Remote yok; ham veri `.gitignore`'da, sadece kod + türetilmiş sonuçlar.

## Tamamlananlar

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
