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
        self.run_tiles = None

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
    def calculate_run(self):    
        #print("Parsing data: " + str(self.data))
        expected_length = (self.endx - self.startx)
        output = []
        d = self.data
        dp = 0

        inst = d[dp]

        while(None != inst):
            #print("starting inst: ", inst)

            if(0 <= inst <= 7):
                for i in range(inst+1):
                    #print("heterogenous: ", inst)
                    dp+=1
                    tile = d[dp]
                    #print("selected tile: ", tile)
                    output.append(tile)
                dp+=1
            else:
                #print("homogenous: ", inst)
                length = inst - 6 #MAGIC NUMBER: Described in the algorightm
                for i in range(length):
                    #print("Tracking tile " , i)
                    tile = d[dp+1]
                    #print("selected tile: ", tile)
                    output.append(tile)
                dp += 2
            if( (dp+1) < len(d)):
                inst = d[dp]
            else:
                inst = None

        #print("testing expected_length...")
        if(len(output) != expected_length):
            #print("ERROR: Output is the wrong length! expected: ",expected_length," actual: ",len(output))
            exit(255)

        #print("Looks good!")
        #print(output)
        self.run_tiles = output


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
