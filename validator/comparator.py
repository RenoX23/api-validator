TYPE_MAP = {
    "string": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict
}

def compare(actual, expected, path=""):
    mismatches = []

    for key, expected_type in expected.items():
        current_path = f"{path}.{key}" if path else key

        # Key missing from actual response
        if key not in actual:
            mismatches.append({
                "field": current_path,
                "issue": "missing",
                "expected": expected_type,
                "got": None
            })
            continue

        actual_value = actual[key]

        # Expected type is a nested object — recurse
        if isinstance(expected_type, dict):
            if not isinstance(actual_value, dict):
                mismatches.append({
                    "field": current_path,
                    "issue": "type_mismatch",
                    "expected": "dict",
                    "got": type(actual_value).__name__
                })
            else:
                nested = compare(actual_value, expected_type, path=current_path)
                mismatches.extend(nested)
            continue

        # Expected type is a string like "int", "string" etc
        if expected_type not in TYPE_MAP:
            mismatches.append({
                "field": current_path,
                "issue": "unknown_type_in_schema",
                "expected": expected_type,
                "got": None
            })
            continue

        expected_python_type = TYPE_MAP[expected_type]

        if not isinstance(actual_value, expected_python_type):
            mismatches.append({
                "field": current_path,
                "issue": "type_mismatch",
                "expected": expected_type,
                "got": type(actual_value).__name__
            })

    # Check for extra fields in actual not in schema
    for key in actual:
        current_path = f"{path}.{key}" if path else key
        if key not in expected:
            mismatches.append({
                "field": current_path,
                "issue": "extra_field",
                "expected": None,
                "got": type(actual[key]).__name__
            })

    return mismatches
