import json
import argparse
from validator.fetcher import fetch
from validator.comparator import compare
from validator.reporter import print_report

def load_config(path):
    with open(path, "r") as f:
        return json.load(f)

def run(config_path):
    config = load_config(config_path)
    endpoints = config["endpoints"]
    results = []

    for endpoint in endpoints:
        name = endpoint["name"]
        url = endpoint["url"]
        expected_schema = endpoint["expected_schema"]

        print(f"  Checking: {name}...")

        fetch_result = fetch(url)

        if not fetch_result["success"]:
            results.append({
                "name": name,
                "url": url,
                "fetch_error": fetch_result["error"],
                "mismatches": []
            })
            continue

        mismatches = compare(fetch_result["data"], expected_schema)

        results.append({
            "name": name,
            "url": url,
            "fetch_error": None,
            "mismatches": mismatches
        })

    print_report(results)

def main():
    parser = argparse.ArgumentParser(
        description="API Response Validator — validate API endpoints against expected schemas"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/sample.json",
        help="Path to config JSON file (default: config/sample.json)"
    )
    args = parser.parse_args()
    run(args.config)

if __name__ == "__main__":
    main()
