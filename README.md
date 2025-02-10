## Question 1 - Parallélisation ensemble de Mandelbrot


### 1.1 Analyse du Speedup pour le Calcul Parallèle de l'Ensemble de Mandelbrot

#### (1) Observation des Résultats
| Nombre de Processus | Temps Total (s) | Speedup |
|---------:|-----------------:|---------:|
|        1 |             3.2  |  1       |
|        2 |             1.78 |  1.79775 |
|        3 |             2.39 |  1.33891 |
|        4 |             2.38 |  1.34454 |
|        6 |             2.51 |  1.2749  |
|        8 |             2.71 |  1.18081 |

On observe que l'augmentation du nombre de processus améliore initialement les performances (1 → 2 processus), mais qu'après un certain seuil, le speedup ne continue pas à augmenter de manière significative.

#### (2) Analyse des Raisons Possibles
- **Overhead de Communication** : L'utilisation de MPI entraîne un échange de données entre processus, ce qui peut ralentir l'exécution globale, surtout lorsque le processus 0 doit rassembler toutes les données.
- **Répartition Déséquilibrée de la Charge** : Certains processus peuvent se voir attribuer des zones plus complexes à calculer, entraînant une exécution plus 


### 1.2 Analyse des Performances pour la Répartition Statique Optimisée

#### (1) Résultats Expérimentaux
| Nombre de Processus | Temps Total (s) | Speedup |
|--------------------|----------------|---------|
|   Nombre de Processus |   Temps Total (s) |   Speedup |
|----------------------:|------------------:|----------:|
|                     1 |              3.24 |   1       |
|                     2 |              1.81 |   1.79006 |
|                     3 |              1.87 |   1.73262 |
|                     4 |              1.79 |   1.81006 |
|                     6 |              1.84 |   1.76087 |
|                     8 |              2.03 |   1.59606 |

On constate que le speedup augmente lorsque l'on passe de 1 à 2 processus, mais que l'amélioration devient moins significative à mesure que le nombre de processus augmente.

#### (2) Comparaison avec la Répartition Uniforme
Par rapport à la répartition uniforme des lignes, cette méthode réduit la charge de travail inégale entre les processus. 

#### (3) Limites de cette Stratégie
Cette stratégie peut poser plusieurs problèmes :
- Déséquilibre résiduel : Même si l'attribution des lignes est optimisée, certaines parties de l'image nécessitent plus de calculs, créant un déséquilibre entre processus.
- Overhead de communication : À mesure que le nombre de processus augmente, la gestion des communications et de la synchronisation entraîne un coût supplémentaire qui limite les gains de performance.


### 1.3 Analyse des Performances pour la Stratégie Maître-Esclave

#### (1) Résultats Expérimentaux
| Nombre de Processus | Temps Total (s) | Speedup |
|--------------------|----------------|---------|
|   Nombre de Processus |   Temps Total (s) |   Speedup |
|----------------------:|------------------:|----------:|
|                     1 |              7.46 |   1       |
|                     2 |              8    |   0.9325  |
|                     3 |              6.42 |   1.16199 |
|                     4 |              5.83 |   1.27959 |
|                     6 |              5.83 |   1.27959 |
|                     8 |              5.62 |   1.3274  |

On observe que le speedup initialement augmente totalement avec le nombre de processus.

#### (2) Comparaison avec les Autres Méthodes
Par rapport à la répartition statique des lignes :
- Cette stratégie est plus dynamique : les tâches sont distribuées en fonction de la disponibilité des processus, évitant ainsi les problèmes de charge déséquilibrée.
- Mais elle entraîne un overhead de communication qui peut ralentir les performances lorsque le nombre de processus augmente.






## Question 2 - Produit Matrice-Vecteur

### (a) **Méthode par Colonnes**
| Nombre de Processus | Nloc (par colonnes) | Temps Total (s) | Speedup |
|--------------------|-------------------|----------------|---------|
|   Nombre de Processus |   Nloc (par colonnes) |   Temps Total (s) |   Speedup |
|----------------------:|----------------------:|------------------:|----------:|
|                     1 |                  5760 |            0.3073 |  1        |
|                     2 |                  2880 |            0.5983 |  0.513622 |
|                     3 |                  1920 |            0.4668 |  0.658312 |
|                     4 |                  1440 |            0.41   |  0.749512 |
|                     6 |                   960 |            0.39   |  0.787949 |
|                     8 |                   720 |            0.35   |  0.878    |

### (b) **Méthode par Lignes**
| Nombre de Processus | Nloc (par lignes) | Temps Total (s) | Speedup |
|--------------------|-----------------|----------------|---------|
|   Nombre de Processus |   Nloc (par lignes) |   Temps Total (s) |   Speedup |
|----------------------:|--------------------:|------------------:|----------:|
|                     1 |                5760 |            0.0197 | 1         |
|                     2 |                2880 |            0.0112 | 1.75893   |
|                     3 |                1920 |            0.3669 | 0.0536931 |
|                     4 |                1440 |            0.009  | 2.18889   |
|                     6 |                 960 |            0.007  | 2.81429   |
|                     8 |                 720 |            0.006  | 3.28333   |

### **Analyse et Conclusion**
1. Par Colonnes : On observe que l'exécution n'est pas strictement linéairement scalable, ce qui indique une surcharge de communication et une gestion de mémoire moins efficace.
2. Par Lignes : Cette méthode offre une accélération plus marquée, montrant une meilleure efficacité avec un faible overhead de communication.









## Question 3 - Entraînement pour l'examen écrit

### (1)

Alice a observé que **90% du temps** de son programme peut être parallélisé. Nous utilisons la **loi d'Amdahl**, qui exprime le **speedup maximal** en fonction de la proportion parallélisable **p = 0.9** :

$$
S(n) = \frac{1}{(1 - p) + \frac{p}{n}}
$$

En prenant la limite lorsque **n → ∞** (nombre de nœuds de calcul très élevé), la formule devient :

$$
S_{\max} = \frac{1}{1 - 0.9} = \frac{1}{0.1} = 10
$$

Donc, **même avec un nombre infini de nœuds**, Alice ne pourra jamais dépasser une accélération de **10x**.

---

### (2) Nombre optimal de nœuds

Dans un contexte réel, il est important de choisir un nombre de nœuds suffisant **sans gaspiller de ressources CPU**. Selon la loi d'Amdahl :

- Avec **n = 4** nœuds :

  $$
  S(4) = \frac{1}{(1 - 0.9) + \frac{0.9}{4}}
  $$

  $$
  S(4) = \frac{1}{0.1 + 0.225} = \frac{1}{0.325} \approx 3.08
  $$

Cela montre que **l'ajout de plus de 4 nœuds ne serait pas très bénéfique**. Un nombre raisonnable de nœuds se situerait entre **4 et 8**, car au-delà, le gain est marginal.

---

### (3) Accélération selon la loi de Gustafson

Lorsque **la quantité de données est doublée**, nous supposons une complexité parallèle **linéaire** et utilisons la **loi de Gustafson** :

$$
S(n) = n - (1 - p) \times n
$$

Sachant qu'Alice a obtenu une accélération **S(n) = 4** pour un certain nombre de nœuds **n**, nous cherchons la nouvelle accélération **S'(n)** en doublant la charge de travail.

Avec **p = 0.9**, et en supposant que le même nombre de nœuds **n** est utilisé :

$$
S'(n) = n - (1 - 0.9) \times n
$$

$$
S'(n) = n - 0.1 \times n = 0.9n
$$

Cela signifie que **l'accélération augmentera presque linéairement avec la charge de travail**. Si **S(n) = 4** auparavant, alors avec **2× plus de données**, Alice pourrait atteindre :

$$
S'(n) = 2 \times 4 = 8
$$

Donc, en doublant les données, Alice pourrait espérer une accélération **jusqu'à 8x** en utilisant la loi de Gustafson.
