import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from tkinter import filedialog as fd
import pandas as pd
import os
from fit_psyche.psychometric_curve import PsychometricCurve

def getITI(file, disp=False):

    # Calcul TMS
    # Récupère la cellule avec les timing du tms : file.iloc[0]['tms1.rt']
    # Retire le crochet de début et de fin : [1:len(file.iloc[0]['tms1.rt']) - 1]
    # Fait une liste avec les différents éléments séparé par une virgule list(... .split(',')))
    tms1Str = list(file.iloc[0]['tms1.rt'][1:len(file.iloc[0]['tms1.rt']) - 1].split(','))

    # Converti les string en float
    tms1 = [float(i) for i in tms1Str]

    # Calcul des iti
    iti1 = []
    for i in range(1, len(tms1)):
        iti1.append(tms1[i]-tms1[i-1])

    # Retrait des tap outlier +/- 3 MAD
    toRemove = []
    for i in iti1:
        if (i > np.median(iti1)+3*stats.median_abs_deviation(iti1) or
                i < np.median(iti1)-3*stats.median_abs_deviation(iti1)):
            toRemove.append(i)
    iti1Clean = [i for i in iti1 if i not in toRemove]

    # Idem pour le TMS 2
    tms2Str = list(file.iloc[142]['tms2.rt'][1:len(file.iloc[142]['tms2.rt']) - 1].split(','))
    tms2 = [float(i) for i in tms2Str]
    iti2 = []
    for i in range(1, len(tms2)):
        iti2.append(tms2[i]-tms2[i-1])
    toRemove = []
    for i in iti2:
        if (i > np.median(iti2)+3*stats.median_abs_deviation(iti2) or
                i < np.median(iti2)-3*stats.median_abs_deviation(iti2)):
            toRemove.append(i)
    iti2Clean = [i for i in iti2 if i not in toRemove]

    # Idem pour le TMS 3
    tms3Str = list(file.iloc[144]['tms3.rt'][1:len(file.iloc[144]['tms3.rt']) - 1].split(','))
    tms3 = [float(i) for i in tms3Str]
    # Calcul des iti
    iti3 = []
    for i in range(1, len(tms3)):
        iti3.append(tms3[i]-tms3[i-1])
    toRemove = []
    for i in iti3:
        if (i > np.median(iti3)+3*stats.median_abs_deviation(iti3) or
                i < np.median(iti3)-3*stats.median_abs_deviation(iti3)):
            toRemove.append(i)
    iti3Clean = [i for i in iti3 if i not in toRemove]

    # if len(iti1)<15 or len(iti2)<15 or len(iti3)<15:
    #     print('Check sujet : ', file.at[0,'Participant'])
    #     print('Nb tap = ', len(iti1), len(iti2), len(iti3))

    if disp:
        # print('Moyenne iti TMS 1 = ', str(np.mean(iti1)))
        # print('Ecart type iti TMS 1 = ', str(np.std(iti1)))
        # print('Moyenne iti TMS 2 = ', str(np.mean(iti2)))
        # print('Ecart type iti TMS 2 = ', str(np.std(iti2)))
        # print('Moyenne iti TMS 3 = ', str(np.mean(iti3)))
        # print('Ecart type iti TMS 3 = ', str(np.std(iti3)))
        fig, axs = plt.subplots(3, 2)
        axs[0, 0].plot(iti1)
        axs[1, 0].plot(iti2)
        axs[2, 0].plot(iti3)
        axs[0, 0].set_title('ITI bruts')
        axs[0, 1].set_title('ITI corrigés')
        axs[0, 0].hlines(np.mean(iti1), 0, len(iti1), linestyles='dashed', colors='red')
        axs[1, 0].hlines(np.mean(iti2), 0, len(iti2), linestyles='dashed', colors='red')
        axs[2, 0].hlines(np.mean(iti3), 0, len(iti3), linestyles='dashed', colors='red')

        axs[0, 1].plot(iti1Clean)
        axs[1, 1].plot(iti2Clean)
        axs[2, 1].plot(iti3Clean)
        axs[0, 1].hlines(np.mean(iti1Clean), 0, len(iti1Clean), linestyles='dashed', colors='red')
        axs[1, 1].hlines(np.mean(iti2Clean), 0, len(iti2Clean), linestyles='dashed', colors='red')
        axs[2, 1].hlines(np.mean(iti3Clean), 0, len(iti3Clean), linestyles='dashed', colors='red')
        plt.show()
        input('Press enter')

    return [iti1Clean, iti2Clean, iti3Clean]


# Récupère l'estimation et la retourne en nombre de secondes
def getEstim(file, disp=False):
    # Estimation
    # Récupère le texte, vire le \n à la fin, sépare avec le : et transforme en liste
    estimTxt = list(file.iloc[143]['estim.text'].replace('\n','')[0:5].split(':'))

    # Puis calcul en seconde la durée
    estimationSec = int(estimTxt[0]) * 60 + int(estimTxt[1])
    if disp:
        print('Estimation de la durée de la récupération : ', estimTxt[0], ' minutes ', estimTxt[1], ' secondes')
    return estimationSec


# Récupère l'accuracy du calcul mental et retourne le % de bonnes réponses
def getAccCalcul(file, disp=False):
    if disp:
        print('Calcul mental :', str(np.sum(file['StressAcc'])*2), '% bonnes réponses')
    return np.sum(file['StressAcc'])*2

# Calcul le nombre de réponses longues pour chaque durée
def getBiss(file, disp=False):
    countBiss1 = file["stimulusauditif1"][(file["RepBiss1Acc"] == 1)].value_counts().reindex\
        (index=['208.wav', '272.wav', '336.wav', '400.wav', '464.wav', '528.wav', '592.wav']).to_list()
    countBiss2 = file["stimulusauditif2"][(file["RepBiss2Acc"] == 1)].value_counts().reindex\
        (index=['208.wav', '272.wav', '336.wav', '400.wav', '464.wav', '528.wav', '592.wav']).to_list()

    # Remplace les Nan par des 0
    countBiss1 = [0 if x != x else x for x in countBiss1]
    countBiss2 = [0 if x != x else x for x in countBiss2]

    # Passe d'un compte (/10) à une valeur entre 0 et 1
    countBiss1 = [i/10 for i in countBiss1]
    countBiss2 = [i/10 for i in countBiss2]

    # Affichage des 2 courbes de bissections
    if disp:
        print('Bissection 1 : ', countBiss1)
        print('Bissection 2 : ', countBiss2)
        fig, ax = plt.subplots()
        ax.plot(countBiss1, color='red', label='Biss1')
        ax.plot(countBiss2, color='blue', label='Biss2')
        ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
        ax.set_xticklabels(['208', '272', '336', '400', '464', '528', '592'])
        ax.set_ylim([0, 1])
        plt.legend()
        plt.title('Sujet n°'+str(file.Participant[0]))
        plt.show()

    return countBiss1, countBiss2

def getCond(numCond):
    if numCond==1:
        return ['Rien', 'Non', 'Non']
    elif numCond==2:
        return ['Musique', 'Oui', 'Non']
    elif numCond==3:
        return ['Odeur', 'Non', 'Oui']
    elif numCond==4:
        return ['Odeur + Musique', 'Oui', 'Oui']
    else:
        return 'Mauvaise condition'


# Calcul les VD pour un participant
def getVDOneParticipant(affichage=True):
    filename = fd.askopenfilename()
    file = pd.read_csv(filename)
    if np.sum(file['RepAppBissAcc']) < 8:
        print('Nb mauvaise réponse app : ', str(np.sum(file['RepAppBissAcc'])))

    getITI(file, disp=affichage)
    getEstim(file, disp=affichage)
    getAccCalcul(file, disp=affichage)
    getBiss(file, disp=affichage)


# Calcul les VD pour tous les participants et créé un fichier de résultats à la racine
def getVDAll():

    dir_path = 'C:/Users/rmoncorge/OneDrive - Université de Bourgogne/Thèse/Chambijon/Data/'

    sites = ['Chambery/', 'Dijon/']

    results = [['Sujet', 'Age', 'Sexe', 'Condition', 'Musique', 'Odeur', 'Site', 'MoyTMS1', 'EtTMS1', 'MoyTMS2', 'EtTMS2', 'MoyTMS3', 'EtTMS3', 'TMS2-1', 'TMS3-1',
                '%BRCalcul', 'Estim']]
    resultsBiss = [['Sujet', 'Condition', 'Bissection', 'DurStim', 'RepLong', 'RepCourt']]
    durée = [208, 272, 336, 400, 464, 528, 592]
    for site in sites:
        for filename in os.listdir(dir_path+site):
            if filename[-4:] == ".csv":
                file = pd.read_csv(dir_path + site + filename)
                if np.sum(file['RepAppBissAcc']) < 8:
                    print('Sujet : ',str(file.iloc[0]['Participant']),'Nb mauvaise réponse app : ',
                          str(np.sum(file['RepAppBissAcc'])))

                allITI = getITI(file, disp=False)
                estim = getEstim(file)
                calcul = getAccCalcul(file)

                biss1, biss2 = getBiss(file, False)

                # Test en rajoutant un 1 et un 0 pour un meilleur fit de la courrbe psychométrique
                # resultsBiss.append([filename[0:7], getCond(file.at[0, 'Condition']), '1', '0', 0, 1])

                for idxBiss1 in range(0, len(biss1)):
                    resultsBiss.append([filename[0:7], getCond(file.at[0, 'Condition']), '1', str(durée[idxBiss1]),
                                        biss1[idxBiss1], 1-biss1[idxBiss1]])

                # resultsBiss.append([filename[0:7], getCond(file.at[0, 'Condition']), '1', '600', 1, 0])
                # resultsBiss.append([filename[0:7], getCond(file.at[0, 'Condition']), '2', '0', 0, 1])

                for idxBiss2 in range(0, len(biss1)):
                    resultsBiss.append([filename[0:7], getCond(file.at[0, 'Condition']), '2',
                                        str(durée[idxBiss2]), biss2[idxBiss2], 1 - biss2[idxBiss2]])

                # resultsBiss.append([filename[0:7], getCond(file.at[0, 'Condition']), '2', '600', 1, 0])


                # fitBiss1 = PsychometricCurve(model='wh').fit(durée, biss1)
                # fitBiss2 = PsychometricCurve(model='wh').fit(durée, biss2)

                results.append(
                    [filename[0:7], file.at[0, 'Âge'], file.at[0, 'Sexe (H/F)'], getCond(file.at[0, 'Condition'])[0],
                     getCond(file.at[0, 'Condition'])[1], getCond(file.at[0, 'Condition'])[2], site,
                     np.mean(allITI[0]), np.std(allITI[0]), np.mean(allITI[1]), np.std(allITI[1]), np.mean(allITI[2]),
                     np.std(allITI[2]), (np.mean(allITI[1]) - np.mean(allITI[0]))/np.mean(allITI[0]),
                     (np.mean(allITI[2]) - np.mean(allITI[0]))/np.mean(allITI[0]), calcul, estim])

    resultsToCsv = pd.DataFrame(results[1:], columns=results[0])
    resultsToCsv.to_csv(dir_path + '/Resultats sans bissection.csv', sep=';', index=False, decimal=',')
    #
    # resultsBissToCsv = pd.DataFrame(resultsBiss[1:], columns=resultsBiss[0])
    # resultsBissToCsv.to_csv(dir_path + '/Calcul bissection.csv', sep=';', index=False, decimal=',')

