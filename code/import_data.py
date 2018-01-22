#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created a long time ago in a galaxy far, far away

@author: ppx
"""
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
PURPOSE OF THE ALGORITHM :

To have a great model for my scripts
"""
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
PACKAGES IMPORTED :
"""
import os
import csv
import sys
import ast
import pymysql.cursors
import decimal
from decimal import Decimal
import pandas as pd
import numpy as np
# If a package is not working, run 'pip install name_of_the_package' in your terminal
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#|
#|
#|
#|
#|
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
VARIABLES :
"""
### IMPORT
path_import = '/Users/ppx/Desktop/M2 DS/projet_lolo_paulo/data/'
path_import = 'C:/Users/Loic/Documents/TP_AccidentsRouteLyon/data/'
data_caracteristiques_file = 'caracteristiques_2016.csv'
data_lieux_file = 'lieux_2016.csv'
data_usagers_file = 'usagers_2016.csv'
data_vehicules_file = 'vehicules_2016.csv'



### EXPORT
path_export = '/Users/ppx/Desktop/M2 DS/projet_lolo_paulo/result/'
path_export = 'C:/Users/Loic/Documents/TP_AccidentsRouteLyon/data/'
result_file = 'the_result_file.csv'

### PONCTUAL 
action_made = - 1
action_number = 2
print_progress_mode = True
column_type_caracteristiques = {'Num_Acc': np.int64}
column_type_usagers = {'Num_Acc': np.int64}
column_type_vehicules = {'Num_Acc': np.int64}
column_type_lieux = {'Num_Acc': np.int64,
                        'catr': np.int64,
                        'voie': np.string_,
                        'v1':np.float64,
                        'v2':np.string_,
                        'circ':np.float64,
                        'nbv':np.float64,
                        'pr':np.float64,
                        'pr1':np.float64,
                        'vosp':np.float64,
                        'prof':np.float64,
                        'plan':np.float64,
                        'lartpc':np.float64,
                        'larrout':np.float64,
                        'surf':np.float64,
                        'infra':np.float64,
                        'situ':np.float64,
                        'env1':np.float64}

columns_unuseful = ['trajet',
                    'an',
                    'com',
                    'adr',
                    'lat',
                    'long',
                    'dep']

vehicule_classique = [7,10]
vehicule_air_libre = [1,2,30,31,32,33,34,35,36]
vehicule_lourd = [13,14,15,16,17,37,38,39,40]








export_mode = False




### decoupe_journee aurait mérite à etre clusterisée
decoupe_journee = [[0,559],[600,1159],[1200,1359],[1400,1759],[1800,2159], [2200,2401] ]
ct_several_veh = 0

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
DEFINITION OF FUNCTIONS :
"""

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

def print_progress(mode):
	global action_made
	global action_number
	if mode == True:
		action_made += 1
		restart_line()
		printProgressBar(action_made, action_number, prefix = 'Progress:', suffix = 'Complete', length = 50)


def journee_decoupe(_integer):
    global decoupe_journee

    for moment in range(0,len(decoupe_journee)):
        if (decoupe_journee[moment][0] <= _integer) and (_integer <= decoupe_journee[moment][1]):
            result = moment
            break

    return result

def vehicule_type(_int):
    if _int in vehicule_air_libre:
        return 1
    elif _int in vehicule_classique:
        return 2
    elif _int in vehicule_lourd:
        return 3
    else:
        return 0

def vehicule_oppose(_string, _data, _catv):
    global ct_several_veh

    liste_vehicules = list(set(merged_data[merged_data.Num_Acc == _string]['catv']))
    liste_vehicules.remove(_catv)
    if len(liste_vehicules) == 1:
        return liste_vehicules[0]
    elif len(liste_vehicules) == 0:
        return _catv
    else:
        ct_several_veh += 1
        return liste_vehicules[0]

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
DATA READING 
"""

### (classik mode) :
data_vehicules = pd.read_csv(path_import + data_vehicules_file, dtype = column_type_vehicules)
data_vehicules.fillna(0, inplace = True)

data_usagers = pd.read_csv(path_import + data_usagers_file, dtype = column_type_usagers)
data_usagers.fillna(0, inplace = True)

data_lieux = pd.read_csv(path_import + data_lieux_file, dtype = column_type_lieux,error_bad_lines=False)
data_lieux.fillna(0, inplace = True)

data_caracteristiques = pd.read_csv(path_import + data_caracteristiques_file, dtype = column_type_caracteristiques, sep = ";")
data_caracteristiques.fillna(0, inplace = True)

"""
data_lieux
    à priori, v1 et v2 ne servent à rien
    env1 inutilisable







"""
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
PLAYING WITH THE DATA :
"""
data_usagers = data_usagers.sort_values('Num_Acc')

data_vehicules = data_vehicules.sort_values('Num_Acc')
merged_data = pd.merge(data_usagers ,data_vehicules, on = ['Num_Acc','num_veh'], how = 'inner')
merged_data = pd.merge(merged_data ,data_caracteristiques, on = 'Num_Acc', how = 'inner')

merged_data = merged_data.drop_duplicates()





merged_data = merged_data.drop(columns_unuseful, axis = 1)
### On va rester dans la métropole : 
merged_data = merged_data[merged_data.gps == 'M']
merged_data = merged_data.drop('gps', axis = 1)


### merged_data['num_veh_x'] = merged_data['num_veh_x'].apply(lambda x: str(x))
### petite boucle
merged_data['mom'] = merged_data.apply(lambda x: journee_decoupe(x['hrmn']), axis=1)


### merged_data.info()
isnull_essai = data_lieux.isnull()



merged_data.groupby(['Num_Acc'])

### Petite boucle pour trouver le vehicule 'adverse'

merged_data['catvopp'] = merged_data.apply(lambda x: vehicule_oppose(x['Num_Acc'],merged_data, x['catv']), axis=1)
merged_data['catv_gen'] = merged_data.apply(lambda x: vehicule_type(x['catv']), axis=1)
merged_data['catvopp_gen'] = merged_data.apply(lambda x: vehicule_type(x['catvopp']), axis=1)


### Entropie
### runfile('/Users/ppx/Desktop/modeles/python/script_download/pandas_entropy.py', wdir='/Users/ppx/Desktop/modeles/python/script_download')
### entropie = ID3_entropies(merged_data)





#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
RESULT EXPORT :
"""
if export_mode:
    merged_data.to_csv(path_export + result_file)
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
CLEANING THE MEMORY
"""


del action_made



### to run it 
### runfile('/Users/ppx/Desktop/M2 DS/projet_lolo_paulo/code/import_data.py', wdir='/Users/ppx/Desktop/M2 DS/projet_lolo_paulo/code')
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
END
"""
os.system('say "fini"')