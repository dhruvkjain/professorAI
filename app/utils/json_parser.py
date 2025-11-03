import json
import re


def extract_json_from_document(document_text):
   
    json_pattern = r'\[\s*\{.*?\}\s*\]'
    match = re.search(json_pattern, document_text, re.DOTALL)

    def try_parse_json(json_str):
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None

    if match:
        data = try_parse_json(match.group(0))
        if data is not None:
            return data

    start_idx = document_text.find('[')
    end_idx = document_text.rfind(']')
    if start_idx != -1 and end_idx != -1:
        json_str = document_text[start_idx:end_idx + 1]
        data = try_parse_json(json_str)
        if data is not None:
            return data

    return None