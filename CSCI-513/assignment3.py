import re
from collections import namedtuple
extract_row = re.compile(r"^(\w+)\t(\d+)\t(\w+)\t(\d+)\t(\d+)\n?$")
Game = namedtuple('Game', ['visitor_team', 'visitor_points'
                          , 'home_team', 'home_points', 'attendance'])
games = set()
with open("nba.txt", "r") as nba_file:
    header_line = next(nba_file)
    for row_line in nba_file:
        R = re.fullmatch(extract_row, row_line)
        if R: games.add(Game(R[1], int(R[2]), R[3], int(R[4]), int(R[5])))
        else: print("Error:", row_line)
        
wins = dict()
for game in games:
    winner = None
    if game.home_points > game.visitor_points: winner = game.home_team
    if game.visitor_points > game.home_points: winner = game.visitor_team
    if winner:
        if winner not in wins:
            wins[winner] = 1
        else: wins[winner] += 1

with open("wins.csv", "w") as wins_file:
    for team, win_count in sorted(wins.items()):
        wins_file.write(f"{team},{win_count}\n")