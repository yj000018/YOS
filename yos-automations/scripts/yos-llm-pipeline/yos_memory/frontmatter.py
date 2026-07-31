import yaml
import re
from typing import Dict, Any, Tuple

def read_markdown(content: str) -> Tuple[Dict[str, Any], str]:
    """
    Parse a Markdown string with YAML frontmatter.
    Returns (metadata_dict, body_string).
    """
    if not content.startswith("---\n"):
        return {}, content
        
    # Match the frontmatter block
    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not match:
        return {}, content
        
    yaml_str, body = match.groups()
    try:
        metadata = yaml.safe_load(yaml_str) or {}
        return metadata, body.lstrip()
    except yaml.YAMLError:
        return {}, content

def write_markdown(metadata: Dict[str, Any], body: str) -> str:
    """
    Generate a Markdown string with YAML frontmatter.
    """
    # Use sort_keys=False to preserve dictionary order if Python >= 3.7
    yaml_str = yaml.dump(metadata, sort_keys=False, allow_unicode=True, default_flow_style=False)
    
    # Ensure body doesn't have excessive leading/trailing newlines
    body_clean = body.strip()
    
    return f"---\n{yaml_str}---\n\n{body_clean}\n"
