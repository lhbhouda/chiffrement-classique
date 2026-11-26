#!/usr/bin/env python3


import random
import string

ALPHABET = string.ascii_lowercase  # "abcdefghijklmnopqrstuvwxyz"


# ----------------------------------------------------------------------
# 1) CÉSAR : on décale chaque lettre de "cle" positions
# ----------------------------------------------------------------------
def cesar_chiffrer(texte, cle):
    resultat = ""
    for c in texte:
        if c.isascii() and c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            resultat += chr((ord(c) - base + cle) % 26 + base)
        else:
            resultat += c  # espaces, chiffres, ponctuation : inchangés
    return resultat


def cesar_dechiffrer(texte, cle):
    return cesar_chiffrer(texte, -cle)


def cesar_force_brute(texte):
    """Essaie les 26 clés possibles et affiche chaque résultat."""
    for cle in range(26):
        print(f"Clé {cle:2d} : {cesar_dechiffrer(texte, cle)}")


# ----------------------------------------------------------------------
# 2) SUBSTITUTION : chaque lettre est remplacée par une autre
#    La clé est un "alphabet mélangé" de 26 lettres (ex: qwertyuiopasdfghjklzxcvbnm)
# ----------------------------------------------------------------------
def cle_substitution_valide(cle):
    return len(cle) == 26 and sorted(cle.lower()) == list(ALPHABET)


def generer_cle_substitution():
    lettres = list(ALPHABET)
    random.shuffle(lettres)
    return "".join(lettres)


def substitution_chiffrer(texte, cle):
    resultat = ""
    for c in texte:
        if c.isascii() and c.isalpha():
            nouvelle = cle[ALPHABET.index(c.lower())]
            resultat += nouvelle.upper() if c.isupper() else nouvelle
        else:
            resultat += c
    return resultat


def substitution_dechiffrer(texte, cle):
    resultat = ""
    for c in texte:
        if c.isascii() and c.isalpha():
            ancienne = ALPHABET[cle.index(c.lower())]
            resultat += ancienne.upper() if c.isupper() else ancienne
        else:
            resultat += c
    return resultat


# ----------------------------------------------------------------------
# 3) TRANSPOSITION (par colonnes) : la clé = nombre de colonnes
#    On lit le texte colonne par colonne.
#    Ex: "BONJOUR" avec clé 3 -> colonnes : B-J-R / O-O / N-U -> "BJROONU"
# ----------------------------------------------------------------------
def transposition_chiffrer(texte, cle):
    resultat = ""
    for col in range(cle):
        resultat += texte[col::cle]  # une lettre sur "cle", à partir de col
    return resultat


def transposition_dechiffrer(texte, cle):
    n = len(texte)
    resultat = [""] * n
    pos = 0
    for col in range(cle):
        for i in range(col, n, cle):
            resultat[i] = texte[pos]
            pos += 1
    return "".join(resultat)


# ----------------------------------------------------------------------
# Fonctions utilitaires pour le menu
# ----------------------------------------------------------------------
def demander_entier(message, minimum=None, maximum=None):
    while True:
        try:
            valeur = int(input(message))
            if minimum is not None and valeur < minimum:
                print(f"  -> La valeur doit être >= {minimum}")
            elif maximum is not None and valeur > maximum:
                print(f"  -> La valeur doit être <= {maximum}")
            else:
                return valeur
        except ValueError:
            print("  -> Entre un nombre entier.")


def demander_cle_substitution(mode):
    while True:
        if mode == "chiffrer":
            cle = input("Clé (26 lettres uniques) ou ENTRÉE pour en générer une : ").lower()
            if cle == "":
                cle = generer_cle_substitution()
                print("Clé générée (GARDE-LA pour déchiffrer) :", cle)
                return cle
        else:
            cle = input("Clé (26 lettres uniques) : ").lower()
        if cle_substitution_valide(cle):
            return cle
        print("  -> Clé invalide : il faut les 26 lettres de l'alphabet, chacune une seule fois.")


def traiter(algo, mode):
    texte = input("Texte : ")

    if algo == "1":  # César
        cle = demander_entier("Clé (décalage 0-25) : ", 0, 25)
        if mode == "chiffrer":
            print("Résultat :", cesar_chiffrer(texte, cle))
        else:
            print("Résultat :", cesar_dechiffrer(texte, cle))

    elif algo == "2":  # Substitution
        cle = demander_cle_substitution(mode)
        if mode == "chiffrer":
            print("Résultat :", substitution_chiffrer(texte, cle))
        else:
            print("Résultat :", substitution_dechiffrer(texte, cle))

    elif algo == "3":  # Transposition
        cle = demander_entier("Clé (nombre de colonnes >= 2) : ", 2)
        if mode == "chiffrer":
            print("Résultat :", transposition_chiffrer(texte, cle))
        else:
            print("Résultat :", transposition_dechiffrer(texte, cle))


def main():
    while True:
        print("\n===== CHIFFREMENT CLASSIQUE =====")
        print("1. César")
        print("2. Substitution")
        print("3. Transposition")
        print("4. Force brute sur César")
        print("0. Quitter")
        algo = input("Ton choix : ").strip()

        if algo == "0":
            print("Au revoir !")
            break

        elif algo == "4":
            texte = input("Texte chiffré à casser : ")
            cesar_force_brute(texte)

        elif algo in ("1", "2", "3"):
            print("a. Chiffrer")
            print("b. Déchiffrer")
            action = input("Ton choix : ").strip().lower()
            if action == "a":
                traiter(algo, "chiffrer")
            elif action == "b":
                traiter(algo, "dechiffrer")
            else:
                print("Choix invalide.")

        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()
