#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FOUNDATION_DIR = ROOT / "foundation"
OUTPUT_PATH = FOUNDATION_DIR / "asset_manager_master.csv"
MANUAL_ENTRIES_PATH = FOUNDATION_DIR / "asset_manager_manual_entries.json"

MACRO_OVERRIDES = {
    "EdRAM": {
        "fed_year_end_rate_2026_status": "qualitative",
        "fed_year_end_rate_2026_why": "Fed may become more accommodative after Powell.",
        "fed_year_end_rate_2026_page": "10",
        "fed_year_end_rate_2026_raw_wording": "il parait raisonnable d’envisager une banque centrale plus accommodante",
        "ecb_deposit_rate_year_end_2026_status": "qualitative",
        "ecb_deposit_rate_year_end_2026_why": "ECB may need to ease if euro appreciation hurts competitiveness.",
        "ecb_deposit_rate_year_end_2026_page": "10",
        "ecb_deposit_rate_year_end_2026_raw_wording": "la BCE pourrait etre contrainte d’assouplir sa politique si la Fed engage une nouvelle baisse de taux",
        "eur_usd_2026_status": "qualitative",
        "eur_usd_2026_why": "Dollar weakness is a live axis; EUR/USD is discussed around 1.16 to 1.19.",
        "eur_usd_2026_page": "12",
        "eur_usd_2026_raw_wording": "Il a finalement atteint 1,19 en seance, mais evolue depuis le mois de juillet autour de 1,16.",
    }
}


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def read_manual_entries(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a list of objects")
    return [dict(item) for item in data]


def base_topic_columns(topic_id: str) -> list[str]:
    return [
        f"{topic_id}_view",
        f"{topic_id}_why",
        f"{topic_id}_page",
        f"{topic_id}_raw_wording",
    ]


def base_metric_columns(metric_id: str) -> list[str]:
    return [
        f"{metric_id}_status",
        f"{metric_id}_value",
        f"{metric_id}_why",
        f"{metric_id}_page",
        f"{metric_id}_raw_wording",
    ]


def default_cell_value(fieldname: str) -> str:
    if fieldname.endswith("_status") or fieldname.endswith("_view"):
        return "ND"
    return ""


def normalize_view(fieldname: str, value: str) -> str:
    normalized = (value or "").strip() or "ND"
    if normalized == "ND":
        return "ND"

    if fieldname == "fixed_income_duration_view":
        duration_map = {
            "positive": "long",
            "negative": "short",
            "overweight": "long",
            "underweight": "short",
        }
        return duration_map.get(normalized, normalized)

    directional_map = {
        "overweight": "positive",
        "underweight": "negative",
    }
    return directional_map.get(normalized, normalized)


def normalize_macro_field(row: dict[str, str], metric_id: str) -> None:
    status_key = f"{metric_id}_status"
    value_key = f"{metric_id}_value"
    why_key = f"{metric_id}_why"
    page_key = f"{metric_id}_page"
    raw_key = f"{metric_id}_raw_wording"

    status = (row.get(status_key) or "").strip() or "ND"
    row[status_key] = status

    if status == "qualitative":
        row[value_key] = ""
        return

    if status == "ND":
        row[value_key] = ""
        row[why_key] = ""
        row[page_key] = ""
        row[raw_key] = ""


def normalize_topic_field(row: dict[str, str], topic_id: str) -> None:
    view_key = f"{topic_id}_view"
    why_key = f"{topic_id}_why"
    page_key = f"{topic_id}_page"
    raw_key = f"{topic_id}_raw_wording"

    row[view_key] = normalize_view(view_key, row.get(view_key, ""))
    if row[view_key] == "ND":
        row[why_key] = ""
        row[page_key] = ""
        row[raw_key] = ""


def main() -> int:
    macro_headers, macro_rows = read_csv_rows(FOUNDATION_DIR / "macro_master.csv")
    _, positioning_rows = read_csv_rows(FOUNDATION_DIR / "positioning_master.csv")
    manual_entries = read_manual_entries(MANUAL_ENTRIES_PATH)

    metric_ids = [header[: -len("_value")] for header in macro_headers if header.endswith("_value")]
    topic_ids: list[str] = []
    seen_topics: set[str] = set()
    for row in positioning_rows:
        topic_id = row["topic_id"]
        if topic_id not in seen_topics:
            seen_topics.add(topic_id)
            topic_ids.append(topic_id)

    fieldnames = [
        "manager",
        "group",
        "source_file",
        "source_type",
        "aum_label",
        "markets",
    ]
    for metric_id in metric_ids:
        fieldnames.extend(base_metric_columns(metric_id))
    for topic_id in topic_ids:
        fieldnames.extend(base_topic_columns(topic_id))

    combined: dict[str, dict[str, str]] = {}

    for row in macro_rows:
        manager = row["manager"]
        source_file = row["source_file"]
        combined[manager] = {
            "manager": manager,
            "group": row["group"],
            "source_file": source_file,
            "source_type": Path(source_file).suffix.lower().lstrip("."),
            "aum_label": "",
            "markets": "",
        }
        for metric_id in metric_ids:
            value = (row.get(f"{metric_id}_value") or "").strip()
            combined[manager][f"{metric_id}_status"] = "quantitative" if value else "ND"
            combined[manager][f"{metric_id}_value"] = value
            combined[manager][f"{metric_id}_why"] = (row.get(f"{metric_id}_why") or "").strip()
            combined[manager][f"{metric_id}_page"] = (row.get(f"{metric_id}_page") or "").strip()
            combined[manager][f"{metric_id}_raw_wording"] = (row.get(f"{metric_id}_raw_wording") or "").strip()

    for row in positioning_rows:
        manager = row["manager"]
        topic_id = row["topic_id"]
        view = (row["view"] or "").strip() or "ND"
        combined.setdefault(
            manager,
            {
                "manager": manager,
                "group": row["group"],
                "source_file": row["source_file"],
                "source_type": Path(row["source_file"]).suffix.lower().lstrip("."),
                "aum_label": "",
                "markets": "",
            },
        )
        combined[manager][f"{topic_id}_view"] = view
        combined[manager][f"{topic_id}_why"] = (row["why"] or "").strip()
        combined[manager][f"{topic_id}_page"] = (row["page"] or "").strip()
        combined[manager][f"{topic_id}_raw_wording"] = (row["raw_wording"] or "").strip()

    for entry in manual_entries:
        manager = (entry.get("manager") or "").strip()
        if not manager:
            raise ValueError("Manual entries must include a non-empty 'manager'")

        row = combined.setdefault(
            manager,
            {field: default_cell_value(field) for field in fieldnames},
        )
        row["manager"] = manager

        for key, value in entry.items():
            if key not in fieldnames:
                raise ValueError(f"Unknown field in manual entry for {manager}: {key}")
            row[key] = (value or "").strip()

        source_file = row.get("source_file", "")
        if source_file and not row.get("source_type"):
            row["source_type"] = Path(source_file).suffix.lower().lstrip(".")

    for row in combined.values():
        for field in fieldnames:
            row.setdefault(field, default_cell_value(field))
        for metric_id in metric_ids:
            normalize_macro_field(row, metric_id)
        for topic_id in topic_ids:
            normalize_topic_field(row, topic_id)

    for manager, overrides in MACRO_OVERRIDES.items():
        if manager not in combined:
            continue
        combined[manager].update(overrides)
        for metric_id in metric_ids:
            normalize_macro_field(combined[manager], metric_id)

    ordered_rows = sorted(
        combined.values(),
        key=lambda row: (row["group"], row["manager"]),
    )

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ordered_rows)

    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
