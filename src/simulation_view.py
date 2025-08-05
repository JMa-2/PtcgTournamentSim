import tkinter as tk
from tkinter import filedialog, ttk
import json
from tournament import Tournament
from tournament_logic import TournamentStructure
import datetime

class SimulationView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Simulation View").pack()

        self.run_button = tk.Button(self, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack()

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack()

        self.results_text = tk.Text(self)
        self.results_text.pack(fill=tk.BOTH, expand=True)

        tk.Button(self, text="Export Results", command=self.export_results).pack()

    def run_simulation(self):
        self.run_button.config(text="Running...", state=tk.DISABLED)
        self.update_idletasks() # Update the UI immediately

        num_players = int(self.master.master.configuration_view.num_players_entry.get())
        tournament_style = self.master.master.configuration_view.tournament_style_var.get()
        play_rates = {entry[0].get(): float(entry[1].get()) for entry in self.master.master.configuration_view.deck_entries}
        num_simulations = int(self.master.master.configuration_view.num_simulations_var.get())

        self.tournament_wins = {deck: 0 for deck in self.master.master.decks}
        self.top_cuts = {deck: 0 for deck in self.master.master.decks}
        self.total_match_wins = {deck: 0 for deck in self.master.master.decks}
        self.total_match_points = {deck: 0 for deck in self.master.master.decks}
        self.total_matches_played = {deck: 0 for deck in self.master.master.decks}

        self.progress_bar["maximum"] = num_simulations
        
        actual_deck_player_counts = {deck: 0 for deck in self.master.master.decks}

        for i in range(num_simulations):
            tournament = Tournament(self.master.master.decks, play_rates, self.master.master.win_rates, self.master.master.tie_rates, num_players, tournament_style, self.master.master.win_rate_format)
            results = tournament.simulate()
            self.tournament_wins[results['winner']] += 1

            if tournament.tournament_structure.num_top_cut_players > 0:
                for player in tournament.top_players:
                    self.top_cuts[player.deck] += 1

            if i == 0:
                for player in tournament.players:
                    actual_deck_player_counts[player.deck] += 1

            for player in tournament.players:
                self.total_match_wins[player.deck] += player.matches_won
                self.total_match_points[player.deck] += player.match_points
                self.total_matches_played[player.deck] += player.total_matches_played
            
            self.progress_bar["value"] = i + 1
            self.update_idletasks()

        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, f"Tournament Results ({num_simulations} simulations):\n\n")

        sorted_decks = sorted(self.master.master.decks, key=lambda deck: self.tournament_wins[deck], reverse=True)

        for deck in sorted_decks:
            self.results_text.insert(tk.END, f"Deck: {deck}\n")
            self.results_text.insert(tk.END, f"  Tournament Wins: {self.tournament_wins[deck]}\n")
            total_deck_instances = num_simulations * actual_deck_player_counts[deck]
            if total_deck_instances > 0:
                top_cut_conversion_rate = (self.top_cuts[deck] / total_deck_instances) * 100
                self.results_text.insert(tk.END, f"  Top Cut Conversion Rate: {top_cut_conversion_rate:.2f}%\n\n")
            else:
                self.results_text.insert(tk.END, f"  Top Cut Conversion Rate: 0.00%\n\n")
        
        self.results_text.insert(tk.END, "\n--- Simulation Configuration ---\n")
        self.results_text.insert(tk.END, f"Number of Players: {num_players}\n")
        self.results_text.insert(tk.END, f"Tournament Style: {tournament_style}\n")
        self.results_text.insert(tk.END, f"Number of Simulations: {num_simulations}\n")
        self.results_text.insert(tk.END, f"Win Rate Format: {self.master.master.win_rate_format}\n")
        self.results_text.insert(tk.END, "\nDeck Play Rates:\n")
        other_play_rate = 100 - sum(play_rates.values())
        play_rates["Other"] = other_play_rate
        for deck, rate in play_rates.items():
            self.results_text.insert(tk.END, f"  {deck}: {rate}%\n")

        self.run_button.config(text="Run Simulation", state=tk.NORMAL)


    

# ... (rest of the file)

    def export_results(self):
        now = datetime.datetime.now()
        default_filename = f"results_{now.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialfile=default_filename)
        if not filepath:
            return

        results = {
            "tournament_wins": self.tournament_wins,
            "total_match_wins": self.total_match_wins,
            "total_match_points": self.total_match_points
        }

        with open(filepath, 'w') as f:
            json.dump(results, f, indent=4)