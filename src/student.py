from typing import List

from src.participant import Participant

class Student(Participant):
    """A class representing the 'Student' type of Participant'."""
    
    def __init__(self, name: str, preferences: List[Participant]): 
        super(Student, self).__init__(name, preferences)
        self.placement = None
        self.__options = self.preferences[:]

    @property
    def options(self):
        return self.__options

    def place(self, school: Participant) -> None: 
        """Assigns a School to the Student."""

        if not self.placement: 
            self.placement = school
            return True
        else: 
            return False

    def displace(self, school: Participant) -> None:
        """Unassigns a School as the Student's placement.s"""

        if school == self.placement: 
            self.placement = None
            return True
        else:
            return False

    def discount(self, school: Participant) -> list:
        """Discount a school from the student's options."""
        self.__options.remove(school)
        print(self.name, [school.name for school in self.__options])