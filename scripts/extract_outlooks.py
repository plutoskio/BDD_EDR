#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
import subprocess
import sys
import warnings
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}

logging.getLogger("pypdf").setLevel(logging.ERROR)
warnings.filterwarnings(
    "ignore",
    message="Rotated text discovered. Output will be incomplete.",
)


@dataclass
class ExtractionResult:
    source: str
    output: str
    kind: str
    method: str
    success: bool
    pages: int | None
    characters: int
    warnings: list[str]
    error: str | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mirror outlook source files into plain text for easier code ingestion."
    )
    parser.add_argument(
        "--source-dir",
        default="outlooks",
        help="Directory containing the original source outlook files.",
    )
    parser.add_argument(
        "--output-dir",
        default="outlooks_txt",
        help="Directory where extracted text files will be written.",
    )
    return parser.parse_args()


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00a0", " ")
    text = text.replace("\u200b", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def ensure_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"Required tool not found on PATH: {name}")
    return path


def extract_docx(source_path: Path) -> tuple[str, str]:
    pandoc_path = ensure_tool("pandoc")
    completed = subprocess.run(
        [pandoc_path, str(source_path), "-t", "plain"],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout, "pandoc"


def extract_pdf(source_path: Path) -> tuple[str, str, int, list[str]]:
    reader = PdfReader(str(source_path))
    page_count = len(reader.pages)
    pages: list[str] = []
    warnings: list[str] = []

    for index, page in enumerate(reader.pages, start=1):
        text = ""
        try:
            text = page.extract_text(extraction_mode="layout") or ""
            method = "pypdf-layout"
        except TypeError:
            text = page.extract_text() or ""
            method = "pypdf"

        if not text.strip():
            warnings.append(f"page_{index}_empty")

        pages.append(f"## Page {index}\n\n{text.strip()}\n")

    combined = "\n".join(pages).strip() + "\n"
    return combined, method, page_count, warnings


def build_header(
    source_path: Path,
    result_method: str,
    kind: str,
    page_count: int | None,
) -> str:
    lines = [
        f"Source file: {source_path.name}",
        f"Source path: {source_path.as_posix()}",
        f"Type: {kind}",
        f"Extraction method: {result_method}",
        f"Extracted at UTC: {datetime.now(timezone.utc).isoformat()}",
    ]
    if page_count is not None:
        lines.append(f"Page count: {page_count}")
    return "\n".join(lines) + "\n\n---\n\n"


def convert_one(source_path: Path, output_dir: Path) -> ExtractionResult:
    output_path = output_dir / f"{source_path.stem}.txt"
    warnings: list[str] = []

    try:
        if source_path.suffix.lower() == ".docx":
            body, method = extract_docx(source_path)
            page_count = None
            kind = "docx"
        elif source_path.suffix.lower() == ".pdf":
            body, method, page_count, warnings = extract_pdf(source_path)
            kind = "pdf"
        else:
            raise RuntimeError(f"Unsupported file extension: {source_path.suffix}")

        body = normalize_text(body)
        header = build_header(source_path, method, kind, page_count)
        output_path.write_text(header + body, encoding="utf-8")

        if len(body.strip()) < 500:
            warnings.append("low_text_volume")

        return ExtractionResult(
            source=str(source_path.as_posix()),
            output=str(output_path.as_posix()),
            kind=kind,
            method=method,
            success=True,
            pages=page_count,
            characters=len(body),
            warnings=warnings,
            error=None,
        )
    except Exception as exc:  # noqa: BLE001
        return ExtractionResult(
            source=str(source_path.as_posix()),
            output=str(output_path.as_posix()),
            kind=source_path.suffix.lower().lstrip("."),
            method="failed",
            success=False,
            pages=None,
            characters=0,
            warnings=warnings,
            error=str(exc),
        )


def main() -> int:
    args = parse_args()
    source_dir = Path(args.source_dir)
    output_dir = Path(args.output_dir)

    if not source_dir.is_dir():
        print(f"Source directory not found: {source_dir}", file=sys.stderr)
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)

    source_files = sorted(
        path
        for path in source_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    results = [convert_one(path, output_dir) for path in source_files]

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_dir": source_dir.resolve().as_posix(),
        "output_dir": output_dir.resolve().as_posix(),
        "counts": {
            "total": len(results),
            "success": sum(1 for result in results if result.success),
            "failed": sum(1 for result in results if not result.success),
        },
        "files": [asdict(result) for result in results],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    failures = [result for result in results if not result.success]
    for result in results:
        status = "OK" if result.success else "FAIL"
        warning_suffix = f" warnings={','.join(result.warnings)}" if result.warnings else ""
        print(
            f"[{status}] {Path(result.source).name} -> {Path(result.output).name}"
            f" method={result.method} chars={result.characters}{warning_suffix}"
        )
        if result.error:
            print(f"  error: {result.error}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
