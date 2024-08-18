import pytest

from . import validate_input_keys


def test_validate_input_keys__when_all_keys_are_present() -> None:
    json_input_data = {
        "key1": "value1",
        "key2": "value2",
    }
    valid_keys = ["key1", "key2"]

    validate_input_keys(json_input_data, valid_keys)


def test_validate_input_keys__when_some_keys_are_missing() -> None:
    json_input_data = {
        "key1": "value1",
    }
    valid_keys = ["key1", "key2"]

    with pytest.raises(ValueError) as exc_info:
        validate_input_keys(json_input_data, valid_keys)
    assert str(exc_info.value) == "Missing keys: key2"


def test_validate_input_keys__when_some_keys_are_invalid() -> None:
    json_input_data = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
    }
    valid_keys = ["key1", "key2"]

    with pytest.raises(ValueError) as exc_info:
        validate_input_keys(json_input_data, valid_keys)
    assert str(exc_info.value) == "Invalid keys: key3"
