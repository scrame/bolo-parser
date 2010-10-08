This file describes the format of a Bolo and WinBolo map file, and 
defines some (semi)useful structures to support reading and 
writing of that file format.

Tabs are four spaces, and no lines exceed 80 characters.

12 Byte preamble, consisting of an eight byte string "BMAPBOLO"
and four data bytes:
MAP_VERSION, to allow for future map files with different formats.
p, the number of pillboxes on the map
b, the number of refuelling bases on the map
s, the number of tank starting square on the map

The current MAP_VERSION is 1.


This preamble is followed by:
5 bytes of pillbox info, repeated p times. The format is as follows:
typedef struct {
MAP_X x;     // Pill X and Y Co-ordinates
MAP_Y y;
BYTE owner;  // should be 0xFF except in speciality maps
BYTE armour; // range 0-15 (dead pillbox = 0, full strength = 15)
BYTE speed;  // typically 50. Time between shots, in 20ms units
             // Lower values makes the pillbox start off 'angry'
} BMAP_pill_info;

6 bytes of refuelling base info, repeated b times. The structure is as
follows:
typedef struct {
MAP_X x;      // Base X and Y Co-ordinates
MAP_Y y;
BYTE owner;   // should be 0xFF except in speciality maps
BYTE armour;  // initial stocks of base. Maximum value 90
BYTE shells;  // initial stocks of base. Maximum value 90
BYTE mines;   // initial stocks of base. Maximum value 90
} BMAP_base_info;

3 bytes of start square info, repeated s times:
typedef struct {
MAP_X x;  // Start X and Y Co-ordinates
MAP_Y y;
BYTE dir; // Direction towards land from this start. Range 0-15
} BMAP_start_info;


The remainder of the file -- the data which specifies the terrain of
each map square -- follows after this header.

The map is described by a series of horizontal 'runs' of non-deepsea squares.
Any square of the map not included in any 'run' is deep sea. The data portion
of each 'run' is subject to simple run-length encoding to save space.

Each run is described by a run header followed by the run data.
The run header structure is:
BYTE datalen;// length of the data for this run INCLUDING this 4 byte header
BYTE y;      // y co-ordinate of this run.
BYTE startx; // first square of the run
BYTE endx;   // last square of run + 1 (ie first deep sea square after run)

The run data takes the form of a series of NIBBLEs, where NIBBLE means
half a byte, most significant half first, least significant second.

x = startx;
while (x < endx)
	{
	The first nibble encodes the length of this portion of the run,
	and whether this portion is a sequence of different squares,
	or a sequence of identical squares.
	
	If length is 0-7 then this is a sequence of different squares.
	The next (len+1) nibbles give the terrain for the next (len+1) squares.
	
	If length is 8-15 then this is a sequence of identical squares repeated.
	The next single  nibble gives the terrain for the next (len-6) squares.
	} (repeat until run is complete)

If a run ends on an odd nibble, then it is padded out to a whole number
of bytes with an extra zero nibble.

The terrain types are:
0 Building 1 River 2 Swamp 3 Crater 4 Road 5 Forest 6 Rubble 7 Grass
8 Shot building 9 River with boat, and 10-15 are 2-7 with mines on them.

The intention is to have one 'run' per map row, but it is allowable (though
less efficient) to have more than one run per row if you wish, and if (god
forbid) you feel the need to have deep sea in the middle of your map, then
the only way to encode this is to have a run, then a gap, then another run.

The end of the map is marked by a run { 4, 0xFF, 0xFF, 0xFF };
This MUST be present or WinBolo will reject the map as invalid.

Notes:

** I use these types:
typedef unsigned char  BYTE;
typedef unsigned short WORD;
typedef BYTE MAP_X, MAP_Y;

** Coordinates start at (0,0) in the top left, and extend rightwards and
downwards. No terrain may enter a twenty square border around the edge
of the map -- ie nothing except deep sea at coordinates less than 20 or
greater than 236. This imposes an absolute maximum map size of 216x216.
Start squares may go slightly further out, but not within ten squares
of the edges. In order to stop players from "wrapping around" the game
area, Bolo generates a ten square wide border of mines in the deep sea
all around the edge of the 'world'. This is why you must not place start
squares into this border.

** Start squares indicate where new tanks may appear, and which direction
the tank will face when it appears (so that players don't have trouble
finding the land). Start squares must be on deep sea, or they will be
ignored. The direction has the value in the range 0-15, and, following
the usual mathematical convention, 0 points to the right, and values
increase in the anticlockwise direction. The units are 22.5 degree
increments, ie 0 is East, 4 is North, 8 is West and 12 is South.

** Please try to make your editor encourage the users to draw their maps
centred in the game play area. I'd like to discourage people from cramming
maps up into the top left corner of the game area. My intention is that
the major land mass should exist in the middle, circled evenly on all
sides by the distant sea mines. The sea mines should not play a strong
role in the game -- they are only there to catch strays who wander too
far from the island.

** You should check the MAP_VERSION field to ensure that you are reading
a map file format that you understand. This header file describes file
format version 1.

** The terrain specified in the file for any square containing a pillbox
or refuelling base IS SIGNIFICANT. That terrain is what will remain when
the pillbox (or base, in the future perhaps) is removed.

** No square may contain more than one base or pillbox.

** The run-length encoding of the map data is done to keep the size of map
files small, so that (after encoding with BinHex) they can be directly posted
to news groups, or sent by e-mail, without requiring any further compression.
Everard Island (the built-in map) encodes to under 2KB using this scheme.

