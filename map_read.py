#!/usr/bin/python

##### TODO: Handle with commandline
map_file= "maps/Fitzhu.map"

print("Opening: " + map_file);

fd = open(map_file, "rb");

def read_byte():
    return ord(fd.read(1))


#Utility class that provides integer lookups for english names or symbols.
#Not currently used.
#Possibly YAGNI
class TerrainIndex:
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






####TODO: CLASSES -- either find a good inheritance hierarchy, or convert to structs and write in C.
##                      or at least make this a module.
#Classes that the files collections are mapped to.
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
    def __init__(self):
        self.datalen = None
        self.y = None
        self.startx = None
        self.endx = None
        self.data = None


    def get_nibblets(self):
        return ((self.datalen -4) * 2)

    def get_expected_length(self):
        return self.endx - self.startx
        
    #The hard part. The data is held in run-level encoding, and has to read the MSB of 
    #each byte of data. 
    def parse_map_data(self, binary_input_data):
        if(4 != self.datalen):
            data_counter = 0;
            retval = []
            while(data_counter < self.datalen-4):
                data_byte = binary_input_data[data_counter]
                #extract the most significant nibble (in decimal, not binary)
                ms_nibble = ((data_byte & 240) >> 4)
                #extract least significant nibble
                ls_nibble = (data_byte & 15)
                data_counter += 1
                retval.append(ms_nibble)
                retval.append(ls_nibble)

            self.data = retval

    #the other hard part, execute the following algorithm:


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
        return ("\nlen:\t" + str(self.datalen)
        + ("\ny:\t" + str(self.y))
        + ("\nstartx:\t" + str(self.startx))
        + ("\nendx:\t" + str(self.endx))
        + ("\nexpected output length:\t" + str(self.get_expected_length()))
        + ("\nnibblets:\t" + str(self.get_nibblets()))
        + ("\ndata:\t" + str(self.data)))


#Start of reading!
#assumes fd is a file descriptor.

header = str(fd.read(8))

#File identifier
if("BMAPBOLO" != header):
    print "Error! Invalid or corrupted map file"
    exit(0)

print header + " looks good."


#for now, print statements, and variables describe the process.
#The rest of the script procedurally creates the map.

map_version = read_byte()
print("Map version: " + str(map_version))

num_pillboxes = read_byte()
print("No. Pillboxes: " + str(num_pillboxes))

num_refuelling_stations = read_byte()
print("No. Refuelling Stations: " + str(num_refuelling_stations))

num_tank_starting_squares = read_byte()
print("No. Tank starting squares: " + str(num_tank_starting_squares))



print("Parsing Pillboxes")
pillboxes = []
for i in range(num_pillboxes):
    print("Pillbox no: " + str(i))
    pillbox = Pillbox()
    pillbox.x = read_byte()
    pillbox.y = read_byte()
    pillbox.owner = read_byte()
    pillbox.armor = read_byte()
    pillbox.speed = read_byte()
    print(pillbox)
    pillboxes.append(pillbox)

print("Parsing Refuelling Stations")
refuellers = []
for i in range(num_refuelling_stations):
    print("Refueller no: " + str(i) )
    refueller = Refueller()
    refueller.x = read_byte()
    refueller.y = read_byte()
    refueller.owner = read_byte()
    refueller.armor = read_byte()
    refueller.shells = read_byte()
    refueller.mines = read_byte()
    print(refueller)
    refuellers.append(refueller)

print("Parsing Starting Squares")
starting_squares = []
for i in range(num_tank_starting_squares):
    print("Starter no: " + str(i) )
    start = StartingPoint()
    start.x = read_byte()
    start.y = read_byte()
    start.dir = read_byte()
    print(start)
    starting_squares.append(start)


map = [[None for i in range(256)] for j in range(256)]

runs = []
print("Parsing runs.")
keep_running = True

count = 0
while(keep_running):
    print "Run no:" + str(count)
    run = Run()
    run.datalen = read_byte()
    run.y = read_byte()
    run.startx = read_byte()
    run.endx = read_byte()
    raw_data = fd.read(run.datalen - 4) # MAGIC NUMBER: datalen includes the length of the header. 
                                        # 4 means there is no data!!!

    binary_data = []
    #parse byte-by-byte into integral data from binary.
    for i in raw_data:
        binary_data.append(ord(i))

    run.parse_map_data(binary_data)

    runs.append(run)

    if(run.isEOF()):
        print("EOF")
        keep_running = False
        break

    count += 1



print("Encountered last run. Exiting.")
print("Closing map file...")
fd.close()


#
for run in runs:
    print(run)

print("Good Bye!")
