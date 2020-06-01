class Participant:
    """
    A class to represent a Participant to be matched by the Programme.
    
    Attributes
    ----------
    name:str
        name of the Participant
    preferences:list
        a preference-ordered list of the Participant's preferences for other 
        Participants
        
    Methods
    -------
    preference_match(counterparty)
        Accepts another Programme Participant (counterparty) as an argument. 
        Returns TRUE where the Participant is in the counterparty's preferences 
        and vice versa; otherwise returns FALSE
    """
            
    def __init__(self, name, preferences):
        self.name = name 
        self.preferences = preferences

    def preference_match(self, counterparty):
        """Returns True where the Participant is in the counterparty's 
        preferences and vice versa
        """

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

        
class School(Participant):
    """
    A class representing the 'School' type of the 'Participant' parent class.
    Schools may have multiple 'placements' (matches to 'Student' participants).
    
    Attributes
    
    ----------
    type:str
        indicates the type participant (e.g. 'School')
    max_placements:int
        the maximum number of 'placements' a School may have
    placements:list
        a list containing the Participants currently matched with the School
    full:boolean
        indicates whether the the School is full (the number of 'tentative' *or*
        'final' placements at the School matches the School's max_placements
        value) 
    final:boolean
        indicates whether the the School is definitively full (the number of 
        'final' placements at the School matches the School's max_placements 
        value) 
        
    Methods
    -------
    place(student, placement_type)
        removes a Student from the School's placements and updates the 
        full/final attributes
    displace(student)
        removes a given Student from the School's list of placements. Will also 
        revent full/final values to FALSE
    lowest_ranking_placement()
        returns the lowest ranked tentatively placed Student for the School
    highest_ranking_cantidate()
        returns the highest ranked tentatively matched or currently unmatched 
        Student from the School's preferences
    prefers(student)
        returns TRUE where the School prefers the given Student to the current 
        lowest ranking placement
    get_placements(type=None)
        returns all placements of a given type. If no type is specified, all 
        current placements will be returned
    """ 
        
    def __init__(self, name, preferences, max_placements): 
        super(School, self).__init__(name, preferences)
        self.type = 'School'
        self.max_placements = max_placements
        self.placements = {}
        self.full = False
        self.final = False

    def place(self, student, placement_type):
        """Assigns a Student to the School's placements and updates the 
        full/final attributes
        """
        
        self.placements[student] = placement_type
        if len(self.placements)  == self.max_placements: 
            self.full = True
        if len(self.get_placements('final')) == self.max_placements: 
            self.final = True
        return True

    def displace(self, student):
        """Removes a Student from the School's placements and updates the 
        full/final attributes
        """
        
        del(self.placements[student])
        self.full = False
        self.final = False
        return True

    def lowest_ranking_placement(self): 
        """Returns the lowest ranked tentatively placed Student for the School
        """

        tentative_placements = self.get_placements('tentative')
        tentative_placement_ranks = []
        for placement in tentative_placements: 
            tentative_placement_ranks.append(self.preferences.index(placement))
        lowest_ranking = max(tentative_placement_ranks)
        lowest_ranked = self.preferences[lowest_ranking]
        return lowest_ranked

    def highest_ranking_candidate(self):
        """Returns the highest ranked tentatively matched or currently unmatched 
        Student from the School's preferences
        """
        
        candidates = self.preferences[:]
        for student in self.get_placements('final'):
            candidates.remove(student)        
        return candidates[0]
        

    def prefers(self, student):
        """Returns True where the School prefers the given Student to the 
        current lowest ranking placement
        """

        if (self.preferences.index(student) < 
            self.preferences.index(self.lowest_ranking_placement())): 
            return True
        else: 
            return False

    def get_placements(self, type=None):
        """Returns all placements of a given type. If no type is specified, all 
        current placements will be returned
        """

        placements = []                
        for placement in self.placements: 
            if self.placements[placement] == type or type == None: 
                placements.append(placement)     
        return placements 

    
class Student(Participant):
    """
    A class representing the 'Student' type of the 'Participant' parent class.
    Students may have only one 'placement' (match to 'School' Participants).
    
    Attributes    
    ----------
    type:str
        indicates the type participant (e.g. 'Student')
    placement:Participant
        indicates the School the Student is currently placed with
    options:list
        a list subset of the Student's preferences. Schools are removed from the
        'options' list where the match between Student:School is determined as 
        not viable
     
    Methods
    -------
    place(school)
        assigns a School to the Student
    displace(school)
        removes the assignment of the given School as the Student's placement
    """ 
    
    def __init__(self, name, preferences): 
        super(Student, self).__init__(name, preferences)
        self.type = 'Student'
        self.placement = None
        self.options = self.preferences[:]

    def place(self, school): 
        """Assigns a School to the Student"""

        if not self.placement: 
            self.placement = school
            return True
        else: 
            return False

    def displace(self, school):
        """Removes the assignment of the given School as the Student's placement
        """

        if school == self.placement: 
            self.placement = None
            return True
        else:
            return False


class Programme: 
    """
    Class representing the Programme through which participants will be matched.
    
    Attributes
    ----------
    students:list
        a list of Students to be matched by the Programme
    schools:list
        a list of Schools to be matched by the Programme
    pending:list
        a subset of the Students list containing only those Students who are 
        still to be matched
    
    Methods
    -------
    qualify_match(student, school)
        Identifies whether a valid match can be created between a Student 
        and a School. 

        A match cannot be made where the School doesn't rank
        the Student (and vice versa), or when the School is full and does not
        prefer the given Student to its lowest ranked tentative placement.

        A match is considered 'final' if the Student is the School's highest
        ranked unplaced or tentatively placed Student
    match(student, school, match_type='tentative') 
        Matches a Student and a School and reflects the match in the placement 
        assignments for each
    unmatch(student, school)
        Unmatches a Student and a School, updating the placement assignments 
        for each
    run(self)
        Cycles through all Students in a 'pending' pile, and attempts to 
        match them to their preferred School 'options'. A qualified match will
        result in a placement
    """    
       
    def __init__(self, students, schools):
        self.students = students
        self.schools = schools
        self.pending = self.students[:]

    def qualify_match(self, student, school):
        """"Identifies whether a valid match can be created between a Student 
        and a School. 

        A match cannot be made where the School doesn't rank
        the Student (and vice versa), or when the School is full and does not
        prefer the given Student to its lowest ranked tentative placement.

        A match is considered 'final' if the Student is the School's highest
        ranked unplaced or tentatively placed Student
        """

        if not student.preference_match(school): 
            return False

        if (school.final) or (school.full and not school.prefers(student)): 
            return False
       
        if school.highest_ranking_candidate() == student: 
            return 'final'
        
        return 'tentative'

    def match(self, student, school, match_type='tentative'): 
        """Matches a Student and a School and reflects the match in the 
        placement assignments for each
        """

        if school.full and not school.final and school.prefers(student):
            self.unmatch(school.lowest_ranking_placement(), school)

        student.place(school)
        school.place(student, match_type)
            
        return True

    def unmatch(self, student, school):
        """Unmatches a Student and a School, updating the placement assignments 
        for each
        """

        self.pending.append(student)
        student.displace(school)
        school.displace(student)

        return True
 
    def run(self):
        """Cycles through all Students in a 'pending' pile, and attempts to 
        match them to their preferred School 'options'. A qualified match will
        result in a placement
        """

        while self.pending:              
            student = self.pending.pop(0)
            """print(
                  f"\n{student.name} - " +
                  f"{[item.name for item in student.options]}"
                 )"""
            while student.options: 
                school = student.options.pop(0)
                #print(f" * Matching {student.name} with {school.name}")
                match_type = self.qualify_match(student, school)
                if match_type:
                    self.match(student, school, match_type) 
                    break

