# Guide d'Implémentation - Logique Métier

Ce document vous guide pour implémenter la **logique métier** des 4 modules. L'interface est déjà prête !

## 🎯 Votre Mission

Compléter les fonctions `solve_*()` dans `main.py` et créer les modules manquants dans `core/`.

---

## 📐 Module 1 : Systèmes Linéaires

### ✅ Déjà fait
- `core/linear_system.py` existe déjà
- Fonction `solve_linear_system(a, b)` fonctionnelle

### 🔨 À faire dans `main.py`

Remplacez la fonction `solve_linear_system(self)` (ligne ~334) :

```python
def solve_linear_system(self):
    try:
        if self.ls_input_mode.get() == "manual":
            # Récupérer la matrice A
            matrix_text = self.ls_matrix_a.get('1.0', tk.END).strip()
            lines = matrix_text.split('\n')
            a = [[float(x) for x in line.split()] for line in lines if line.strip()]
            
            # Récupérer le vecteur b
            vector_text = self.ls_vector_b.get().strip()
            b = [float(x.strip()) for x in vector_text.split(',')]
            
        else:  # Mode CSV
            import pandas as pd
            path = self.ls_csv_path.get()
            if not path:
                messagebox.showwarning("Attention", "Veuillez sélectionner un fichier CSV")
                return
            
            # Charger le CSV
            df = pd.read_csv(path)
            # Supposons que la dernière colonne est b, les autres sont A
            a = df.iloc[:, :-1].values.tolist()
            b = df.iloc[:, -1].values.tolist()
        
        # Appeler la fonction de résolution
        from core.linear_system import solve_linear_system
        solution = solve_linear_system(a, b)
        
        # Afficher les résultats
        self.ls_results.delete('1.0', tk.END)
        self.ls_results.insert(tk.END, "=== SOLUTION DU SYSTÈME ===\n\n")
        
        for i, val in enumerate(solution):
            self.ls_results.insert(tk.END, f"x{i+1} = {val:.4f}\n")
        
        self.ls_results.insert(tk.END, f"\nSolution complète : {solution}\n")
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la résolution :\n{str(e)}")
```

---

## 📊 Module 2 : Programmation Linéaire

### ✅ Déjà fait
- `core/linear_programmation.py` existe
- Fonctions `lp_solve()`, `lp_maximize_from_csv()`, `lp_minimize_from_csv()` fonctionnelles

### 🔨 À faire dans `main.py`

Remplacez la fonction `solve_lp(self)` (ligne ~341) :

```python
def solve_lp(self):
    try:
        problem_type = self.lp_problem_type.get()  # "maximize" ou "minimize"
        
        if self.lp_input_mode.get() == "csv":
            # Mode CSV (recommandé)
            path = self.lp_csv_path.get()
            if not path:
                messagebox.showwarning("Attention", "Veuillez sélectionner un fichier CSV")
                return
            
            # Appeler la fonction appropriée
            if problem_type == "maximize":
                from core.linear_programmation import lp_maximize_from_csv
                result = lp_maximize_from_csv(path, "Benefits", "Products")
            else:
                from core.linear_programmation import lp_minimize_from_csv
                # Adaptez selon votre CSV
                result = lp_minimize_from_csv(path, "Cost", "Products")
        
        else:  # Mode manuel
            # Récupérer les données
            obj_text = self.lp_objective.get().strip()
            obj_coef = [float(x.strip()) for x in obj_text.split(',')]
            
            constr_text = self.lp_constraints.get('1.0', tk.END).strip()
            constr_lines = constr_text.split('\n')
            constr_coef = [[float(x) for x in line.split()] for line in constr_lines if line.strip()]
            
            rhs_text = self.lp_rhs.get().strip()
            rhs = [float(x.strip()) for x in rhs_text.split(',')]
            
            # Variables de décision (générer automatiquement)
            decision_vars = [f"x{i+1}" for i in range(len(obj_coef))]
            
            # Appeler la fonction de résolution
            from core.linear_programmation import lp_solve
            result = lp_solve(
                problem_name="LP_Problem",
                decision_vars=decision_vars,
                decision_vars_coef=obj_coef,
                constraintes_coef=constr_coef,
                constraintes_inequality=rhs,
                maximize=(problem_type == "maximize")
            )
        
        # Afficher les résultats
        self.lp_results.delete('1.0', tk.END)
        self.lp_results.insert(tk.END, f"=== RÉSULTATS - {'MAXIMISATION' if problem_type == 'maximize' else 'MINIMISATION'} ===\n\n")
        
        if result:
            for var, val in result.items():
                self.lp_results.insert(tk.END, f"{var} = {val}\n")
        
        # Optionnel : Ajouter un graphique
        # self.plot_lp_results(result)
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la résolution :\n{str(e)}")
```

---

## 📈 Module 3 : Régression Linéaire

### 🆕 À créer : `core/regression.py`

```python
import numpy as np
from typing import Tuple, Dict

def linear_regression(x: list[float], y: list[float]) -> Dict[str, float]:
    """
    Calcule la régression linéaire y = ax + b
    
    Args:
        x: Liste des valeurs X
        y: Liste des valeurs Y
    
    Returns:
        Dictionnaire contenant:
        - 'a': pente
        - 'b': ordonnée à l'origine
        - 'r2': coefficient de détermination R²
    """
    x_array = np.array(x)
    y_array = np.array(y)
    
    # Nombre de points
    n = len(x_array)
    
    # Calcul de la pente (a) et de l'ordonnée (b)
    x_mean = np.mean(x_array)
    y_mean = np.mean(y_array)
    
    # a = Σ[(xi - x_mean)(yi - y_mean)] / Σ[(xi - x_mean)²]
    numerator = np.sum((x_array - x_mean) * (y_array - y_mean))
    denominator = np.sum((x_array - x_mean) ** 2)
    a = numerator / denominator
    
    # b = y_mean - a * x_mean
    b = y_mean - a * x_mean
    
    # Calcul du R² (coefficient de détermination)
    y_pred = a * x_array + b
    ss_res = np.sum((y_array - y_pred) ** 2)  # Somme des carrés des résidus
    ss_tot = np.sum((y_array - y_mean) ** 2)  # Somme totale des carrés
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    return {
        'a': a,
        'b': b,
        'r2': r2,
        'equation': f"y = {a:.4f}x + {b:.4f}"
    }

def predict(x_new: float, a: float, b: float) -> float:
    """Prédit une valeur y pour un x donné"""
    return a * x_new + b
```

### 🔨 À faire dans `main.py`

Remplacez la fonction `compute_regression(self)` (ligne ~345) :

```python
def compute_regression(self):
    try:
        if self.reg_input_mode.get() == "manual":
            # Récupérer X et Y
            x_text = self.reg_x.get().strip()
            y_text = self.reg_y.get().strip()
            
            x = [float(val.strip()) for val in x_text.split(',')]
            y = [float(val.strip()) for val in y_text.split(',')]
            
        else:  # Mode CSV
            import pandas as pd
            path = self.reg_csv_path.get()
            if not path:
                messagebox.showwarning("Attention", "Veuillez sélectionner un fichier CSV")
                return
            
            df = pd.read_csv(path)
            x = df.iloc[:, 0].tolist()
            y = df.iloc[:, 1].tolist()
        
        # Vérifier que X et Y ont la même longueur
        if len(x) != len(y):
            raise ValueError("X et Y doivent avoir le même nombre d'éléments")
        
        # Calculer la régression
        from core.regression import linear_regression
        result = linear_regression(x, y)
        
        # Afficher les résultats
        self.reg_results.delete('1.0', tk.END)
        self.reg_results.insert(tk.END, "=== RÉGRESSION LINÉAIRE ===\n\n")
        self.reg_results.insert(tk.END, f"Équation : {result['equation']}\n")
        self.reg_results.insert(tk.END, f"Pente (a) : {result['a']:.4f}\n")
        self.reg_results.insert(tk.END, f"Ordonnée (b) : {result['b']:.4f}\n")
        self.reg_results.insert(tk.END, f"Coefficient R² : {result['r2']:.4f}\n")
        
        # Afficher le graphique
        self.plot_regression(x, y, result['a'], result['b'])
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du calcul :\n{str(e)}")

def plot_regression(self, x, y, a, b):
    """Affiche le graphique de régression"""
    import numpy as np
    
    # Effacer le graphique précédent
    for widget in self.reg_graph_frame.winfo_children():
        widget.destroy()
    
    # Créer la figure
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # Nuage de points
    ax.scatter(x, y, color='blue', label='Données', s=50)
    
    # Droite de régression
    x_line = np.linspace(min(x), max(x), 100)
    y_line = a * x_line + b
    ax.plot(x_line, y_line, color='red', label=f'y = {a:.2f}x + {b:.2f}')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Régression Linéaire')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Afficher dans Tkinter
    canvas = FigureCanvasTkAgg(fig, master=self.reg_graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
```

---

## 🎲 Module 4 : Processus Stochastique

### 🆕 À créer : `core/stochastic.py`

```python
import numpy as np
from typing import List, Tuple

def markov_chain(
    transition_matrix: np.ndarray,
    initial_state: np.ndarray,
    steps: int
) -> Tuple[List[np.ndarray], np.ndarray]:
    """
    Simule une chaîne de Markov
    
    Args:
        transition_matrix: Matrice de transition (n x n)
        initial_state: État initial (vecteur de probabilités)
        steps: Nombre d'étapes
    
    Returns:
        - Liste des états à chaque étape
        - État stationnaire (si convergence)
    """
    states = [initial_state]
    current_state = initial_state.copy()
    
    for _ in range(steps):
        # Multiplier par la matrice de transition
        current_state = current_state @ transition_matrix
        states.append(current_state.copy())
    
    return states, current_state

def random_walk(steps: int, start: int = 0, p_up: float = 0.5) -> List[int]:
    """
    Simule une marche aléatoire
    
    Args:
        steps: Nombre de pas
        start: Position initiale
        p_up: Probabilité d'aller vers le haut
    
    Returns:
        Liste des positions à chaque étape
    """
    positions = [start]
    current_pos = start
    
    for _ in range(steps):
        # Décision : monter ou descendre
        if np.random.random() < p_up:
            current_pos += 1
        else:
            current_pos -= 1
        positions.append(current_pos)
    
    return positions

def simulate_multiple_walks(n_walks: int, steps: int, start: int = 0, p_up: float = 0.5) -> List[List[int]]:
    """Simule plusieurs marches aléatoires"""
    walks = []
    for _ in range(n_walks):
        walk = random_walk(steps, start, p_up)
        walks.append(walk)
    return walks
```

### 🔨 À faire dans `main.py`

Remplacez la fonction `simulate_stochastic(self)` (ligne ~349) :

```python
def simulate_stochastic(self):
    try:
        process_type = self.stoch_type.get()
        
        if process_type == "markov":
            # Chaîne de Markov
            matrix_text = self.stoch_matrix.get('1.0', tk.END).strip()
            lines = matrix_text.split('\n')
            matrix = np.array([[float(x) for x in line.split()] for line in lines if line.strip()])
            
            initial_text = self.stoch_initial.get().strip()
            initial = np.array([float(x.strip()) for x in initial_text.split(',')])
            
            steps = int(self.stoch_steps.get())
            
            # Simuler
            from core.stochastic import markov_chain
            states, final_state = markov_chain(matrix, initial, steps)
            
            # Afficher les résultats
            self.stoch_results.delete('1.0', tk.END)
            self.stoch_results.insert(tk.END, "=== CHAÎNE DE MARKOV ===\n\n")
            self.stoch_results.insert(tk.END, f"État initial : {initial}\n")
            self.stoch_results.insert(tk.END, f"État final (étape {steps}) : {final_state}\n")
            self.stoch_results.insert(tk.END, f"\nÉvolution :\n")
            
            for i, state in enumerate(states[:min(10, len(states))]):  # Afficher les 10 premiers
                self.stoch_results.insert(tk.END, f"Étape {i}: {state}\n")
            
            # Graphique
            self.plot_markov_chain(states)
            
        else:  # Marche aléatoire
            steps = int(self.stoch_steps.get())
            
            from core.stochastic import simulate_multiple_walks
            walks = simulate_multiple_walks(n_walks=5, steps=steps, start=0, p_up=0.5)
            
            # Afficher résultats
            self.stoch_results.delete('1.0', tk.END)
            self.stoch_results.insert(tk.END, "=== MARCHES ALÉATOIRES ===\n\n")
            self.stoch_results.insert(tk.END, f"Nombre de simulations : 5\n")
            self.stoch_results.insert(tk.END, f"Nombre de pas : {steps}\n")
            
            # Graphique
            self.plot_random_walks(walks)
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la simulation :\n{str(e)}")

def plot_markov_chain(self, states):
    """Affiche l'évolution de la chaîne de Markov"""
    import numpy as np
    
    # Effacer le graphique précédent
    for widget in self.stoch_graph_frame.winfo_children():
        widget.destroy()
    
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # Convertir en array pour faciliter le traçage
    states_array = np.array(states)
    n_states = states_array.shape[1]
    
    for i in range(n_states):
        ax.plot(states_array[:, i], label=f'État {i+1}', marker='o')
    
    ax.set_xlabel('Étapes')
    ax.set_ylabel('Probabilité')
    ax.set_title('Évolution de la Chaîne de Markov')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    canvas = FigureCanvasTkAgg(fig, master=self.stoch_graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def plot_random_walks(self, walks):
    """Affiche les marches aléatoires"""
    # Effacer le graphique précédent
    for widget in self.stoch_graph_frame.winfo_children():
        widget.destroy()
    
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    for i, walk in enumerate(walks):
        ax.plot(walk, alpha=0.6, label=f'Marche {i+1}')
    
    ax.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    ax.set_xlabel('Étapes')
    ax.set_ylabel('Position')
    ax.set_title('Marches Aléatoires')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    canvas = FigureCanvasTkAgg(fig, master=self.stoch_graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
```

---

## ✅ Checklist d'Implémentation

### Module 1 : Systèmes Linéaires
- [ ] Remplacer `solve_linear_system()` dans `main.py`
- [ ] Tester avec saisie manuelle
- [ ] Tester avec import CSV
- [ ] Vérifier l'affichage des résultats

### Module 2 : Programmation Linéaire
- [ ] Remplacer `solve_lp()` dans `main.py`
- [ ] Tester maximisation avec CSV
- [ ] Tester minimisation avec CSV
- [ ] Tester saisie manuelle
- [ ] (Optionnel) Ajouter graphique

### Module 3 : Régression Linéaire
- [ ] Créer `core/regression.py`
- [ ] Implémenter `linear_regression()`
- [ ] Remplacer `compute_regression()` dans `main.py`
- [ ] Ajouter `plot_regression()` dans `main.py`
- [ ] Tester avec données manuelles
- [ ] Tester avec CSV

### Module 4 : Processus Stochastique
- [ ] Créer `core/stochastic.py`
- [ ] Implémenter `markov_chain()`
- [ ] Implémenter `random_walk()`
- [ ] Remplacer `simulate_stochastic()` dans `main.py`
- [ ] Ajouter `plot_markov_chain()` et `plot_random_walks()`
- [ ] Tester chaînes de Markov
- [ ] Tester marches aléatoires

---

## 🚀 Conseils

1. **Testez au fur et à mesure** : Ne codez pas tout d'un coup
2. **Utilisez les print()** pour déboguer
3. **Gérez les exceptions** : Utilisez try/except partout
4. **Validez les entrées** : Vérifiez que les données sont cohérentes
5. **Commentez votre code** : Facilitez la maintenance

Bon courage ! 🎓
