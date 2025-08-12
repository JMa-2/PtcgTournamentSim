import tkinter as tk
from tkinter import ttk

class PlayerSkillView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.enable_skill_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self, text="Enable Player Skill", variable=self.enable_skill_var).pack()

        tk.Label(self, text="Player Skill Settings").pack()

        self.skill_entries = {}

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

    def update_deck_list(self, decks):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.skill_entries = {}

        tk.Label(self.scrollable_frame, text="Deck").grid(row=0, column=0, padx=10)
        tk.Label(self.scrollable_frame, text="Skill Value (%)").grid(row=0, column=1, padx=10)

        for i, deck in enumerate(decks):
            tk.Label(self.scrollable_frame, text=deck).grid(row=i + 1, column=0, padx=10)
            skill_entry = tk.Entry(self.scrollable_frame, width=10)
            skill_entry.grid(row=i + 1, column=1, padx=10)
            self.skill_entries[deck] = skill_entry

    def get_skill_values(self):
        if not self.enable_skill_var.get():
            return {}
            
        skill_values = {}
        for deck, entry in self.skill_entries.items():
            try:
                skill_values[deck] = float(entry.get())
            except ValueError:
                skill_values[deck] = 0.0
        return skill_values

    def set_skill_values(self, skill_values):
        for deck, value in skill_values.items():
            if deck in self.skill_entries:
                self.skill_entries[deck].delete(0, tk.END)
                self.skill_entries[deck].insert(0, str(value))
