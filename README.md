# Task Graphs

The purpose of this application is to process a stream of text containing task execution orders into valid task execution groups.

## Example

    ❯ echo 'T:A,B\nA:\nB:\n\nT:A,B\nA:C\nB:C\nC:D\nD:' |  python main.py

    A B T
    D C A B T

Comments and empty lines should be ignored.

    ❯ echo 'B:A\n#this is a comment\n\n\nlearn:win,fail' | python main.py 2>error_log

    A B
    win fail learn

Entire files can be sent in for processing.

    ❯ cat lib/sample_file.txt |  python main.py 2>error_log                         
    A B T
    D C A B T
    F D E A B C T
    Build LoadTest FunctionalTest VirusScan Release

A single solution per group is all that's needed, but if you want to see all the potential solutions, set `OUTPUT_ALL_SOLUTIONS=True` in main.py.

    ❯ echo 'Release:LoadTest,FunctionalTest,VirusScan\nLoadTest:Build\nFunctionalTest:Build\nVirusScan:Build\nBuild:' |  python main.py 2>error_log 
    Build LoadTest FunctionalTest VirusScan Release
    Build FunctionalTest LoadTest VirusScan Release
    Build VirusScan LoadTest FunctionalTest Release
    Build LoadTest VirusScan FunctionalTest Release
    Build FunctionalTest VirusScan LoadTest Release
    Build VirusScan FunctionalTest LoadTest Release

## First time setup

Ideally, set up a python virtual environment.  This was tested using python 3.8.11, but should work on python3.8+.

    python3.8 -m virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Dependencies

This application makes use of [networkx](https://networkx.org/) for converting task execution orders into a Directed Acyclic Graph (DAG).  The benefit of doing this is two-fold:

1.  We benefit from using existing graph based algorithms that can detect the topology of the graph, outputting all the possible paths taken through the graph (considering the dependencies).
2.  We can detect if a graph is in fact not acyclic (or has a cycle) very simply.  A cycle is any point in which there a cyclic dependencies (a loop) in which case it would be impossible to resolve dependencies.

## Contribution guide

The developers of this repository use automatic code linting and formatting tools.  Currently, `flake8`, `blue` (less opinionated black formatter), and `isort` are used.  Please run these tools manually, through your IDE, or via pre-commit hook to maintain standardization across the code base.

## Definitions

A `task execution order` defines all the tasks as nodes, and their dependent nodes in format `Node:NodeDependencyA,NodeDependendyB`.

A `task execution group` is a valid ordering or execution plan that if executed from left to right would result in all dependencies being executed first followed by the nodes that rely on them.

## Test

To run the unit tests or see code coverage of the tests, run pytest:

    ❯ pytest
    Test session starts (platform: darwin, Python 3.8.11, pytest 6.2.5, pytest-sugar 0.9.4)
    plugins: sugar-0.9.4, cov-3.0.0
    collecting ... 
     tests/test_invalid_tasks.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓                                                                                                                                                     59% █████▉    
     tests/test_text_streams.py ✓✓✓✓✓✓✓✓✓                                                                                                                                                                        78% ███████▉  
     tests/test_valid_tasks.py ✓✓✓✓✓✓✓✓✓✓                                                                                                                                                                       100% ██████████

    ---------- coverage: platform darwin, python 3.8.11-final-0 ----------
    Name                             Stmts   Miss  Cover   Missing
    --------------------------------------------------------------
    task_graphs/StreamProcessor.py       8      0   100%
    task_graphs/TaskGroups.py           69      0   100%
    task_graphs/__init__.py              0      0   100%
    --------------------------------------------------------------
    TOTAL                               77      0   100%


    Results (0.66s):
          46 passed

## With more time

1.  Fuzzing stdin with a larger sample size of inputs
2.  Could add parameters for outputting the graphs to their own images directly via Matplotlib.  This would enable one to conceptualize large sets of dependencies.
3.  Remote git repository with CI/CD best practices
4.  Add an API to trigger from other systems
