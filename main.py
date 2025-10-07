from controllers import player_controller, tournament_controller, round_controller, match_controller
import os
#from views.views import MatchView

def main():
    player_view = player_controller.PlayerView()
    tournament_view = tournament_controller.TournamentView()
    round_view = round_controller.RoundView()
    match_view = match_controller.MatchView()

    # Data containers
    players = []
    tournaments = []
    rounds = []
    matches = []

    # Initialize controllers
    player_manager = player_controller.PlayerController(players, player_view)
    tournament_manager = tournament_controller.TournamentController(tournaments, tournament_view, player_manager)          
    #tournament_manager = tournament_controller.TournamentController(tournaments, tournament_view)
    #round_manager = round_controller.RoundController(rounds, round_view) #Not used yet and here
    #match_manager = match_controller.MatchController(matches, match_view) #Not used yet and here

    # Menu loop
    while True:
        print("\n=== Chess Tournament Menu ===")
        print("1. Add a new player to the club")
        print("2. Show all players")
        print("3. Create a new tournament")
        print("4. Show tournaments")
        print("5. Manage a tournament")
        print("0. Exit")

        choice = input("Your choice: ")

        if choice == "1":
            # Add player through PlayerManagerController
            #If a player with the same name last name already exists, it will erase the oldest one
            player_manager.add_player()

        elif choice == "2":
            players = player_manager.get_all_players()
            player_manager.show_all_players(players)

        elif choice == "3":
            # Create a new tournament
            tournament_manager.create_tournament()

            #To do - Faire une boucle pour ajouter des rounds et des matchs et des joueurs

        elif choice == "4":
            # Show all tournaments
            loaded_tournaments = tournament_manager.get_all_tournaments()
            tournament_manager.show_all_tournaments(loaded_tournaments)

        elif choice == "5":
            print("\n=== Tournament Management ===")
            loaded_tournaments = tournament_manager.get_all_tournaments()

            if not loaded_tournaments:
                print("No tournaments available. Please create one first.")
            else:
                print("Available tournaments:")
                tournament_manager.show_all_tournaments_with_index(loaded_tournaments)
                try:
                    selection = int(input("Select a tournament number: "))
                    tournament = loaded_tournaments[selection - 1]
                    print(f"Selected tournament: {tournament.name}")
                    # Attach controller for this tournament
                    chosen_tournament_controller = tournament_controller.TournamentController(
                        tournament, tournament_view, player_manager
                    )
                    chosen_tournament_controller.manage_tournament(tournament)
                except (ValueError, IndexError):
                    print("Invalid choice.")
                    continue
                if not tournament:
                    print("No tournament found with that number.")
                    continue
        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
