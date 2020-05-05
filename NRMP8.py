class Participant:
    def __init__(self, name, preferences):
        self.name = name 
        self.preferences = preferences

    def preference_match(self, counterparty):
        """Returns True where the participant is in the counterparty's 
        preferences and vice versa
        """

        if ((counterparty in self.preferences) and 
            (self in counterparty.preferences)): 
            return True
        else:
            return False

    def strikethrough(self):
        """Returns the participant's name in strikethrough font"""

        strikethrough = ''
        for c in self.name: 
            strikethrough += c + '\u0336'

        
class School(Participant):
    def __init__(self, name, preferences, max_placements): 
        super(School, self).__init__(name, preferences)
        self.type = 'School'
        self.max_placements = max_placements
        self.placements = {}
        self.full = False
        self.final = False

    def place(self, student, placement_type):
        """Assigns a student to the school's placements and updates the 
        full/final attributes
        """
        
        self.placements[student] = placement_type
        if len(self.placements)  == self.max_placements: 
            self.full = True
        if len(self.get_placements('final')) == self.max_placements: 
            self.final = True
        return True

    def displace(self, student):
        """Removes a student from the school's placements and updates the 
        full/final attributes
        """
        
        del(self.placements[student])
        self.full = False
        self.final = False
        return True

    def lowest_ranking_placement(self): 
        """Returns the lowest ranked tentatively placed student for 
        the school
        """

        tentative_placements = self.get_placements('tentative')
        tentative_placement_ranks = []
        for placement in tentative_placements: 
            tentative_placement_ranks.append(self.preferences.index(placement))
        lowest_ranking = max(tentative_placement_ranks)
        lowest_ranked = self.preferences[lowest_ranking]
        return lowest_ranked

    def highest_ranking_candidate(self):
        """Returns the highest ranked tentatively matched or currently
        unmatched student from the school's preferences"""
        
        candidates = self.preferences[:]
        for student in self.get_placements('final'):
            candidates.remove(student)        
        return candidates[0]
        

    def prefers(self, student):
        """Returns True where the school prefers the given student to the 
        current lowest ranking placement
        """

        if (self.preferences.index(student) < 
            self.preferences.index(self.lowest_ranking_placement())): 
            return True
        else: 
            return False

    def get_placements(self, type=None):
        """Returns all placements of a given type. If no type is specified, 
        all current placements will be returned.
        """

        placements = []                
        for placement in self.placements: 
            if self.placements[placement] == type or type == None: 
                placements.append(placement)     
        return placements 

    
class Student(Participant):
    def __init__(self, name, preferences): 
        super(Student, self).__init__(name, preferences)
        self.type = 'Student'
        self.placement = None
        self.options = self.preferences[:]

    def place(self, school, type): 
        """Assigns a school to the student"""

        if not self.placement: 
            self.placement = school
            return True
        else: 
            return False

    def displace(self, school):
        """Removes the assignment of the given school as the student's 
        placement
        """

        if school == self.placement: 
            self.placement = []
            return True
        else:
            return False


class Programme: 
    def __init__(self, students, schools):
        self.students = students
        self.schools = schools
        self.pending = self.students[:]

    def qualify_match(self, student, school):
        """"Identifies whether a valid match can be created between a student 
        and a school. 

        A match cannot be made where the school doesn't rank
        the student (and vice versa), or when the school is full and does not
        prefer the given student to its lowest ranked tentative placement.

        A match is considered 'final' if the student is the school's highest
        ranked unplaced or tentatively placed student.
        """

        if not student.preference_match(school): 
            print(f" * No preference match for {student.name} at {school.name}")
            return False

        if (school.final) or (school.full and not school.prefers(student)): 
            print(
                  f" * {school.name} is full: " +
                  f"{[student.name for student in school.placements]}"
                 )
            return False
       
        if school.highest_ranking_candidate() == student: 
            print(" * I think this match should be final!")
            return 'final'
        
        return 'tentative'

    def match(self, student, school, match_type='tentative'): 
        """Matches a student and a school and reflects the match in the 
        placement assignments for each
        """

        if school.full and not school.final and school.prefers(student):
            self.unmatch(school.lowest_ranking_placement(), school)

        student.place(school, match_type)
        school.place(student, match_type)
            
        print(f" * Assigning {student.name} to {school.name} as {match_type}")
        return True

    def unmatch(self, student, school):
        """Unmatches a student and a school, updating the placement assignments 
        for each
        """

        self.pending.append(student)
        student.displace(school)
        school.displace(student)

        print(f" * Removing {student.name} from {school.name}")
        return True
 
    def run(self):
        """Cycles through all students in a 'pending' pile, and attempts to 
        match them to their preferred school 'options'. A qualified match will
        result in a placement.
        """

        while self.pending:              
            student = self.pending.pop(0)
            print(
                  f"\n{student.name} - " +
                  f"{[item.name for item in student.options]}"
                 )
            while student.options: 
                school = student.options.pop(0)
                print(f" * Matching {student.name} with {school.name}")
                match_type = self.qualify_match(student, school)
                if match_type:
                    self.match(student, school, match_type) 
                    break
              
        
Mercy = School(name = "Mercy", max_placements = 2, preferences = [])
City = School(name = "City", max_placements = 2, preferences = [])
General = School(name = "General", max_placements = 2, preferences = [])


Arthur = Student(name = "Arthur", preferences = [City])
Sunny = Student(name = "Sunny", preferences = [City, Mercy])
Joseph = Student(name = "Joseph", preferences = [City, General, Mercy])
Latha = Student(name = "Latha", preferences = [Mercy, City, General])
Darius = Student(name = "Darius", preferences = [City, Mercy, General])


Mercy.preferences = [Darius, Joseph]
City.preferences = [Darius, Arthur, Sunny, Latha, Joseph]
General.preferences = [Darius, Arthur, Joseph, Latha]

students = [Arthur, Sunny, Joseph, Latha, Darius]
schools = [Mercy, City, General]

NRMP = Programme(students, schools)

NRMP.run()

print('\n')

for school in NRMP.schools: 
    for student, status in school.placements.items(): 
        print(f"{student.name} is matched with {school.name} as {status}")

        



                



