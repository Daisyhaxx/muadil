"""Proje geneli veri yolları.

Veri, OneDrive senkronizasyonuna girmesin diye repo dışında tutulur.
Varsayılan: ~/player-data. Değiştirmek için PLAYER_DATA_DIR ortam değişkeni.
"""
import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("PLAYER_DATA_DIR", Path.home() / "player-data"))
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
