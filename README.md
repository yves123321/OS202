
# TD1
#### Qizheng WANG
#### Remarque: J'ai terminé les deux premières parties, **README** est l'enregistrement de mes résultats.
# I. Partie 1

`pandoc -s --toc README.md --css=./github-pandoc.css -o README.html`


## Produit matrice-matrice

### Effet de la taille de la matrice

  n            | MFlops
---------------|--------
1024 (origine) | 61.6447
1023           | 96.6385
1025           | 96.7703


*Expliquer les résultats：*

*Les résultats montrent une variation significative des performances en fonction de la taille de la matrice. Pour 𝑛=1024 n=1024, la performance est plus faible (61.64 MFlops) par rapport aux tailles non alignées 𝑛=1023 n=1023 et 𝑛=1025
n=1025 (~96.7 MFlops). Cette différence est due à l’alignement mémoire : 1024 est une puissance de 2, ce qui peut entraîner des conflits de cache (cache associatif), tandis que 1023 et 1025 répartissent mieux les accès mémoire, réduisant les cache misses et améliorant ainsi la performance.*

### Permutation des boucles

*Expliquer comment est compilé le code (ligne de make ou de gcc) : on aura besoin de savoir l'optim, les paramètres, etc. Par exemple :*

`make TestProduct.exe && ./TestProduct.exe 1024`


  ordre           | time    | MFlops  |
------------------|---------|---------|
i,j,k (origine)   | 16.0961 | 133.417 |
j,i,k             | 23.5417 | 91.2202 |
i,k,j             | 39.2870 | 54.6614 |
k,i,j             | 28.3425 | 75.7691 |
j,k,i             | 12.0201 | 178.658 |
k,j,i             | 13.5173 | 158.869 |


*Discuter les résultats.*

Les résultats montrent une forte dépendance de la performance à l'ordre des boucles. L'ordre j,k,i est le plus rapide (12.02s, 178.66 MFlops), suivi de k,j,i (13.52s, 158.87 MFlops), indiquant une meilleure exploitation du cache et de la localité mémoire. Ces résultats suggèrent que prioriser l'itération sur les colonnes (j) ou les lignes (k) avant les multiplications internes améliore les performances.



### OMP sur la meilleure boucle

`make TestProduct.exe && OMP_NUM_THREADS=8 ./TestProduct.exe 1024`

  OMP_NUM         | MFlops  |  MFlops(n=2048) | MFlops(n=512)  | 
------------------|---------|-----------------|----------------|
1                 | 17.8758 |     17.8758     |     36.5950    |
2                 | 34.0799 |     19.6172     |     49.5074    |
3                 | 51.9702 |     19.6053     |     53.0270    |
4                 | 51.9944 |     19.3541     |     87.4854    |
5                 | 55.4674 |     19.2349     |     95.6910    |
6                 | 54.6610 |     22.0020     |     88.8524    |
7                 | 58.7588 |     51.5638     |     109.757    |
8                 | 63.2577 |     54.3109     |     81.0722    |

*Tracer les courbes de speedup (pour chaque valeur de n), discuter les résultats.*
![Description](./output.png)

Les courbes de speedup montrent une accélération variable en fonction de la taille de la matrice et du nombre de threads. Pour \( n=1024 \) et \( n=512 \), le speedup est presque linéaire jusqu'à 8 threads, indiquant une bonne scalabilité. Cependant, pour \( n=2048 \), l'accélération reste faible jusqu'à 6 threads, puis augmente fortement à 7 et 8 threads. Cela peut être dû à la saturation de la bande passante mémoire et à une mauvaise exploitation du cache pour de grandes matrices.


### Produit par blocs

`make TestProduct.exe && ./TestProduct.exe 1024`

  szBlock         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | 
------------------|---------|----------------|----------------|
origine (=max)    | 133.417 | 138.241 | 159.076 |
32                | 151.514 | 146.692 | 171.390 |
64                | 156.570 | 151.630 | 163.212 | 
128               | 159.440 | 157.445 | 167.792 |
256               | 150.700 | 148.322 | 153.776 |
512               | 110.821 | 109.987 | 139.625 |
1024              | 51.7021 | 52.4546 | 80.7186 |

*Discuter les résultats.*
L’optimisation par blocs améliore la performance du produit matrice-matrice en exploitant mieux la hiérarchie de la mémoire cache. On observe que la performance (en MFlops) augmente avec la taille du bloc jusqu’à un certain seuil, avec un maximum autour de 128. Au-delà de cette valeur, les performances diminuent, notamment pour `szBlock = 512` et `1024`, car les blocs deviennent trop grands pour tenir dans le cache L1 ou L2.


### Bloc + OMP


  szBlock      | OMP_NUM | MFlops  | MFlops(n=2048) | MFlops(n=512)  |
---------------|---------|---------|----------------|----------------|
1024           |  1      | 58.7836 |    34.3739     |    97.9819     |
1024           |  8      | 61.8933 |    43.2985     |    133.653     |
512            |  1      | 130.785 |    120.942     |    137.855     |
512            |  8      | 133.325 |    122.377     |    123.671     |

*Discuter les résultats.*

L’optimisation par blocs améliore les performances tant que la taille des blocs reste adaptée à la capacité du cache. Un szBlock trop grand réduit les performances à cause des cache misses et du mauvais équilibrage du travail entre threads. Dans ce cas, szBlock = 512 semble être le meilleur compromis pour tirer profit à la fois du cache et du parallélisme.

### Comparaison avec BLAS, Eigen et numpy

*Comparer les performances avec un calcul similaire utilisant les bibliothèques d'algèbre linéaire BLAS, Eigen et/ou numpy.*

| Bibliothèques  | MFlops  | MFlops(n=2048) |
|      BLAS      | 39426.9 |    35753.1     |

Les performances du produit matrice-matrice avec BLAS sont plusieurs ordres de grandeur supérieures à celles de notre implémentation optimisée. Parce que BLAS a exploite des optimisations bas niveau.

### Tips

```
	env
	OMP_NUM_THREADS=4 ./produitMatriceMatrice.exe
```

```
    $ for i in $(seq 1 4); do elap=$(OMP_NUM_THREADS=$i ./TestProductOmp.exe|grep "Temps CPU"|cut -d " " -f 7); echo -e "$i\t$elap"; done > timers.out
```




# II. Partie 2 - Jeton
## II.1 Résultats des temps d'exécution MPI

### Tableau des temps d'exécution

| Nombre de processus (p) | Temps d'exécution (s) |
|------------------------|----------------------|
| 1                      | 0.003123             |
| 2                      | 0.004135             |
| 4                      | 0.042656             |
| 8                      | 0.223999             |

---

### Calcul du Speedup

Le Speedup est défini par la formule :

\[
S(p) = \frac{T_1}{T_p}
\]

| Nombre de processus (p) | Temps d'exécution (s) | Speedup \( S(p) \) |
|------------------------|----------------------|-----------------|
| 1                      | 0.003123             | 1.00            |
| 2                      | 0.004135             | 1.51            |
| 4                      | 0.042656             | 0.29            |
| 8                      | 0.223999             | 0.11            |

---

### Analyse des résultats

- On observe que le temps d'exécution n'est pas linéairement réduit avec l'augmentation du nombre de processus.
- Le Speedup est bien inférieur à l'idéal (qui serait proche de p). Cela indique probablement que la communication MPI domine le temps de calcul, rendant l'exécution inefficace au-delà de 4 processus.






## II.2 Résultats des temps d'exécution OpenMP

### Tableau des temps d'exécution OpenMP

| Nombre de threads (p) | Temps d'exécution (s) |
|----------------------|----------------------|
| 1                    | 0.000542             |
| 2                    | 0.000844             |
| 4                    | 0.000848             |
| 8                    | 0.002269             |

---

### Calcul du Speedup OpenMP

Le Speedup est défini par la formule :

\[
S(p) = \frac{T_1}{T_p}
\]

| Nombre de threads (p) | Temps d'exécution (s) | Speedup \( S(p) \) |
|----------------------|----------------------|-----------------|
| 1                    | 0.000542             | 1.00            |
| 2                    | 0.000844             | 1.28            |
| 4                    | 0.000848             | 2.55            |
| 8                    | 0.002269             | 1.92            |

---

### Analyse des résultats OpenMP

Le Speedup attendu en OpenMP est généralement linéaire avec le nombre de threads, mais ici, on observe une accélération très faible, ce qui indique probablement une surcharge due à la gestion des threads ou un manque d'optimisation des accès mémoire.



## II.3 Résultats des temps d'exécution MPI (Python)
### Tableau des temps d'exécution MPI (Python)

| Nombre de processus (p) | Temps d'exécution (s) |
|------------------------|----------------------|
| 1                      | 0.006500             |
| 2                      | 0.023315             |
| 4                      | 0.129870             |
| 8                      | 0.463661             |

---

### Calcul du Speedup MPI (Python)

\[
S(p) = \frac{T_2}{T_p}
\]

| Nombre de processus (p) | Temps d'exécution (s) | Speedup \( S(p) \) |
|------------------------|----------------------|-----------------|
| 1                      | 0.016500             | 1.00            |
| 2                      | 0.034021             | 0.97            |
| 4                      | 0.068253             | 0.96            |
| 8                      | 0.148798             | 0.88            |

---

### Analyse des résultats MPI (Python)

Contrairement à ce qu'on pourrait attendre, l'augmentation du nombre de processus entraîne une dégradation des performances.













# III. Partie 2 - Calcul de Pi

## III.1 Tableau des temps d'exécution

### Méthode Séquentielle
| Nombre de processus/threads | Temps d'exécution (s) |
|----------------------------|----------------------|
| 1 (Séquentiel)             | 2.596822             |

### OpenMP (Mémoire partagée)
| Nombre de threads | Temps d'exécution (s) |
|------------------|----------------------|
| 1               | 1.037327              |
| 2               | 0.569004              |
| 4               | 0.586210              |
| 8               | 0.633730              |

### MPI (Mémoire distribuée en C)
| Nombre de processus | Temps d'exécution (s) |
|--------------------|----------------------|
| 1                | 1.060543              |
| 2                | 0.560285              |
| 4                | 0.541664              |
| 8                | 0.529933              |

### MPI (Python - `mpi4py`)
| Nombre de processus | Temps d'exécution (s) |
|--------------------|----------------------|
| 1                | 47.035593             |
| 2                | 26.989896             |
| 4                | 27.864133             |
| 8                | 28.408249             |

---

## III.2 Tableau du Speedup

Le speedup est calculé comme :
\[
S(p) = \frac{T_1}{T_p}
\]

### OpenMP
| Nombre de threads | Temps d'exécution (s) | Speedup \( S(p) \) |
|------------------|----------------------|-----------------|
| 1               | 1.037327              | 1.00            |
| 2               | 0.569004              | 1.82            |
| 4               | 0.586210              | 1.77            |
| 8               | 0.633730              | 1.64            |

### MPI en C
| Nombre de processus | Temps d'exécution (s) | Speedup \( S(p) \) |
|--------------------|----------------------|-----------------|
| 1                | 1.060543              | 1.00            |
| 2                | 0.560285              | 1.89            |
| 4                | 0.541664              | 1.96            |
| 8                | 0.529933              | 2.00            |

### MPI en Python
| Nombre de processus | Temps d'exécution (s) | Speedup \( S(p) \) |
|--------------------|----------------------|-----------------|
| 1                | 47.035593             | 1.00            |
| 2                | 26.989896             | 1.74            |
| 4                | 27.864133             | 1.69            |
| 8                | 28.408249             | 1.66            |

---

## III.3 Analyse des résultats

### 1. OpenMP (Mémoire partagée)
- Le speedup est presque linéaire pour 2 threads (1.82x).
- À partir de 4 threads, l'accélération se stabilise voire diminue légèrement, indiquant une saturation mémoire ou une surcharge due à la synchronisation des threads.

### 2. MPI en C (Mémoire distribuée)
- Très bon speedup jusqu'à 4 processus (~1.96x).

### 3. MPI en Python (`mpi4py`)
- Performances globalement beaucoup plus lentes que C et OpenMP.
- L’accélération existe (1.74x à 2 processus) mais s'effondre après 4 processus.

Conclusion : Pour un calcul parallèle performant, OpenMP est efficace pour des systèmes mono-machine, tandis que MPI en C est préférable pour des exécutions distribuées.

