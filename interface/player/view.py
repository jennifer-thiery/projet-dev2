from domain.player import PlayerManager


def show_players():
    all_players = PlayerManager().all_players

    # Have length of longest element of each attribut
    w_firstname = max(len(p.firstname) for p in all_players) + 4
    w_lastname = max(len(p.lastname) for p in all_players) + 4
    w_club = max(len(p.club) for p in all_players) + 4
    w_email = max(len(p.email) for p in all_players) + 4

    print("--- Liste des participants ---\n")
    print(
        f"{'Licence':<12}{'Nom':<{w_lastname}}{'Prénom':<{w_firstname}}{'Club':<{w_club}}{'Classement':<14}{'Email':<{w_email}}{'Numéro de téléphone':<20}"
    )
    print("-" * (w_firstname + w_lastname + w_club + w_email + 12 + 14 + 20))

    for player in all_players:
        print(
            f"{player.licence_number:<12}{player.lastname:<{w_lastname}}{player.firstname:<{w_firstname}}{player.club:<{w_club}}{player.federation_ranking:<14}{player.email:<{w_email}}{player.phone_number:<20}"
        )

    input("\n[Enter] pour revenir au menu de la gestion des participants")


if __name__ == "__main__":
    show_players()
