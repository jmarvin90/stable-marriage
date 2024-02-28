from __future__ import annotations

class Participant:
    """A class to represent a Participant to be matched by the Programme"""
            
    def __init__(self, name: str, preferences: list):
        self.name = name
        self.preferences = preferences

    def preference_match(self, counterparty: Participant):
        """"""

        if ((counterparty in self.preferences) and 
            (self in counterparty.preferences)): 
            
            return True
        else:
            return False

    def strikethrough(self):
        """Returns the Participant's name in strikethrough font"""

        strikethrough = ''
        for c in self.name: 
            strikethrough += c + '\u0336'