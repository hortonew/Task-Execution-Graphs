"""Process a stream of text and produce valid task graphs considering dependencies."""
import sys

from task_graphs.StreamProcessor import Stream, StreamException
from task_graphs.TaskGroups import TaskException, TaskGroupBuilder

# Single solution per group
OUTPUT_ALL_SOLUTIONS = True


def main():
    # accept stdin: cat test.txt | python main.py
    try:
        process_stream()
    except TaskException as texception:
        exit_gracefully(texception)
    except StreamException as sexception:
        exit_gracefully(sexception)
    except Exception as e:
        exit_gracefully(e)


def process_stream():
    """
    Ingests a stream from stdin and reports 1 possible task execution order per task group.

    Example:
        input: 'B:A\n#this is a comment\n\n\nlearn:win,fail'
        output:
            A B
            win fail learn
    """
    stream = Stream(sys.stdin.readlines())
    builder = TaskGroupBuilder(stream)
    tasks = builder.convert_stream_to_definitions()
    task_groups = builder.build_task_groups(tasks)
    if len(task_groups) == 0:
        exit_gracefully('No task execution groups could be created.')

    # Output a single result per task group
    for task_group in task_groups:
        results = task_group.calculate_possible_orderings()
        if OUTPUT_ALL_SOLUTIONS:
            for result in results:
                print(result)
        else:
            print(results[0])


def exit_gracefully(error):
    """Helper function to return an error to stderr and return exit code 1."""
    print(error, file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main()
