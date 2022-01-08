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