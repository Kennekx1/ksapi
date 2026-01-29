# Kaspi.kz Price & Seller Scraper

This project automates the extraction of product prices and **accurate seller counts** from Kaspi.kz.

## Key Features
- **Smart Scraper (`kaspi_scraper.js`)**: 
  - Bypass blocking by interception of internal API calls.
  - Returns **EXACT** number of sellers (e.g., 24, 13, 1), not just "1" or "5+".
  - Handles dynamic loading and "Offers" tab logic.
- **ODS Integration**:
  - `prepare_products.py`: Reads product list from a spreadsheet (`.ods`).
  - `update_ods.py`: Writes results back to the spreadsheet, appending new columns.

## Tech Stack
- **Node.js**: Playwright (Browser Automation), Puppeteer Stealth
- **Python**: Pandas, Odfpy (Excel/ODS manipulation)

## Installation

1. Install Node.js dependencies:
   ```bash
   npm install
   ```
2. Setup Python environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install pandas odfpy
   ```

## Usage

1. **Prepare input**: Place your product list in an `.ods` file or `products.json`.
2. **Run Scraper**:
   ```bash
   node kaspi_scraper.js
   ```
3. **Export/Update ODS**:
   ```bash
   python3 update_ods.py
   ```
