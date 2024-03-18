import numpy as np
from tkinter import filedialog as fd
import pandas as pd
import functions as fnc
import os

# -----------    Chambijon   --------------

dir_path = 'C:/Users/rmoncorge/OneDrive - Université de Bourgogne/Thèse/Chambijon/Data/Chambery/'

# filename = fd.askopenfilename()
# file = pd.read_csv(filename)
# if np.sum(file['RepAppBissAcc']) < 8:
#     print('Nb mauvaise réponse app : ', str(np.sum(file['RepAppBissAcc'])), ' \nRetrait du sujet : ',
#           str(file.iloc[0]['Participant']))
# else:
#     allITI = fnc.getITI(file)
# estim = fnc.getEstim(file)
# calcul = fnc.getAccCalcul(file)
# biss1, biss2 = fnc.getBiss(file, False)

results = [['Sujet', 'Condition', 'MoyTMS1', 'EtTMS1', 'MoyTMS2', 'EtTMS2', 'MoyTMS3', 'EtTMS3', 'TMS2-1', 'TMS3-2',
            '%BRCalcul', 'Estim' ]]
for filename in os.listdir(dir_path):
    if filename[-4:] == ".csv":
        file = pd.read_csv(dir_path+filename)
        if np.sum(file['RepAppBissAcc']) < 8:
            print('Nb mauvaise réponse app : ', str(np.sum(file['RepAppBissAcc'])), ' \nRetrait du sujet : ',
                  str(file.iloc[0]['Participant']))
        else:
            allITI = fnc.getITI(file, disp=False)
            estim = fnc.getEstim(file)
            calcul = fnc.getAccCalcul(file)
            biss1, biss2 = fnc.getBiss(file, False)
            results.append([filename[0:7], fnc.getCond(file.at[0,'Condition']), np.median(allITI[0]),np.std(allITI[0]),
                            np.median(allITI[1]), np.std(allITI[1]), np.median(allITI[2]), np.std(allITI[2]),
                            np.median(allITI[1]) - np.median(allITI[0]), np.median(allITI[2]) - np.median(allITI[0]),
                            calcul, estim])

resultsToCsv = pd.DataFrame(results[1:], columns=results[0])
resultsToCsv.to_csv(dir_path + '/FinalResults.csv', sep=';', index=False, decimal=',')

