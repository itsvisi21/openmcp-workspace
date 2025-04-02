"""OpenMCP Library Module

This module provides common utilities and functions used across the OpenMCP project.
"""
from typing import Any, Dict, List, Optional
import json


def merge_configs(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two configuration dictionaries with override taking precedence.
    
    Args:
        base: Base configuration dictionary
        override: Override configuration dictionary
    
    Returns:
        Merged configuration dictionary
    """
    result = base.copy()
    for key, value in override.items():
        if (
            key in result 
            and isinstance(result[key], dict) 
            and isinstance(value, dict)
        ):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    return result


def parse_json_string(json_str: str) -> Optional[Dict[str, Any]]:
    """Parse a JSON string into a dictionary.
    
    Args:
        json_str: JSON string to parse
    
    Returns:
        Parsed dictionary or None if parsing fails
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None


def filter_dict_keys(data: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, Any]:
    """Filter a dictionary to only include specified keys.
    
    Args:
        data: Dictionary to filter
        allowed_keys: List of keys to keep
    
    Returns:
        Filtered dictionary
    """
    return {k: v for k, v in data.items() if k in allowed_keys}


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """Flatten a nested dictionary using dot notation.
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key for nested items
        sep: Separator to use between keys
    
    Returns:
        Flattened dictionary
    """
    items: List[tuple] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items) 