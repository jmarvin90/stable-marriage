import unittest
from NRMP8 import Student, School, Programme

class TestNRMPMatching(unittest.TestCase):
    def setUp(self):
        """
        Create a set of Student, School participants with the relevant 
        preferences for use in all test methods.
        """
    
        self.Mercy = School(
                            name="Mercy", 
                            max_placements=2, 
                            preferences=[]
                           )
                           
        self.City = School(
                            name="City", 
                            max_placements=2, 
                            preferences=[]
                          )
        
        self.General = School(
                            name="General", 
                            max_placements=2,
                            preferences=[]
                          )

        self.Arthur = Student(
                            name="Arthur", 
                            preferences=[self.City]
                          )
                          
        self.Sunny = Student(
                            name="Sunny", 
                            preferences=[self.City, self.Mercy]
                          )
                          
        self.Joseph = Student(
                            name="Joseph", 
                            preferences=[self.City, self.General, self.Mercy]
                          )
        
        self.Latha = Student(
                            name="Latha", 
                            preferences=[self.Mercy, self.City, self.General]
                          )
        
        self.Darius = Student(
                            name="Darius", 
                            preferences=[self.City, self.Mercy, self.General]
                          )

        self.Mercy.preferences = [
                            self.Darius, 
                            self.Joseph
                          ]
                          
        self.City.preferences = [
                            self.Darius, 
                            self.Arthur, 
                            self.Sunny, 
                            self.Latha, 
                            self.Joseph
                          ]
                          
        self.General.preferences = [
                            self.Darius, 
                            self.Arthur, 
                            self.Joseph, 
                            self.Latha
                          ]

        self.students = [
                            self.Arthur, 
                            self.Sunny, 
                            self.Joseph, 
                            self.Latha, 
                            self.Darius
                          ]
                          
        self.schools = [self.Mercy, self.City, self.General]

        self.NRMP = Programme(self.students, self.schools)
        self.NRMP.run()

    def test_assignments(self):
        """Test that all Students are placed with the correct Schools."""
        
        self.assertIn(self.Arthur, self.City.placements)
        self.assertIn(self.Darius, self.City.placements)
        self.assertIn(self.Joseph, self.General.placements)
        self.assertIn(self.Latha, self.General.placements)
        self.assertTrue(self.Sunny.placement == None)
        
    def test_assignment_types(self):
        """Test that all Student placements are of the correct type."""
        
        self.assertTrue(self.City.placements[self.Arthur] == 'tentative')
        self.assertTrue(self.City.placements[self.Darius] == 'final')
        self.assertTrue(self.General.placements[self.Joseph] == 'tentative')
        self.assertTrue(self.General.placements[self.Latha] == 'tentative')
        
if __name__ == '__main__':
    unittest.main()
