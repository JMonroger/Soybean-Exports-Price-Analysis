
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import seaborn as sns

chemin = "C:/Users/jules/OneDrive/Desktop/Projet Python/ExportSalesDataByCommodity.xls"
soybeanfutures = "C:/Users/jules/OneDrive/Desktop/Projet Python/SoybeanFutures.xls"
df = pd.read_excel(chemin)
soybeanfut = pd.read_excel(soybeanfutures)

#Evolution des Weekly Exports
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(by="Date")

#Evolution des prix futures du Soybean
soybeanfut["Date"] = pd.to_datetime(soybeanfut["Date"])
soybeanfut = soybeanfut.sort_values(by="Date")

#Affichage des Graphs
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].plot(df["Date"], df["Weekly Exports"], color='blue')
axes[0].set_title("Evolution des Weekly Exports par semaine vers la Chine")
axes[0].set_xlabel("Temps")
axes[0].set_ylabel("Exportations (T)")
axes[0].grid(True)
axes[0].tick_params(axis='x', rotation=45)

axes[1].plot(soybeanfut["Date"], soybeanfut["Close"], color='green')
axes[1].set_title("Evolution des prix futures du Soybean")
axes[1].set_xlabel("Temps")
axes[1].set_ylabel("Prix Closing(USD)")
axes[1].grid(True)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

#Construction du graph pour comparé l'évolution des weekly exports vers la Chine avec le prix du futures du soybean
fusion = pd.concat([df, soybeanfut[["Close"]]], axis=1)
selections = ["Date","Weekly Exports","Close"]
exports_prix = fusion[selections]
exports_prix = exports_prix.set_index("Date").sort_index()

plt.figure(figsize=(12, 6))
exports_norm = (exports_prix["Weekly Exports"] - exports_prix["Weekly Exports"].min()) / (exports_prix["Weekly Exports"].max() - exports_prix["Weekly Exports"].min())
close_norm = (exports_prix["Close"] - exports_prix["Close"].min()) / (exports_prix["Close"].max() - exports_prix["Close"].min())

plt.plot(exports_norm, label="Weekly Exports (normalisé)", color="blue")
plt.plot(close_norm, label="Close (normalisé)", color="red")
plt.title("Évolution comparée des Weekly Exports et du Closing price du Futures de Soybean")
plt.xlabel("Temps")
plt.ylabel("Valeurs normalisées")
plt.legend()
plt.show()

#Création de la matrice de correlation

matrice_correlation = exports_prix[["Weekly Exports", "Close"]].corr()
print(matrice_correlation)

plt.figure(figsize=(10,8))
sns.heatmap(matrice_correlation, annot=True,cmap="coolwarm",vmin=1,vmax=1)
plt.show()

#On regarde la correlation avec un décalage de temps 

lags = range(-10, 11)  
resultats_corr = []

for lag in lags:
    if lag < 0:
        corr = exports_prix["Weekly Exports"].shift(-lag).corr(exports_prix["Close"])
        resultats_corr.append(corr)
    else:
        corr = exports_prix["Weekly Exports"].corr(exports_prix["Close"].shift(lag))
        resultats_corr.append(corr)

plt.figure(figsize=(12, 6))        
plt.plot(lags, resultats_corr, 'o-')
plt.show()

   


