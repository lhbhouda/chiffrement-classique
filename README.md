# Chiffrement classique

Mini projet Python de cryptographie classique, codé from scratch (sans bibliothèque externe).

## Algorithmes
- **César** : décalage des lettres avec une clé de 0 à 25
- **Substitution** : alphabet mélangé de 26 lettres comme clé
- **Transposition** : lecture du texte par colonnes (clé = nombre de colonnes)
- **Force brute sur César** : essaie les 26 clés possibles

## Utilisation
```bash
python3 part1.py
```
Un menu permet de choisir l'algorithme, de chiffrer ou déchiffrer, et de saisir la clé.

## Exemple
César, clé 3 : `Bonjour` → `Erqmrxu`
