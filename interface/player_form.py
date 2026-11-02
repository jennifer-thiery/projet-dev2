from domain.player import Player, PlayerManager


def form_add_player():
    print("--- Renseignez les informations du joueur ---")
    licence_number = input("Numéro de licence : ")
    firstname = input("Prénom : ")
    lastname = input("Nom : ")
    club = input("Club : ")
    federation_ranking = input("Classement fédéral : ")
    email = input("Email : ")
    phone_number = input("Numéro de téléphone : ")

    new_player = Player(
        licence_number=licence_number,
        firstname=firstname,
        lastname=lastname,
        club=club,
        federation_ranking=federation_ranking,
        email=email,
        phone_number=phone_number,
    )

    print("--- Aperçu du joueur ---")
    print(new_player.player_overview())

    PlayerManager().add_player(new_player)
    print(f"Joueur {licence_number} : {firstname} {lastname} ajouté")
