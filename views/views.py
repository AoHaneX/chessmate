class TournamentView:

    def display_tournament(self, tournament):
        print("\n=== Tournament Information ===")
        print(f"Name             : {tournament.name}")
        print(f"Status           : {tournament.status}")
        print(f"Location         : {tournament.location}")
        print(f"Start date       : {tournament.start_date}")
        print(f"End date         : {tournament.end_date}")
        print(f"Number of rounds : {tournament.number_of_rounds}")
        print(f"Current round    : {tournament.current_round}")
        if tournament.players is not None:
            print(f"Registered players : {len(tournament.players)}")
        print(f"Description      : {tournament.description}")
        print("================================\n")

    def display_players(self, tournament):
        print("\n--- List of players ---")
        for i, player in enumerate(sorted(tournament.players, key=lambda p: p.last_name), start=1):
            print(f"{i}. {player.first_name} {player.last_name} "
                  f"(National ID: {player.national_id}, Ranking: {player.ranking})")
        print("-------------------------\n")

    def display_rounds(self, tournament):
        print("\n=== Tournament Rounds ===")
        for i, round_obj in enumerate(tournament.rounds, start=1):
            print(f"Round {i} : {round_obj.name} "
                  f"| Status: {round_obj.status} "
                  f"| Start: {round_obj.start_date} "
                  f"| End: {round_obj.end_date if round_obj.end_date else 'ongoing'}")
        print("==========================\n")

    def ask_tournament_name(self):
        return input("Enter the tournament name: ")

    def ask_tournament_location(self):
        return input("Enter the tournament location: ")

    def ask_start_date(self):
        return input("Enter the tournament start date (DD/MM/YYYY): ")

    def ask_end_date(self):
        return input("Enter the tournament end date (DD/MM/YYYY): ")

    def ask_description(self):
        return input("Enter a description for the tournament: ")
    
    def ask_round(self):
        
        return input("Enter the number of rounds for the tournament: ")
    
    
class RoundView:

    def display_round(self, round_obj):
        print("\n=== Round Information ===")
        print(f"Name       : {round_obj.name}")
        print(f"Status     : {round_obj.status}")
        print(f"Start date : {round_obj.start_date}")
        print(f"End date   : {round_obj.end_date if round_obj.end_date else 'ongoing'}")
        print(f"Number of matches : {len(round_obj.matches)}")
        print("================================\n")

    def display_matches(self, round_obj):
        print(f"\n--- Matches for {round_obj.name} ---")
        if not round_obj.matches:
            print("No matches scheduled yet.")
        else:
            for i, match in enumerate(round_obj.matches, start=1):
                player1, score1 = match[0]
                player2, score2 = match[1]
                print(f"{i}. {player1.first_name} {player1.last_name} ({score1}) "
                      f"vs {player2.first_name} {player2.last_name} ({score2})")
        print("--------------------------------------\n")

    def ask_round_name(self):
        return input("Enter the round name (e.g., 'Round 1'): ")
    
class MatchView:
    """View for the Match model (console output)"""

    def display_match(self, match):
        player1, score1 = match[0]
        player2, score2 = match[1]
        print("\n=== Match Information ===")
        print(f"{player1.first_name} {player1.last_name} ({score1}) "
              f"vs {player2.first_name} {player2.last_name} ({score2})")
        print("================================\n")

    def ask_match_result(self, match):
        player1, _ = match[0]
        player2, _ = match[1]

        print(f"\nEnter the result for the match: "
              f"{player1.first_name} {player1.last_name} vs {player2.first_name} {player2.last_name}")
        print("Options: 1 = Player 1 wins, 2 = Player 2 wins, 0 = Draw")

        while True:
            result = input("Your choice: ")
            if result == "1":
                return 1.0, 0.0
            elif result == "2":
                return 0.0, 1.0
            elif result == "0":
                return 0.5, 0.5
            else:
                print("Invalid choice. Please enter 1, 2, or 0.")

    def display_match_result(self, match):
        player1, score1 = match[0]
        player2, score2 = match[1]
        print("\n--- Match Result ---")
        print(f"{player1.first_name} {player1.last_name}: {score1} point(s)")
        print(f"{player2.first_name} {player2.last_name}: {score2} point(s)")
        print("---------------------\n")
        
class PlayerView:

    def display_player(self, player):
        print("\n=== Player Information ===")
        print(f"Name         : {player.first_name} {player.last_name}")
        print(f"Birth date   : {player.birth_date}")
        print(f"National ID  : {player.national_id}")
        print(f"Ranking      : {player.ranking}")
        print("================================\n")

    def display_all_players(self, players):
        print("\n--- List of players (alphabetical order) ---")
        for i, player in enumerate(sorted(players, key=lambda p: (p.last_name, p.first_name)), start=1):
            print(f"{i}. {player.first_name} {player.last_name} "
                  f"(National ID: {player.national_id}, Ranking: {player.ranking})")
        print("------------------------------------------------\n")

    def ask_first_name(self):
        return input("Enter the player's first name: ")

    def ask_last_name(self):
        return input("Enter the player's last name: ")

    def ask_birth_date(self):
        return input("Enter the player's birth date (DD/MM/YYYY): ")

    def ask_national_id(self):
        return input("Enter the player's national chess ID (e.g., AB12345): ")

    def ask_ranking(self):
        while True:
            try:
                return int(input("Enter the player's ranking (integer): "))
            except ValueError:
                print("Invalid input. Please enter a number.")