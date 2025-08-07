import pprint
import sys
import json
from pathlib import Path
from typing import Any

if len(sys.argv) != 4:
    raise ValueError(
        "Invalid number of arguments supplied "
        f"(must get 3 paths, got {len(sys.argv) - 1} args)"
    )

try:
    args: list[Path] = [Path(arg) for arg in sys.argv[1:]]

except ValueError as err:
    raise ValueError("Must get only paths as arguments") from err

tests_path: Path
values_path: Path
report_path: Path
tests_path, values_path, report_path = args

with tests_path.open(encoding="utf-8") as report_file:
    tests_data: dict[str, list[dict[str, Any]]] = json.load(report_file)

with values_path.open(encoding="utf-8") as report_file:
    tests_results: dict[str, Any] = json.load(report_file)


def preprocess_test_results(test_results_values: dict[str, Any]) -> dict[int, dict[str, Any]]:
    preprocessed_results: dict[int, dict[str, Any]] = {}
    for test_result in test_results_values["values"]:
        preprocessed_results[test_result["id"]] = {"value": test_result["value"]}

    return preprocessed_results


def fill_results(
    tests_data_input: list[dict[str, Any]],
    tests_results_input: dict[int, dict[str, Any]]
) -> None:
    for test in tests_data_input:
        if "id" in test and "value" in test:
            result_id: int = test["id"]
            test["value"] = tests_results_input[result_id]["value"]

        if "values" in test:
            fill_results(test["values"], tests_results_input)


fill_results(
    tests_data["tests"],
    preprocess_test_results(tests_results)
)

with report_path.open(mode="w+") as report_file:
    json.dump(tests_data, report_file, indent=2)
