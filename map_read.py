#!/usr/bin/python

class Pillbox:
    def __init__(self):
        self.x = None
        self.y = None
        self.owner = None
        self.armor = None
        self.speed = None

    def __repr__(self):
        return ("x:\t" + str(self.x)
        + ("\ny:\t" + str(self.x))
        + ("\nowner:\t" + str(self.owner))
        + ("\narmor:\t" + str(self.armor))
        + ("\nspeed:\t" + str(self.speed)))


class Refueller:
    def __init__(self):
        self.x = None
        self.y = None
        self.owner = None
        self.armor = None
        self.shells = None
        self.mines = None
        
    def __repr__(self):
        return ("x:\t" + str(self.x)
        + ("\ny:\t" + str(self.x))
        + ("\nowner:\t" + str(self.owner))
        + ("\narmor:\t" + str(self.armor))
        + ("\nshells:\t" + str(self.shells))
        + ("\nmines:\t" + str(self.mines)))


class StartingPoint:
    def __init__(self):
        self.x = None
        self.y = None
        self.dir = None
    
    def __repr__(self):
        return ("x:\t" + str(self.x)
        + ("\ny:\t" + str(self.x))
        + ("\ndir:\t" + str(self.dir)))

class Run:
    terrain_names = [
        "building",
        "river",
        "swamp",
        "crater",
        "road",
        "forest",
        "rubble",
        "grass",
        "shot building",
        "river with boat",
        "swamp w/mine",
        "crater w/mine",
        "road w/mine",
        "forest w/mine",
        "rubble w/mine",
        "grass w/mine"
        ]

    terrain_symbols = [
        "[]",
        "SS",
        "VV",
        "__",
        "==",
        "^^",
        "XX",
        ";;",
        "][",
        "BB",
        "V*",
        "_*",
        "=*",
        "^*",
        "X*",
        ";*"
        ]

    def __init__(self):
        self.datalen = None
        self.y = None
        self.startx = None
        self.endx = None
        self.data = None


    #The hard part. The data is held in run-level encoding, and has to read the MSB of 
    #each byte of data. 
    def apply_to_map(self, map):
        if(4 != self.datalen):
            data_counter = 0;
            for x in range(self.startx, self.endx):
                print x,":",self.y,self.data[data_counter]
                map[self.y][x] = self.data[data_counter]
                data_counter += 1
        
    #from the docs:
    #The end of the map is marked by a run { 4, 0xFF, 0xFF, 0xFF };
    def isEOF(self):
        if(4 == self.datalen):
            if(255 == self.y):
                if(255 == self.startx):
                    if(255 == self.endx):
                        return True
        return False
        
    def __repr__(self):
        return ("len:\t" + str(self.datalen)
        + ("\ny:\t" + str(self.y))
        + ("\nstartx:\t" + str(self.startx))
        + ("\nendx:\t" + str(self.endx)))

map_file= "maps/Fitzhu.map"

print("Opening: " + map_file);

fd = open(map_file, "rb");

header = str(fd.read(8))

if("BMAPBOLO" != header):
    print "Error! Invalid or corrupted map file"
    exit(0)

print header + " looks good."

map_version = ord(fd.read(1))
print("Map version: " + str(map_version))

num_pillboxes = ord(fd.read(1))
print("No. Pillboxes: " + str(num_pillboxes))

num_refuelling_stations = ord(fd.read(1))
print("No. Refuelling Stations: " + str(num_refuelling_stations))

num_tank_starting_squares = ord(fd.read(1))
print("No. Tank starting squares: " + str(num_tank_starting_squares))



print("Parsing Pillboxes")
pillboxes = []
for i in range(num_pillboxes):
    print("Pillbox no: " + str(i))
    pillbox = Pillbox()
    pillbox.x = ord(fd.read(1))
    pillbox.y = ord(fd.read(1))
    pillbox.owner = ord(fd.read(1))
    pillbox.armor = ord(fd.read(1))
    pillbox.speed = ord(fd.read(1))
    print(pillbox)
    pillboxes.append(pillbox)

print("Parsing Refuelling Stations")
refuellers = []
for i in range(num_refuelling_stations):
    print("Refueller no: " + str(i) )
    refueller = Refueller()
    refueller.x = ord(fd.read(1))
    refueller.y = ord(fd.read(1))
    refueller.owner = ord(fd.read(1))
    refueller.armor = ord(fd.read(1))
    refueller.shells = ord(fd.read(1))
    refueller.mines = ord(fd.read(1))
    print(refueller)
    refuellers.append(refueller)

print("Parsing Starting Squares")
starting_squares = []
for i in range(num_tank_starting_squares):
    print("Starter no: " + str(i) )
    start = StartingPoint()
    start.x = ord(fd.read(1))
    start.y = ord(fd.read(1))
    start.dir = ord(fd.read(1))
    print(start)
    starting_squares.append(start)


map = [[None for i in range(256)] for j in range(256)]

runs = []
print("Parsing runs.")
keep_running = True
count = 1
while(keep_running):
    print "Run no:" + str(count)
    run = Run()
    run.datalen = ord(fd.read(1))
    run.y = ord(fd.read(1))
    run.startx = ord(fd.read(1))
    run.endx = ord(fd.read(1))
    raw_data = fd.read(run.datalen - 4) # MAGIC NUMBER: datalen includes the length of the header. 
                                        # 4 means there is no data!!!


    #parse byte-by-byte into integral data from binary.
    run.data = []
    for i in raw_data:
        run.data.append(ord(i))

    print(run)

    print("Applying to map")
    run.apply_to_map(map)


    count += 1

    if(run.isEOF()):
        keep_running = False




print("Encountered last run. Exiting.")
print("Closing map file...")
fd.close()

print("printing rendered map.")
for i in map:
    for j in i:
        if(None == j):
            print(".."),
        else:
            print(j),
        print(" "),
    print("")

print("Good Bye!")
