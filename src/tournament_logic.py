SWISS_ROUND_FORMAT = "SWISS ROUNDS ONLY"
SINGLE_DAY_FORMAT = "SINGLE DAY"
CHAMPIONSHIP_FORMAT = "CHAMPIONSHIP FORMAT"
FORMAT_TYPES = [SWISS_ROUND_FORMAT, SINGLE_DAY_FORMAT, CHAMPIONSHIP_FORMAT]

class TournamentStructure:
    def __init__(self, num_players, format):
        self.num_players = num_players

        if format not in FORMAT_TYPES:
            self.format = SWISS_ROUND_FORMAT
        else:
            self.format = format

        self.num_phase_one_rounds = get_phase_one_round_count(self.num_players, self.format)
        self.phase_two_point_threshold = get_phase_two_point_threshold(self.num_players, self.format)
        self.num_phase_two_rounds = get_phase_two_round_count(self.num_players, self.format)
        self.num_top_cut_players = get_top_cut_num_players(self.num_players, self.format)
        self.top_cut_format = get_top_cut_format(self.num_players, self.format)
        self.max_asymmetrical_players = get_max_asymmetrical_players(self.num_players, self.format)


# numbers are pull directly from pokemon tcg rulebook
def get_phase_one_round_count(num_players, format):
    round_count = 0

    if format == SWISS_ROUND_FORMAT:
        if num_players <= 8:
            round_count = 3
        elif num_players <= 16:
            round_count = 4
        elif num_players <= 32:
            round_count = 5
        elif num_players <= 64:
            round_count = 6
        elif num_players <= 128:
            round_count = 7
        elif num_players <= 256:
            round_count = 8
        elif num_players <= 512:
            round_count = 9
        elif num_players > 512:
            round_count = 10

    elif format == SINGLE_DAY_FORMAT:
        if num_players <= 8:
            round_count = 3
        elif num_players <= 12:
            round_count = 4
        elif num_players <= 20:
            round_count = 5
        elif num_players <= 32:
            round_count = 5
        elif num_players <= 64:
            round_count = 6
        elif num_players <= 128:
            round_count = 7
        elif num_players <= 226:
            round_count = 8
        elif num_players <= 409:
            round_count = 9
        elif num_players > 490:
            round_count = 10

    elif format == CHAMPIONSHIP_FORMAT:
        if num_players <= 8:
            round_count = 3
        elif num_players <= 16:
            round_count = 4
        elif num_players <= 32:
            round_count = 6
        elif num_players <= 64:
            round_count = 7
        elif num_players <= 128:
            round_count = 6
        elif num_players <= 256:
            round_count = 7
        elif num_players <= 512:
            round_count = 8
        elif num_players <= 1024:
            round_count = 8
        elif num_players <= 2048:
            round_count = 8
        elif num_players <= 4096:
            round_count = 9
        elif num_players <= 8192:
            round_count = 9
    
    return round_count


def get_phase_two_point_threshold(num_players, format):
    point_threshold = 0

    if format == CHAMPIONSHIP_FORMAT:
        if num_players <= 64:
            point_threshold = 0
        elif num_players <= 128:
            point_threshold = 10
        elif num_players <= 256:
            point_threshold = 13
        elif num_players <= 512:
            point_threshold = 16
        elif num_players <= 1024:
            point_threshold = 16
        elif num_players <= 2048:
            point_threshold = 16
        elif num_players <= 4096:
            point_threshold = 19
        elif num_players <= 8192:
            point_threshold = 19

    return point_threshold

def get_phase_two_round_count(num_players, format):
    round_count = 0

    if format == CHAMPIONSHIP_FORMAT:
        if num_players <= 64:
            round_count = 0
        elif num_players <= 128:
            round_count = 2
        elif num_players <= 256:
            round_count = 2
        elif num_players <= 512:
            round_count = 2
        elif num_players <= 1024:
            round_count = 3
        elif num_players <= 2048:
            round_count = 4
        elif num_players <= 4096:
            round_count = 4
        elif num_players <= 8192:
            round_count = 5
    
    return round_count


def get_top_cut_num_players(num_players, format):
    top_cut_players = 0

    if format == SINGLE_DAY_FORMAT:
        if num_players <= 8:
            top_cut_players = 0
        elif num_players <= 12:
            top_cut_players = 4
        elif num_players <= 20:
            top_cut_players = 4
        elif num_players <= 32:
            top_cut_players = 4
        elif num_players <= 64:
            top_cut_players = 8
        elif num_players <= 128:
            top_cut_players = 8
        elif num_players <= 226:
            top_cut_players = 8
        elif num_players <= 409:
            top_cut_players = 8
        elif num_players > 490:
            top_cut_players = 8

    elif format == CHAMPIONSHIP_FORMAT:
        if num_players <= 8:
            top_cut_players = 0
        elif num_players <= 16:
            top_cut_players = 4
        elif num_players <= 32:
            top_cut_players = 4
        elif num_players <= 64:
            top_cut_players = 6
        elif num_players <= 128:
            top_cut_players = 8
        elif num_players <= 256:
            top_cut_players = 8
        elif num_players <= 512:
            top_cut_players = 8
        elif num_players <= 1024:
            top_cut_players = 8
        elif num_players <= 2048:
            top_cut_players = 8
        elif num_players <= 4096:
            top_cut_players = 8
        elif num_players <= 8192:
            top_cut_players = 8

    return top_cut_players


def get_top_cut_format(num_players, format):
    top_cut_format = "symmetrical"

    if (format == CHAMPIONSHIP_FORMAT) and (num_players > 8):
        top_cut_format = "asymmetrical"

    return top_cut_format


def get_max_asymmetrical_players(num_players, format):
    max_players = 0

    if format == CHAMPIONSHIP_FORMAT:
        if num_players > 8:
            max_players = 32

    return max_players
