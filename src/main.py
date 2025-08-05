
import tkinter as tk
from tkinter import font
from configuration_view import ConfigurationView
from matchup_view import MatchupView
from simulation_view import SimulationView

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pokémon TCG Tournament Simulator")
        self.geometry("1024x768")

        # Set a larger default font
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=12)

        self.decks = []
        self.win_rates = {}
        self.tie_rates = {}
        self.num_simulations = 1000 # Default value
        print(f"DEBUG: App instance ID: {id(self)}")

        # Header
        header_frame = tk.Frame(self)
        header_frame.pack(fill=tk.X)

        self.config_button = tk.Button(header_frame, text="Configuration", command=self.show_configuration_view)
        self.config_button.pack(side=tk.LEFT)
        self.matchup_button = tk.Button(header_frame, text="Matchups", command=self.show_matchup_view)
        self.matchup_button.pack(side=tk.LEFT)
        self.sim_button = tk.Button(header_frame, text="Simulation", command=self.show_simulation_view)
        self.sim_button.pack(side=tk.LEFT)
        tk.Button(header_frame, text="Import Config", command=lambda: self.configuration_view.import_config()).pack(side=tk.LEFT)
        tk.Button(header_frame, text="Export Config", command=lambda: self.configuration_view.export_config()).pack(side=tk.LEFT)

        # Main content area
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.configuration_view = ConfigurationView(self.main_frame)
        self.matchup_view = MatchupView(self.main_frame)
        self.simulation_view = SimulationView(self.main_frame)

        self.show_configuration_view()

    def show_configuration_view(self):
        self.matchup_view.pack_forget()
        self.simulation_view.pack_forget()
        self.configuration_view.pack(fill=tk.BOTH, expand=True)
        self.config_button.config(state=tk.DISABLED)
        self.matchup_button.config(state=tk.NORMAL)
        self.sim_button.config(state=tk.NORMAL)

    def show_matchup_view(self):
        self.update_matchup_data()
        self.configuration_view.pack_forget()
        self.simulation_view.pack_forget()
        self.matchup_view.pack(fill=tk.BOTH, expand=True)
        self.config_button.config(state=tk.NORMAL)
        self.matchup_button.config(state=tk.DISABLED)
        self.sim_button.config(state=tk.NORMAL)

    def update_matchup_data(self):
        self.decks = [entry[0].get() for entry in self.configuration_view.deck_entries]
        self.decks.append("Other")
        self.matchup_view.update_grid(self.decks, self.win_rates, self.tie_rates)

    def show_simulation_view(self):
        self.win_rates, self.tie_rates = self.matchup_view.get_matchup_data()
        self.win_rate_format = self.configuration_view.win_rate_format_var.get()
        self.configuration_view.pack_forget()
        self.matchup_view.pack_forget()
        self.simulation_view.pack(fill=tk.BOTH, expand=True)
        self.config_button.config(state=tk.NORMAL)
        self.matchup_button.config(state=tk.NORMAL)
        self.sim_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = App()
    app.mainloop()
