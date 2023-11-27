import numpy as np
from tkinter import filedialog as fd
import pandas as pd
import functions as fnc

# -----------    Chambijon   --------------

filename = fd.askopenfilename()
file = pd.read_csv(filename)

if np.sum(file['RepAppBissAcc']) < 8:
    print('Nb mauvaise réponse app : ', str(np.sum(file['RepAppBissAcc'])), ' \nRetrait du sujet : ', str(file.iloc[0]['Participant']))
else:
    allITI = fnc.getITI(file)
    estim = fnc.getEstim(file)
    calcul = fnc.getAccCalcul(file)
    biss1, biss2 = fnc.getBiss(file, True)


