# Date      21.11
# Author    T. Boudier / Qiselong
# Version   2 (25.11)

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
# Moreover I can justify the computation of all values by saying it can be interesting later with the model 

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
max_size = 100000 #max size of file allowed
w_time = 5
COUNT_MAX = 5           # COUNT_MAX entries are processed before updtating the content of travels.txt.
s = '45.1524,5.74812' #Eybens
d = '45.273157,5.9244034' #froges
msg = 'Note the execution must be done from ORCO21 folder.\nIf any problem to access file verify the cmd is open at the right location.\n'
#modes:
#   generation: uses the locations.txt to generate travels.txt (1: erase all content from travels; 2: add all combination from the content of )
#   computation: uses travels.txt to compute
mode = 'computation' # 'generation2' ; 'computation'
# files adresses
locations = 'LT/project/txt_files/locations.txt'
travels = 'LT/project/txt_files/travels.txt'
distances = 'LT/project/txt_files/distances.txt'


def main():
    print(msg)
    if mode == 'generation1' or mode == 'generation2':
        generation(locations, travels, mode)
        print("Travels file has been filled without mistake\n" + "*"*80)
        
    if mode == 'generation1':
        f = open(distances, 'w')
        f.close()

    active_line=-1
    done = False
    f= open(travels, 'r')
    
    print("Process Start: find an active line.")

    content = f.readlines()
    content = content[1: len(content)]
    for line_number in range(len(content)):
        line = content[line_number]
        if  line[-2]== '0':
            active_line = line_number
            break

    if active_line == -1:
        print("No line to process. Script stopped.")
    
    print('Process continues at line ' + str(active_line) + ' of ' + str(len(content)) )
            
    f.close()

    print("active linve found.\nFound "+str(len(content) - active_line) +" instances to compute.\nFilling the distance file... ")

    f =open(distances,'a')

    while active_line != len(content):
        count = 0
        while count < COUNT_MAX:
            count +=1
            line = content[active_line]
            sd = pick(line)

            distance, duration = call(sd)
            to_append =sd + ';' + str(distance)+';'+str(duration)

            print("Entry: " + to_append)
            print(str(active_line) + '/' + str(len(content)))

            time.sleep(w_time)

            f.write(to_append+'\n')
            content[active_line] = update_line(content[active_line])
            active_line +=1

        #if we reach COUNT_MAX: close distances, open travels and update it with content. 
        print("*"*18 + "\nUpdating travels.txt\n" + "*"*18)
        f.close()

        f = open(travels, 'w')
        for entry in content:
            f.write(entry)
        f.close()

        f = open(distances, 'a')






    
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

def pick(line):
    '''
    extract s;d from a line
    '''
    return line[0: len(line)-3]

def update_line(line):
    '''
    replace the 0 by a 1 in a line.
    '''
    return line[0: len(line)-2] + '1\n'

main()
