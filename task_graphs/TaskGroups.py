"""A TaskGroups module used to process and build task execution groups."""
import re
from typing import Any, List, Tuple

import networkx as nx

from .StreamProcessor import Stream


class TaskException(Exception):
    pass


class TaskGroup:
    def __init__(self, task_definition: List[str]):
        """
        A group of tasks and associated task dependencies

        Args:
            task_definition (List[str]): Relationships between tasks and which tasks they're dependent on
        """
        if not task_definition or not isinstance(task_definition, list):
            raise TaskException('Empty task definition.')

        self.task_definition = task_definition
        self.valid_node = '^[a-zA-Z]{1,20}'

    def get_node_and_dependencies(self, task: str) -> Tuple[str, List[str]]:
        """Identify the node and dependencies for a given task."""
        if task is None:
            raise TaskException('Empty task provided.')

        dependency_pair = task.split(':')
        if len(dependency_pair) != 2:
            raise TaskException(
                'Task improperly formatted. Use format Node:DependentNode, or Node: if it has no dependencies'
            )

        if re.search(f'^{self.valid_node}:', task) is None:
            raise TaskException(
                'Task improperly formatted.  Task requires 1-20 Roman Alphabet characters followed by colon (:)'
            )

        node = task.split(':')[0]
        dependencies = task.split(':')[1].split(',')

        return node, dependencies

    def is_dependency(self, dependency: str) -> bool:
        """Identify if this is a valid task dependency or not."""
        if (
            len(dependency) > 0
            and re.search(f'{self.valid_node}', dependency) is None
        ):
            raise TaskException(
                'Invalid dependent task.  Dependent task must be 1-20 Roman Alphabet characters.'
            )

        return len(dependency) > 0

    def build_dependency_graph(self) -> nx.DiGraph:
        """Convert a given task definition into a graph object"""
        g = nx.DiGraph()
        for task in self.task_definition:
            node, dependencies = self.get_node_and_dependencies(task)
            for dependency in dependencies:
                if self.is_dependency(dependency):
                    g.add_edge(node, dependency)

        if not nx.is_directed_acyclic_graph(g):
            raise TaskException(
                'Cyclical dependencies detected.  Invalid task definition.'
            )
        return g

    def calculate_possible_orderings(self) -> List[str]:
        """
        Accepts a task definition (T:A,B) and returns a list of possible orderings

        Args:
            task_definition (List[str]): A (e.g. ['T:A,B', 'A:', 'B:'])

        Returns:
            List[str]: All possible orderings (e.g. ['A B T', 'B A T'])
        """
        g = self.build_dependency_graph()

        # Reverse each task order to do dependencies first
        all_directed_topologies = list(nx.all_topological_sorts(g))
        return [
            ' '.join(task_order[::-1])
            for task_order in all_directed_topologies
        ]


class TaskGroupBuilder:
    """A task group builder used in processing a stream of text into task execution groups."""

    def __init__(self, stream: Stream):
        self.stream = stream.lines

    @staticmethod
    def is_ignorable(line: str) -> bool:
        """Identify if the line is an ignorable line type."""
        return bool(line.startswith('#') or len(line) == 0 or line == '\n')

    def build_task_groups(self, tasks: List[List[str]]) -> List[TaskGroup]:
        """Convert each task to a task group."""
        task_groups: List[TaskGroup] = []
        for task in tasks:
            task_group = TaskGroup(task)
            task_groups.append(task_group)

        return task_groups

    def convert_stream_to_definitions(self) -> List[List[str]]:
        """Take a stream of text in list format and produce list of task definitions."""
        in_group = False
        current_group: List[Any] = []
        groups: List[Any] = []
        for line in self.stream:
            # Line shouldn't be ignored
            if not self.is_ignorable(line):
                # In a group
                if not in_group:
                    in_group = True
                    current_group = []

                current_group.append(line.replace('\n', ''))
            elif in_group:
                # Line should be ignored, but a task group may have ended
                groups.append(current_group)
                in_group = False

        # Clean up if exiting due to end of file
        if in_group and current_group:
            groups.append(current_group)

        # Change to convert to task groups
        return groups
