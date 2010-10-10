#Classes that the files collections are mapped to.
import pprint

class Pillbox:
    pass

class Refueller:
    pass

class StartingPoint:
    pass

class Run:
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
        expected_length = (self.endx - self.startx)
        output = []
        d = self.data
        dp = 0

        inst = d[dp]

        while(None != inst):
            if(0 <= inst <= 7):
                length = inst + 1 #MAGIC NUMBER: Described in the algorightm
                for i in range(length):
                    dp+=1
                    tile = d[dp]
                    output.append(tile)
                dp+=1
            else:
                length = inst - 6 #MAGIC NUMBER: Described in the algorightm
                for i in range(length):
                    tile = d[dp+1]
                    output.append(tile)
                dp += 2
            if( (dp+1) < len(d)):
                inst = d[dp]
            else:
                inst = None

        if(len(output) != expected_length):
            print("ERROR: Output is the wrong length! expected: ",expected_length," actual: ",len(output))
            exit(255)

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
