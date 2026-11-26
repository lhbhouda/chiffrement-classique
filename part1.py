#!/usr/bin/env python3


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# ----------------------------------------------------------------------
# Outil : mettre un texte au format A-Z
# ----------------------------------------------------------------------
def nettoyer(texte):
    """Majuscules, accents retirés, on ne garde que A-Z."""
    accents = {"É": "E", "È": "E", "Ê": "E", "Ë": "E", "À": "A", "Â": "A",
               "Ä": "A", "Î": "I", "Ï": "I", "Ô": "O", "Ö": "O", "Ù": "U",
               "Û": "U", "Ü": "U", "Ç": "C"}
    resultat = ""
    for c in texte.upper():
        c = accents.get(c, c)
        if c in ALPHABET:
            resultat += c
    return resultat


# ----------------------------------------------------------------------
# 1) CÉSAR : C = (M + k) mod 26
# ----------------------------------------------------------------------
def cesar_chiffrer(message, k):
    resultat = ""
    for c in message:
        m = ALPHABET.index(c)
        resultat += ALPHABET[(m + k) % 26]
    return resultat


def cesar_dechiffrer(message, k):
    return cesar_chiffrer(message, -k)


def cesar_force_brute(message):
    """Teste les 25 clés (1 à 25) et renvoie la liste (clé, texte)."""
    return [(k, cesar_dechiffrer(message, k)) for k in range(1, 26)]


# ----------------------------------------------------------------------
# 2) SUBSTITUTION : A -> 1re lettre de la clé, B -> 2e, etc.
# ----------------------------------------------------------------------
def cle_substitution_valide(cle):
    return len(cle) == 26 and sorted(cle) == list(ALPHABET)


def substitution_chiffrer(message, cle):
    resultat = ""
    for c in message:
        resultat += cle[ALPHABET.index(c)]
    return resultat


def substitution_dechiffrer(message, cle):
    resultat = ""
    for c in message:
        resultat += ALPHABET[cle.index(c)]
    return resultat


# ----------------------------------------------------------------------
# 3) TRANSPOSITION PAR COLONNES avec mot-clé
#    - message écrit en lignes sous le mot-clé (dernière ligne complétée par X)
#    - colonnes numérotées dans l'ordre alphabétique des lettres du mot-clé
#    - lecture de chaque colonne de haut en bas, dans cet ordre
# ----------------------------------------------------------------------
def ordre_colonnes(mot_cle):
    """Renvoie les indices des colonnes dans l'ordre alphabétique du mot-clé.
    Si une lettre est répétée, la plus à gauche passe en premier."""
    return sorted(range(len(mot_cle)), key=lambda i: (mot_cle[i], i))


def transposition_chiffrer(message, mot_cle):
    n_col = len(mot_cle)
    while len(message) % n_col != 0:
        message += "X"
    resultat = ""
    for col in ordre_colonnes(mot_cle):
        resultat += message[col::n_col]  # colonne de haut en bas
    return resultat


def transposition_dechiffrer(message, mot_cle):
    n_col = len(mot_cle)
    n_lig = len(message) // n_col
    lignes_cols = [""] * n_col          # contenu de chaque colonne d'origine
    pos = 0
    for col in ordre_colonnes(mot_cle):
        lignes_cols[col] = message[pos:pos + n_lig]
        pos += n_lig
    resultat = ""
    for i in range(n_lig):              # on relit ligne par ligne
        for col in range(n_col):
            resultat += lignes_cols[col][i]
    return resultat


# ----------------------------------------------------------------------
# Interface terminal
# ----------------------------------------------------------------------
def demander_entier(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("  -> Entre un nombre entier.")


def demander_texte(message):
    while True:
        texte = nettoyer(input(message))
        if texte:
            return texte
        print("  -> Texte vide (seules les lettres A-Z sont gardées).")


def demander_cle_substitution():
    while True:
        cle = nettoyer(input("Clé (26 lettres uniques) : "))
        if cle_substitution_valide(cle):
            return cle
        print("  -> Il faut les 26 lettres de l'alphabet, chacune une seule fois.")


def main():
    while True:
        print("\n===== CRYPTOBOX - BRIQUE 1 =====")
        print("1. César")
        print("2. Substitution")
        print("3. Transposition (mot-clé)")
        print("4. Force brute sur César")
        print("0. Quitter")
        choix = input("Ton choix : ").strip()

        if choix == "0":
            print("Au revoir !")
            break

        if choix == "4":
            message = demander_texte("Texte chiffré : ")
            for k, texte in cesar_force_brute(message):
                print(f"k = {k:2d} : {texte}")
            continue

        if choix not in ("1", "2", "3"):
            print("Choix invalide.")
            continue

        action = input("a. Chiffrer   b. Déchiffrer : ").strip().lower()
        if action not in ("a", "b"):
            print("Choix invalide.")
            continue
        message = demander_texte("Message : ")

        if choix == "1":
            k = demander_entier("Clé k : ")
            f = cesar_chiffrer if action == "a" else cesar_dechiffrer
            print("Résultat :", f(message, k))
        elif choix == "2":
            cle = demander_cle_substitution()
            f = substitution_chiffrer if action == "a" else substitution_dechiffrer
            print("Résultat :", f(message, cle))
        else:
            mot_cle = demander_texte("Mot-clé : ")
            f = transposition_chiffrer if action == "a" else transposition_dechiffrer
            print("Résultat :", f(message, mot_cle))


if __name__ == "__main__":
    main()
