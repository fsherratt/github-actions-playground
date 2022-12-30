import argparse
import logging

from testbot.dependency import ProjectModification, find_modified_files


def parse_args() -> argparse.Namespace:
    """
    Setup argument parsing

    :return:
    :rtype:
    """
    args = argparse.ArgumentParser(allow_abbrev=False)
    args.add_argument("--root-dir", type=str, help="Set root directory to search from")
    args.add_argument(
        "-O",
        "--enable-output",
        action=argparse.BooleanOptionalAction,
        help="Print final output",
    )
    args.add_argument(
        "-V",
        "--verbose",
        action=argparse.BooleanOptionalAction,
        help="Set Logging Level to Verbose",
    )

    return args.parse_args()


def main(root_path: str) -> list:
    """Main function"""

    python_dependency = ProjectModification(root_path)

    files_changed = find_modified_files(root_path, comparison_branch="")
    subprojects_changed = python_dependency.find_modified_subprojects(files_changed)
    affected_projects = python_dependency.find_affected_subprojects(files_changed)

    # Print out the results of this function
    logging.info("Files modified `%s`", files_changed)
    logging.info("In the subprojects `%s`", list(subprojects_changed))
    logging.info("To test run the following subproject test suites `%s`", list(affected_projects))

    return list(affected_projects)


if __name__ == "__main__":
    input_args = parse_args()

    if input_args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    result = main(input_args.root_dir)

    if input_args.enable_output:
        print(result)
