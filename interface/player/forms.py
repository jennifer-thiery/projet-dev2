from time import sleep

from domain.enums import FederationRanking
from domain.player import Player, PlayerManager
from lib.tools import ct


def required_input(prompt: str):
    while True:
        value = input(prompt)

        if value == "":
            print("Veillez introduire une valeur !")
        else:
            return value


def form_add_player():
    while True:
        ct()
        print("\n=== Ajouter un participant ===")
        licence_number = required_input("Numéro de licence : ")

        # Check licence number before asking other informations
        if len(licence_number) != 8 or not licence_number.isdigit():
            print("La licence doit être composée de 8 chiffres.")
        elif PlayerManager().licence_exists(licence_number):
            print(f"La licence {licence_number} existe déjà dans la liste des participants")
        else:
            break

        while True:
            user_rep = input("Quitter [Q] ou Recommencer [R] : ")[:1]

            if user_rep == "Q":
                print("Création du joueur annulée.")
                return
            elif user_rep == "R":
                break
            else:
                print("Entrée invalide")

    print("\n--- Renseignez les informations du joueur ---")
    firstname = required_input("Prénom : ")
    lastname = required_input("Nom : ")
    club = required_input("Club : ")

    # Check if it's a valid federation ranking
    while True:
        federation_ranking = required_input("Classement fédéral : ")
        if federation_ranking not in FederationRanking:
            print("Classement invalide")
        else:
            break

    email = required_input("Email : ")
    phone_number = required_input("Numéro de téléphone : ")

    # Display informations of the new player
    new_player = Player(
        licence_number=licence_number,
        firstname=firstname,
        lastname=lastname,
        club=club,
        federation_ranking=federation_ranking,
        email=email,
        phone_number=phone_number,
    )
    print("\n--- Aperçu du joueur ---")
    print(new_player.player_overview())

    # Ask confirmation before adding player to list
    while True:
        confirm = input("Validez-vous la création de ce joueur ? [O/N] : ")[:1]
        if confirm == "O":
            PlayerManager().add_player(new_player)
            print(f"Joueur {licence_number} : {firstname} {lastname} ajouté")
            sleep(1.5)
            break
        elif confirm == "N":
            return
        else:
            print("Entrée invalide")


def form_edit_player():
    print("edit player")


def form_delete_player():
    print("delete player")
