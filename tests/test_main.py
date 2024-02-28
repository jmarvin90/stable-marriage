import pytest
from src.student import Student
from src.school import School
from src.programme import Programme

@pytest.fixture
def mercy() -> School:
    return School(
      name="Mercy", 
      max_placements=2, 
      preferences=[]
    )

@pytest.fixture
def city() -> School:
  return School(
    name="City", 
    max_placements=2, 
    preferences=[]
  )

@pytest.fixture
def general() -> School:
  return School(
    name="General", 
    max_placements=2,
    preferences=[]
  )

@pytest.fixture
def arthur(city: School) -> Student:
  return Student(
    name="Arthur", 
    preferences=[city]
  )

@pytest.fixture
def sunny(city: School, mercy: School) -> Student:
  return Student(
    name="Sunny", 
    preferences=[city, mercy]
  )

@pytest.fixture
def joseph(city: School, general: School, mercy: School) -> Student:
  return Student(
    name="Joseph", 
    preferences=[city, general, mercy]
  )

@pytest.fixture
def latha(mercy: School, city: School, general: School) -> Student:
  return Student(
    name="Latha", 
    preferences=[mercy, city, general]
  )

@pytest.fixture
def darius(city: School, mercy: School, general: School) -> Student:
  return Student(
    name="Darius", 
    preferences=[city, mercy, general]
  )

@pytest.fixture
def students(
  arthur: Student, 
  sunny: Student, 
  joseph: Student, 
  latha: Student, 
  darius: Student
) -> list:
  return [arthur, sunny, joseph, latha, darius]

@pytest.fixture
def schools(
  mercy: School, 
  city: School, 
  general: School,
  arthur: Student, 
  sunny: Student, 
  joseph: Student, 
  latha: Student, 
  darius: Student
) -> list:
  mercy.preferences = [darius, joseph]
  city.preferences = [darius, arthur, sunny, latha, joseph]
  general.preferences = [darius, arthur, joseph, latha]
  return [mercy, city, general]

@pytest.fixture
def programme(students: list, schools: list) -> Programme:
  return Programme(students=students, schools=schools)

def test_assignment(
  programme: Programme, arthur: Student, city: School
) -> None:
  programme.run()
  assert (
    arthur in city.placements
  )