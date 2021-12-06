## Date 1.12
## Author: Thomas B

## Objective: do a quick interface to fill the gps coordinates of the datas. 
## NEW: Add to the database the GPS values

database = 'LT/project/txt_files/database.txt'
locations = 'LT/project/txt_files/locations.txt'
msg = 'Note the execution must be done from ORCO21 folder.\nIf any problem to access file verify the cmd is open at the right location.\n'


GPS_LOCS = []

def main():
    print(msg)

    print("Objective: add to the database file the GPS Values")

    f = open(locations, 'r')
    content_locs = f.readlines()
    f.close()

    f = open(database, 'r')
    content_database = f.readlines()
    f.close()

    f = open(database, 'w')
    for i in range(len(content_database)):
        entry_0 = content_database[i]
        gps_val = content_locs[i]

        entry_0 = entry_0.split(']')
        f.write(entry_0[0] +',' + gps_val[0: len(gps_val)-1] + ']\n')
        

    
    




main()
