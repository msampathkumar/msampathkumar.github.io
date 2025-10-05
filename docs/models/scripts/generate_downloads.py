# scripts/generate_downloads.py

import os
from pathlib import Path
from playwright.sync_api import sync_playwright
import re

# --- Configuration ---
# Add all the web pages you want to capture here
URLS_TO_CAPTURE = [
    "https://en.wikipedia.org/wiki/Poland",
    "https://en.wikipedia.org/wiki/Warsaw",
    "https://en.wikipedia.org/wiki/Masovian_Voivodeship"
]


# --- Script Logic ---
def generate_safe_filename(url):
    """Creates a clean filename from a URL (e.g., 'poland')."""
    # Takes the last part of the URL path
    name = url.split('/')[-1]
    # Removes special characters and makes it lowercase
    return re.sub(r'[^a-z0-9_]', '', name.lower())


def main():
    # Define the output directory relative to the script's location
    # This assumes the script is in project/scripts/ and output is in project/docs/assets/downloads/
    script_dir = Path(__file__).parent
    output_dir = script_dir.parent / "docs" / "assets" / "downloads"

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"✅ Output directory is ready at: {output_dir}")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        for url in URLS_TO_CAPTURE:
            print(f"Processing URL: {url}...")

            try:
                # Go to the page and wait for it to be fully loaded
                page.goto(url, wait_until='networkidle', timeout=60000)

                # Generate a clean base filename
                base_filename = generate_safe_filename(url)

                # --- Create PDF ---
                pdf_path = output_dir / f"{base_filename}.pdf"
                page.pdf(path=pdf_path, format='A4', print_background=True)
                print(f"   -> Saved PDF to {pdf_path}")

                # --- Create PNG ---
                png_path = output_dir / f"{base_filename}.png"
                page.screenshot(path=png_path, full_page=True)
                print(f"   -> Saved PNG to {png_path}")

            except Exception as e:
                print(f"   ❌ Failed to process {url}. Error: {e}")

        browser.close()
        print("\n🎉 All tasks complete!")


if __name__ == "__main__":
    # Before running, make sure you have installed playwright:
    # pip install playwright
    # python -m playwright install
    main()