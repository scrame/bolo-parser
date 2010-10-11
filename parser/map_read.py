#parse_file takes a file descriptor of a map file and processes it.

from special_tiles import *
from terrain import *
from os.path import basename


class MapFile:

    def __init__(self,map_file):
        fd = open(map_file, "rb");

        self.map_name=basename(map_file)
        self.read_header(fd)
        self.read_pillboxes(fd)
        self.read_refuellers(fd)
        self.read_starting_squares(fd)
        self.read_runs(fd)

        self.calculate_map()
        self.write_map()

        fd.close()
        fd = None

    def write_map(self):
        f = open(self.map_name + ".txt", "w")
        for x in self.map:
            for y in x:
                if(TerrainIndex.default_index == y):
                    f.write(TerrainIndex.default_symbol),
                else:
                    f.write(TerrainIndex.terrain_symbols[y])
            f.write("\n")
        f.close()

    def calculate_map(self):
        print("trying to calculate the map")
        self.map = []
        #zeroing out the map.
        for i in range(256):
            row = []
            for j in range(256):
                row.append(TerrainIndex.default_index)
            self.map.append(row)
            
        for run in self.runs:
            i = run.startx
            for d in run.run_tiles:
                self.map[i][run.y] = d
                i+=1

    def read_header(self,fd):
        self.header = str(fd.read(8))

        if("BMAPBOLO" != self.header):
            print("Error! Invalid or corrupted map file")
            exit(255)

        self.map_version = ord(fd.read(1))
        self.num_pillboxes = ord(fd.read(1))
        self.num_refuelling_stations = ord(fd.read(1))
        self.num_tank_starting_squares = ord(fd.read(1))
        

    def read_pillboxes(self,fd):
        self.pillboxes = []
        for i in range(self.num_pillboxes):
            pillbox = Pillbox()
            pillbox.x = ord(fd.read(1))
            pillbox.y = ord(fd.read(1))
            pillbox.owner = ord(fd.read(1))
            pillbox.armor = ord(fd.read(1))
            pillbox.speed = ord(fd.read(1))
            self.pillboxes.append(pillbox)
            
    def read_refuellers(self,fd):
        self.refuellers = []
        for i in range(self.num_refuelling_stations):
            refueller = Refueller()
            refueller.x = ord(fd.read(1))
            refueller.y = ord(fd.read(1))
            refueller.owner = ord(fd.read(1))
            refueller.armor = ord(fd.read(1))
            refueller.shells = ord(fd.read(1))
            refueller.mines = ord(fd.read(1))
            self.refuellers.append(refueller)

    def read_starting_squares(self,fd):
        self.starting_squares = []
        for i in range(self.num_tank_starting_squares):
            start = StartingPoint()
            start.x = ord(fd.read(1))
            start.y = ord(fd.read(1))
            start.dir = ord(fd.read(1))
            self.starting_squares.append(start)

    def read_runs(self,fd):
        self.runs = []
        keep_running = True
        while(keep_running):
            run = Run()
            run.datalen = ord(fd.read(1))
            run.y = ord(fd.read(1))
            run.startx = ord(fd.read(1))
            run.endx = ord(fd.read(1))
            raw_data = fd.read(run.datalen - 4) # MAGIC NUMBER: datalen includes the length of the header. 

            binary_data = []
            for i in raw_data:
                binary_data.append(ord(i))

            run.parse_map_data(binary_data)

            if(run.isEOF()):
                keep_running = False
                break

            run.calculate_run()
            self.runs.append(run)
