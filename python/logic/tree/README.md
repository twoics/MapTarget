Here are the modules that implement the logic of the KD-tree

- `point`: implements a point class on a two-dimensional plane

- `node`: implements a node class containing a `point` and some useful data (or None)

- `tree`: Implements a class that executes the basic logic of the KD-tree

- `tree_map`: implements a class, a descendant of Kd-tree, which uses the distance on the sphere as a metric 
for the distance between points (needed to find objects by coordinates - latitude and longitude)
