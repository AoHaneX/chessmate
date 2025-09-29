from models import match_model
from views.views import MatchView

class MatchController:

    def __init__(self, match, view):
        self.match = match
        self.view = view

    def set_result(self):
        """Ask user to enter the result of the match and update scores"""
        score1, score2 = self.view.ask_match_result((self.match.player1, self.match.player2))
        self.match.set_result(score1, score2)

    def show_match(self):
        """Display match info and result"""
        self.view.display_match(self.match)
        self.view.display_match_result((self.match.player1, self.match.player2))
