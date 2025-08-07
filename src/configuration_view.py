import tkinter as tk
from tkinter import filedialog, ttk
import json
import datetime
from tournament_logic import TournamentStructure, FORMAT_TYPES

import datetime

class ConfigurationView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left column (Decks)
        self.deck_frame = tk.Frame(main_frame)
        self.deck_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Button(self.deck_frame, text="Add Deck", command=lambda: self.add_deck_entry(self.deck_list_frame)).pack()

        # Create a scrollable frame for the deck list
        canvas = tk.Canvas(self.deck_frame)
        scrollbar = ttk.Scrollbar(self.deck_frame, orient="vertical", command=canvas.yview)
        self.deck_list_frame = ttk.Frame(canvas)

        self.deck_list_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.deck_list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")


        tk.Label(self.deck_list_frame, text="Decks").grid(row=0, column=0)
        tk.Label(self.deck_list_frame, text="Play Rate (%)").grid(row=0, column=1)

        self.deck_entries = []
        self.add_deck_entry(self.deck_list_frame)

        self.other_play_rate_label = tk.Label(self.deck_list_frame, text="Other: 100.0%")
        self.other_play_rate_label.grid(row=99, column=0, columnspan=2)

        # Right column (Options)
        options_frame = tk.Frame(main_frame)
        options_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.ties_var = tk.BooleanVar()
        tk.Checkbutton(options_frame, text="Allow Ties", variable=self.ties_var, command=self.toggle_ties).pack()

        self.win_rate_format_var = tk.StringVar(value="BO1")
        tk.Radiobutton(options_frame, text="BO1 Win Rates", variable=self.win_rate_format_var, value="BO1").pack()
        bo3_match_radio = tk.Radiobutton(options_frame, text="BO3 Match Win Rates", variable=self.win_rate_format_var, value="BO3_MATCH")
        bo3_match_radio.pack()
        self.create_tooltip(bo3_match_radio, "The deck's win rate for the whole match.")

        bo3_game_radio = tk.Radiobutton(options_frame, text="BO3 Game Win Rates", variable=self.win_rate_format_var, value="BO3_GAME")
        bo3_game_radio.pack()
        self.create_tooltip(bo3_game_radio, "The deck's win rate of one game in a max of three game match.")

        tk.Label(options_frame, text="Number of Players").pack()
        self.num_players_entry = tk.Entry(options_frame)
        self.num_players_entry.pack()

        tk.Label(options_frame, text="Tournament Style").pack()
        self.tournament_style_var = tk.StringVar(value=FORMAT_TYPES[0])
        self.tournament_style_menu = tk.OptionMenu(options_frame, self.tournament_style_var, *FORMAT_TYPES)
        self.tournament_style_menu.pack()

        tk.Label(options_frame, text="Number of Simulations").pack()
        self.num_simulations_var = tk.StringVar(value="1000") # Default to 1000
        self.num_simulations_menu = tk.OptionMenu(options_frame, self.num_simulations_var, "1000", "5000", "10000")
        self.num_simulations_menu.pack()

    def toggle_ties(self):
        self.master.master.update_matchup_data()

    def add_deck_entry(self, parent):
        row = len(self.deck_entries) + 1

        deck_name_entry = tk.Entry(parent)
        deck_name_entry.grid(row=row, column=0)

        play_rate_entry = tk.Entry(parent)
        play_rate_entry.grid(row=row, column=1)
        play_rate_entry.bind("<KeyRelease>", self.update_other_play_rate)

        delete_button = tk.Button(parent, text="X", command=lambda: self.delete_deck_entry(row - 1))
        delete_button.grid(row=row, column=2)

        self.deck_entries.append((deck_name_entry, play_rate_entry, delete_button))

    def delete_deck_entry(self, index):
        deck_name_entry, play_rate_entry, delete_button = self.deck_entries.pop(index)
        deck_name_entry.destroy()
        play_rate_entry.destroy()
        delete_button.destroy()
        self.update_other_play_rate()

    def update_other_play_rate(self, event=None):
        total_play_rate = 0
        for _, play_rate_entry, _ in self.deck_entries:
            try:
                total_play_rate += float(play_rate_entry.get())
            except ValueError:
                pass

        other_play_rate = 100 - total_play_rate
        self.other_play_rate_label.config(text=f"Other: {other_play_rate:.1f}%")

    

    def import_config(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not filepath:
            return

        with open(filepath, 'r') as f:
            config = json.load(f)

        # Clear existing deck entries
        for widget in self.deck_list_frame.winfo_children():
            widget.destroy()
        self.deck_entries = []

        # Re-grid initial labels
        tk.Label(self.deck_list_frame, text="Decks").grid(row=0, column=0)
        tk.Label(self.deck_list_frame, text="Play Rate (%)").grid(row=0, column=1)

        # Load new deck entries
        for deck_info in config["decks"]:
            self.add_deck_entry(self.deck_list_frame)
            deck_name_entry, play_rate_entry, _ = self.deck_entries[-1]
            deck_name_entry.insert(0, deck_info["name"])
            play_rate_entry.insert(0, deck_info["play_rate"])

        self.ties_var.set(config["allow_ties"])
        self.win_rate_format_var.set(config["win_rate_format"])
        self.num_players_entry.delete(0, tk.END)
        self.num_players_entry.insert(0, config["num_players"])
        self.tournament_style_var.set(config["tournament_style"])
        self.num_simulations_var.set(config.get("num_simulations", "1000")) # Load with default if not present
        loaded_win_rates = config["win_rates"]
        converted_win_rates = {}
        for key, value in loaded_win_rates.items():
            deck1, deck2 = key.split('_', 1)
            converted_win_rates[(deck1, deck2)] = value
        self.master.master.win_rates = converted_win_rates

        loaded_tie_rates = config.get("tie_rates", {})
        converted_tie_rates = {}
        for key, value in loaded_tie_rates.items():
            deck1, deck2 = key.split('_', 1)
            converted_tie_rates[(deck1, deck2)] = value
        self.master.master.tie_rates = converted_tie_rates

        self.other_play_rate_label = tk.Label(self.deck_list_frame, text="Other: 100.0%")
        self.other_play_rate_label.grid(row=99, column=0, columnspan=2)
        self.update_other_play_rate()

    def export_config(self):
        self.master.master.win_rates, self.master.master.tie_rates = self.master.master.matchup_view.get_matchup_data()
        now = datetime.datetime.now()
        default_filename = f"config_{now.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialfile=default_filename)
        if not filepath:
            return

        converted_win_rates = {}
        for (d1, d2), rate in self.master.master.win_rates.items():
            converted_win_rates[f"{d1}_{d2}"] = rate
        
        converted_tie_rates = {}
        for (d1, d2), rate in self.master.master.tie_rates.items():
            converted_tie_rates[f"{d1}_{d2}"] = rate

        config = {
            "decks": [],
            "allow_ties": self.ties_var.get(),
            "win_rate_format": self.win_rate_format_var.get(),
            "num_players": int(self.num_players_entry.get()),
            "tournament_style": self.tournament_style_var.get(),
            "num_simulations": int(self.num_simulations_var.get()),
            "win_rates": converted_win_rates,
            "tie_rates": converted_tie_rates
        }

        for deck_name_entry, play_rate_entry, _ in self.deck_entries:
            config["decks"].append({
                "name": deck_name_entry.get(),
                "play_rate": float(play_rate_entry.get())
            })

        with open(filepath, 'w') as f:
            json.dump(config, f, indent=4)

    def create_tooltip(self, widget, text):
        tool_tip = ToolTip(widget, text)
        widget.bind("<Enter>", tool_tip.showtip)
        widget.bind("<Leave>", tool_tip.hidetip)

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

    def showtip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self, event):
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None
