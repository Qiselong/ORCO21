### Date: 1.12 
### Author: Thomas B.
### Objective: XD

database = 'LT/project/txt_files/database.txt'
locations = 'LT/project/txt_files/locations.txt'
msg = 'Note the execution must be done from ORCO21 folder.\nIf any problem to access file verify the cmd is open at the right location.\n'

def main():
    print(msg)
    Result = []
    f = open(locations)
    content = f.readlines()
    for line in content:

        tmp = line.split(',')
        long = tmp[0]
        lat = tmp[1]
        lat = lat[0:len(lat)-1]
        Result.append(lat + ',' + long + '\n')
    f.close()

    print(Result)

    f = open(locations, 'w')
    for entry in Result:
        f.write(entry)


main()