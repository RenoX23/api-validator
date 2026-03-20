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
        if actual_value is None:
            mismatches.append({
                "field": current_path,
                "issue": "null_value",
                "expected": expected_type,
                "got": None
                })
            continue

        # Expected type is a nested object — recurse
        # Expected type is a list_of hint — validate each element
        if isinstance(expected_type, dict) and "list_of" in expected_type:
            element_type = expected_type["list_of"]
            if not isinstance(actual_value, list):
                mismatches.append({
                    "field": current_path,
                    "issue": "type_mismatch",
                    "expected": "list",
                    "got": type(actual_value).__name__
                })
            else:
                expected_element_type = TYPE_MAP.get(element_type)
                for i, element in enumerate(actual_value):
                    if isinstance(element, bool) and expected_element_type == int:
                        mismatches.append({
                            "field": f"{current_path}[{i}]",
                            "issue": "type_mismatch",
                            "expected": element_type,
                            "got": "bool"
                        })
                    elif expected_element_type and not isinstance(element, expected_element_type):
                        mismatches.append({
                            "field": f"{current_path}[{i}]",
                            "issue": "type_mismatch",
                            "expected": element_type,
                            "got": type(element).__name__
                        })
            continue

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

        if isinstance(actual_value, bool) and expected_python_type == int:
            mismatches.append({
                "field": current_path,
                "issue": "type_mismatch",
                "expected": expected_type,
                "got": "bool"
             })
            continue

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
