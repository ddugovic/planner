Tile World Planner v0.2
=======================

Methodology:
The planner agent pddlagent.py encodes the game state into fast-downward PDDL
problems with varying objectives, uses fast-downward to solve those problems,
and translates fast-downward output into moves to be executed by the agent
runner run_agent.py.

Setup:
This requires the tworld_py interface and should be updated with it.  Also,
as a part of that we need data, sets, and res directories from the tile world
source code, or from the levelsets repository.

set that up with (or similar)

    $ ln -s ../levelsets/data .
    $ ln -s ../levelsets/sets .
    $ ln -s ../tworld_py/res .

The fast-downward library strongly recommends the use of Python 2.7 or newer.

Usage:

    $ export FAST_DOWNWARD_HOME=/path/to/fast-downward
    $ python2.7 run_agent.py

At this point you have to press an arrow key to start the planner, which makes
moves until the level ends.

A unit test pddl/fd_run.sh is provided for debugging and can be run with:

    $ cd pddl/
    $ ./fd_run.sh domain.pddl tw-agent1.pddl

A problem generator script pddl/pddlgen.py is provided and can be run with:

    $ cd pddl/
    $ python pddlgen.py > tw_hazard.pddl

and can be tested with:

    $ ./fd_run.sh domain.pddl tw_hazard.pddl
