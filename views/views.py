class TournamentView:

    def display_tournament(self, tournament):
        print("\n=== Tournament Information ===")
        print(f"Name             : {tournament.name}")
        print(f"Status           : {tournament.status}")
        print(f"Location         : {tournament.location}")
        print(f"Start date       : {tournament.start_date}")
        print(f"End date         : {tournament.end_date}")
        if tournament.players is not None:
            print(f"Registered players : {len(tournament.players)}")
        print(f"Description      : {tournament.description}")
        print("================================\n")

    def manage_player(self, tournament):
        print("\n=== Player Management ===")
        print("1. Register a player")
        print("2. Show registered players")
        print("0. Back to tournament menu")
        return input("Your choice: ")

    def ask_round_management_choice(self):
        """Display the round and match management menu."""
        print("\n--- Round & Match Management ---")
        print("1. Generate rounds and matches")
        print("2. Show all rounds")
        print("3. Show matches for a round")
        print("4. Enter match results")
        print("5. Show current standings")
        print("6. Start tournament")
        print("7. End tournament")
        print("0. Back")
        return input("Your choice: ")

    def display_tournament_simplified(self, tournament):
        return f"{tournament.name} ({tournament.status})"

    def display_players(self, tournament, players=None):
        print("\n--- List of players ---")
        if players is None:
            players = tournament.players
        for i, player in enumerate(sorted(players, key=lambda p: p.last_name), start=1):
            print(f"{i}. {player.first_name} {player.last_name} "
                  f"(National ID: {player.national_id}, Ranking: {player.ranking})")
        print("-------------------------\n")
    
    def display_matches(self, round_obj):
        """Display all matches in a round."""
        print(f"\n--- Matches for {round_obj.name} ---")
        for match in round_obj.matches:
            player1 = match.player1
            player2 = match.player2
            score1 = match.score1
            score2 = match.score2
            print("\n=== Match Information ===")
            print(f"{player1.first_name} {player1.last_name} ({score1})  vs  {player2.first_name} {player2.last_name} ({score2})")
            print("================================\n")

    def display_rounds(self, tournament):
        print("\n=== Tournament Rounds ===")
        if not tournament.rounds:
            print("No rounds available yet.")
            print("==========================\n")
            return
        for i, round_obj in enumerate(tournament.rounds, start=1):
            if isinstance(round_obj, dict):
                name = round_obj.get("name", "Unknown")
                status = round_obj.get("status", "unknown")
                start_date = round_obj.get("start_date", "N/A")
                end_date = round_obj.get("end_date") or "ongoing"
            else:
                name = round_obj.name
                status = round_obj.status
                start_date = round_obj.start_date
                end_date = round_obj.end_date or "ongoing"
            print(f"Round {i} : {name} | Status: {status} | Start: {start_date} | End: {end_date}")
        print("==========================\n")

    def display_management_menu(self, tournament):
        """Show the tournament management menu"""
        print(f"\n=== Managing Tournament: {tournament.name} ===")
        print("1. Show tournament info")
        print("2. Manage players")
        print("3. Show tournament players")
        print("4. Manage rounds")
        print("0. Back to main menu")

    def ask_management_choice(self):
        return input("Your choice: ")

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

    def display_standings(self, players):
        """Display players sorted by score and ranking."""
        print("\n=== Current Standings ===")
        for i, p in enumerate(players, start=1):
            print(f"{i}. {p.first_name} {p.last_name} "
                  f"(ID: {p.national_id}) | Score: {p.score} | Global Ranking: {p.ranking}")
        print("==========================\n")


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
        print(f"\n--- Matches for {round_obj.get('name') if isinstance(round_obj, dict) else round_obj.name} ---")
        matches = round_obj.get("matches") if isinstance(round_obj, dict) else round_obj.matches
        if not matches:
            print("No matches available yet.")
            print("-----------------------------\n")
            return

        for i, match in enumerate(matches, start=1):
            if isinstance(match, dict):
                p1 = match.get("player1", "Unknown")
                p2 = match.get("player2", "Unknown")
                s1 = match.get("score1", 0.0)
                s2 = match.get("score2", 0.0)
                print(f"{i}. {p1} ({s1}) vs {p2} ({s2})")
            else:
                p1 = match.player1
                p2 = match.player2
                print(f"{i}. {p1.first_name} {p1.last_name} ({match.score1}) vs "
                    f"{p2.first_name} {p2.last_name} ({match.score2})")

        print("-----------------------------\n")
        """if not round_obj.matches:
            print("No matches scheduled yet.")
        else:
            for i, match in enumerate(round_obj.matches, start=1):
                player1, score1 = match[0]
                player2, score2 = match[1]
                print(f"{i}. {player1.first_name} {player1.last_name} ({score1}) "
                      f"vs {player2.first_name} {player2.last_name} ({score2})")
        print("--------------------------------------\n")"""

    def ask_round_name(self):
        return input("Enter the round name (e.g., 'Round 1'): ")


class MatchView:
    """View for the Match model (console output)"""

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