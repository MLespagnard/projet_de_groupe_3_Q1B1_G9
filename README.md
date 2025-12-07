# projet_de_groupe_3_Q1B1_G9
# 📌 Mini-Projet – Classifieur Naïf Bayésien (UNamur)

Ce dépôt contient le code du mini-projet d’informatique visant à développer un **classifieur automatique de documents texte** utilisant une méthode inspirée du **Naive Bayes**.
Le but est de déterminer le **thème le plus probable** d’un fichier en se basant sur les fichiers déjà classés.

---

## 📁 Structure du projet

```
.
├── main.py
├── README.md
├── labels.txt
├── sorted/
│   ├── comp.graphics/
│   ├── sci.space/
│   ├── talk.politics.guns/
│   └── ... (1 dossier par thème contenant des fichiers déjà classés)
├── unsorted/
│   └── fichiers à prédire
└── result/
    └── dossiers où seront placés les fichiers classés automatiquement
```

* **sorted/** : données d’apprentissage, déjà triées par thème
* **unsorted/** : fichiers dont le thème doit être prédit
* **result/** : dossiers où le programme placera les fichiers selon leurs thèmes prédits
* **labels.txt** : journal listant pour chaque fichier :

  ```
  <nom> <thème-prédit>
  ```

---

## 🎯 Objectif du projet

L’objectif est de :

1. **Analyser les fichiers existants** dans `sorted/`
2. **Apprendre des probabilités de mots par thème**
3. **Classer automatiquement** les fichiers du dossier `unsorted/`
4. **Enregistrer le résultat** dans `result/` et dans `labels.txt`

Aucune bibliothèque externe n’est autorisée :
➡️ tout doit se faire uniquement avec le Python standard.

---

## 🧠 Principe du classifieur

### 1. Prétraitement des textes

Pour chaque fichier :

* conversion en minuscules
* suppression de la ponctuation
* suppression des mots inutiles (stop words)
* séparation en mots

---

### 2. Apprentissage des probabilités

Pour chaque thème `T` :

* compter **le nombre total de fichiers** du thème
* pour chaque mot `w`, compter **le nombre de fichiers du thème contenant ce mot au moins une fois**

On calcule ensuite :

[
P(w \mid T) =
\frac{\text{nb de fichiers de T contenant w (ou 1 si jamais vu)}}{\text{nb total de fichiers de T}}
]

➡️ **Règle technique du projet** :
Si un mot n’apparaît jamais dans un thème mais existe dans d’autres, il compte comme ayant une occurrence fictive de 1.

Cela évite les probabilités nulles.

---

### 3. Classification d’un fichier

Pour chaque fichier de `unsorted/`, le programme :

1. lit et nettoie les mots
2. calcule un score pour chaque thème basé sur :

   * la probabilité que le mot apparaisse dans le thème
   * la probabilité qu’il n’apparaisse pas
3. sélectionne le thème avec le score le plus élevé
4. déplace le fichier dans `result/<theme>/`
5. enregistre la prédiction dans `labels.txt`

---

## 🚀 Exécution

À la racine du projet :

```
python3 main.py
```

Le programme :

* apprend les probabilités depuis `sorted/`
* classe les fichiers de `unsorted/`
* met à jour `labels.txt`
* crée automatiquement la structure dans `result/`

---

## 📄 Exemple d’entrée dans labels.txt

```
12345 sci.space
98765 comp.graphics
37261 talk.politics.guns
```

---

## 🧪 Tests et validation

* Tester avec un fichier simple contenant un mot très fréquent dans un thème
* Vérifier que les probabilités sont bien calculées
* Vérifier que les fichiers déplacés correspondent aux thèmes annoncés
* Contrôler `labels.txt`

---

## 👥 Membres du groupe

*(Ajoute ici votre liste si besoin)*

---

## 📌 Licence

Projet académique – Université de Namur.
Usage strictement pédagogique.
