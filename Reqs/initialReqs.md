I want to make a tournament sim for the pokemon trading card game to aid in understanding what deck should perform best based on user inputted information. The simulator should be a python application. The application should operate in its own standalone application that can run on both windows and linux operating systems.

The application should have three main views. The user should be able to move between each view freely.

The first view should be where the user can configure the initial settings. The initial settings should contain the following:

- the deck lists to include in the simulation
- the play rate percentage of each deck list
- an option to allow tie rates to be included in the calculation
- an option to control whether BO1 (best of 1) win rates, BO3 (best of three) match win rates, or BO3 game win rates are input. BO3 game win rates allow the user to enter a deck's win rate of one game in a max of three game match. BO3 match win rates are the deck's win rate for the whole match.
- the number of players in the tournament and the ability to select from the rule appropriate tournament style based on the number of players as decribed in the rules in the Rules/ directory.




The second view should be where the user can input win rates and tie rates (if needed per user setting) for each deck's matchup. The user should have the ability to export 




The third view should be where the user can execute the simulation of the tournament and view data on the results of the simulation. The simulation should run 1000 versions of the tournament to gather what deck is most likely to win. The official tournament structure and rules must be followed and are detailed in the Rules/ directory. 

The presented data following a simulation should include things such as:

- the number of times the deck won a version of the tournament
- the overall match win rate of each deck
- the average number of match points each deck type received














Other requirements:

- the softtware shall allow the user to export and import saves of the information entered in the first and second view, allowing the user to continue for where they left off 
- the shoftware shall allow the user to export results of a simulation
- when entering the deck lists for each deck, there should always be an included deck list called "Other" that contains a play rate of (100% - [the sum of all other decks play rates])
- the sum of play rates for all included decks should never be more than 100% 
- the combined win rate and tie rate of deck's matchup should never be more than 100%
- Repeated matchups win rates should not need to be entered twice. For example, deck1 vs deck2 is identical to deck2 vs deck1, therefore only one matchup should need win rate information.