import argparse
import logging

from testbot.dependency import ProjectModification, find_modified_files


def setup_argparse() -> argparse.ArgumentParser:
    """
    Setup argument parsing

    :return:
    :rtype:
    """
    args = argparse.ArgumentParser(allow_abbrev=False)
    args.add_argument("--root-dir", nargs=1, type=str)
    args.add_argument("-O", "--Enable-Output", nargs="?", const=False, type=bool)

    return args.parse_known_args()


def main(root_path: str) -> list:
    """Main function"""

    python_dependency = ProjectModification(root_path)

    files_changed = find_modified_files(root_path, comparison_branch="")
    subprojects_changed = python_dependency.find_modified_subprojects(files_changed)
    affected_projects = python_dependency.find_affected_subprojects(files_changed)

    # Print out the results of this function
    logging.info("\nFiles modified")
    logging.info("----------")
    for item in files_changed:
        logging.info(item)

    logging.info("\nSubprojects Changed")
    logging.info("----------")
    logging.info(list(subprojects_changed))

    logging.info("\nRequires the following subproject test suites to be run")
    logging.info("----------")
    logging.info(list(affected_projects))

    return list(affected_projects)


if __name__ == "__main__":
    ROOT_PATH = "../../"

    args = setup_argparse()
    logging.basicConfig(level=logging.INFO)

    print(main(ROOT_PATH))
