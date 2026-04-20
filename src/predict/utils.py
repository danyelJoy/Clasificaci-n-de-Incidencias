from __future__ import annotations

import csv
from pathlib import Path
from datetime import datetime
from typing import Any


FIELDS = [
    "timestamp",
    "ticket_text",
    "category",
    "confidence",
    "confidence_status",
    "priority",
    "reason",
]


def ensure_csv_exists(csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    if not csv_path.exists():
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()


def save_confidence(value: Any)-> float:
    """Convertir la confianza a float de forma segura"""
    try:
        return round(float(value), 4)
    except(TypeError, ValueError):
        return 0.0
print("DEBUG UTILS FILE CARGADO")
def append_prediction_to_csv(csv_path: Path, ticket_text: str, result: dict ) -> None:
    ensure_csv_exists(csv_path)

    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "ticket_text": ticket_text,
        "category": result.get("category", "unknown"),
        "confidence": save_confidence(result.get("confidence", 0.0)),
        "confidence_status": result.get("confidence_status", "unknown"),
        "priority":  result.get("priority", "unknown"),
        "reason": result.get("reason", "")
    }
 
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(row)


