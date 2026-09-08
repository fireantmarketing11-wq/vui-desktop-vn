"""Quản lý truyện cười tiếng Việt"""
import random
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA_DIR = BASE / "data"
JOKES_FILE = DATA_DIR / "jokes_vn.txt"


def _load_jokes():
    try:
        txt = JOKES_FILE.read_text(encoding="utf-8")
        # các truyện cách nhau bằng dòng trống
        parts = [p.strip() for p in txt.split("\n\n") if p.strip()]
        return parts
    except Exception:
        return ["Chưa có truyện cười (file lỗi hoặc chưa có dữ liệu)"]


_jokes = _load_jokes()


def get_random_joke():
    return random.choice(_jokes)


def get_all_jokes():
    return list(_jokes)
