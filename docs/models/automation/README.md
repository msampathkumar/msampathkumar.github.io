# Gemini Model Report Generator

This directory contains a Python-based system for generating beautiful,
single-page HTML reports for Google's Gemini models based on a simple CSV data
source.

## Overview

The system uses a Jinja2 template (`model_card.html`) and a stylesheet
(`style.css`) to render data from a CSV file (`models.csv`). The main script,
`generate_report.py`, reads the data, processes it, and generates a separate
HTML report for each model defined in the CSV.

## File Structure

- `generate_report.py`: The main script to execute for generating reports.
- `models.csv`: The data source. Each row represents a different Gemini model.
- `model_card.html`: The main Jinja2 template for the report page.
- `style.css`: The stylesheet that controls the look and feel of the generated
  reports.
- `model_data.py`: Contains the Python `dataclass` definitions that structure
  the model data.
- `footer.html`: A shared HTML snippet for the report footer, included by the
  main template.
- `background.png`: The background image used for the report page.

## Prerequisites

- Python 3.6+
- Jinja2 library

To install the required library, run:

```bash
pip install Jinja2
```

## How to Use

### 1. Add Model Data

To add a new model, open the `models.csv` file and add a new row. Ensure you
follow the existing format:

- **Simple Fields**: `name`, `variant`, `api_name`, etc., are plain text.
- **List Fields**: Fields like `location` and `model_features` should contain
  values separated by a semicolon (`;`).
- **SDK/ADK Fields**: These should be in a `key:value` format, with each pair
  separated by a semicolon (e.g., `Python:1.0;Go:2.0`).

### 2. Generate Reports

Once you have updated the CSV file, run the generation script from your
terminal:

```bash
python generate_report.py
```

The script will create a new `report_<model_variant_name>.html` file in this
directory for each model in the CSV.

## Future Plans

- **Web Scraper Integration**: The next planned feature is a web-scraper to
  automatically fetch and update model details from official sources. This will
  help keep the data in `models.csv` current, with the exception of the
  `pricing` information, which will still require manual entry.
