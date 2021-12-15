## Date 8.12
# Author: Thomas B
# Objective:    Print an iterative solution with a gif

import igraph
from igraph import Plot
from igraph import layout
from matplotlib import use
import time
import requests
import math
import imageio

p1 = Plot()
# Operation:    
#   1. Gather gps coordinates of useful cities.
    # 45 y variates as usual
    # 5 x variates as usual
#   2. Organize a good layout according to the GPS coordinates
#   3. Gather population values from rawdata

## Annexe
additional_entries = [['Depot', '00000', 0, 0, 0, 0, 0, 0, 5.87114, 45.2313]]
distances = 'LT/project/txt_files/distances.txt'
w_time = 5.1
duration = 1

# Solution found for MILP. Each y_i correspond to a tour; ordered. each x_i correspond to a fraction of the tour realized. 
y_1 = [9, 11, 1, 5]
y_2 = [4]
y_3 = [7]
y_4 = [2, 7]
y_5 = [8, 10, 6]
y_6 = [3]
y_7 = [0, 9]
Y = [y_1, y_2, y_3, y_4, y_5, y_6, y_7]

x_1 = [0.23, 1, 1, 1]
x_2 = [1]
x_3 = [0.5]
x_4 = [1, 0.5]
x_5 = [1, 1, 1]
x_6 = [1]
x_7 = [1, 0.77]
X = [x_1, x_2, x_3, x_4, x_5, x_6, x_7]

 
raw_data = [['Allevard', 38006, 25.63, 4062.0, '158', 326, 356,6.0744406,45.3934726],
['Barraux', 38027, 11.13, 1918.0, '172', 223, 80,5.9773523,45.4337691],
['Bernin', 38039, 7.67, 3044.0, '397', 84, 343,5.8664744,45.2693836],
['Biviers', 38045, 6.17, 2359.0, '382', 16, 392,5.7965125,45.2375922],
['Chamrousse', 38567, 13.29, 403, 30.0, 124, 506,5.8931619,45.1171487],
['Chapareillan', 38075, 30.28, 2997.0, '99',185, 33,5.9907289,45.4628848],
['Crêts-en-Belledonne', 38439, 3.0, 299, 98.0, 272, 199,6.0255,45.2232],
['Crolles', 38140, 14.21, 8260.0, '581', 115, 321 ,5.8839432,45.2845907],
['Froges', 38175, 6.43, 3361.0, '523', 156, 347,5.9244034,45.273157],
['Goncelin', 38181, 14.36, 2470.0, '172', 225, 237,5.9780213,45.3426289],
['Hurtières', 38192, 3.35, 181, 54.0, 208, 313,5.9689556,45.2881528],
['La-Buissière', 38062, 7.71, 700, 91.0, 223, 126,5.9778214,45.4026017],
['La-Chapelle-du-Bard', 38078, 27.71, 577, 21.0, 390, 127,6.09529,45.4228],
['La-Combe-de-Lancey', 38120, 18.55, 705, 38.0, 164, 480,5.8995138,45.2256285],
['La-Flachère', 38166, 2.85, 478, 168.0, 193, 142,5.96212,45.3966],
['La-Pierre', 38303, 3.31, 570, 172.0, 180, 305,5.94734,45.2942],
['La-Terrasse', 38503, 9.47, 2524.0, '267', 166, 255,5.9309164,45.3240258],
['Laval-en-Belledonne', 38206, 25.33, 982, 39.0, 225, 400,5.93266,45.2526],
['Le-Champ-près-Froges', 38070, 4.83, 1186.0, '246', 162, 323,5.9308898,45.2789481],
['Le-Cheylas', 38100, 8.44, 2555.0, '303', 245, 152,5.9920438,45.3698678],
['Le-Haut-Bréda', 38163, 393.0, 5, 337, 288,6.0866978,45.3232851],
['Le-Moutaret', 38268, 5.29, 261, 49.0, 327, 85,6.08859,45.4318],
['Le-Touvet', 38511, 11.56, 3203.0, '277', 177, 222,5.9515976,45.3592324],
['Le-Versoud', 38538, 6.35, 4876.0, '768', 83, 412,5.8603962,45.2151366],
['Les-Adrets', 38002, 16.15, 1025.0, '63', 239, 347,5.96427,45.2711],
['Lumbin', 38214, 6.77, 2151.0, '318', 148, 286,5.9107644,45.3060201],
['Montbonnot-Saint-Martin', 38249, 6.38, 5306.0, '832', 39, 413,5.8,45.2333],
['Plateau-des-Petites-Roches', 38395, 2.0, 408, 65.0, 115, 223,5.8811206,45.3109829],
['Pontcharra', 38314, 15.58, 7376.0, '473', 249, 113,6.0204233,45.4327537],
['Revel', 38334, 29.55, 1313.0, '44', 139, 502,5.8667,45.1833],
['Saint-Ismier', 38397, 14.9, 7026.0, '472', 45, 355,5.8281,45.2485],
['Saint-Jean-le-Vieux', 38404, 4.59, 295, 64.0, 108, 438,5.8833,45.2083],
["Saint-Martin-d'Uriage", 38422, 29.69, 5482.0, '185', 77, 520,5.8383,45.1522],
['Saint-Maximin', 38426, 10.35, 659, 64.0, 296, 298,6.0158,45.2512],
['Saint-Mury-Monteymond', 38430, 11.09, 319, 29.0, 167, 438,5.92682,45.2262],
['Saint-Nazaire-les-Eymes', 38431, 8.49, 2949.0, '347', 85, 374,5.8490243,45.2566002],
['Saint-Vincent-de-Mercuze', 38466, 7.85, 1512.0, '193', 200, 189,5.95104,45.373],
['Sainte-Agnès', 38350, 26.85, 558, 21.0, 191, 422,5.9246904,45.2364294],
["Sainte-Marie-d'Alloix", 38417, 3.04, 483, 159.0, 213, 170,5.9668316,45.3796447],
['Sainte-Marie-du-Mont', 38418, 23.87, 236, 9.9, 158, 122,5.9416,45.4180],
['Tencin', 38501, 6.75, 2112.0, '313', 188, 279,5.9577176,45.3082543],
['Theys', 38504, 35.77, 1980.0, '55', 254, 299,5.9957494,45.3015475] ]

#

selected_cities = [i for i in range(12)]
city_col = 'black'
active_col = 'red'
depot_col = 'blue'

active_edge_col = 'red'
inactive_edge_col = 'black'

images_loc = 'LT/project/images/'
gif_loc = 'LT/project/gif/'

def main():
    # 1
    useful_entries =[]
    for i in selected_cities:
        useful_entries.append(raw_data[i])

    for entry  in additional_entries:
        useful_entries.append(entry)


    #2
    GPSX, GPSY = [], []
    for entry in useful_entries:
        GPSX.append(entry[-2])
        GPSY.append(entry[-1])

    xmax, xmin, ymin, ymax = min(GPSX), max(GPSX), min(GPSY), max(GPSY)

    COOX, COOY = [], []

    for i in range(len(GPSX)):
        COOX.append(100*(GPSX[i]-xmin)/(xmax-xmin))
        COOY.append(100*(GPSY[i]-ymin)/(ymax-ymin))

    g = igraph.Graph(len(selected_cities)+1)
    layout1 = g.layout('rt', 2)

    for i in range(len(layout1)):
        layout1[i] = (-COOX[i], -COOY[i])

    #3 
    for v in g.vs:
        v['type'] = 'city'
    g.vs[-1]['type'] = 'depot'
    for vi in range(len(g.vs)):
        
        g.vs[vi]['label'] = useful_entries[vi][0]

    

    vs_dict = {'city' : city_col, 'active' : active_col, 'depot': depot_col }
    es_dict = {'inactive' : inactive_edge_col, 'active': active_edge_col}
    
    #n: plot 

    #name = images_loc + 'test.png'
    #igraph.plot(g, name, layout = layout1, vertex_color = [vs_dict[v_type]  for v_type in g.vs['type']], vertex_size = [1.7*pop_i for pop_i in Pop  ] )
    partial_solution(X, Y, useful_entries, g,layout1)


def get_matrix(dim, verb = True, data = raw_data):
    k = 0
    if dim == 'distance':
        k=1
    elif dim == 'duration':
        k=2
    else:
        print('dim parameter invalid. duration or distance are the only possibilities.')
        return None
    #f = open(database)
    #content_database = f.readlines()
    
    #S = len(content_database)
    S = len(data)
    M = []
    for i in range(S):
        M_i = []
        for j in range(S):
            if verb:
                print('seek ' + str(i) + ',' +str(j), end = ' / ')
            gps1, gps2 = get_gps(i, data), get_gps(j, data)
            dist, dura = seek(gps1, gps2)
            if k ==1:
                M_i.append(dist)
            else: 
                M_i.append(dura)
        M.append(M_i)
        if verb:
            print("line " + str(i) + "out of " + str(S) + "computed.")

    return M

def seek(gps1, gps2):
    """
    look in the distance file for a line corresponding to a travel from gps1 to gps2. If we can't find one, add it and wait for 5 seconds. 
    """
    f = open(distances, 'r')
    line = f.readline()
    split = line.split(";")

    while len(split) >= 4 :
        if split[0] == str(gps1) and split[1] == str(gps2) or split[1] == str(gps1) and split[0] == str(gps2):
            resa, resb = split[2], split[3]
            resb = resb[0: len(resb)-1]

            return resa, resb
        line = f.readline()
        split = line.split(";")

    f.close()
    
    # if we arrive here it means the travel from gps1 to gps2 has not been computed for some reason.
    print("\nTravel from " + gps1 + ' to '+ gps2 + 'has not been ever computed. We compute it now.')
    sd = gps1 + ';' + gps2
    dist, dura = call(sd)

    f = open(distances, 'a')
    f.write(gps1 + ";" + gps2 + ';'+dist+';'+dura+'\n' )
    f.close()

    print("distance.txt file succesfully appened. The script goes to sleep for " + str(w_time)+ 'secs.')
    time.sleep(w_time)
    return dist, dura



def call(sd):   #infamously copy pasted from fuck_me.py.
    """
    use osrm to get the distance between s and d. Note sd must be a string obtained by doing: s+';'+d
    """
    url = "http://router.project-osrm.org/route/v1/driving/"+ sd + "?alternatives=true"
    r = requests.get(url)
    res = r.json()
    return str(res["routes"][0]["distance"]), str(res["routes"][0]["duration"])


def get_gps(i, data=raw_data):
    """ 
    uses the raw_data table to get the gps values of the city i as a string.
    """
    return str(data[i][-2]) + ',' + str(data[i][-1])

## Partial sol

def partial_solution(X, Y, useful_entries,g, layout):
    """
    returns the value of the solution (time) and plots it as a gif.
    """
    optimal_value(X, Y, useful_entries)
    solution_animation(X, Y, useful_entries,g, layout)

def solution_animation(X, Y, useful_entries,g, layout1):
    """
    animates as a gif the solution given.
    g is a igraph.Graph, layout is the associated layout.
    """

    #for each tour, print two images: before and after the tour.
    # each city start with a size of 20 and get gradually reduced as the tour goes up.
    for v in g.vs:
        v["size"] = 30


    for i in range(len(Y)):
        name = images_loc +'tour_'+str(i+1)
        tour = [12] + Y[i] + [12]
        gp = g
        

        igraph.plot(gp, name +'_1.png', layout = layout1, vertex_size = [ v["size"] for v in gp.vs  ] )

        for j in range(len(tour)-1):
            gp.add_edge(tour[j], tour[j+1])

        
        igraph.plot(gp, name+'_2.png', layout=layout1, vertex_size = [ v["size"] for v in gp.vs  ])

        for j in range(len(Y[i])):
            v_j = Y[i][j]
            f_j = X[i][j]
            g.vs[v_j]["size"] = gp.vs[v_j]["size"] - 30* (f_j)

        nE = len(g.es)

        for e_i in range(nE):
            g.delete_edges(0)

        ## Gif ploting

    filename_list = []
    for i in range(1, 8):
        name = images_loc + 'tour_' + str(i) 
        filename_list.append(name+ '_1.png')
        filename_list.append(name+ '_2.png')

    images = []
    for fname in filename_list:
        images.append(imageio.imread(fname))
    imageio.mimsave(gif_loc + 'gif_sol_12.gif', images, duration=duration)
    




def optimal_value(X, Y, useful_entries):
    """
    computes the optimal (time) value of the solution obtained.
    """
    Mt = get_matrix('duration',verb = False, data = useful_entries)

    total_time = 0 

    for k in range(len(Y)):
        tour_time = 0
        tour = [12] + Y[k] + [12]
        for i in range(len(tour)-1):
            tour_time += float(Mt[tour[i]][tour[i+1]])
        total_time += tour_time
    print("total traveling time is " + str(total_time))


    total_pop = 0
    for entry in useful_entries:
        total_pop += entry[3]

    gather_time = 3600*7*total_pop/2000 
    print("total population of the sector is " + str(total_pop) +'\nleading to a total gathering time of ' + str(gather_time) )
    

    return total_time + gather_time
        




###

# What does a solution looks like? 

#### MAIN

main()