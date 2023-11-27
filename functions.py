import numpy as np
import matplotlib.pyplot as plt

def getITI(file):

    # Calcul TMS
    # Récupère la cellule avec les timing du tms, converti la chaine de caractère en liste de nombre
    tms1Str = list(file.iloc[0]['tms1.rt'][1:len(file.iloc[0]['tms1.rt']) - 1].split(','))
    tms1 = [float(i) for i in tms1Str]
    # Calcul des iti
    iti1 = []
    for i in range(1, len(tms1)):
        iti1.append(tms1[i]-tms1[i-1])
    toRemove = []
    for i in iti1:
        if i > np.mean(iti1)+3*np.std(iti1) or i < np.mean(iti1)-3*np.std(iti1):
            toRemove.append(i)

    print('Moyenne iti TMS 1 = ', str(np.mean(iti1)))
    print('Ecart type iti TMS 1 = ', str(np.std(iti1)))

    tms2Str = list(file.iloc[142]['tms2.rt'][1:len(file.iloc[142]['tms2.rt']) - 1].split(','))
    tms2 = [float(i) for i in tms2Str]
    # Calcul des iti
    iti2 = []
    for i in range(1, len(tms2)):
        iti2.append(tms2[i]-tms2[i-1])
    print('Moyenne iti TMS 2 = ', str(np.mean(iti2)))
    print('Ecart type iti TMS 2 = ', str(np.std(iti2)))

    tms3Str = list(file.iloc[144]['tms3.rt'][1:len(file.iloc[144]['tms3.rt']) - 1].split(','))
    tms3 = [float(i) for i in tms3Str]
    # Calcul des iti
    iti3 = []
    for i in range(1, len(tms3)):
        iti3.append(tms3[i]-tms3[i-1])
    print('Moyenne iti TMS 3 = ', str(np.mean(iti3)))
    print('Ecart type iti TMS 3 = ', str(np.std(iti3)))

    return [iti1,iti2,iti3]


# Récupère l'estimation et la retourne en nombre de secondes
def getEstim(file):
    # Estimation
    # Récupère le texte, vire le \n à la fin, sépare avec le : et transforme en liste
    estimTxt = list(file.iloc[143]['estim.text'][0:5].split(':'))
    # Puis calcul en seconde la durée
    estimationSec = int(estimTxt[0] * 60) + int(estimTxt[1])
    print('Estimation de la durée de la récupération : ', estimTxt[0], ' minutes ', estimTxt[1], ' secondes')
    return estimationSec


# Récupère l'accuracy du calcul mental et retourne le % de bonnes réponses
def getAccCalcul(file):
    print('Calcul mental :', str(np.sum(file['StressAcc'])*2), '% bonnes réponses')
    return np.sum(file['StressAcc'])*2

# Calcul le nombre de réponses longues pour chaque durée
def getBiss(file, affichage = False):
    countBiss1 = file["stimulusauditif1"][(file["RepBiss1Acc"] == 1)].value_counts().reindex\
        (index=['208.wav', '272.wav', '336.wav', '400.wav', '464.wav', '528.wav', '592.wav']).to_list()
    countBiss2 = file["stimulusauditif2"][(file["RepBiss2Acc"] == 1)].value_counts().reindex\
        (index=['208.wav', '272.wav', '336.wav', '400.wav', '464.wav', '528.wav', '592.wav']).to_list()

    # Remplace les Nan par des 0
    countBiss1 = [0 if x != x else x for x in countBiss1]
    countBiss2 = [0 if x != x else x for x in countBiss2]

    print('Bissection 1 : ', countBiss1)
    print('Bissection 2 : ', countBiss2)

    # Affichage des 2 courbes de bissections
    if affichage:
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

