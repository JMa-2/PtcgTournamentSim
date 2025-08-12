class Player:
    def __init__(self, deck, skill):
        self.deck = deck
        self.skill = skill
        self.match_points = 0
        self.opponents = []
        self.matches_won = 0
        self.matches_lost = 0
        self.matches_tied = 0
        self.total_matches_played = 0
        self.had_bye = False

    def get_win_percentage(self):
        total_matches = self.matches_won + self.matches_lost + self.matches_tied
        if total_matches == 0:
            return 0.0
        return self.matches_won / total_matches

    def get_opponent_win_percentage(self):
        if not self.opponents:
            return 0.0
        return sum(opponent.get_win_percentage() for opponent in self.opponents) / len(self.opponents)
