"""Paylaşılan arama servisi. Veri ilk istekte bir kez yüklenir; yeni lig inince /api/reload."""
from functools import lru_cache

from src.similarity.service import SimilarityService


@lru_cache
def get_service() -> SimilarityService:
    return SimilarityService()
