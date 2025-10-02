import csv
import os
from jinja2 import Environment, FileSystemLoader
from model_data import GeminiModel, ModelContext, ModelPricing

# SVG icons for modalities
MODALITY_ICONS = {
    "Text": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><line x1="10" y1="9" x2="8" y2="9"></line></svg>""",
    "Audio": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line></svg>""",
    "Video": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect><line x1="7" y1="2" x2="7" y2="22"></line><line x1="17" y1="2" x2="17" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line><line x1="2" y1="7" x2="7" y2="7"></line><line x1="2" y1="17" x2="7" y2="17"></line><line x1="17" y1="17" x2="22" y2="17"></line><line x1="17" y1="7" x2="22" y2="7"></line></svg>""",
    "Image": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>""",
}


def parse_list(text: str) -> list[str]:
    """Parses a semicolon-separated string into a list."""
    if not text:
        return []
    return [item.strip() for item in text.split(";")]


def parse_sdks(sdk_string: str) -> dict[str, str]:
    """Parses a string like 'Python:1.0;Go:2.0' into a dictionary."""
    sdks = {}
    if not sdk_string:
        return sdks
    for item in sdk_string.split(";"):
        try:
            key, value = item.split(":", 1)
            sdks[key.strip()] = value.strip()
        except ValueError:
            print(f"Warning: Skipping malformed SDK entry: {item}")
    return sdks


def create_model_from_row(row: dict) -> GeminiModel:
    """Creates a GeminiModel object from a CSV row dictionary."""
    pricing = ModelPricing(
        input_text=(
            float(row["price_input_text"]) if row.get("price_input_text") else None
        ),
        input_audio=(
            float(row["price_input_audio"]) if row.get("price_input_audio") else None
        ),
        input_video=(
            float(row["price_input_video"]) if row.get("price_input_video") else None
        ),
        input_image=(
            float(row["price_input_image"]) if row.get("price_input_image") else None
        ),
        output_text=(
            float(row["price_output_text"]) if row.get("price_output_text") else None
        ),
        output_audio=(
            float(row["price_output_audio"]) if row.get("price_output_audio") else None
        ),
        output_video=(
            float(row["price_output_video"]) if row.get("price_output_video") else None
        ),
        output_image=(
            float(row["price_output_image"]) if row.get("price_output_image") else None
        ),
    )

    context = ModelContext(
        input_modalities=parse_list(row["input_modalities"]),
        output_modalities=parse_list(row["output_modalities"]),
        input_max_tokens=int(row["input_max_tokens"]),
        output_max_tokens=int(row["output_max_tokens"]),
    )

    return GeminiModel(
        name=row["name"],
        variant=row["variant"],
        api_name=row["api_name"],
        release_date=row["release_date"],
        knowledge_cutoff=row["knowledge_cutoff"],
        location=parse_list(row["location"]),
        model_features=parse_list(row["model_features"]),
        sdks=parse_sdks(row["sdks"]),
        adk=parse_sdks(row["adk"]),
        pricing=pricing,
        context=context,
    )


def main():
    """Main function to generate reports from CSV data."""
    # Ensure you have Jinja2 installed: pip install Jinja2
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_dir))
    template = env.get_template("template_model_card.html")

    csv_path = os.path.join(current_dir, "models.csv")

    try:
        with open(csv_path, mode="r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                model_obj = create_model_from_row(row)

                # Format numbers with commas for the template
                template_data = {
                    "model": {
                        "name": model_obj.name,
                        "variant": model_obj.variant,
                        "api_name": model_obj.api_name,
                        "release_date": model_obj.release_date,
                        "knowledge_cutoff": model_obj.knowledge_cutoff,
                        "input": {
                            "modalities": [
                                MODALITY_ICONS.get(m, m)
                                for m in model_obj.context.input_modalities
                            ],
                            "max_tokens": f"{model_obj.context.input_max_tokens:,}",
                        },
                        "output": {
                            "modalities": [
                                MODALITY_ICONS.get(m, m)
                                for m in model_obj.context.output_modalities
                            ],
                            "max_tokens": f"{model_obj.context.output_max_tokens:,}",
                        },
                        "location": model_obj.location,
                        "model_features": model_obj.model_features,
                        "pricing": {
                            "input": {
                                "text": model_obj.pricing.input_text,
                                "audio": model_obj.pricing.input_audio,
                                "video": model_obj.pricing.input_video,
                                "image": model_obj.pricing.input_image,
                            },
                            "output": {
                                "text": model_obj.pricing.output_text,
                                "audio": model_obj.pricing.output_audio,
                                "video": model_obj.pricing.output_video,
                                "image": model_obj.pricing.output_image,
                            },
                        },
                        "sdks": model_obj.sdks,
                        "adk": model_obj.adk,
                    }
                }

                output_html = template.render(template_data)

                # Sanitize api_name for the filename
                safe_api_name = (
                    model_obj.api_name.lower().replace(" ", "_").replace("-", "_")
                )
                output_filename = f"report_{safe_api_name}.html"
                output_path = os.path.join(current_dir, output_filename)

                with open(output_path, "w", encoding="utf-8") as outfile:
                    outfile.write(output_html)
                print(f"Successfully generated report: {output_path}")

    except FileNotFoundError:
        print(f"Error: The file {csv_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
