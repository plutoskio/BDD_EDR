#!/usr/bin/env python3
"""Build a transparent client x fund prospect-scoring matrix from CRM_2025.xlsx.

The engine is intentionally rule-based rather than predictive. It ranks where
Sales should focus first given the current installed base, channel patterns, and
product fit visible in the CRM snapshot.
"""

from __future__ import annotations

import csv
import json
import math
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path


NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
GENERIC_TAGS = {"equity", "fixed_income", "multi_asset", "alternatives"}

SEGMENT_CAPABILITY = {
    "Insurance Company / Own Account": 0.95,
    "Sovereign / Pension Fund": 0.95,
    "Pension Fund / Other": 0.90,
    "Pension Fund / Employee Saving Scheme": 0.85,
    "AM company / Own account": 0.90,
    "AM company / Fund of Funds": 0.90,
    "AM company / EdR Fund of Funds": 0.90,
    "AM company / Independant": 0.80,
    "Insurance Company / Retirement Scheme": 0.80,
    "Insurance Company / Mutuelle": 0.75,
    "Insurance Company / Unit Link": 0.70,
    "Bank / EdR Private Banking": 0.70,
    "Bank / Private Banking": 0.65,
    "Single Family Office": 0.65,
    "Multi Familly Office / Wealth manager": 0.65,
    "Independant Financial Advisor": 0.55,
    "Bank / Own Account": 0.60,
    "Bank / Trading Platform": 0.50,
    "Bank / Online Broker": 0.45,
    "Bank / Retail": 0.40,
    "Corporate": 0.45,
    "Non-profit Organisation / Charity / Foundation": 0.40,
    "Unknown": 0.50,
}

REASON_TEXT = {
    "current_holding_strength": "large installed holding in the target fund",
    "target_share": "target fund already matters within this relationship",
    "relationship_strength": "large existing EdRAM relationship",
    "breadth": "broad wallet makes the relationship commercially important",
    "channel_fit": "segment is a natural fit for this fund",
    "country_fit": "fund already shows product-market fit in this country",
    "adjacency": "client already uses adjacent sleeves/products",
    "avg_ticket": "ticket size supports a meaningful allocation",
    "freshness": "low current exposure leaves whitespace for a new sleeve",
    "diversification": "wallet is not overly concentrated in one existing line",
}


def module_paths() -> tuple[Path, Path, Path]:
    base_dir = Path(__file__).resolve().parent
    repo_dir = base_dir.parent
    return base_dir, repo_dir / "CRM_2025.xlsx", base_dir / "outputs"


def clip(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def log_norm(value: float, max_value: float) -> float:
    if value <= 0 or max_value <= 0:
        return 0.0
    return clip(math.log1p(value) / math.log1p(max_value))


def ratio_to_score(ratio: float) -> float:
    """Map a lift ratio into a 0-1 commercial-fit score with 0.5 as neutral."""
    if ratio <= 0:
        return 0.0
    return clip(1.0 / (1.0 + math.exp(-2.0 * math.log(ratio))))


def complexity_score(segment: str, complexity: int) -> float:
    segment_capability = SEGMENT_CAPABILITY.get(segment, 0.50)
    complexity_norm = (complexity - 1) / 4
    return clip(1.0 - abs(segment_capability - complexity_norm))


def read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []

    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    strings = []
    for si in root.findall(f"{NS}si"):
        strings.append("".join(node.text or "" for node in si.iterfind(f".//{NS}t")))
    return strings


def cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    value_node = cell.find(f"{NS}v")
    if value_node is None:
        return ""
    if cell.get("t") == "s":
        return shared_strings[int(value_node.text)]
    return value_node.text or ""


def read_xlsx_records(path: Path) -> list[dict[str, str | float]]:
    with zipfile.ZipFile(path) as archive:
        shared_strings = read_shared_strings(archive)
        sheet_root = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        rows = sheet_root.find(f"{NS}sheetData").findall(f"{NS}row")

        header_map = {}
        for cell in rows[0].findall(f"{NS}c"):
            column = "".join(ch for ch in cell.get("r") if ch.isalpha())
            header_map[column] = cell_value(cell, shared_strings)

        records = []
        for row in rows[1:]:
            raw = {}
            for cell in row.findall(f"{NS}c"):
                column = "".join(ch for ch in cell.get("r") if ch.isalpha())
                raw[column] = cell_value(cell, shared_strings)

            record = {header_map[col]: raw.get(col, "") for col in header_map}
            record["AUM (€)"] = float(record["AUM (€)"] or 0)
            records.append(record)

    return records


def infer_taxonomy(fund_name: str) -> dict[str, object]:
    name = fund_name.lower()
    asset_class = "equity"
    role = "satellite"
    complexity = 3
    tags = set()

    if any(token in name for token in ["bond", "credit", "yield", "millesima", "hybrid", "souver", "duration"]):
        asset_class = "fixed_income"
        role = "core"
        tags.update({"fixed_income", "carry", "income"})
    elif any(token in name for token in ["allocation", "quam", "ultim"]):
        asset_class = "multi_asset"
        role = "core"
        tags.update({"multi_asset", "diversified"})
    elif any(token in name for token in ["gold", "catalyst"]):
        asset_class = "alternatives"
        role = "satellite"
        complexity = 4
        tags.update({"alternatives", "alpha"})
    else:
        asset_class = "equity"
        tags.add("equity")

    keyword_tags = {
        "financial": "financials",
        "health": "healthcare",
        "big data": "technology",
        "tech": "technology",
        "china": "china",
        "india": "india",
        "emerging": "em",
        "euro": "europe",
        "europe": "europe",
        "tricolore": "france",
        "green": "climate",
        "climate": "climate",
        "resilience": "resilience",
        "sustainable": "sustainable",
        "small": "small_cap",
        "value": "value",
    }
    for token, tag in keyword_tags.items():
        if token in name:
            tags.add(tag)

    if "thematic" in tags or {"technology", "healthcare", "climate", "resilience"} & tags:
        role = "satellite"
        complexity = max(complexity, 4)

    return {
        "asset_class": asset_class,
        "role": role,
        "complexity": complexity,
        "tags": sorted(tags or {asset_class}),
    }


def load_taxonomy(path: Path, funds_in_crm: set[str]) -> tuple[dict[str, dict[str, object]], list[str]]:
    manual = json.loads(path.read_text())
    resolved = {}
    inferred = []

    for fund in sorted(funds_in_crm):
        if fund in manual:
            resolved[fund] = manual[fund]
        else:
            resolved[fund] = infer_taxonomy(fund)
            inferred.append(fund)

    return resolved, inferred


def primary_tags(fund_meta: dict[str, object]) -> list[str]:
    tags = [tag for tag in fund_meta["tags"] if tag not in GENERIC_TAGS]
    return tags or list(fund_meta["tags"])


def build_client_profiles(records: list[dict[str, str | float]], taxonomy: dict[str, dict[str, object]]) -> dict[str, dict[str, object]]:
    profiles = {}

    for record in records:
        relationship = str(record["Business Relationship"]).strip()
        country = str(record["Business Country"]).strip()
        segment = str(record["BR Segmentation"]).strip()
        fund = str(record["Fund"]).strip()
        aum = float(record["AUM (€)"])

        if not fund:
            continue

        client_key = f"{relationship} | {country} | {segment}"
        profile = profiles.setdefault(
            client_key,
            {
                "client_key": client_key,
                "business_relationship": relationship,
                "country": country,
                "segment": segment,
                "line_count": 0,
                "total_aum": 0.0,
                "holdings": defaultdict(float),
            },
        )

        profile["line_count"] += 1
        profile["total_aum"] += aum
        profile["holdings"][fund] += aum

    for profile in profiles.values():
        total_aum = profile["total_aum"]
        holdings = profile["holdings"]
        unique_funds = len(holdings)
        max_fund_aum = max(holdings.values()) if holdings else 0.0

        asset_class_aum = defaultdict(float)
        role_aum = defaultdict(float)
        tag_aum = defaultdict(float)

        for fund, aum in holdings.items():
            meta = taxonomy[fund]
            asset_class_aum[meta["asset_class"]] += aum
            role_aum[meta["role"]] += aum

            tags = list(dict.fromkeys(meta["tags"]))
            weighted_aum = aum / len(tags)
            for tag in tags:
                tag_aum[tag] += weighted_aum

        profile["unique_funds"] = unique_funds
        profile["avg_line_aum"] = total_aum / profile["line_count"] if profile["line_count"] else 0.0
        profile["avg_fund_aum"] = total_aum / unique_funds if unique_funds else 0.0
        profile["max_fund_aum"] = max_fund_aum
        profile["concentration_ratio"] = max_fund_aum / total_aum if total_aum else 0.0
        profile["asset_class_aum"] = dict(asset_class_aum)
        profile["asset_class_share"] = {k: v / total_aum for k, v in asset_class_aum.items()}
        profile["role_aum"] = dict(role_aum)
        profile["role_share"] = {k: v / total_aum for k, v in role_aum.items()}
        profile["tag_aum"] = dict(tag_aum)
        profile["tag_share"] = {k: v / total_aum for k, v in tag_aum.items()}

    return profiles


def build_fund_stats(records: list[dict[str, str | float]]) -> tuple[dict[str, object], dict[str, dict[str, object]]]:
    overall_country_aum = defaultdict(float)
    overall_segment_aum = defaultdict(float)
    fund_stats = {}

    for record in records:
        fund = str(record["Fund"]).strip()
        country = str(record["Business Country"]).strip()
        segment = str(record["BR Segmentation"]).strip()
        aum = float(record["AUM (€)"])

        if not fund:
            continue

        overall_country_aum[country] += aum
        overall_segment_aum[segment] += aum

        stats = fund_stats.setdefault(
            fund,
            {
                "total_aum": 0.0,
                "country_aum": defaultdict(float),
                "segment_aum": defaultdict(float),
            },
        )
        stats["total_aum"] += aum
        stats["country_aum"][country] += aum
        stats["segment_aum"][segment] += aum

    overall = {
        "total_aum": sum(overall_country_aum.values()),
        "country_aum": dict(overall_country_aum),
        "segment_aum": dict(overall_segment_aum),
    }
    return overall, fund_stats


def empirical_fit(fund_total: float, fund_bucket: float, overall_total: float, overall_bucket: float) -> float:
    if fund_total <= 0 or overall_total <= 0:
        return 0.5
    fund_share = fund_bucket / fund_total
    overall_share = overall_bucket / overall_total if overall_bucket > 0 else 0.0
    if overall_share <= 0:
        return 0.5
    return ratio_to_score(fund_share / overall_share)


def build_reason_list(components: dict[str, float], weights: dict[str, float]) -> list[str]:
    ranked = sorted(
        ((weights[name] * value, name) for name, value in components.items()),
        reverse=True,
    )
    reasons = []
    for _, name in ranked:
        text = REASON_TEXT.get(name)
        if text and text not in reasons:
            reasons.append(text)
        if len(reasons) == 3:
            break
    return reasons


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    base_dir, crm_path, output_dir = module_paths()
    taxonomy_path = base_dir / "fund_taxonomy.json"
    output_dir.mkdir(parents=True, exist_ok=True)

    records = read_xlsx_records(crm_path)
    funds_in_crm = {str(record["Fund"]).strip() for record in records if str(record["Fund"]).strip()}
    taxonomy, inferred_funds = load_taxonomy(taxonomy_path, funds_in_crm)

    profiles = build_client_profiles(records, taxonomy)
    overall_stats, fund_stats = build_fund_stats(records)

    max_total_aum = max(profile["total_aum"] for profile in profiles.values())
    max_avg_line_aum = max(profile["avg_line_aum"] for profile in profiles.values())
    max_unique_funds = max(profile["unique_funds"] for profile in profiles.values())

    max_client_holding_by_fund = defaultdict(float)
    for profile in profiles.values():
        for fund, aum in profile["holdings"].items():
            max_client_holding_by_fund[fund] = max(max_client_holding_by_fund[fund], aum)

    taxonomy_rows = []
    for fund in sorted(taxonomy):
        meta = taxonomy[fund]
        taxonomy_rows.append(
            {
                "fund": fund,
                "asset_class": meta["asset_class"],
                "role": meta["role"],
                "complexity": meta["complexity"],
                "tags": ", ".join(meta["tags"]),
                "taxonomy_source": "inferred" if fund in inferred_funds else "manual",
            }
        )
    write_csv(
        output_dir / "fund_taxonomy_resolved.csv",
        taxonomy_rows,
        ["fund", "asset_class", "role", "complexity", "tags", "taxonomy_source"],
    )

    score_rows = []
    top_rows = []

    for client_key in sorted(profiles):
        profile = profiles[client_key]
        relationship_strength = (
            0.55 * log_norm(profile["total_aum"], max_total_aum)
            + 0.20 * log_norm(profile["avg_line_aum"], max_avg_line_aum)
            + 0.15 * log_norm(profile["unique_funds"], max_unique_funds)
            + 0.10 * (1.0 - profile["concentration_ratio"])
        )
        avg_ticket_norm = log_norm(profile["avg_line_aum"], max_avg_line_aum)
        breadth_norm = log_norm(profile["unique_funds"], max_unique_funds)

        for fund in sorted(taxonomy):
            meta = taxonomy[fund]
            fund_total = fund_stats[fund]["total_aum"]

            current_target_aum = profile["holdings"].get(fund, 0.0)
            holds_target = current_target_aum > 0
            current_target_share = current_target_aum / profile["total_aum"] if profile["total_aum"] else 0.0

            segment_fit_empirical = empirical_fit(
                fund_total,
                fund_stats[fund]["segment_aum"].get(profile["segment"], 0.0),
                overall_stats["total_aum"],
                overall_stats["segment_aum"].get(profile["segment"], 0.0),
            )
            country_fit = empirical_fit(
                fund_total,
                fund_stats[fund]["country_aum"].get(profile["country"], 0.0),
                overall_stats["total_aum"],
                overall_stats["country_aum"].get(profile["country"], 0.0),
            )
            channel_fit = (
                0.65 * segment_fit_empirical
                + 0.35 * complexity_score(profile["segment"], int(meta["complexity"]))
            )

            target_asset_class_share = profile["asset_class_share"].get(meta["asset_class"], 0.0)
            target_tags = primary_tags(meta)
            target_tag_share = 0.0
            if target_tags:
                target_tag_share = sum(profile["tag_share"].get(tag, 0.0) for tag in target_tags) / len(target_tags)
            adjacency = clip(0.55 * target_asset_class_share + 0.45 * target_tag_share)
            freshness = clip(1.0 - (0.65 * target_asset_class_share + 0.35 * target_tag_share))
            diversification = clip(1.0 - profile["concentration_ratio"])
            current_holding_strength = log_norm(current_target_aum, max_client_holding_by_fund[fund])

            defend_weights = {
                "current_holding_strength": 0.35,
                "target_share": 0.20,
                "relationship_strength": 0.15,
                "breadth": 0.10,
                "channel_fit": 0.10,
                "country_fit": 0.10,
            }
            defend_components = {
                "current_holding_strength": current_holding_strength,
                "target_share": current_target_share,
                "relationship_strength": relationship_strength,
                "breadth": breadth_norm,
                "channel_fit": channel_fit,
                "country_fit": country_fit,
            }
            defend_score = 0.0
            if holds_target:
                defend_score = 100 * sum(defend_weights[k] * defend_components[k] for k in defend_weights)

            cross_weights = {
                "channel_fit": 0.25,
                "country_fit": 0.10,
                "relationship_strength": 0.20,
                "adjacency": 0.25,
                "avg_ticket": 0.10,
                "breadth": 0.10,
            }
            cross_components = {
                "channel_fit": channel_fit,
                "country_fit": country_fit,
                "relationship_strength": relationship_strength,
                "adjacency": adjacency,
                "avg_ticket": avg_ticket_norm,
                "breadth": breadth_norm,
            }
            cross_sell_score = 0.0
            if not holds_target:
                cross_base = sum(cross_weights[k] * cross_components[k] for k in cross_weights)
                cross_sell_score = 100 * cross_base * (0.35 + 0.65 * adjacency)

            new_weights = {
                "channel_fit": 0.25,
                "country_fit": 0.10,
                "relationship_strength": 0.25,
                "avg_ticket": 0.10,
                "freshness": 0.20,
                "diversification": 0.10,
            }
            new_components = {
                "channel_fit": channel_fit,
                "country_fit": country_fit,
                "relationship_strength": relationship_strength,
                "avg_ticket": avg_ticket_norm,
                "freshness": freshness,
                "diversification": diversification,
            }
            new_allocation_score = 0.0
            if not holds_target:
                new_base = sum(new_weights[k] * new_components[k] for k in new_weights)
                new_allocation_score = 100 * new_base * (0.35 + 0.65 * freshness)

            score_options = {
                "defend": defend_score,
                "cross_sell": cross_sell_score,
                "new_allocation": new_allocation_score,
            }
            best_action = max(score_options, key=score_options.get)
            best_score = score_options[best_action]
            if best_action == "defend":
                reasons = build_reason_list(defend_components, defend_weights)
            elif best_action == "cross_sell":
                reasons = build_reason_list(cross_components, cross_weights)
            else:
                reasons = build_reason_list(new_components, new_weights)

            row = {
                "client_key": profile["client_key"],
                "business_relationship": profile["business_relationship"],
                "country": profile["country"],
                "segment": profile["segment"],
                "fund": fund,
                "fund_asset_class": meta["asset_class"],
                "fund_role": meta["role"],
                "fund_complexity": meta["complexity"],
                "total_relationship_aum_eur": round(profile["total_aum"], 2),
                "line_count": profile["line_count"],
                "unique_funds_held": profile["unique_funds"],
                "avg_line_aum_eur": round(profile["avg_line_aum"], 2),
                "concentration_ratio": round(profile["concentration_ratio"], 4),
                "current_target_aum_eur": round(current_target_aum, 2),
                "current_target_share_of_wallet": round(current_target_share, 4),
                "target_asset_class_share": round(target_asset_class_share, 4),
                "target_tag_share": round(target_tag_share, 4),
                "channel_fit_score": round(channel_fit * 100, 2),
                "country_fit_score": round(country_fit * 100, 2),
                "relationship_strength_score": round(relationship_strength * 100, 2),
                "adjacency_score": round(adjacency * 100, 2),
                "freshness_score": round(freshness * 100, 2),
                "defend_score": round(defend_score, 2),
                "cross_sell_score": round(cross_sell_score, 2),
                "new_allocation_score": round(new_allocation_score, 2),
                "best_action": best_action,
                "best_score": round(best_score, 2),
                "reason_1": reasons[0] if len(reasons) > 0 else "",
                "reason_2": reasons[1] if len(reasons) > 1 else "",
                "reason_3": reasons[2] if len(reasons) > 2 else "",
            }
            score_rows.append(row)

    write_csv(
        output_dir / "client_fund_scores.csv",
        score_rows,
        [
            "client_key",
            "business_relationship",
            "country",
            "segment",
            "fund",
            "fund_asset_class",
            "fund_role",
            "fund_complexity",
            "total_relationship_aum_eur",
            "line_count",
            "unique_funds_held",
            "avg_line_aum_eur",
            "concentration_ratio",
            "current_target_aum_eur",
            "current_target_share_of_wallet",
            "target_asset_class_share",
            "target_tag_share",
            "channel_fit_score",
            "country_fit_score",
            "relationship_strength_score",
            "adjacency_score",
            "freshness_score",
            "defend_score",
            "cross_sell_score",
            "new_allocation_score",
            "best_action",
            "best_score",
            "reason_1",
            "reason_2",
            "reason_3",
        ],
    )

    for fund in sorted(taxonomy):
        fund_rows = [row for row in score_rows if row["fund"] == fund]
        for action_key in ("defend_score", "cross_sell_score", "new_allocation_score"):
            top_candidates = sorted(
                [row for row in fund_rows if row[action_key] > 0],
                key=lambda item: item[action_key],
                reverse=True,
            )[:25]
            action_name = action_key.replace("_score", "")
            for rank, row in enumerate(top_candidates, start=1):
                top_rows.append(
                    {
                        "fund": fund,
                        "action": action_name,
                        "rank": rank,
                        "client_key": row["client_key"],
                        "business_relationship": row["business_relationship"],
                        "country": row["country"],
                        "segment": row["segment"],
                        "score": row[action_key],
                        "current_target_aum_eur": row["current_target_aum_eur"],
                        "total_relationship_aum_eur": row["total_relationship_aum_eur"],
                        "reason_1": row["reason_1"],
                        "reason_2": row["reason_2"],
                        "reason_3": row["reason_3"],
                    }
                )

    write_csv(
        output_dir / "top_targets_by_fund_and_action.csv",
        top_rows,
        [
            "fund",
            "action",
            "rank",
            "client_key",
            "business_relationship",
            "country",
            "segment",
            "score",
            "current_target_aum_eur",
            "total_relationship_aum_eur",
            "reason_1",
            "reason_2",
            "reason_3",
        ],
    )

    summary_rows = []
    for fund in sorted(taxonomy):
        fund_rows = [row for row in score_rows if row["fund"] == fund]
        summary_rows.append(
            {
                "fund": fund,
                "asset_class": taxonomy[fund]["asset_class"],
                "role": taxonomy[fund]["role"],
                "clients_scored": len(fund_rows),
                "existing_holders": sum(1 for row in fund_rows if row["current_target_aum_eur"] > 0),
                "avg_defend_score": round(sum(row["defend_score"] for row in fund_rows) / len(fund_rows), 2),
                "avg_cross_sell_score": round(sum(row["cross_sell_score"] for row in fund_rows) / len(fund_rows), 2),
                "avg_new_allocation_score": round(sum(row["new_allocation_score"] for row in fund_rows) / len(fund_rows), 2),
                "top_defend_score": round(max(row["defend_score"] for row in fund_rows), 2),
                "top_cross_sell_score": round(max(row["cross_sell_score"] for row in fund_rows), 2),
                "top_new_allocation_score": round(max(row["new_allocation_score"] for row in fund_rows), 2),
            }
        )

    write_csv(
        output_dir / "fund_score_summary.csv",
        summary_rows,
        [
            "fund",
            "asset_class",
            "role",
            "clients_scored",
            "existing_holders",
            "avg_defend_score",
            "avg_cross_sell_score",
            "avg_new_allocation_score",
            "top_defend_score",
            "top_cross_sell_score",
            "top_new_allocation_score",
        ],
    )

    summary = {
        "crm_rows": len(records),
        "unique_client_keys": len(profiles),
        "funds_in_crm": len(funds_in_crm),
        "scores_written": len(score_rows),
        "inferred_taxonomy_funds": inferred_funds,
    }
    (output_dir / "run_summary.json").write_text(json.dumps(summary, indent=2))

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
