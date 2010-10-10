#parse_file takes a file descriptor of a map file and processes it.

from special_tiles import *

#TODO: Make it return something.

def parse_file(fd):
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

    print("Parsing runs.")
    runs = []
    keep_running = True

    count = 0
    while(keep_running):
        print "Run no:" + str(count)
        run = Run()
        run.datalen = ord(fd.read(1))
        run.y = ord(fd.read(1))
        run.startx = ord(fd.read(1))
        run.endx = ord(fd.read(1))
        raw_data = fd.read(run.datalen - 4) # MAGIC NUMBER: datalen includes the length of the header. 
                                        # 4 means there is no data!!!

        binary_data = []
        #parse byte-by-byte into integral data from binary.
        for i in raw_data:
            binary_data.append(ord(i))

        run.parse_map_data(binary_data)

        if(run.isEOF()):
            print("Encountered last run. Exiting.")
            keep_running = False
            break

        run.calculate_run()
        runs.append(run)
        count += 1

