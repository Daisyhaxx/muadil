"""Değerlendirme sonuçlarının markdown tabloları."""
import pandas as pd

from ..features.positions import GROUP_LABELS
from .bootstrap import format_difference, mrr_difference
from .metrics import random_baseline, summarize
from .variants import BASELINE, Variant


def _fmt(column: str, value: float) -> str:
    if column.startswith("R@"):
        return f"{value * 100:.1f}%"
    if column.startswith("MRR"):
        return f"{value:.3f}"
    return f"{value:.0f}"


def _metric_cells(summary: dict[str, float], columns: list[str]) -> dict[str, str]:
    return {c: _fmt(c, summary[c]) for c in columns}


def markdown_table(rows: list[dict[str, str]], text_columns: int = 1) -> str:
    """İlk `text_columns` sütun sola, kalanlar (sayılar) sağa hizalı."""
    columns = list(rows[0])
    align = ["---" if i < text_columns else "---:" for i in range(len(columns))]
    lines = [f"| {' | '.join(columns)} |", f"|{'|'.join(align)}|"]
    lines += [f"| {' | '.join(row[c] for c in columns)} |" for row in rows]
    return "\n".join(lines)


def comparison_table(
    results: dict[Variant, pd.DataFrame], pair_labels: list[str],
    rank: str = "rank", pool_size: str = "pool_size",
) -> str:
    """Tüm yöntemler, sezon çiftleri birlikte; MRR'a göre sıralı. Çiftlerin MRR'ı ayrıca."""
    metrics = ["R@1", "R@5", "R@10", "MRR"]
    rows = []
    for variant, ranks in results.items():
        feature_set, normalization, metric = variant.labels
        if variant == BASELINE:
            feature_set += " (mevcut)"
        row = {"Feature seti": feature_set, "Normalizasyon": normalization, "Metrik": metric}
        row |= _metric_cells(summarize(ranks[rank]), metrics)
        for label in pair_labels:
            row[f"MRR {label}"] = _fmt("MRR", summarize(ranks.loc[ranks.pair == label, rank])["MRR"])
        rows.append(row)
    rows.sort(key=lambda r: float(r["MRR"]), reverse=True)

    any_ranks = next(iter(results.values()))
    random = {"Feature seti": "Rastgele sıralama", "Normalizasyon": "", "Metrik": ""}
    random |= _metric_cells(random_baseline(any_ranks[pool_size]), metrics)
    for label in pair_labels:
        pool = any_ranks.loc[any_ranks.pair == label, pool_size]
        random[f"MRR {label}"] = _fmt("MRR", random_baseline(pool)["MRR"])
    return markdown_table(rows + [random], text_columns=3)


def _slices(ranks: pd.DataFrame) -> list[tuple[str, pd.DataFrame]]:
    slices = [("Tümü", ranks)]
    slices += [(GROUP_LABELS[g], ranks[ranks.position_group == g]) for g in GROUP_LABELS]
    slices += [
        ("Aynı lig", ranks[~ranks.changed_league]),
        ("Lig değiştirdi", ranks[ranks.changed_league]),
        ("Aynı takım", ranks[~ranks.changed_team]),
        ("Takım değiştirdi", ranks[ranks.changed_team]),
    ]
    return [(name, part) for name, part in slices if len(part)]


def difference_table(results: dict[Variant, pd.DataFrame], comparisons: list[tuple[str, Variant, Variant]]) -> str:
    """Lig içi havuzda MRR farkı a − b ve %95 eşleştirilmiş bootstrap aralığı; tüm sorgular ve kesitler."""
    rows = []
    for label, a, b in comparisons:
        ra, rb = results[a], results[b]
        row = {"Karşılaştırma": label}
        for name, part in _slices(ra):
            if name in GROUP_LABELS.values():
                continue
            row[f"{name} (n={len(part)})"] = format_difference(
                mrr_difference(ra.loc[part.index, "league_rank"], rb.loc[part.index, "league_rank"]))
        rows.append(row)
    return markdown_table(rows)


def breakdown_table(ranks: pd.DataFrame) -> str:
    """Mevki grubu, lig/takım değişikliği kırılımı. Havuz = ortalama aday sayısı (tüm ligler)."""
    metrics = ["n", "R@1", "R@5", "R@10", "MRR", "Medyan sıra"]
    rows = []
    for name, part in _slices(ranks):
        row = {"Kesit": name} | _metric_cells(summarize(part["rank"]), metrics)
        row["Havuz"] = f"{part.pool_size.mean():.0f}"
        row["Rastgele R@10"] = _fmt("R@10", random_baseline(part.pool_size)["R@10"])
        row["MRR (lig içi havuz)"] = _fmt("MRR", summarize(part["league_rank"])["MRR"])
        rows.append(row)
    return markdown_table(rows)
