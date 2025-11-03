import ast
import re

def extract_list(document_text):
    start_idx = document_text.find('[')
    end_idx = document_text.rfind(']')
    
    if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
        return None
    
    list_str = document_text[start_idx:end_idx + 1]
    
    try:
        parsed_list = ast.literal_eval(list_str)
        
        if isinstance(parsed_list, list):
            return [str(item).strip() for item in parsed_list]
        else:
            return None
            
    except (ValueError, SyntaxError):
        return extract_list_regex(list_str)


def extract_list_regex(list_str):
    content = list_str.strip()[1:-1]
    
    if not content.strip():
        return []
    pattern = r'''(?:['"]((?:[^'"]|(?<=\\)['"])*)['"]|([^,]+))'''
    matches = re.findall(pattern, content)
    
    result = []
    for match in matches:
        item = match[0] if match[0] else match[1]
        item = item.strip()
        if item:
            result.append(item)
    
    return result if result else None