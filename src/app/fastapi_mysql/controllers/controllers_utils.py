from typing import Any, Dict, List


def validate_input_keys(json_input_data: Dict[str, Any], valid_keys: List[str]) -> None:
    input_keys = set(json_input_data.keys())
    valid_keys_set = set(valid_keys)

    missing_keys = valid_keys_set - input_keys
    invalid_keys = input_keys - valid_keys_set

    if missing_keys or invalid_keys:
        error_message = []
        if missing_keys:
            error_message.append(f"Missing keys: {', '.join(missing_keys)}")
        if invalid_keys:
            error_message.append(f"Invalid keys: {', '.join(invalid_keys)}")

        raise ValueError(". ".join(error_message))
