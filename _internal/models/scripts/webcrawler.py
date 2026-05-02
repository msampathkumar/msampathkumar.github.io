import os
import re
import yaml
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime, timedelta

# --- Configuration ---
PARSE_URLS = [
    'https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-pro',
    'https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash',
    'https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash-lite',
    'https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-0-flash',
    'https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-0-flash-lite'
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WEBPAGES_DIR = os.path.join(SCRIPT_DIR, 'webpages')
GITHUB_PAGES_DIR = os.path.join(WEBPAGES_DIR, 'github')
CONFIG_DIR = os.path.join(SCRIPT_DIR, '..', 'config')


def download_pages(urls, directory):
    """Downloads the HTML content of the given URLs to the specified directory."""
    os.makedirs(directory, exist_ok=True)
    print(f"Downloader: Output directory is ready at: {directory}")

    for url in urls:
        path = urlparse(url).path
        if path.endswith('/'):
            path = path[:-1]
        filename = os.path.basename(path) + '.html'
        if not filename.strip() or filename == '.html':
            filename = url.replace('https://','').replace('http://','').replace('/','_') + '.html'
        
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            if datetime.now() - file_mod_time < timedelta(hours=24):
                print(f"   -> Skipping {url}, already downloaded recently.")
                continue

        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"   -> Successfully downloaded {url} to {filepath}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Failed to download {url}. Error: {e}")

def get_sdk_adk_info():
    """Reads the original models.yaml to get a list of SDK/ADK repos and languages."""
    sdk_info = {'sdks': [], 'adk': []}
    try:
        with open(os.path.join(CONFIG_DIR, 'models.yaml'), 'r') as f:
            data = yaml.safe_load(f)
            if data and data['models']:
                first_model = data['models'][0]
                sdk_info['sdks'] = first_model.get('sdks', [])
                sdk_info['adk'] = first_model.get('adk', [])
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"Warning: Could not read SDK/ADK info from models.yaml. Error: {e}")
    return sdk_info

def parse_github_page(html_filepath):
    """Parses a downloaded GitHub page to find the latest release version."""
    with open(html_filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    release_link = soup.select_one('a[href*="/releases/tag/"]')
    if release_link:
        return os.path.basename(release_link['href'])

    return None

def parse_model_page(html_filepath):
    """Parses a single Google Cloud model page to extract one or more models."""
    print(f"\nParser: Processing {html_filepath}...")
    with open(html_filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    models_on_page = []
    all_tables = soup.find_all('table', class_='vertex-ai-model-table')

    for table in all_tables:
        with open(os.path.join(CONFIG_DIR, 'template.yml'), 'r') as f:
            model_data = yaml.safe_load(f)

        rows = table.find_all('tr')
        for row in rows:
            header = row.find('th')
            if not header:
                continue

            if header.get('id') == 'model-id':
                code_tag = row.find('code')
                if code_tag:
                    api_name = code_tag.text.strip()
                    model_data['api_name'] = api_name
                    
                    match = re.search(r'(gemini(?:-live)?-\d\.\d)', api_name)
                    if match:
                        family_name = match.group(1).replace('-', ' ').title()
                    else:
                        family_name = api_name.split('-')[0].title()
                    model_data['name'] = family_name

                    prev_sibling = table.find_previous_sibling()
                    if prev_sibling and prev_sibling.name.startswith('h'):
                        model_data['model_name'] = prev_sibling.text.strip()
                    else:
                        model_data['model_name'] = api_name.replace('-', ' ').title()

                    print(f"   -> Found model: {model_data['model_name']} ({api_name})")

            if header.get('id') == 'supported-io':
                list_items = row.find_all('li')
                for item in list_items:
                    if 'Inputs:' in item.text:
                        inputs = [span.text.strip() for span in item.find_all('span')]
                        model_data['context']['input_modalities'] = inputs
                    if 'Outputs:' in item.text:
                        outputs = [span.text.strip() for span in item.find_all('span')]
                        model_data['context']['output_modalities'] = outputs

            if header.get('id') == 'token-limits':
                list_items = row.find_all('li')
                for item in list_items:
                    text = item.text.strip()
                    if 'Maximum input tokens:' in text:
                        model_data['context']['input_max_tokens'] = text.split(':')[-1].strip()
                    if 'Maximum output tokens:' in text:
                        model_data['context']['output_max_tokens'] = text.split(':')[-1].strip()

        cutoff_header = soup.find('th', id='knowledge-cutoff-date')
        if cutoff_header and cutoff_header.find_next_sibling('td'):
            model_data['knowledge_cutoff'] = cutoff_header.find_next_sibling('td').text.strip()

        pricing_modalities = ['text', 'image', 'audio', 'video']
        input_modalities_lower = {m.lower() for m in model_data['context']['input_modalities']}
        output_modalities_lower = {m.lower() for m in model_data['context']['output_modalities']}

        for pm in pricing_modalities:
            if pm in input_modalities_lower:
                model_data['pricing']['input'][pm] = '$NA'
            if pm in output_modalities_lower:
                model_data['pricing']['output'][pm] = '$NA'

        if model_data['api_name']:
            models_on_page.append(model_data)

    return models_on_page

def main():
    """Main function to run the web crawler and parser."""
    sdk_adk_info = get_sdk_adk_info()
    sdk_urls = {item['url']: item['lang'] for item in sdk_adk_info['sdks']}
    adk_urls = {item['url']: item['lang'] for item in sdk_adk_info['adk']}
    all_github_urls = list(sdk_urls.keys()) + list(adk_urls.keys())

    print("--- Downloading Model Documentation Pages ---")
    download_pages(PARSE_URLS, WEBPAGES_DIR)
    print("\n--- Downloading GitHub Repository Pages ---")
    download_pages(all_github_urls, GITHUB_PAGES_DIR)

    print("\n--- Parsing GitHub Pages for Versions ---")
    version_cache = {}
    for url in all_github_urls:
        path = urlparse(url).path
        if path.endswith('/'):
            path = path[:-1]
        filename = os.path.basename(path) + '.html'
        if not filename.strip() or filename == '.html':
            filename = url.replace('https://','').replace('http://','').replace('/','_') + '.html'

        filepath = os.path.join(GITHUB_PAGES_DIR, filename)
        if os.path.exists(filepath):
            version = parse_github_page(filepath)
            if version:
                version_cache[url] = version
                print(f"   -> Found version {version} for {url}")

    print("\n--- Parsing Model Documentation Pages ---")
    all_crawled_models = []
    for filename in os.listdir(WEBPAGES_DIR):
        if filename.endswith('.html') and filename != 'github':
            filepath = os.path.join(WEBPAGES_DIR, filename)
            models_from_page = parse_model_page(filepath)
            if models_from_page:
                all_crawled_models.extend(models_from_page)

    for model in all_crawled_models:
        for url, lang in sdk_urls.items():
            model['sdks'].append({
                'lang': lang,
                'url': url,
                'version': version_cache.get(url, 'N/A')
            })
        for url, lang in adk_urls.items():
            model['adk'].append({
                'lang': lang,
                'url': url,
                'version': version_cache.get(url, 'N/A')
            })

    if all_crawled_models:
        output_filepath = os.path.join(CONFIG_DIR, 'models_crawled.yaml')
        final_output = {'models': all_crawled_models}
        with open(output_filepath, 'w') as f:
            yaml.dump(final_output, f, default_flow_style=False, sort_keys=False)
        print(f"\n🎉 Successfully created {output_filepath} with {len(all_crawled_models)} models.")
    else:
        print("\nNo models were parsed. No output file created.")

if __name__ == "__main__":
    print("Running Webcrawler...")
    print("Please make sure you have installed the required libraries:")
    print("pip install requests beautifulsoup4 pyyaml")
    main()
