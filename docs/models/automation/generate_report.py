import os
import yaml
from jinja2 import Environment, FileSystemLoader
from model_data import GeminiModel, ModelContext, ModelPricing

# SVG icons for modalities
MODALITY_ICONS = {
    "Text": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><line x1="10" y1="9" x2="8" y2="9"></line></svg>''',
    "Audio": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line></svg>''',
    "Video": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect><line x1="7" y1="2" x2="7" y2="22"></line><line x1="17" y1="2" x2="17" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line><line x1="2" y1="7" x2="7" y2="7"></line><line x1="2" y1="17" x2="7" y2="17"></line><line x1="17" y1="17" x2="22" y2="17"></line><line x1="17" y1="7" x2="22" y2="7"></line></svg>''',
    "Image": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>''',
}

def create_model_from_dict(data: dict) -> GeminiModel:
    """Creates a GeminiModel object from a dictionary."""
    pricing_data = data.get("pricing", {})
    input_pricing = pricing_data.get("input", {})
    output_pricing = pricing_data.get("output", {})
    pricing = ModelPricing(
        input_text=input_pricing.get("text"),
        input_audio=input_pricing.get("audio"),
        input_video=input_pricing.get("video"),
        input_image=input_pricing.get("image"),
        output_text=output_pricing.get("text"),
        output_audio=output_pricing.get("audio"),
        output_video=output_pricing.get("video"),
        output_image=output_pricing.get("image"),
    )

    context_data = data.get("context", {})
    context = ModelContext(
        input_modalities=context_data.get("input_modalities", []),
        output_modalities=context_data.get("output_modalities", []),
        input_max_tokens=context_data.get("input_max_tokens"),
        output_max_tokens=context_data.get("output_max_tokens"),
    )

    return GeminiModel(
        name=data.get("name"),
        variant=data.get("variant"),
        api_name=data.get("api_name"),
        release_date=data.get("release_date"),
        knowledge_cutoff=data.get("knowledge_cutoff"),
        location=data.get("location", []),
        model_features=data.get("model_features", []),
        sdks=data.get("sdks", {}),
        adk=data.get("adk", {}),
        pricing=pricing,
        context=context,
    )


def main():
    """Main function to generate reports from YAML data."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_dir))
    template = env.get_template("template_model_card.html")

    yaml_path = os.path.join(current_dir, "..", "config", "models.yaml")

    try:
        with open(yaml_path, "r", encoding="utf-8") as infile:
            data = yaml.safe_load(infile)
            for model_data in data.get("models", []):
                model_obj = create_model_from_dict(model_data)

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
                            "max_tokens": f'{model_obj.context.input_max_tokens:,}',
                        },
                        "output": {
                            "modalities": [
                                MODALITY_ICONS.get(m, m)
                                for m in model_obj.context.output_modalities
                            ],
                            "max_tokens": f'{model_obj.context.output_max_tokens:,}',
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

                safe_api_name = (
                    model_obj.api_name.lower().replace(" ", "_").replace("-", "_")
                )
                output_filename = f"report_{safe_api_name}.html"
                output_path = os.path.join(current_dir, "..", "reports", output_filename)

                with open(output_path, "w", encoding="utf-8") as outfile:
                    outfile.write(output_html)
                print(f"Successfully generated report: {output_path}")

    except FileNotFoundError:
        print(f"Error: The file {yaml_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()