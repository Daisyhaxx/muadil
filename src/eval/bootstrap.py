"""İki yöntemin aynı sorgulardaki farkı için eşleştirilmiş bootstrap güven aralığı."""
import numpy as np
import pandas as pd

RESAMPLES = 10_000
CHUNK = 500  # bellek: CHUNK × sorgu sayısı indeks


def mrr_difference(a: pd.Series, b: pd.Series, seed: int = 0) -> tuple[float, float, float]:
    """a, b: aynı sorguların sıraları (aynı sırada). Döner: (MRR farkı a − b, %95 alt, %95 üst)."""
    diff = 1 / a.to_numpy(dtype=float) - 1 / b.to_numpy(dtype=float)
    rng = np.random.default_rng(seed)
    means = np.concatenate([diff[rng.integers(0, len(diff), (CHUNK, len(diff)))].mean(axis=1)
                            for _ in range(RESAMPLES // CHUNK)])
    return float(diff.mean()), float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def format_difference(result: tuple[float, float, float]) -> str:
    mean, low, high = result
    return f"{mean:+.3f} [{low:+.3f}, {high:+.3f}]"
