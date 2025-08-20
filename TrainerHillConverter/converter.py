import csv
import json
import argparse
import math
from datetime import datetime

def convert_trainerhill_to_ptcg_sim(input_csv_path, output_json_path):
    decks = set()
    win_rates = {}

    with open(input_csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            deck1, deck2, _, _, _, _, win_rate_str = row
            decks.add(deck1)
            decks.add(deck2)
            
            key = f"{deck1.replace('-', ' ')}_{deck2.replace('-', ' ')}"
            if win_rate_str == '':
                win_rate_str = '50.0'
            win_rates[key] = float(win_rate_str) / 100.0

    deck_list = sorted(list(decks))
    num_decks = len(deck_list)
    play_rate = math.floor(100.0 / num_decks) if num_decks > 0 else 0

    output_data = {
        "decks": [{"name": deck.replace('-', ' '), "play_rate": play_rate} for deck in deck_list],
        "allow_ties": False,
        "win_rate_format": "BO3_GAME",
        "num_players": 1000,
        "tournament_style": "CHAMPIONSHIP_FORMAT",
        "num_simulations": 10000,
        "win_rates": {f"{d1.replace('-', ' ')}_{d2.replace('-', ' ')}": win_rates.get(f"{d1.replace('-', ' ')}_{d2.replace('-', ' ')}", 0.5) for d1 in deck_list for d2 in deck_list},
        "tie_rates": {f"{d1.replace('-', ' ')}_{d2.replace('-', ' ')}": 0 for d1 in deck_list for d2 in deck_list},
        "skill_values": {deck.replace('-', ' '): 0 for deck in deck_list},
        "enable_skill": False
    }

    with open(output_json_path, 'w') as jsonfile:
        json.dump(output_data, jsonfile, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert TrainerHill CSV to PtcgTournamentSim JSON format.')
    parser.add_argument('input_file', type=str, help='The path to the input CSV file.')
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'/home/jmaier/Documents/Gits/PtcgTournamentSim/TrainerHillConverter/converted_trainerhill_data_{timestamp}.json'
    convert_trainerhill_to_ptcg_sim(args.input_file, output_file)