# Date      21.11
# Author    T. Boudier / Qiselong

# Notes

# Computation may take an extensive amount of time as we have to wait between two requests. Assume the cheapest model will need two hours of computation.
# It is reasonnable to assume a mistake may occur at some time for instance connextion issue, etc. For this reason we will files extensively.
# 
# The most common type of files used are .json. I know nothing about json because I come from a math formation. We will use .txt.
# we use three files:
# travels.txt distance.txt locations.txt
# locations.txt is all the coordinates of the model. 
# each line of travels.txt is two numbers (float) and a boolean (0/1)
# 0 means the travel hasn't been computed yet
# each line of distance.txt is two numbers: one distance, one time.
#
# At first computation we generate all the travels according to locations.txt. 
# An intelligent mind would forbidd to generate all travels, sadly i'm a donkey.

# At each iteration: 

#   open travels.txt. 
#   pick 1st line ending with a 0 
#   gather s and d (start & destination) and line number
#   close travels.txt
#   open distance.txt
#   compute with requests... the distance with s and d
#   write on the last line s, d and the result computed.
#   close distance.txt
#   open travels .txt. 
#   go to line number and replace the 0 with a 1
#   go next line and repeat.

import time
import requests



#parameters
w_time = 5.1
s = '45.1524,5.74812' #Eybens
d = '45.273157,5.9244034' #froges
msg = 'Note the execution must be done from ORCO21 folder.\nIf any problem to access file verify the cmd is open at the right location.\n'
#modes:
#   generation: uses the locations.txt to generate travels.txt (1: erase all content from travels; 2: add all combination from the content of )
#   computation: uses travels.txt to compute
mode = 'generation1'
# files adresses
locations = 'LT/project/txt_files/locations.txt'
travels = 'LT/project/txt_files/travels.txt'
distances = 'LT/project/txt_files/distances.txt'


def main():
    print(msg)
    if mode == 'generation1' or mode == 'generation2':
        generation(locations, travels, mode)

    act_line=-1
    done = False:
    while done == False:
        f= open(travels, 'r')
        if act_line==-1:
            line = f.readline()
            if line[-1]==0:
                #get line number, etc.TODO

# functions

def generation(locations, travels, mode):
    """
    fill the travels file with datas of locations file acoording to the method explicited in notes (L. 4)
    mode == generation1 => travels will be erased beforehand
    mode == generation2 => possible travels will be added to travels. To use if we clustered the stuff beforehand or if datas are obtained slowly.
    """

    Locs = []
    f = open(locations, 'r')
    for line in f:
        Locs.append(line)
    for line in range(len(Locs)-1):
        Locs[line] = Locs[line][0: len(Locs[line])-2]

    f.close()

    if mode == 'generation1':
        open(travels, 'w').close()

    f = open(travels, 'a')
    f.write("\n")

    for s in range(len(Locs)):
        for d in range(s):
            f.write(Locs[s] + ";"+Locs[d]+ ";0\n")
    f.close() 
            
# STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN

def call(sd):
    """
    use osrm to get the distance between s and d. Note sd must be a string obtained by doing: s+';'+d
    """
    url = "http://router.project-osrm.org/route/v1/driving/"+ sd + "?alternatives=true"
    r = requests.get(url)
    res = r.json()
    return res["routes"][0]["distance"], res["routes"][0]["duration"]

# STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN STEPHANE BERN





main()
