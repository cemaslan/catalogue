#!/usr/bin/env python3
"""
Builds a standalone, zero-dependency searchable product catalog (index.html)
from a Sage Accounting Online Ireland `stock_item_export.csv` file.

Usage:
    python3 build.py [path/to/stock_item_export.csv] [--title "Your Store Catalogue"]
"""

import argparse
import csv
import html
import json
from pathlib import Path


def build_catalog(csv_path: Path, template_path: Path, output_path: Path, title: str) -> int:
    products = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            active = (row.get("Active") or "Yes").strip().lower()
            if active not in ("yes", "y", "true", "1", ""):
                continue

            code = (row.get("Item Code*") or row.get("Item Code") or "").strip()
            desc = (row.get("Description*") or row.get("Description") or "").strip()
            if not code or not desc:
                continue

            raw_price = (row.get("Sales Price 1 Value") or "0").strip()
            try:
                price = round(float(raw_price), 2)
            except ValueError:
                price = 0.0

            category = (row.get("Category") or "").strip() or "Other"
            barcode = (row.get("Barcode") or "").strip()

            products.append([code, desc, price, category, barcode])

    template = template_path.read_text(encoding="utf-8")
    products_json = json.dumps(products, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    subtitle = f"{len(products):,} products · Prices in EUR"

    rendered = (
        template.replace("__TITLE__", html.escape(title))
        .replace("__SUBTITLE__", html.escape(subtitle))
        .replace("__PRODUCTS_JSON__", products_json)
    )
    output_path.write_text(rendered, encoding="utf-8")
    return len(products)


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Build searchable product catalog from Sage CSV export.")
    parser.add_argument(
        "csv_file",
        nargs="?",
        default=str(here / "stock_item_export.csv"),
        help="Path to stock_item_export.csv",
    )
    parser.add_argument(
        "--title",
        default="Electric Power Tool Co. Ltd.",
        help="Page title / store name",
    )
    parser.add_argument(
        "--out",
        default=str(here / "index.html"),
        help="Output HTML path",
    )
    args = parser.parse_args()

    count = build_catalog(
        csv_path=Path(args.csv_file),
        template_path=here / "template.html",
        output_path=Path(args.out),
        title=args.title,
    )
    size_kb = Path(args.out).stat().st_size / 1024
    print(f"Built {args.out} with {count} products ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
