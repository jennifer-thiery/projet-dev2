from copy import copy
from random import randint

from data.action_db_tournament import save_match_result
from domain.match import Match
from domain.tournament import Tournament


def result_random(match: Match) -> None:
    sets = []
    no_winner = True
    while no_winner:
        play1 = randint(0, 11)
        play2 = randint(0, 11)
        if play1 > play2:
            play1 = 11
            play2 = play2 if play1 - 2 >= play2 else randint(0, 9)
            sets.append((play1, play2))
        elif play1 < play2:
            play2 = 11
            play1 = play1 if play2 - 2 >= play1 else randint(0, 9)
            sets.append((play1, play2))
        play1 = 0
        play2 = 0
        for game in sets:
            if game[0] > game[1]:
                play1 += 1
            else:
                play2 += 1
        no_winner = not (play1 == 3 or play2 == 3)
    match.record_result(sets)


def generate_for_pools(tournament: Tournament) -> None:
    for bracket in tournament.brackets:
        for pool in bracket.pools:
            for match in pool.matches:
                if not match.is_played():
                    result = copy(match)
                    result_random(result)
                    save_match_result(bracket.type, result)
