# match.py

import random

class Match:
    def __init__(self, player1, player2, win_rates, tie_rates, win_rate_format):
        self.player1 = player1
        self.player2 = player2
        self.win_rates = win_rates
        self.tie_rates = tie_rates
        self.win_rate_format = win_rate_format

    def simulate(self):
        win_rate = self.win_rates.get((self.player1.deck, self.player2.deck), self.win_rates.get((self.player2.deck, self.player1.deck), 0.5))
        tie_rate = self.tie_rates.get((self.player1.deck, self.player2.deck), self.tie_rates.get((self.player2.deck, self.player1.deck), 0.0))

        rand_val = random.random()

        if rand_val < tie_rate:
            self.player1.matches_tied += 1
            self.player2.matches_tied += 1
            self.player1.match_points += 1
            self.player2.match_points += 1
        elif self.win_rate_format == "BO3_GAME":
            player1_game_wins = 0
            player2_game_wins = 0
            
            # Simulate games until one player wins 2 games
            while player1_game_wins < 2 and player2_game_wins < 2:
                game_rand_val = random.random()
                if game_rand_val < win_rate:
                    player1_game_wins += 1
                else:
                    player2_game_wins += 1
            
            if player1_game_wins == 2:
                self.player1.matches_won += 1
                self.player2.matches_lost += 1
                self.player1.match_points += 3
            else:
                self.player2.matches_won += 1
                self.player1.matches_lost += 1
                self.player2.match_points += 3
        else: # BO1 or BO3_MATCH
            if rand_val < win_rate:
                self.player1.matches_won += 1
                self.player2.matches_lost += 1
                self.player1.match_points += 3
            else:
                self.player2.matches_won += 1
                self.player1.matches_lost += 1
                self.player2.match_points += 3
        
        self.player1.total_matches_played += 1
        self.player2.total_matches_played += 1
