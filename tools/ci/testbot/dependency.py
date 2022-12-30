"""Determine the affected subprojects due to changes in the current branch"""
import glob
import logging
import os
import pathlib
import re


class ProjectModification:
    """Establish the python dependencies of the directory and allow querying of modifications"""

    def __init__(self, root_path: str) -> None:
        self.root_path = root_path

        self.subprojects = self.find_subprojects()
        self.subproject_connections = {}

        for subproject in self.subprojects:
            self.subproject_connections[subproject] = self.find_editable_installs(subproject)

        self.dependency_graph = self.generate_dependency_graph(self.subproject_connections)

    def find_subprojects(self) -> set[str]:
        """
        Find all python subprojects, assuming every directory containing either a setup.py or a
        Pipfile is a subproject
        """
        subprojects = []

        subprojects.extend(glob.glob(self.root_path + "**/pyproject.toml", recursive=True))

        subprojects = [str(pathlib.Path(project).parent) for project in subprojects]
        return set(subprojects)

    def find_editable_installs(self, project_path: str) -> set[str]:
        """
        Extract the path of all editable installs from the subproject Pipfile

        :param path: Path to directory containing pyproject
        :type path: str

        :return: set of editable install paths
        :rtype: set[str]
        """
        editable_lines = set()

        # Find every line which contains a path = "..." string and capture the install name and path
        search_pattern = r"^(.*).?=.?{.*path.?=.?\"(.*)\""

        with open(project_path + "/pyproject.toml", mode="r", encoding="UTF-8") as file:
            for line in file:
                if re_groups := re.search(search_pattern, line):
                    # editable_name = re_groups[1].rstrip()

                    editable_path = re_groups[2]
                    editable_path = os.path.normpath(project_path + "/" + editable_path)

                    editable_lines.add(editable_path)

        logging.info(
            "Project `%s` contains %d editable installs `%s`",
            project_path,
            len(editable_lines),
            list(editable_lines),
        )

        return editable_lines

    def generate_dependency_graph(self, nodes: dict[str, set[str]]) -> dict[str, set[str]]:
        """
        Generate a graph of the project dependencies

        :param nodes: Dictionary containing all imports for each node
        :type nodes: dict[str, set[str]]

        :return: A dictionary containing the direct dependents of each node
        :rtype: dict
        """

        graph: dict[str, set[str]] = {}

        for node in nodes.keys():
            graph[node] = set()

        for node, edges in nodes.items():
            for edge in edges:
                try:
                    graph[edge].add(node)
                except KeyError:
                    logging.warning("Library %s is unknown", edge)

        return graph

    def find_recursive_dependencies(
        self, starting_node: str, dependencies_graph: dict[str, set[str]]
    ) -> list[str]:
        """
        Recursively find all dependents of a starting node

        :param starting_node: Name of the starting graph node
        :type starting_node: str

        :param dependencies_graph: A dictionary containing the direct dependents of each node
        :type dependencies_graph: dict

        :return: List of node names that are dependent on the starting node
        :rtype: list
        """
        node_list = []
        for node in dependencies_graph[starting_node]:
            node_list.append(node)
            node_list.extend(self.find_recursive_dependencies(node, dependencies_graph))

        return node_list

    def find_modified_subprojects(self, files_changed: list[str]) -> set:
        """
        Using a list of changed files changed find which subprojects have been changed

        :param files_changed: List of files changed
        :type files_changed: list[str]

        :return: Set containing all subprojects changed
        :rtype: set
        """
        subprojects_changed = set()

        for file in files_changed:
            for subproject in self.subprojects:
                common_prefix = str(os.path.commonprefix([file, subproject]))

                if subproject == common_prefix:
                    subprojects_changed.add(common_prefix)
                    break

        return subprojects_changed

    def find_affected_subprojects(self, files_changed: list[str]) -> set[str]:
        """
        Follow the graph to find all affected subprojects

        :param files_changed: List of files changed
        :type files_changed: list[str]

        :return: Set containing all subprojects that are affected by changed to the input list
        :rtype: set
        """
        affected_projects = []

        subprojects_changed = self.find_modified_subprojects(files_changed)

        for project in subprojects_changed:
            affected_projects.append(project)
            affected_projects.extend(
                self.find_recursive_dependencies(project, self.dependency_graph)
            )

        return set(affected_projects)

    def remove_root_dir(self, input_set: set) -> list:
        return [item[len(self.root_path) :] for item in input_set]


def find_modified_files(root_path: str, comparison_branch: str = "dev") -> list[str]:
    """
    Get a list of all the files that have been modified compared to dev

    :param comparison_branch: Name of the default branch
    :type comparison_branch: str

    :return: List of files paths for files changed
    :rtype: list
    """
    cmd = f"cd {root_path} && git diff --name-only --diff-filter=ACMRT {comparison_branch}"
    output = os.popen(cmd).read()[:-1]

    if len(output) == 0:
        return []

    files_changed = output.split("\n")
    return [root_path + file for file in files_changed]
