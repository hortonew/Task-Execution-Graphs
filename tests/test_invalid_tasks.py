import pytest
from task_graphs.TaskGroups import TaskException, TaskGroup


@pytest.mark.parametrize(
    'task_definition',
    [
        '',
        ['A:B,C', 'B:C', 'C:A'],
        ['A;B,C', 'B;C', 'C;A'],
        4,
        [],
        (4, 'test'),
        {},
        {'test': 123456789123456789123456789},
        ['ABCDEFGHIJKLMNOPQRSTU:B', 'B:'],
        ['A;B,C', 'B;C', 'C;A'],
        ['A'],
        {1, 2, 3},
        {'one', 'two'},
        ['A123:AZ5'],
        ['A:B;C', 'B:C', 'CA'],
        ['A:;'],
        ['#A:B'],
        ['#;:B'],
        ['#:B'],
        None,
        (None, None),
        {None},
        'None',
        [None],
        '♥',
        ['♥:B'],
        ['B:♥'],
    ],
)
def test_invalid_task_definitions(task_definition):
    with pytest.raises(TaskException):
        task_group = TaskGroup(task_definition)
        task_group.calculate_possible_orderings()
