from models import match_model
from views.views import MatchView

class MatchController:

    def __init__(self, player, view):
        self.player = player
        self.view = view
        
    def set_result(self, score1, score2):
        """Ask user to enter the result of the match and update scores"""
        self.score1 = score1
        self.score2 = score2

    def show_match(self):
        """Display match info and result"""
        self.view.display_match(self.match)
        self.view.display_match_result((self.match.player1, self.match.player2))
    
    def set_scores(self, score1, score2):
        self.players[0][1] = score1
        self.players[1][1] = score2
        
    def get_result(self):
        """Return the result as a tuple of (player, score)."""
        return ([self.player1, self.score1], [self.player2, self.score2])