from src.participant import Participant

class School(Participant):
    """A class representing the 'School' type of Participant.""" 
        
    def __init__(self, name: str, preferences: list, max_placements: int): 
        super(School, self).__init__(name, preferences)
        self.max_placements = max_placements
        self.__placements = {}

    @property
    def placements(self) -> dict:
        return self.__placements

    def __get_placements_of_type(self, placement_type: str) -> list:
        return [
            student for student, p_type in self.__placements.items()
            if p_type == placement_type
        ]

    @property
    def is_full(self) -> bool:
        return len(self.__placements) == self.max_placements

    @property
    def is_final(self) -> bool:
        return (
            len(self.__get_placements_of_type('final')) == 
            self.max_placements
        )

    def place(self, student: Participant, placement_type: str):
        """Assign a Student to the School's placements."""
        self.__placements[student] = placement_type
        return True

    def displace(self, student: Participant):
        """Removes a Student from the School's placements."""
        del(self.__placements[student])
        return True

    @property
    def lowest_ranked_placement(self): 
        """Returns the lowest ranked tentatively placed Student."""

        ranks = [
            self.preferences.index(student) 
            for student in self.__get_placements_of_type('tentative')
        ]
        
        lowest_ranking = max(ranks)
        return self.preferences[lowest_ranking]

    @property
    def highest_ranking_candidate(self):
        """Return the highest ranked tentatively matched / unmatched Student."""
        
        unplaced_candidates = [
            candidate for candidate in self.preferences 
            if candidate not in self.__placements.keys() or 
            self.__placements[candidate] != 'final'
        ]
  
        return unplaced_candidates[0]
        
    def prefers(self, student: Participant):
        """"""

        if (
            self.preferences.index(student) < 
            self.preferences.index(self.lowest_ranked_placement)
        ): 
            return True
        return False
