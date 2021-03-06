# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 15:28:55 2021

@author: Zakaria
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap



data = pd.read_csv('cancer_du_sein-wisconsin.csv')

data.columns

X = data[['Épaisseur', 'Taille_cellules_épithéliale']].values
target = data['Classe'].values

x_train, x_test, y_train, y_test = train_test_split(X, target, test_size=0.3, random_state=42, stratify=target)

# Initialisation du Classifieur avec trois voisins
model_knn_classifier = KNeighborsClassifier(n_neighbors=3)

# Adapter le classifieur aux données d'entrainement
model_knn_classifier.fit(x_train, y_train)

# Faire une prédiction
y_pred = model_knn_classifier.predict(x_test)


#====================EVALUATION DU MODELE=======================

# le score de prédiction du modele
scor = model_knn_classifier.score(x_test, y_test)
print('le score de prediction du modèle est : ',scor, '\nDonc notre permet de détecter à ',scor*100,'% une classe de cancer')

# la matrice de confusion nous permet de voir sur combien de lignes le modèle a eu raison, et sur combien de ligne il s'est trompé
cm = confusion_matrix(y_test, y_pred)

# FONCTION AFFIACHAGE REGION
def affichage_region_dec(X, y, classifier, test_idx=None, resolution=0.02):
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'green', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])
    
    # trace la surface de décision
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())
    
    X_test, y_test = X[test_idx, :], y[test_idx]
    
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1],
                    alpha=0.8, c=cmap(idx),
                    marker=markers[idx], label=cl)
        if test_idx:
            X_test, y_test = X[test_idx, :], y[test_idx]
            plt.scatter(X_test[:, 0], X_test[:, 1], c='',
                        alpha=1.0, linewidth=1, marker='o',
                        s=55, label='legend')

X_combine = np.vstack((x_train, x_test))
#Empilez les tableaux en séquence verticalement 
y_combine = np.hstack((y_train, y_test))
#Empilez les tableaux en séquence horizontalement

affichage_region_dec(X_combine,
                      y_combine, classifier=model_knn_classifier,
                      test_idx=range(105,150))
   
plt.xlabel('Épaisseur')
plt.ylabel('Taille_cellules_épithéliale')
plt.legend(loc='upper left')
plt.show()  