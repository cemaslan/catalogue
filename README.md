# Searchable Product Catalogue

A fast, mobile-friendly, single-file interactive product catalogue built from a Sage Accounting Online Ireland `stock_item_export.csv` export.

## Features

- **Omni Search (filters as you type)**: Searches across product code, description, category, and barcode.
  - Order-independent matching (`12mm sds` and `sds 12` return the same items).
  - Hardware-smart size matching (`12mm` matches `12 X 350MM` without matching `125MM`; `12x350` splits into `12` and `350`).
  - Handles shorthand & spacing differences (`sds+` -> `SDS PLUS`, `holesaw` <-> `HOLE SAW`, `wirebrush` <-> `WIRE BRUSH`, `bp115` -> `BP-115-M14`).
  - Automatic 1-typo fallback (`roto broach` -> `ROTA BROACH`) if no exact match is found.
  - Highlights matched terms so customers can immediately spot the right size.
- **Simple & Clear**: Shows only **Product Code**, **Description**, and **Price (EUR)** — no stock counts or clutter.
- **Ex. VAT / Inc. 23% VAT toggle**: Defaults to the Sage export price (`Ex. VAT`), with a 1-tap toggle to view `Inc. 23% VAT`.
- **Tap-to-copy Product Code**: Tapping any product code copies it to the clipboard for easy texting, calling, or ordering.
- **Shareable URLs**: Search queries and category filters stay in the URL (`?q=12mm+sds`), so you can email pre-filtered links too.

## Updating the Catalogue from Sage

Whenever you export a new `stock_item_export.csv` from Sage Accounting Online:

```bash
python3 build.py path/to/stock_item_export.csv --title "Your Store Catalogue"
```

This regenerates `index.html` as a self-contained ~175 KB file with zero external dependencies.

## Hosting Online to Email a Link to Customers

Because `index.html` is a single self-contained file, you can host it for free in under a minute on any static host:

- **GitHub Pages**: Push `index.html` to a GitHub repository and enable **Settings -> Pages**.
- **Netlify Drop**: Drag and drop the `product-catalog` folder onto [app.netlify.com/drop](https://app.netlify.com/drop).
- **Cloudflare Pages**: Upload the folder containing `index.html` to Cloudflare Pages.
