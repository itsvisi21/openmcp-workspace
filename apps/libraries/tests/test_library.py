"""Tests for the OpenMCP Library Module."""
import pytest
from library import merge_configs, parse_json_string, filter_dict_keys, flatten_dict


def test_merge_configs_simple():
    """Test merging simple configurations."""
    base = {"a": 1, "b": 2}
    override = {"b": 3, "c": 4}
    result = merge_configs(base, override)
    assert result == {"a": 1, "b": 3, "c": 4}


def test_merge_configs_nested():
    """Test merging nested configurations."""
    base = {
        "server": {
            "host": "localhost",
            "port": 8000,
            "settings": {"debug": True}
        }
    }
    override = {
        "server": {
            "port": 9000,
            "settings": {"debug": False, "reload": True}
        }
    }
    result = merge_configs(base, override)
    assert result == {
        "server": {
            "host": "localhost",
            "port": 9000,
            "settings": {"debug": False, "reload": True}
        }
    }


def test_parse_json_string_valid():
    """Test parsing valid JSON string."""
    json_str = '{"name": "test", "value": 42}'
    result = parse_json_string(json_str)
    assert result == {"name": "test", "value": 42}


def test_parse_json_string_invalid():
    """Test parsing invalid JSON string."""
    json_str = '{"name": "test", value: 42}'  # Missing quotes around value
    result = parse_json_string(json_str)
    assert result is None


def test_filter_dict_keys():
    """Test filtering dictionary keys."""
    data = {
        "name": "test",
        "value": 42,
        "debug": True,
        "settings": {"mode": "prod"}
    }
    allowed_keys = ["name", "value"]
    result = filter_dict_keys(data, allowed_keys)
    assert result == {"name": "test", "value": 42}
    assert len(result) == 2


def test_flatten_dict_simple():
    """Test flattening simple nested dictionary."""
    data = {
        "a": 1,
        "b": {
            "c": 2,
            "d": 3
        }
    }
    result = flatten_dict(data)
    assert result == {
        "a": 1,
        "b.c": 2,
        "b.d": 3
    }


def test_flatten_dict_deep():
    """Test flattening deeply nested dictionary."""
    data = {
        "server": {
            "host": "localhost",
            "settings": {
                "debug": True,
                "db": {
                    "url": "sqlite:///test.db"
                }
            }
        }
    }
    result = flatten_dict(data)
    assert result == {
        "server.host": "localhost",
        "server.settings.debug": True,
        "server.settings.db.url": "sqlite:///test.db"
    }


def test_flatten_dict_custom_separator():
    """Test flattening dictionary with custom separator."""
    data = {
        "a": {
            "b": {
                "c": 1
            }
        }
    }
    result = flatten_dict(data, sep='_')
    assert result == {"a_b_c": 1} 