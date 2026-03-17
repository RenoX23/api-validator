def print_report(results):
    print("\n" + "=" * 60)
    print("  API VALIDATION REPORT")
    print("=" * 60)

    passed = 0
    failed = 0

    for result in results:
        name = result["name"]
        url = result["url"]
        mismatches = result["mismatches"]
        fetch_error = result.get("fetch_error")

        print(f"\n[ {name} ]")
        print(f"  URL: {url}")

        if fetch_error:
            print(f"  STATUS : ERROR")
            print(f"  REASON : {fetch_error}")
            failed += 1
            continue

        real_issues = [m for m in mismatches if m["issue"] != "extra_field"]
        extras = [m for m in mismatches if m["issue"] == "extra_field"]

        if not real_issues:
            print(f"  STATUS : PASS")
            passed += 1
        else:
            print(f"  STATUS : FAIL")
            failed += 1

        for m in real_issues:
            field = m["field"]
            issue = m["issue"]

            if issue == "missing":
                print(f"  └─ '{field}' is missing from response")
            elif issue == "type_mismatch":
                print(f"  └─ '{field}' expected {m['expected']}, got {m['got']}")
            elif issue == "unknown_type_in_schema":
                print(f"  └─ '{field}' has unknown type '{m['expected']}' in schema")

        if extras:
            print(f"  WARNINGS ({len(extras)} extra fields not in schema):")
            for m in extras:
                print(f"  └─ '{m['field']}' returned by API but not in schema")

    print("\n" + "=" * 60)
    print(f"  TOTAL: {passed + failed} endpoints | PASSED: {passed} | FAILED: {failed}")
    print("=" * 60 + "\n")
