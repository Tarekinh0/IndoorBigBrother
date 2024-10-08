import pandas as pd
import numpy as np

df = pd.read_csv('trier.csv')
print(df.shape[1])
df = df.dropna(axis=1, thresh=25) #axe des colonnes, efface la si contient moins de 15 entrees
print(df.shape[1])
df = df.replace(np.nan, -95.0)

df.to_csv('corrected.csv', index=False)  

Y = df.iloc[:, :1] # removes the other rows, keeps only the zone
Y.to_csv('Y.csv', index=False, header=True) # saves in csv, header false removes the column name
# X=df.iloc[:, 2:].tail(-1) # keeps only the measurements without the zone
X=df.iloc[:, 2:]# keeps only the measurements without the zone
X.to_csv('X.csv', index=False, header=True) # saves in csv, header false removes the column name


# MLP 
# une seule couche cachee => nb neurones cachee = [nb neurones couche d'entree + couche sortie ]/2 = (df.shape[1]+nb(zone))/2
# le nb de neurones = [nb(neurones ) + nb_neurones(couche cachee)]/2


# SVM

# KNN 

# tester tout ca d'ici la semaine prochaine

# call lib numpy ou tensorflow (plus complexe)