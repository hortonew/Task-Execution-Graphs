import pytest
from task_graphs.TaskGroups import TaskGroup

EXAMPLE_1 = ['T:A,B', 'A:', 'B:']
EXAMPLE_2 = ['T:A,B', 'A:C', 'B:C', 'C:D', 'D:']
EXAMPLE_3 = ['T:A,B,C', 'B:D', 'C:F', 'D:F', 'A:D,E,F', 'E:', 'F:']
EXAMPLE_4 = [
    'Release:LoadTest,FunctionalTest,VirusScan',
    'LoadTest:Build',
    'FunctionalTest:Build',
    'VirusScan:Build',
    'Build:',
]
EXAMPLE_5 = ['ABCDEFGHIJKLMNOPQRST:first', 'first:']

EXAMPLE_3_SOLUTION = [
    'F D E A B C T',
    'E F D A B C T',
    'F E D A B C T',
    'F D B E A C T',
    'E F D B A C T',
    'F E D B A C T',
    'F D E B A C T',
    'F C D E A B T',
    'F D C E A B T',
    'E F C D A B T',
    'F E C D A B T',
    'F C E D A B T',
    'F D E C A B T',
    'E F D C A B T',
    'F E D C A B T',
    'F D E A C B T',
    'E F D A C B T',
    'F E D A C B T',
    'F D B C E A T',
    'F C D B E A T',
    'F D C B E A T',
    'E F D B C A T',
    'F E D B C A T',
    'F D E B C A T',
    'F D B E C A T',
    'F C E D B A T',
    'E F C D B A T',
    'F E C D B A T',
    'F D C E B A T',
    'F C D E B A T',
    'E F D C B A T',
    'F E D C B A T',
    'F D E C B A T',
]

EXAMPLE_4_SOLUTION = [
    'Build LoadTest FunctionalTest VirusScan Release',
    'Build FunctionalTest LoadTest VirusScan Release',
    'Build VirusScan LoadTest FunctionalTest Release',
    'Build LoadTest VirusScan FunctionalTest Release',
    'Build FunctionalTest VirusScan LoadTest Release',
    'Build VirusScan FunctionalTest LoadTest Release',
]


@pytest.mark.parametrize(
    'task_definition,expected_result',
    [
        (EXAMPLE_1, ['A B T', 'B A T']),
        (EXAMPLE_2, ['D C A B T', 'D C B A T']),
        (EXAMPLE_3, EXAMPLE_3_SOLUTION),
        (EXAMPLE_4, EXAMPLE_4_SOLUTION),
        (EXAMPLE_5, ['first ABCDEFGHIJKLMNOPQRST']),
    ],
)
def test_valid_task_definitions(task_definition, expected_result):
    task_group = TaskGroup(task_definition)
    task_orders = task_group.calculate_possible_orderings()
    assert task_orders == expected_result


@pytest.mark.parametrize(
    'task_definition,expected_result_count',
    [
        (EXAMPLE_1, 2),
        (EXAMPLE_2, 2),
        (EXAMPLE_3, 33),
        (EXAMPLE_4, 6),
        (EXAMPLE_5, 1),
    ],
)
def test_valid_task_definition_counts(task_definition, expected_result_count):
    task_group = TaskGroup(task_definition)
    task_orders = task_group.calculate_possible_orderings()
    assert len(task_orders) == expected_result_count
