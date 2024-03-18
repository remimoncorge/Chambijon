import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


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

    # Retrait des tap outlier
    toRemove = []
    for i in iti1:
        if (i > np.median(iti1)+3*stats.median_abs_deviation(iti1) or
                i < np.median(iti1)-3*stats.median_abs_deviation(iti1)):
            toRemove.append(i)
    iti1 = [i for i in iti1 if i not in toRemove]

    tms2Str = list(file.iloc[142]['tms2.rt'][1:len(file.iloc[142]['tms2.rt']) - 1].split(','))
    tms2 = [float(i) for i in tms2Str]
    # Calcul des iti
    iti2 = []
    for i in range(1, len(tms2)):
        iti2.append(tms2[i]-tms2[i-1])
    toRemove = []
    for i in iti2:
        if (i > np.median(iti2)+3*stats.median_abs_deviation(iti2) or
                i < np.median(iti2)-3*stats.median_abs_deviation(iti2)):
            toRemove.append(i)
    iti2 = [i for i in iti2 if i not in toRemove]

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
    iti3 = [i for i in iti3 if i not in toRemove]

    if disp:
        # print('Moyenne iti TMS 1 = ', str(np.mean(iti1)))
        # print('Ecart type iti TMS 1 = ', str(np.std(iti1)))
        # print('Moyenne iti TMS 2 = ', str(np.mean(iti2)))
        # print('Ecart type iti TMS 2 = ', str(np.std(iti2)))
        # print('Moyenne iti TMS 3 = ', str(np.mean(iti3)))
        # print('Ecart type iti TMS 3 = ', str(np.std(iti3)))
        fig, axs = plt.subplots(3)
        axs[0].plot(iti1)
        axs[1].plot(iti2)
        axs[2].plot(iti3)
        # axs[0].set_title(str(np.mean(iti1)))
        # axs[1].set_title(str(np.mean(iti2)))
        # axs[2].set_title(str(np.mean(iti3)))
        axs[0].hlines(np.mean(iti1), 0, len(iti1), linestyles='dashed', colors='red')
        axs[1].hlines(np.mean(iti2), 0, len(iti2), linestyles='dashed', colors='red')
        axs[2].hlines(np.mean(iti3), 0, len(iti3), linestyles='dashed', colors='red')
        plt.show()
        input('Press enter')

    return [iti1, iti2, iti3]


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

    # Affichage des 2 courbes de bissections
    if disp:
        print('Bissection 1 : ', countBiss1)
        print('Bissection 2 : ', countBiss2)
        fig, ax = plt.subplots()
        ax.plot(countBiss1, color='red', label='Biss1')
        ax.plot(countBiss2, color='blue', label='Biss2')
        ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
        ax.set_xticklabels(['208', '272', '336', '400', '464', '528', '592'])
        ax.set_ylim([0, 10])
        plt.legend()
        plt.title('Sujet n°'+str(file.Participant[0]))
        plt.show()

    return countBiss1, countBiss2

def getCond(numCond):
    if numCond==1:
        return 'Rien'
    elif numCond==2:
        return 'Musique'
    elif numCond==3:
        return 'Odeur'
    elif numCond==4:
        return 'Musique + Odeur'
    else:
        return 'Mauvaise condition'