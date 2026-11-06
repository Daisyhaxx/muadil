"""Retrieval metrikleri: recall@k, MRR ve rastgele sıralamanın beklenen değerleri."""
import numpy as np
import pandas as pd

KS = (1, 5, 10)


def summarize(ranks: pd.Series) -> dict[str, float]:
    out = {"n": len(ranks)}
    out.update({f"R@{k}": float((ranks <= k).mean()) for k in KS})
    out["MRR"] = float((1 / ranks).mean())
    out["Medyan sıra"] = float(ranks.median())
    return out


def random_baseline(pool_sizes: pd.Series) -> dict[str, float]:
    """Hedef havuzda rastgele bir sırada olsaydı (sorgu başına kendi havuz büyüklüğüyle)."""
    sizes = pool_sizes.to_numpy(dtype=int)
    harmonic = np.cumsum(1 / np.arange(1, sizes.max() + 1))
    out = {"n": len(sizes)}
    out.update({f"R@{k}": float(np.mean(np.minimum(k / sizes, 1))) for k in KS})
    out["MRR"] = float(np.mean(harmonic[sizes - 1] / sizes))
    out["Medyan sıra"] = float(np.median((sizes + 1) / 2))
    return out
