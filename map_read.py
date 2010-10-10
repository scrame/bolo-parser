#parse_file takes a file descriptor of a map file and processes it.

from special_tiles import *

class MapFile:

    def __init__(self,map_file):
        fd = open(map_file, "rb");
        self.header = str(fd.read(8))

        if("BMAPBOLO" != self.header):
            print "Error! Invalid or corrupted map file"
            exit(0)

        self.map_version = ord(fd.read(1))
        self.num_pillboxes = ord(fd.read(1))
        self.num_refuelling_stations = ord(fd.read(1))
        self.num_tank_starting_squares = ord(fd.read(1))

        self.pillboxes = []
        for i in range(self.num_pillboxes):
            pillbox = Pillbox()
            pillbox.x = ord(fd.read(1))
            pillbox.y = ord(fd.read(1))
            pillbox.owner = ord(fd.read(1))
            pillbox.armor = ord(fd.read(1))
            pillbox.speed = ord(fd.read(1))
            self.pillboxes.append(pillbox)

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

        self.starting_squares = []
        for i in range(self.num_tank_starting_squares):
            start = StartingPoint()
            start.x = ord(fd.read(1))
            start.y = ord(fd.read(1))
            start.dir = ord(fd.read(1))
            self.starting_squares.append(start)

        self.runs = []
        keep_running = True

        count = 0
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
                #print("Encountered last run. Exiting.")
                keep_running = False
                break

            run.calculate_run()
            self.runs.append(run)
            count += 1

        fd.close()

