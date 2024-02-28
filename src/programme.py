from typing import List

from src.school import School
from src.student import Student


class Programme: 
    """Class representing the Programme matching Participants."""    
       
    def __init__(self, students: List[Student], schools: List[School]):
        self.students = students
        self.schools = schools
        self.pending = self.students[:]

    def qualify_match(self, student: Student, school: School) -> bool | str:
        """"Validate a proposed match between a Student and School."""

        if not student.preference_match(school): 
            return False

        if (school.is_final) or (school.is_full and not school.prefers(student)): 
            return False
       
        if school.highest_ranking_candidate == student: 
            return 'final'
        
        return 'tentative'

    def match(
        self, student: Student, school: School, match_type: str='tentative'
    ) -> None: 
        """Matches a Student and a School."""

        if school.is_full and not school.is_final and school.prefers(student):
            self.unmatch(school.lowest_ranked_placement, school)

        student.place(school)
        school.place(student, match_type)

    def unmatch(self, student: Student, school: School) -> None:
        """Unmatches a Student and a School."""

        self.pending.append(student)
        student.displace(school)
        school.displace(student)
 
    def run(self) -> None:
        """"""

        while self.pending:              
            student = self.pending.pop(0)
            while student.options: 
                school = student.options[0]
                match_type = self.qualify_match(student, school)
                if match_type:
                    self.match(student, school, match_type) 
                    break
                else:
                    student.discount(school)

