import re

def extract_code_blocks(text):
    code_pattern = re.compile(
        r"```([a-zA-Z0-9_]+)?\n(.*?)```", re.DOTALL
    )

    blocks = {}
    for match in re.finditer(code_pattern, text):
        block_type = match.group(1) or "unknown"
        code_content = match.group(2).strip()
        blocks[block_type] = code_content

    return blocks