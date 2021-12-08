## Date 8.12
# Author: Thomas B
# Objective:    Print an iterative solution with a gif

import igraph
from igraph import Plot
from igraph import layout
from matplotlib import use
p1 = Plot()
# Operation:    
#   1. Gather gps coordinates of useful cities.
    # 45 y variates as usual
    # 5 x variates as usual
#   2. Organize a good layout according to the GPS coordinates
#   3. Gather population values from rawdata

## Annexe
additional_entries = [['Depot', '00000', 0, 0, 0, 0, 0, 0, 5.87114, 45.2313]]

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

selected_cities = [i for i in range(len(raw_data))]
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

    #population:
    Pop = []
    for entry in useful_entries:
        pop = entry[3]
        if pop < 700:
            Pop.append(3)
        elif pop < 2000:
            Pop.append(5)
        elif pop < 4000:
            Pop.append(7)
        elif pop > 8200:
            Pop.append (15)
        else: 
            Pop.append(10)
            
    Pop[-1] = 7

    vs_dict = {'city' : city_col, 'active' : active_col, 'depot': depot_col }
    es_dict = {'inactive' : inactive_edge_col, 'active': active_edge_col}
    
    #n: plot 

    name = images_loc + 'test.png'
    igraph.plot(g, name, layout = layout1, vertex_color = [vs_dict[v_type]  for v_type in g.vs['type']], vertex_size = [1.7*pop_i for pop_i in Pop  ] )
    
###

# What does a solution looks like? 

#### MAIN

main()