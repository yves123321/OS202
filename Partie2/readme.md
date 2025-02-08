# **2.1 Résultats des temps d'exécution MPI**

## **Tableau des temps d'exécution**

| Nombre de processus (p) | Temps d'exécution (s) |
|------------------------|----------------------|
| 1                      | 0.003123             |
| 2                      | 0.004135             |
| 4                      | 0.042656             |
| 8                      | 0.223999             |

---

## **Calcul du Speedup**

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

## **Analyse des résultats**

- On observe que le temps d'exécution n'est pas linéairement réduit avec l'augmentation du nombre de processus.
- Le Speedup est bien inférieur à l'idéal (qui serait proche de p). Cela indique probablement que la communication MPI domine le temps de calcul, rendant l'exécution inefficace au-delà de 4 processus.






# **2.2 Résultats des temps d'exécution OpenMP**

## **Tableau des temps d'exécution OpenMP**

| Nombre de threads (p) | Temps d'exécution (s) |
|----------------------|----------------------|
| 1                    | 0.000542             |
| 2                    | 0.000844             |
| 4                    | 0.000848             |
| 8                    | 0.002269             |

---

## **Calcul du Speedup OpenMP**

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

## **Analyse des résultats OpenMP**

- Le Speedup attendu en OpenMP est généralement linéaire avec le nombre de threads, mais ici, on observe une accélération très faible voire négative à partir de 2 threads.
- Pour p = 8, le temps d'exécution augmente, ce qui indique probablement une surcharge due à la gestion des threads ou un manque d'optimisation des accès mémoire.








# **Résultats des temps d'exécution MPI et OpenMP**


## **Tableau des temps d'exécution MPI (Python)**

| Nombre de processus (p) | Temps d'exécution (s) |
|------------------------|----------------------|
| 1                      | 0.006500             |
| 2                      | 0.023315             |
| 4                      | 0.129870             |
| 8                      | 0.463661             |

---

## **Calcul du Speedup MPI (Python)**

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

## **Analyse des résultats MPI (Python)**

- Contrairement à ce qu'on pourrait attendre, l'augmentation du nombre de processus entraîne une dégradation des performances, ce qui indique que la communication MPI devient un goulot d’étranglement.