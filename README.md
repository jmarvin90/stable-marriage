# stable-marriage
Python solution to the stable marriage/matching problem based on the NRMP algorithm as demonstrated in the below-linked video.

The solution uses an 'applicant-proposing' method to match applicants ('students') to their ranked choice of school.

https://www.youtube.com/watch?v=kvgfgGmemdA

Objectives of the solution were to: 

1. Meet the functional requirements as described in the linked NRMP video
2. Demonstrate awareness of OOO techniques including inheritance
3. Meet (where possible) the PEP8 guidelines for code readability

The solution is comprised of the following components / objects: 

Participant:
 - Each student / school is considered a 'participant'
 - Each participant may have a name, and a rank-ordered list of preferences for other participants
 
 Student: 
  - A type of participant which may have a single 'placement' value
  
 School: 
  - A type of participant which may have multiple 'placement' values of different types ('tentative', 'final') up to a maximum
  
  Programme: 
   - A matching programme which manages the logic used to match all student's to their preferred schools
 


