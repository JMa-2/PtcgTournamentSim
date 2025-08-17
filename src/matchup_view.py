import tkinter as tk
from tkinter import ttk

class MatchupView(tk.Frame):
    def __init__(self, master, version_number):
        super().__init__(master)

        tk.Label(self, text="Matchup View").pack()

        # Create a scrollable frame
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.win_rate_entries = {}
        self.tie_rate_entries = {}

        # Add version label
        version_label = tk.Label(self, text=version_number, anchor="se")
        version_label.pack(side="bottom", fill="x")

    def update_grid(self, decks, win_rates, tie_rates):
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.win_rate_entries = {}
        self.tie_rate_entries = {}

        # Header
        tk.Label(self.scrollable_frame, text="Deck 1").grid(row=0, column=0, padx=30)
        tk.Label(self.scrollable_frame, text="Deck 2").grid(row=0, column=1, padx=30)
        tk.Label(self.scrollable_frame, text="Deck 1's Win Rate (%)").grid(row=0, column=2, padx=30)
        tk.Label(self.scrollable_frame, text="Tie Rate (%)").grid(row=0, column=3, padx=30)

        # Create new list
        row = 1
        for i, deck1 in enumerate(decks):
            for j, deck2 in enumerate(decks):
                if i <= j:
                    tk.Label(self.scrollable_frame, text=deck1).grid(row=row, column=0, padx=30)
                    tk.Label(self.scrollable_frame, text=deck2).grid(row=row, column=1, padx=30)

                    # Win Rate Entry
                    win_entry = tk.Entry(self.scrollable_frame, width=10)
                    win_entry.grid(row=row, column=2, padx=30)
                    self.win_rate_entries[(deck1, deck2)] = win_entry
                    if (deck1, deck2) in win_rates:
                        win_entry.insert(0, str(win_rates.get((deck1, deck2), 0.0) * 100))
                    elif deck1 == deck2 and not self.master.master.configuration_view.ties_var.get():
                        win_entry.insert(0, "50")
                        win_entry.config(state=tk.DISABLED)

                    # Tie Rate Entry
                    tie_entry = tk.Entry(self.scrollable_frame, width=10)
                    tie_entry.grid(row=row, column=3, padx=30)
                    self.tie_rate_entries[(deck1, deck2)] = tie_entry
                    if (deck1, deck2) in tie_rates:
                        tie_entry.insert(0, str(tie_rates.get((deck1, deck2), 0.0) * 100))
                    if not self.master.master.configuration_view.ties_var.get():
                        tie_entry.config(state=tk.DISABLED)

                    row += 1

    def get_matchup_data(self):
        win_rates = {}
        tie_rates = {}
        for (deck1, deck2), entry in self.win_rate_entries.items():
            try:
                win_rate = float(entry.get()) / 100.0
            except ValueError:
                win_rate = 0.0
            win_rates[(deck1, deck2)] = win_rate

            # Get tie rate for the current matchup
            try:
                tie_rate = float(self.tie_rate_entries[(deck1, deck2)].get()) / 100.0
            except ValueError:
                tie_rate = 0.0
            tie_rates[(deck1, deck2)] = tie_rate

            # Populate inverse matchup if decks are different
            if deck1 != deck2:
                win_rates[(deck2, deck1)] = 1.0 - win_rate - tie_rate
                tie_rates[(deck2, deck1)] = tie_rate
        return win_rates, tie_rates
