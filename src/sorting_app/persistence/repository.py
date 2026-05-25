"""Persist T-shirt collections as JSON."""

from __future__ import annotations

import json
from pathlib import Path

from sorting_app.models import TShirt


class TShirtRepository:
    """File-based repository for T-shirt collections."""

    def __init__(self, base_dir: Path | str = "data") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def path_for(self, name: str) -> Path:
        return self.base_dir / f"{name}.json"

    def save(self, name: str, items: list[TShirt]) -> Path:
        path = self.path_for(name)
        payload = [item.to_dict() for item in items]
        path.write_text(json.dumps(payload, indent=2))
        return path

    def load(self, name: str) -> list[TShirt]:
        path = self.path_for(name)
        if not path.exists():
            raise FileNotFoundError(f"no saved collection named '{name}' at {path}")
        data = json.loads(path.read_text())
        return [TShirt.from_dict(entry) for entry in data]

    def list_collections(self) -> list[str]:
        return sorted(p.stem for p in self.base_dir.glob("*.json"))
