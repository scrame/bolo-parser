#!/usr/bin/python

class Pillbox:
    def __init__(self):
        self.x = None
        self.y = None
        self.owner = None
        self.armor = None
        self.speed = None

    def to_s(self):
        print("x:\t" + str(self.x))
        print("y:\t" + str(self.x))
        print("owner:\t" + str(self.owner))
        print("armor:\t" + str(self.armor))
        print("speed:\t" + str(self.speed))


class Refueller:
    def __init__(self):
        self.x = None
        self.y = None
        self.owner = None
        self.armor = None
        self.shells = None
        self.mines = None
        
    def to_s(self):
        print("x:\t" + str(self.x))
        print("y:\t" + str(self.x))
        print("owner:\t" + str(self.owner))
        print("armor:\t" + str(self.armor))
        print("shells:\t" + str(self.shells))
        print("mines:\t" + str(self.mines))


class StartingPoint:
    def __init__(self):
        self.x = None
        self.y = None
        self.dir = None
    
    def to_s(self):
        print("x:\t" + str(self.x))
        print("y:\t" + str(self.x))
        print("dir:\t" + str(self.dir))

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
        
    #from the docs:
    #The end of the map is marked by a run { 4, 0xFF, 0xFF, 0xFF };
    def isEOF(self):
        if(4 == self.datalen):
            if(255 == self.y):
                if(255 == self.startx):
                    if(255 == self.endx):
                        return True
        return False
        
    def to_s(self):
        print("datalen:\t" + str(self.datalen))
        print("y:\t" + str(self.y))
        print("startx:\t" + str(self.startx))
        print("endx:\t" + str(self.endx))




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
    print(pillbox.to_s())
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
    print(refueller.to_s())
    refuellers.append(refueller)

print("Parsing Starting Squares")
starting_squares = []
for i in range(num_tank_starting_squares):
    print("Starter no: " + str(i) )
    start = StartingPoint()
    start.x = ord(fd.read(1))
    start.y = ord(fd.read(1))
    start.dir = ord(fd.read(1))
    print(start.to_s())
    starting_squares.append(start)

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
    run.data = fd.read(run.datalen - 4) # MAGIC NUMBER: datalen includes the length of the header. 

    print(run.to_s())
                                             # 4 means there is no data!!!
    count += 1

    if(run.isEOF()):
        keep_running = False




print("Encountered last run. Exiting.")
print("Closing map file...")
fd.close()

print("Good Bye!")
