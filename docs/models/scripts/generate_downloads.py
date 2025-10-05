# scripts/generate_downloads.py

import os
from pathlib import Path
from playwright.sync_api import sync_playwright

# --- Configuration ---
# The script will find all .html files in the reports directory
# and generate a PDF and PNG for each.

# --- Script Logic ---
def main():
    # Define directories relative to the script's location
    script_dir = Path(__file__).parent
    reports_dir = script_dir.parent / "reports"
    output_dir = script_dir.parent / "downloads"

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"✅ Output directory is ready at: {output_dir}")

    # Find all HTML files in the reports directory
    html_files = list(reports_dir.glob("*.html"))
    if not html_files:
        print("No HTML files found in the reports directory. Exiting.")
        return

    print(f"Found {len(html_files)} HTML files to process.")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        for html_file in html_files:
            # Convert the local file path to a file:// URL
            url = f"file://{html_file.resolve()}"
            print(f"Processing file: {url}...")

            try:
                # Go to the page and wait for it to be fully loaded
                page.goto(url, wait_until='networkidle', timeout=60000)

                # Generate a clean base filename from the HTML file's name
                base_filename = html_file.stem

                # --- Create PDF ---
                pdf_path = output_dir / f"{base_filename}.pdf"
                page.pdf(path=pdf_path, format='A4', print_background=True)
                print(f"   -> Saved PDF to {pdf_path}")

                # --- Create PNG ---
                png_path = output_dir / f"{base_filename}.png"
                page.screenshot(path=png_path, full_page=True)
                print(f"   -> Saved PNG to {png_path}")

            except Exception as e:
                print(f"   ❌ Failed to process {html_file.name}. Error: {e}")

        browser.close()
        print("\n🎉 All tasks complete!")


if __name__ == "__main__":
    # Before running, make sure you have installed playwright:
    # pip install playwright
    # python -m playwright install
    main()
