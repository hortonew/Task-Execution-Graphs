import pytest
from task_graphs.StreamProcessor import Stream, StreamException
from task_graphs.TaskGroups import TaskGroup, TaskGroupBuilder


@pytest.fixture(scope='session')
def sample_file():
    with open('lib/sample_file.txt', 'r') as f:
        execution_order = f.readlines()

    return execution_order


@pytest.fixture(scope='session')
def single_line_file():
    with open('lib/single_line_file.txt', 'r') as f:
        execution_order = f.readlines()

    return execution_order


def test_full_file(sample_file):
    assert len(sample_file) == 113
    stream = Stream(sample_file)
    assert stream.lines == sample_file


def test_create_task_groups_from_stream(sample_file):
    stream = Stream(sample_file)

    tgb = TaskGroupBuilder(stream)
    assert isinstance(stream.lines, list)

    tasks = tgb.convert_stream_to_definitions()
    task_groups = tgb.build_task_groups(tasks)
    assert len(task_groups) == 4
    for task_group in task_groups:
        assert isinstance(task_group, TaskGroup)


def test_create_task_groups_from_stream_single_line(single_line_file):
    stream = Stream(single_line_file)

    tgb = TaskGroupBuilder(stream)
    assert isinstance(stream.lines, list)

    tasks = tgb.convert_stream_to_definitions()
    task_groups = tgb.build_task_groups(tasks)
    assert len(task_groups) == 1
    for task_group in task_groups:
        assert isinstance(task_group, TaskGroup)


@pytest.mark.parametrize('lines', [None, '', 1, {}, {1: 2}, '♥'])
def test_stream_exception(lines):
    with pytest.raises(StreamException):
        Stream(lines)
