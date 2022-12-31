"""Run UnitTests but save the final results to JSON"""
import argparse
import json
import unittest


def get_input_args() -> argparse.Namespace:
    args = argparse.ArgumentParser()
    args.add_argument("--name", "-n", type=str, required=True, help="Unit test name")
    return args.parse_args()


if __name__ == "__main__":
    args = get_input_args()
    tests = unittest.defaultTestLoader.discover(".", pattern="test_*.py")

    # Setup and run the Test
    runner = unittest.TextTestRunner()
    test_results = runner.run(tests)

    # Passes the Result
    result_value: dict[str, int | str] = {}
    result_value["Name"] = args.name
    result_value["Total"] = test_results.testsRun
    result_value["Failures"] = len(test_results.failures)
    result_value["Errors"] = len(test_results.errors)
    result_value["Skipped"] = len(test_results.skipped)
    result_value["Passed"] = (
        result_value["Total"]
        - result_value["Failures"]
        - result_value["Errors"]
        - result_value["Skipped"]
    )

    # Save the result to a JSON-file.
    name = args.name.replace("/", "_")
    result_file_name = f"py_ut_{name}.json"
    with open(result_file_name, "w") as fp:
        json.dump(result_value, fp)

    # If an error occurs print the trace and error
    if result_value["Failures"] or result_value["Errors"]:
        exit(-1)
