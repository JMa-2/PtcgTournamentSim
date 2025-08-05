import random
from player import Player
from match import Match
from tournament_logic import TournamentStructure

class Tournament:
    def __init__(self, decks, play_rates, win_rates, tie_rates, num_players, tournament_style, win_rate_format):
        self.decks = decks
        self.play_rates = play_rates
        self.win_rates = win_rates
        self.tie_rates = tie_rates
        self.num_players = num_players
        self.tournament_structure = TournamentStructure(num_players, tournament_style)
        self.win_rate_format = win_rate_format
        self.players = []
        self.top_players = []

    def simulate(self):
        self.create_players()

        # Phase 1
        for i in range(self.tournament_structure.num_phase_one_rounds):
            self.pair_round(i + 1)

        # Advance players to phase 2
        if self.tournament_structure.num_phase_two_rounds > 0:
            self.players = [p for p in self.players if p.match_points >= self.tournament_structure.phase_two_point_threshold]

            # Phase 2
            for i in range(self.tournament_structure.num_phase_two_rounds):
                self.pair_round(i + 1 + self.tournament_structure.num_phase_one_rounds)

        self.players.sort(key=lambda p: (p.match_points, p.get_opponent_win_percentage()), reverse=True)

        

        if self.tournament_structure.num_top_cut_players > 0:
            if self.tournament_structure.top_cut_format == "asymmetrical":
                top_8_points = self.players[7].match_points
                self.top_players = [p for p in self.players if p.match_points >= top_8_points]
                if len(self.top_players) > self.tournament_structure.max_asymmetrical_players:
                    self.top_players = self.players[:self.tournament_structure.max_asymmetrical_players]
            else:
                self.top_players = self.players[:self.tournament_structure.num_top_cut_players]
            winner = self.run_top_cut(self.top_players)
            return {"winner": winner.deck}
        else:
            return {"winner": self.players[0].deck}

    def create_players(self):
        self.players = []
        
        # Ensure 'Other' deck is in play_rates, even if its play_rate is 0
        if "Other" not in self.play_rates:
            self.play_rates["Other"] = 0.0

        for deck, play_rate in self.play_rates.items():
            num_players_for_deck = round(self.num_players * (play_rate / 100))
            for _ in range(num_players_for_deck):
                self.players.append(Player(deck))

        # Adjust player count to match num_players, adding "Other" for any remainder
        while len(self.players) < self.num_players:
            self.players.append(Player("Other"))
        random.shuffle(self.players)

    def pair_round(self, round_number):
        # 1. Randomize tie-breakers and sort by points
        random.shuffle(self.players)
        self.players.sort(key=lambda p: p.match_points, reverse=True)

        unpaired = list(self.players)
        pairings = []

        # 2. Handle bye for odd number of players
        if len(unpaired) % 2 != 0:
            bye_player = None
            # Give the bye to the lowest-ranked player who has not had one
            for i in range(len(unpaired) - 1, -1, -1):
                player = unpaired[i]
                if not player.had_bye:
                    bye_player = player
                    break
            if bye_player:
                bye_player.had_bye = True
                bye_player.match_points += 3
                unpaired.remove(bye_player)

        # 3. Pair players
        # Use a while loop to process unpaired players efficiently
        while len(unpaired) >= 2:
            p1 = unpaired.pop(0) # Take the highest-ranked available player

            found_opponent = False
            # Try to find a non-rematch opponent from the remaining unpaired players
            for i, p2 in enumerate(unpaired):
                if p2 not in p1.opponents:
                    pairings.append((p1, p2))
                    unpaired.pop(i) # Remove p2 from unpaired
                    found_opponent = True
                    break
            
            if not found_opponent:
                # If no non-rematch opponent found, force a rematch with the next available player.
                # This ensures all players are paired, which is crucial for the simulation.
                p2 = unpaired.pop(0) 
                pairings.append((p1, p2))

        # Execute the matches
        for p1, p2 in pairings:
            match = Match(p1, p2, self.win_rates, self.tie_rates, self.win_rate_format)
            match.simulate()
            p1.opponents.append(p2)
            p2.opponents.append(p1)

    def run_top_cut(self, top_players):
        num_players = len(top_players)
        if num_players == 1:
            return top_players[0]

        next_round_players = []
        players_to_pair = []

        # Check if the number of players is a power of two
        is_power_of_two = (num_players > 0) and (num_players & (num_players - 1) == 0)

        if is_power_of_two:
            players_to_pair = top_players
        else:
            # Asymmetrical bracket
            # Find the next smaller power of two
            p = 1
            while p * 2 < num_players:
                p *= 2
            
            num_to_eliminate = num_players - p
            num_playing = num_to_eliminate * 2
            
            num_byes = num_players - num_playing
            next_round_players.extend(top_players[:num_byes])
            players_to_pair = top_players[num_byes:]

        # Pair players for the current round (high seed vs. low seed)
        for i in range(len(players_to_pair) // 2):
            player1 = players_to_pair[i]
            player2 = players_to_pair[len(players_to_pair) - 1 - i]
            
            # Simulate a single match, not affecting overall stats
            match = Match(player1, player2, self.win_rates, self.tie_rates, self.win_rate_format)
            
            # Store previous match stats to isolate this match's result
            p1_wins_before = player1.matches_won

            match.simulate()

            if player1.matches_won > p1_wins_before:
                next_round_players.append(player1)
            else:
                next_round_players.append(player2)
        
        # Sort the winners based on their original seed to maintain ranking for the next round
        next_round_players.sort(key=lambda p: top_players.index(p))
            
        return self.run_top_cut(next_round_players)
