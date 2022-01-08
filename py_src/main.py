"""
Main.py, part of Blob_Traffic project.
Anthony Luo, Christina Zhang, 2022.
"""

print("HELLO WORLD")

"""
List of thing to be implemented
========================================================================================================================

General:
    - How do we want everything to be organized? 
        -> Classes for Blob?
        -> How to load environment? One big class? One giant unchangable thing? ??!?!?

Environment:
    ! Remember to start simple
    - We need some way to represent the environment for the blobs? Should we give them point clouds?
        -> It would be cool to try and run calculations to determine passable/impassable terrain from point clouds, but do we have the data?
    - What about defined roads and methods?
        -> How do we deal with changing environments such as other blobs?
    - How complex is the environment going to be...

Blobs:
    - Some how have classes for blobs that know that they want to go from one place to another place?
    - How are we teaching the blobs how to get from one place to another place? Are we just praying? A-STAR?
    - Is there anything for intention of motion?
    - how to deal with senorsy stuff like...doors....revolvign doors...other blobs? blob traffic?
    
    - will there be different kinds of blobs? Flying blobs and ground blobs and tunneling blobs?
    
Action Plan:
========================================================================================================================

Step 1:
    - Simple environment with navigatable pathways (simple 2d array suffices).
    - Simple blob that uses predetermined path to go from A -> B.
    - Simple animation to depict this.
        -> Animate the grid
        -> Animate the blob (dot?).
"""


"""
THE GRID
========================================================================================================================
Everything lives on the grid. It defines our world. 

Currently, we have elevation steps as integers from -5 to +5, with 0 being our reference or "ground" elevation.
Walls or other impassable areas are defined using characters, currently denoted 'x'

Now, I need to somehow generate a grid....let's start simple with only 0 and x...
I've added row and column numbers for simplicity...

7 | 0 X 0 0 0 0 0 0 0 0 
6 | 0 X X 0 X X X X X 0
5 | 0 0 X 0 0 0 X 0 0 0
4 | 0 0 0 0 X X X 0 X X
3 | 0 X X 0 X 0 0 0 X 0
2 | 0 X 0 0 X 0 X X X 0
1 | 0 X 0 X X 0 X 0 X 0
0 | 0 0 0 0 X 0 0 0 0 0
    -------------------
^   0 1 2 3 4 5 6 7 8 9 < Column number (+x)
Row number (+y)
"""