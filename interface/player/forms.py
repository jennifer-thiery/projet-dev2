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

            if user_rep.upper() == "Q":
                print("Création du joueur annulée.")
                return
            elif user_rep.upper() == "R":
                break
            else:
                print("Je vous arrête tout de suite, ceci n'est pas une option valide")

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
            print("Je vous arrête tout de suite, ceci n'est pas une option valide")


def form_player_manager():
    licence_number = ""
    player = None
    while True:
        ct()
        print("\n=== modifier ou supprimer un participant ===")
        licence_number = required_input("Numéro de licence : ")
        if len(licence_number) != 8 or not licence_number.isdigit():
            print("La licence doit être composée de 8 chiffres")
        elif not PlayerManager().licence_exists(licence_number):
            print("La licence introduite n'est pas présente dans la liste des joueurs")
        else:
            print(f"Le joueur avec la licence {licence_number} a bien été trouvé")
            player = PlayerManager().player_pointer(licence_number)
            break

        while True:
            ans = input("Quitter [Q] ou Recommencer [R]: ")[:1]
            if ans.upper() == "Q":
                print("Modification ou suppression annulée")
                return
            if ans.upper() == "R":
                break
            else:
                print("Je vous arrête tout de suite, ceci n'est pas une option valide")
    while True:
        ct()
        print(player.player_overview())
        ans = input("Quelle action souhaitez vous effectuer: Modification [M] suppression [S] quitter [Q] : ")[:1]
        if ans.upper() == "M":
            form_edit_player(licence_number, player)
            return
        elif ans.upper() == "S":
            form_delete_player(licence_number, player)
            return
        elif ans.upper() == "Q":
            print("Rien n'est fait")
            return
        else:
            print("Je vous arrête tout de suite, ceci n'est pas une option valide")


def form_edit_player(pLicence_number, player):
    licence_number = player.licence_number
    firstname = player.firstname
    lastname = player.lastname
    club = player.club
    federation_ranking = player.federation_ranking
    email = player.email
    phone_number = player.phone_number
    while True:
        ct()
        print(
            f"""Joueur : {firstname} {lastname} ({licence_number})\nClassement : {federation_ranking}\nClub : {club}\nCoordonées : {email} | {phone_number}\n"""
        )
        print(
            "Que voulez vous modifier?: \n 1: numéro de licence\n 2: Prénom\n 3: nom de famille\n 4: Club\n 5: classement fédéral\n 6: email\n 7: numéro de téléphone\n Q: Quitter sans sauvegarder\n W: sauvegarder et quitter"
        )
        ans = input("votre choix : ")
        if ans.upper() == "Q":
            print("Soyons précis: aucune de vos modifications ont été sauvegardées")
            return
        elif ans == "1":
            while True:
                print("modification du numéro de licence")
                lic_ans = required_input("veuillez entrer le nouveau numéro de licence :")
                if len(lic_ans) != 8 or not lic_ans.isdigit():
                    print("La licence doit être composée de 8 chiffres")
                elif PlayerManager().licence_exists(lic_ans):
                    print("La licence introduite est déjà présente dans la liste des joueurs")
                else:
                    licence_number = lic_ans
                    break
        elif ans == "2":
            print("modification du prénom")
            firstname = required_input("Veuillez introduire le prénom :")
        elif ans == "3":
            print("modification du nom de famille")
            lastname = required_input("Veuillez introduire le nom de famille :")
        elif ans == "4":
            print("modification du club")
            club = required_input("Veuillez introduire le club :")
        elif ans == "5":
            print("modification du classement fédéral")
            federation_ranking = required_input("veuillez introduire le classement fédéral :")
        elif ans == "6":
            print("modification du mail")
            email = required_input("Veuillez introduire l'email :")
        elif ans == "7":
            print("modification du numéro de téléphone")
            phone_number = required_input("Veuillez introduire le numéro de téléphone :")
        elif ans.upper() == "W":
            print("sauvegarde de tout et quitte le menu")
            break
        else:
            print("Je vous arrête tout de suite, ceci n'est pas une option valide")

    PlayerManager().edit_player(
        pLicence_number, licence_number, firstname, lastname, club, federation_ranking, email, phone_number
    )


def form_delete_player(licence_number, player):
    while True:
        ct()
        print(player.player_overview())
        ans = required_input("Êtes-vous sûr de supprimer ce joueur? Oui [O] Non [N] : ")
        if ans.upper() == "O":
            print("suppression du joueur")
            PlayerManager().delete_player(licence_number)
            return
        elif ans.upper() == "N":
            print("Suppression annulée")
            return
        else:
            print("Je vous arrête tout de suite, ceci n'est pas une option valide")
