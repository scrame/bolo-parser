#!/usr/bin/python
from map_read import *

##### TODO: Handle with commandline
map_file= "maps/Fitzhu.map"

print("Opening: " + map_file);

fd = open(map_file, "rb");

MapFile(fd)

print("Closing map file...")
fd.close()

print("Good Bye!")

