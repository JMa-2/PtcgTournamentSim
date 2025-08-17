import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class PlayerSkillView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.enable_skill_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self, text="Enable Player Skill", variable=self.enable_skill_var).pack()

        tk.Label(self, text="Player Skill Settings").pack()

        self.skill_entries = {}

        # Main frame
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Left frame for scrollable list
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True)

        # Create a scrollable frame
        self.canvas = tk.Canvas(left_frame)
        self.scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.canvas.yview)
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

        # Right frame for description
        right_frame = tk.Frame(main_frame, padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True)

        description_label = tk.Label(right_frame, text="About Player Skill", font=("Arial", 12, "bold"))
        description_label.pack(anchor="w")

        description_text = """The Skill Value represents the maximum impact a player's skill can have on a matchup's outcome. In any given match, the total modification to the win percentage is calculated as [Player 1's Skill - Player 2's Skill].

For each tournament simulation, the skill level of all players is randomized based on a normal distribution (bell curve), ensuring a realistic spread of player abilities."""
        
        description_message = tk.Label(right_frame, text=description_text, wraplength=300, justify=tk.LEFT)
        description_message.pack(anchor="w", pady=5)

        def update_wraplength(event):
            description_message.config(wraplength=event.width - 20)

        right_frame.bind("<Configure>", update_wraplength)

        image_path = "Images/Bell-curve.jpg"
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((450, 300), Image.Resampling.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(img)
            image_label = tk.Label(right_frame, image=self.photo_image)
            image_label.pack(anchor="w", pady=5)

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
