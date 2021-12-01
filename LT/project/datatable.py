# Date: 30.10.21 
# Last update: 1.11.21
# Auth: T. Boudier

# Objectif: créer une table de données pour les 46 villes du pays du gresivaudan et qqs. fonctions adaptées à la réflexion autour du problème (ie. )
# Avis aux lecteurs: deésolé pour les commentaires, il est tard et je suis fatigué

#imports
import igraph


#paramètres
# verbose values & thresholds
verbose = 89
RMI_VERB = 90
UPT_VERB = 95

#
read_mode = "ulig2"   # have verbose > RMI_VERB for more infomations
reread = False          # updates or not the D table
fix_shit1 = True       # intermediate fix of some mistakes

#main
def main():
    print("\n")
    if verbose > RMI_VERB:
        read_mode_information()
    if verbose > UPT_VERB :
        print('update the table: ', reread)

    if reread:
            D = data_reading(Raw_data)
    else:
        D = Data_fix_needed

    if fix_shit1:
        for entry in D:
            entry[4] = float(entry[4])  #some entries had wrong types because i trust myself enough so that future-me can fix errors of present-me
    
            coordinates =[]     
                                    #coordinates table
        for entry in D:
            coordinates.append((entry[-2], entry[-1] ))   #y-axis mirror fix
        CD = coordinates
        print(CD)
    else:
        CD = coordinates_table

    print(CD)

    #graph generation is NOW
    g = igraph.Graph(len(CD))

    layout1 = g.layout("rt", 2)
    for i in range(len(layout1)):
        layout1[i] = CD[i]

    #assigning names to our vertices
    vnames = []
    k_tmp = 0
    if read_mode == "ulig2" or read_mode =="lig2":   #depending on read-mode. default is city-name
        k_tmp = 1
    for i in range(len(CD)):
        vnames.append(str(D[i][k_tmp]))

    g.vs["label"] = vnames
    igraph.plot(g, layout= layout1)
    

# raw data: source insee https://www.insee.fr/fr/metadonnees/cog/intercommunalite-metropole/EPCI200018166-cc-le-gresivaudan
# organisation table: Nom commune ; N°Insee ; gentilé ; superficie (km^2) ; population ; densité
# les noms de certains villages ont été modifiés (ex: La chapelle -> La-chapelle) pour des questions de simplicité de lecture.
Raw_data = "Allevard 	38006 	Allevardins 	25,63 	4 062   	158 / Barraux 	38027 	Barolins 	11,13 	1 918   	172 / Bernin 	38039 	Berninois 	7,67 	3 044   	397 / Biviers 	38045 	Bivierois 	6,17 	2 359   	382 / Chamrousse 	38567 	Chamroussiens 	13,29 	403   	30 / Chapareillan 	38075 	Chapareillanais 	30,28 	2 997   	99 / Crêts-en-Belledonne 	38439 		33,8 	3 299   	98 / Crolles 	38140 	Crollois 	14,21 	8 260   	581 / Froges 	38175 	Frogiens 	6,43 	3 361   	523 / Goncelin 	38181 	Goncelinois 	14,36 	2 470   	172 / Hurtières 	38192 	Hurtièrois 	3,35 	181   	54 / La-Buissière 	38062 	Buisserans 	7,71 	700   	91 / La-Chapelle-du-Bard 	38078 	Chapelains 	27,71 	577   	21 / La-Combe-de-Lancey 	38120 	Combinois 	18,55 	705   	38 / La-Flachère 	38166 	Flachèrois 	2,85 	478   	168 / La-Pierre 	38303 	Pierrois 	3,31 	570   	172 / La-Terrasse 	38503 	Terrassons 	9,47 	2 524   	267 / Laval-en-Belledonne 	38206 	Lavallois 	25,33 	982   	39 / Le-Champ-près-Froges 	38070 	Champiots 	4,83 	1 186   	246 / Le-Cheylas 	38100 	Cheylasiens 	8,44 	2 555   	303 / Le-Haut-Bréda 	38163 		78,6 	393   	5 / Le-Moutaret 	38268 	Moutarins 	5,29 	261   	49 / Le-Touvet 	38511 	Touvétains 	11,56 	3 203   	277 / Le-Versoud 	38538 	Bédouins 	6,35 	4 876   	768 / Les-Adrets 	38002 	Campanais 	16,15 	1 025   	63 /Lumbin 	38214 	Lumbinois 	6,77 	2 151   	318 / Montbonnot-Saint-Martin 	38249 	Bonimontains 	6,38 	5 306   	832 / Plateau-des-Petites-Roches 	38395 		36,91 	2 408   	65 / Pontcharra 	38314 	Charrapontains 	15,58 	7 376   	473 / Revel 	38334 	Revélois 	29,55 	1 313   	44 / Saint-Ismier 	38397 	Saint-Ismerusiens 	14,9 	7 026   	472 / Saint-Jean-le-Vieux 	38404 	Saint-Jantets 	4,59 	295   	64 / Saint-Martin-d'Uriage 	38422 	Saint-Martinois 	29,69 	5 482   	185 / Saint-Maximin 	38426 	Saint-Maximinois 	10,35 	659   	64 / Saint-Mury-Monteymond 	38430 	Murimondois 	11,09 	319   	29 / Saint-Nazaire-les-Eymes 	38431 	Saint-Nazairois 	8,49 	2 949   	347 / Saint-Vincent-de-Mercuze 	38466 	Rutissons 	7,85 	1 512   	193 / Sainte-Agnès 	38350 	Gareux 	26,85 	558   	21 / Sainte-Marie-d'Alloix 	38417 	Maloux 	3,04 	483   	159 / Sainte-Marie-du-Mont 	38418 	Montois 	23,87 	236   	9,9 / Tencin 	38501 	Tencinois 	6,75 	2 112   	313 / Theys 	38504 	Tarins 	35,77 	1 980   	55 / Villard-Bonnot 	38547 	Villardiens 	5,84 	7 175   	1 229"


# Following table is intermediate data, used in the creation process to do some plots.
# More specifically, the last two numbers of each entries correspond to some coordinates on a map (have to revert the y-one later.)
# Also for a reason i choosed to ignore before some densities are float and some are strings. This need a fix too. 
Data_fix_needed = [['Allevard', 38006, 25.63, 4062.0, '158', 326, 356],    #
['Barraux', 38027, 11.13, 1918.0, '172', 223, 80],              #
['Bernin', 38039, 7.67, 3044.0, '397', 84, 343],                #
['Biviers', 38045, 6.17, 2359.0, '382', 16, 392],               #
['Chamrousse', 38567, 13.29, 403, 30.0, 124, 506],              #
['Chapareillan', 38075, 30.28, 2997.0, '99',185, 33],          #
['Crêts-en-Belledonne', 38439, 3.0, 299, 98.0, 272, 199],       #
['Crolles', 38140, 14.21, 8260.0, '581', 115, 321],             #
['Froges', 38175, 6.43, 3361.0, '523', 156, 347],               #
['Goncelin', 38181, 14.36, 2470.0, '172', 225, 237],            #
['Hurtières', 38192, 3.35, 181, 54.0, 208, 313],                #
['La-Buissière', 38062, 7.71, 700, 91.0, 223, 126],             #
['La-Chapelle-du-Bard', 38078, 27.71, 577, 21.0, 390, 127],     #
['La-Combe-de-Lancey', 38120, 18.55, 705, 38.0, 164, 480],      #
['La-Flachère', 38166, 2.85, 478, 168.0, 193, 142],             #
['La-Pierre', 38303, 3.31, 570, 172.0, 180, 305],               #
['La-Terrasse', 38503, 9.47, 2524.0, '267', 166, 255],          #
['Laval-en-Belledonne', 38206, 25.33, 982, 39.0, 225, 400],     #
['Le-Champ-près-Froges', 38070, 4.83, 1186.0, '246', 162, 323], #
['Le-Cheylas', 38100, 8.44, 2555.0, '303', 245, 152],           #
['Le-Haut-Bréda', 38163, 393.0, 5, 337, 288],                   #
['Le-Moutaret', 38268, 5.29, 261, 49.0, 327, 85],               #
['Le-Touvet', 38511, 11.56, 3203.0, '277', 177, 222],           #
['Le-Versoud', 38538, 6.35, 4876.0, '768', 83, 412],            #
['Les-Adrets', 38002, 16.15, 1025.0, '63', 239, 347],           #
['Lumbin', 38214, 6.77, 2151.0, '318', 148, 286],               #
['Montbonnot-Saint-Martin', 38249, 6.38, 5306.0, '832', 39, 413],   #
['Plateau-des-Petites-Roches', 38395, 2.0, 408, 65.0, 115, 223],#
['Pontcharra', 38314, 15.58, 7376.0, '473', 249, 113],          #
['Revel', 38334, 29.55, 1313.0, '44', 139, 502],                #
['Saint-Ismier', 38397, 14.9, 7026.0, '472', 45, 355],          #   
['Saint-Jean-le-Vieux', 38404, 4.59, 295, 64.0, 108, 438],      #
["Saint-Martin-d'Uriage", 38422, 29.69, 5482.0, '185', 77, 520],    #
['Saint-Maximin', 38426, 10.35, 659, 64.0, 296, 298],           #
['Saint-Mury-Monteymond', 38430, 11.09, 319, 29.0, 167, 438],   #
['Saint-Nazaire-les-Eymes', 38431, 8.49, 2949.0, '347', 85, 374], #
['Saint-Vincent-de-Mercuze', 38466, 7.85, 1512.0, '193', 200, 189], #
['Sainte-Agnès', 38350, 26.85, 558, 21.0, 191, 422],            #
["Sainte-Marie-d'Alloix", 38417, 3.04, 483, 159.0, 213, 170],   #
['Sainte-Marie-du-Mont', 38418, 23.87, 236, 9.9, 158, 122],     #
['Tencin', 38501, 6.75, 2112.0, '313', 188, 279],               #
['Theys', 38504, 35.77, 1980.0, '55', 254, 299]]                #

#coordinates
coordinates_table = [(326, 356), (223, 80), (84, 343), (16, 392), (124, 506), (185, 33), (272, 199), (115, 321), (156, 347), (225, 237), (208, 313), (223, 126), (390, 127), (164, 480), (193, 142), (180, 305), (166, 255), (225, 400), (162, 323), (245, 152), (337.0, 288), (327, 85), (177, 222), (83, 412), (239, 347), (148, 286), (39, 413), (115, 223), (249, 113), (139, 502), (45, 355), (108, 438), (77, 520), (296, 298), (167, 438), (85, 374), (200, 189), (191, 422), (213, 170), (158, 122), (188, 279), (254, 299)]

def entry_reading(entry):
    '''
    treats an entry. Example of entry: 
    Allevard 	38006 	Allevardins 	25,63 	4 062   	158 
    '''
    L = []
    str = ''
    for i in entry:
        if i != "\t" and i != " " and i == ',':     #pas de conversion en float sur '25,63'
            str += "."
        elif i != "\t" and i != " ":
            str += i
        else:
            if str != "":
                L.append(str)  
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
                str = "" 

    if len(L) == 7 :                     # pas le temps d'expliquer monte dans la couscousmobile 
        L[-2] = L[-3]+L[-2]        

    # post-treatment: turn into integer / floats numbers
    L[1] = int(L[1])
    L[3] = float(L[3])
    L[4] = int(L[4])
    if len(L) >= 6:
        L[5] = float(L[5])

    # output (depend on read-mode)

                        # "all": all information
                    # "default": all but gentillé
                    # "lig1" : name, superficy, pop, density
                    # "lig2" : insee, superficy, pop, density
                    # "ulig1" : name, pop
                    # "ulig2" : insee, pop

    if len(L) == 7:
        del L[4]
    if read_mode == "all":
        return L
    elif read_mode == "default":
        del L[2]
        return L
    elif read_mode == "lig1":
        del L[2]
        del L[1]
        return L
    elif read_mode == "lig2":
        del L[0]
        del L[1]
        return L
    elif read_mode == "ulig1":
        del L[1]
        del L[1]
        del L[1]
        del L[-1]
        return L
    else: 
        del L[0]
        del L[1]
        del L[1]
        del L[-1]
        return L 

def data_reading(R):
    cities_data = []
    entry = ""
    for i in R: 
        if i != "/":
            entry += i
        else: 
            cities_data.append(entry_reading(entry))
            entry = ""
    return cities_data

def read_mode_information():
    '''
    Active iff verbose > RMI_VERB.
    '''
    if read_mode == "all":
        print('read mode: all. Displays all informations.\nCity name ; insee n°; gentillé; surface; population; density.')
    if read_mode == "default":
        print('read mode: default. Displays all but gentillé.\nCity name ; insee n°; surface; population; density. ') 
    if read_mode == "lig1":
        print('read mode: light1 (lig1). Discards gentillé and insee n°.\nCity name; surface; population; density.')
    if read_mode == "lig2":
        print('read mode: light2 (lig2). ulig1 alternative where insee n° replaces city name.\nInsee n° surface; population; density.')
    if read_mode == "ulig1":
        print('read mode: ultralight1 (ulig1). Selects only population data.. Entries are indexed by city name. \nCity name ; population.')
    if read_mode == "ulig2":
        print('read mode: ultralight2. ulig1 alternative where insee n° replaces city name.\nInsee n°; population.')       
    print("\n")

main()