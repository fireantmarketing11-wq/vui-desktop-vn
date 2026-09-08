"""Quản lý mẫu emoji art"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA_DIR = BASE / "data"
TEMPLATES_FILE = DATA_DIR / "emoji_templates.json"


def _load_templates():
    try:
        with open(TEMPLATES_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            return {item["name"]: item["art"] for item in data}
    except Exception:
        return {}


_templates = _load_templates()


def get_template_names():
    return list(_templates.keys())


def generate(name: str) -> str:
    return _templates.get(name, "")
