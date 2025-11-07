# Application de Modélisation Mathématique

Application graphique Python pour la résolution et la modélisation mathématique avancée.

## 📋 Fonctionnalités

L'application comprend **4 modules principaux** :

### 1. 📐 Systèmes Linéaires
Résolution de systèmes d'équations linéaires (Ax = b)
- **Saisie manuelle** : Entrez directement la matrice A et le vecteur b
- **Import CSV** : Chargez les données depuis un fichier
- **Affichage** : Solutions détaillées

### 2. 📊 Programmation Linéaire
Optimisation linéaire (maximisation/minimisation)
- **Maximisation ou Minimisation**
- **Saisie manuelle** : Définissez la fonction objectif et les contraintes
- **Import CSV** : Format de données structuré
- **Visualisation** : Graphiques des résultats

### 3. 📈 Régression Linéaire
Analyse de régression et prédiction
- **Saisie manuelle** : Entrez les paires (X, Y)
- **Import CSV** : Chargez des datasets
- **Résultats** : Équation de la droite, R², coefficients
- **Graphique** : Nuage de points + droite de régression

### 4. 🎲 Processus Stochastique
Simulation de processus aléatoires
- **Chaînes de Markov** : Matrice de transition, états
- **Marches aléatoires** : Simulation de trajectoires
- **Visualisation** : Évolution des états au fil du temps

## 🏗️ Structure du Projet

```
modelisation-math/
│
├── main.py                    # Interface graphique principale
├── core/                      # Modules de calcul
│   ├── __init__.py
│   ├── linear_system.py       # Résolution systèmes linéaires
│   ├── linear_programmation.py # Programmation linéaire
│   ├── regression.py          # Régression linéaire (à créer)
│   └── stochastic.py          # Processus stochastiques (à créer)
│
├── data/csv/                  # Fichiers de données
│   ├── pastry.csv
│   └── ingredient.csv
│
├── ui/                        # Composants UI (optionnel)
│   └── __init__.py
│
├── env/                       # Environnement virtuel Python
└── requirement.txt            # Dépendances
```

## 🚀 Installation

### Prérequis
- Python 3.12+
- pip

### Étapes

1. **Cloner le repository**
```bash
git clone <votre-repo>
cd modelisation-math
```

2. **Activer l'environnement virtuel**
```bash
source env/bin/activate  # Linux/Mac
# ou
.\env\Scripts\activate   # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirement.txt
```

4. **Lancer l'application**
```bash
python main.py
```

## 📦 Dépendances

- **NumPy** : Calculs matriciels et numériques
- **Pandas** : Manipulation de données (CSV)
- **Matplotlib** : Visualisation graphique
- **PuLP** : Programmation linéaire
- **Tkinter** : Interface graphique (inclus avec Python)

## 🎯 Guide d'Utilisation

### Module 1 : Systèmes Linéaires

**Saisie manuelle :**
1. Entrez la matrice A (une ligne par équation, coefficients séparés par des espaces)
   ```
   2 1 -4
   3 3 -5
   4 5 -2
   ```
2. Entrez le vecteur b (valeurs séparées par des virgules)
   ```
   6, 12, 10
   ```
3. Cliquez sur "Résoudre"

**Import CSV :**
- Format attendu : matrice A suivi d'une colonne pour b

### Module 2 : Programmation Linéaire

**Import CSV (recommandé) :**
Format du fichier CSV :
```csv
Products,Resource1,Resource2,Objective
Product1,2,3,5
Product2,1,2,4
Available,50,60,
```

**Saisie manuelle :**
1. Choisissez Maximisation ou Minimisation
2. Entrez les coefficients de la fonction objectif
3. Entrez la matrice des contraintes
4. Entrez les limites (RHS)

### Module 3 : Régression Linéaire

**Saisie manuelle :**
1. Entrez les valeurs X : `1, 2, 3, 4, 5`
2. Entrez les valeurs Y : `2, 4, 5, 4, 5`
3. Cliquez sur "Calculer"

**Résultats affichés :**
- Équation de la droite : y = ax + b
- Coefficient de corrélation R²
- Graphique avec droite de régression

### Module 4 : Processus Stochastique

**Chaîne de Markov :**
1. Entrez la matrice de transition :
   ```
   0.7 0.3
   0.4 0.6
   ```
2. État initial : `1, 0`
3. Nombre d'étapes : `10`
4. Cliquez sur "Simuler"

## 🔧 Développement

### Tâches à implémenter

Vous devez implémenter la **logique métier** dans les fonctions suivantes :

#### Dans `main.py` :

1. **`solve_linear_system(self)`**
   - Récupérer les données depuis l'interface
   - Appeler `solve_linear_system()` depuis `core/linear_system.py`
   - Afficher les résultats

2. **`solve_lp(self)`**
   - Récupérer les données (manuel ou CSV)
   - Appeler `lp_solve()` ou `lp_maximize_from_csv()` depuis `core/linear_programmation.py`
   - Afficher les résultats + graphique

3. **`compute_regression(self)`**
   - Créer le module `core/regression.py`
   - Implémenter le calcul de régression linéaire avec NumPy
   - Afficher équation, R², et graphique avec Matplotlib

4. **`simulate_stochastic(self)`**
   - Créer le module `core/stochastic.py`
   - Implémenter chaînes de Markov et marches aléatoires
   - Afficher résultats + graphique d'évolution

### Structure de code suggérée

```python
# Exemple pour solve_linear_system
def solve_linear_system(self):
    try:
        if self.ls_input_mode.get() == "manual":
            # Récupérer depuis les widgets
            matrix_text = self.ls_matrix_a.get('1.0', tk.END)
            vector_text = self.ls_vector_b.get()
            
            # Parser les données
            a = [[float(x) for x in line.split()] for line in matrix_text.strip().split('\n')]
            b = [float(x.strip()) for x in vector_text.split(',')]
            
        else:  # CSV
            path = self.ls_csv_path.get()
            # Charger avec pandas et extraire a, b
            
        # Appeler la fonction de résolution
        from core.linear_system import solve_linear_system
        solution = solve_linear_system(a, b)
        
        # Afficher les résultats
        self.ls_results.delete('1.0', tk.END)
        self.ls_results.insert(tk.END, f"Solution :\n{solution}\n")
        
    except Exception as e:
        messagebox.showerror("Erreur", str(e))
```

## 📊 Format des Fichiers CSV

### Systèmes Linéaires
```csv
x1,x2,x3,b
2,1,-4,6
3,3,-5,12
4,5,-2,10
```

### Programmation Linéaire
```csv
Products,Farine,Eggs,Benefits
Apple pie,2,3,4
Chocolate cake,1,3,5
Available,50,60,
```

### Régression
```csv
X,Y
1,2
2,4
3,5
4,4
5,5
```

## 🎨 Personnalisation de l'Interface

L'interface utilise **Tkinter** avec le thème **clam**. Vous pouvez personnaliser :
- Les couleurs via `ttk.Style()`
- La disposition avec `pack()`, `grid()`, ou `place()`
- Les polices dans chaque widget

## 📝 Notes Importantes

1. **L'interface est déjà complète** - focalisez-vous sur la logique métier
2. **Tous les placeholders sont marqués** - cherchez "Fonction à implémenter"
3. **Les modules `core/` existants sont déjà fonctionnels** pour les 2 premiers modules
4. **Créez `core/regression.py` et `core/stochastic.py`** pour les modules 3 et 4

## 📄 Licence

Projet académique - Université/École

## 👨‍💻 Auteur

Malcovys
