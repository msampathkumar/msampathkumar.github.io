# Gemini Model Report Generator

This directory contains a Python-based system for generating beautiful,
single-page HTML reports for Google's Gemini models based on a simple YAML data
source.

## Overview

The system uses a Jinja2 template (`template_model_card.html`) and a stylesheet
(`style.css`) to render data from a YAML file (`models.yaml`). The main script,
`generate_report.py`, reads the data, processes it, and generates a separate
HTML report for each model defined in the YAML file.

## File Structure

- `docs/models/automation/generate_report.py`: The main script to execute for generating reports.
- `docs/models/config/models.yaml`: The data source. Each document in the YAML file represents a different Gemini model.
- `docs/models/automation/template_model_card.html`: The main Jinja2 template for the report page.
- `docs/models/automation/style.css`: The stylesheet that controls the look and feel of the generated
  reports.
- `docs/models/automation/model_data.py`: Contains the Python `dataclass` definitions that structure
  the model data.
- `docs/models/automation/footer.html`: A shared HTML snippet for the report footer, included by the
  main template.
- `docs/models/automation/background.png`: The background image used for the report page.
- `docs/models/reports/`: The output directory for the generated HTML reports.
- `docs/models/downloads/`: The output directory for generated PDF and PNG files.

## Prerequisites

- Python 3.6+
- Jinja2 library
- PyYAML library

To install the required libraries, run:

```bash
pip install -r requirements.txt
```

## How to Use

### 1. Add Model Data

To add a new model, open the `docs/models/config/models.yaml` file and add a new document to the `models` list. Ensure you
follow the existing format.

### 2. Generate Reports

Once you have updated the YAML file, run the generation script from your
terminal, from the `docs/models/automation` directory:

```bash
python generate_report.py
```

The script will create a new `report_<model_api_name>.html` file in the `docs/models/reports`
directory for each model in the YAML file.

## Future Plans

- **Web Scraper Integration**: The next planned feature is a web-scraper to
  automatically fetch and update model details from official sources. This will
  help keep the data in `models.yaml` current, with the exception of the
  `pricing` information, which will still require manual entry.