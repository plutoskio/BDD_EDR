#!/usr/bin/env python3
from __future__ import annotations

import csv
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "CRM_2025.xlsx"
OUTPUT_DIR = ROOT / "d3" / "data"
XML_NS = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
TARGET_COUNTRIES = ("FRANCE", "GERMANY", "SWITZERLAND", "ITALY", "SPAIN")


def col_to_index(cell_ref: str) -> int:
    column = ""
    for char in cell_ref:
        if char.isalpha():
            column += char
        else:
            break

    index = 0
    for char in column:
        index = index * 26 + (ord(char.upper()) - 64)
    return index


def load_sheet_rows(xlsx_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with ZipFile(xlsx_path) as archive:
        shared_strings = []
        shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        for item in shared_root.findall("x:si", XML_NS):
            parts = [text.text or "" for text in item.iterfind(".//x:t", XML_NS)]
            shared_strings.append("".join(parts))

        sheet_root = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        xml_rows = sheet_root.findall(".//x:sheetData/x:row", XML_NS)

    def cell_value(cell: ET.Element) -> str:
        value = cell.find("x:v", XML_NS)
        if value is None:
            return ""
        if cell.attrib.get("t") == "s":
            return shared_strings[int(value.text)]
        return value.text or ""

    header_map: dict[int, str] = {}
    for cell in xml_rows[0].findall("x:c", XML_NS):
        header_map[col_to_index(cell.attrib["r"])] = cell_value(cell)

    max_index = max(header_map)
    headers = [header_map.get(index, "") for index in range(1, max_index + 1)]

    rows: list[dict[str, str]] = []
    for xml_row in xml_rows[1:]:
        row = {header: "" for header in headers if header}
        for cell in xml_row.findall("x:c", XML_NS):
            header_index = col_to_index(cell.attrib["r"]) - 1
            if 0 <= header_index < len(headers):
                header = headers[header_index]
                if header:
                    row[header] = cell_value(cell).strip()
        rows.append(row)

    return headers, rows


def parse_amount(raw_value: str) -> float:
    if not raw_value:
        return 0.0
    try:
        return float(raw_value)
    except ValueError:
        return 0.0


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    _, crm_rows = load_sheet_rows(INPUT_PATH)

    country_counts: Counter[str] = Counter()
    country_aum: defaultdict[str, float] = defaultdict(float)
    country_funds: defaultdict[str, set[str]] = defaultdict(set)
    country_segments: defaultdict[str, set[str]] = defaultdict(set)
    country_fund_counts: Counter[tuple[str, str]] = Counter()
    country_fund_aum: defaultdict[tuple[str, str], float] = defaultdict(float)
    country_segment_counts: Counter[tuple[str, str]] = Counter()
    country_segment_aum: defaultdict[tuple[str, str], float] = defaultdict(float)

    for row in crm_rows:
        country = row.get("Business Country", "").strip().upper()
        if country not in TARGET_COUNTRIES:
            continue

        fund = row.get("Fund", "").strip()
        segment = row.get("BR Segmentation", "").strip()
        aum = parse_amount(row.get("AUM (€)", "").strip())

        country_counts[country] += 1
        country_aum[country] += aum

        if fund:
            country_funds[country].add(fund)
            country_fund_counts[(country, fund)] += 1
            country_fund_aum[(country, fund)] += aum

        if segment:
            country_segments[country].add(segment)
            country_segment_counts[(country, segment)] += 1
            country_segment_aum[(country, segment)] += aum

    country_summary_rows: list[dict[str, object]] = []
    for country in TARGET_COUNTRIES:
        country_summary_rows.append(
            {
                "country": country.title(),
                "row_count": country_counts[country],
                "total_aum_eur": f"{country_aum[country]:.2f}",
                "unique_funds": len(country_funds[country]),
                "unique_segments": len(country_segments[country]),
            }
        )

    country_fund_rows: list[dict[str, object]] = []
    for (country, fund), row_count in sorted(
        country_fund_counts.items(),
        key=lambda item: (-country_fund_aum[item[0]], -item[1], item[0][0], item[0][1]),
    ):
        country_fund_rows.append(
            {
                "country": country.title(),
                "fund": fund,
                "row_count": row_count,
                "total_aum_eur": f"{country_fund_aum[(country, fund)]:.2f}",
            }
        )

    country_segment_rows: list[dict[str, object]] = []
    for (country, segment), row_count in sorted(
        country_segment_counts.items(),
        key=lambda item: (-country_segment_aum[item[0]], -item[1], item[0][0], item[0][1]),
    ):
        country_segment_rows.append(
            {
                "country": country.title(),
                "segment": segment,
                "row_count": row_count,
                "total_aum_eur": f"{country_segment_aum[(country, segment)]:.2f}",
            }
        )

    write_csv(
        OUTPUT_DIR / "crm_country_summary.csv",
        ["country", "row_count", "total_aum_eur", "unique_funds", "unique_segments"],
        country_summary_rows,
    )
    write_csv(
        OUTPUT_DIR / "crm_country_fund_summary.csv",
        ["country", "fund", "row_count", "total_aum_eur"],
        country_fund_rows,
    )
    write_csv(
        OUTPUT_DIR / "crm_country_segment_summary.csv",
        ["country", "segment", "row_count", "total_aum_eur"],
        country_segment_rows,
    )

    print(f"Wrote {OUTPUT_DIR / 'crm_country_summary.csv'}")
    print(f"Wrote {OUTPUT_DIR / 'crm_country_fund_summary.csv'}")
    print(f"Wrote {OUTPUT_DIR / 'crm_country_segment_summary.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
