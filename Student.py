class Student:
    # Class that holds student information
    # Constructor For Student Class
    # NOTE: Student Table automatically increments studentID
    def __init__(self):
        self.studentID = 0
        self.firstName = ''
        self.lastName = ''
        self.GPA = 0.0
        self.major = ''
        self.facultyAdvisor = ''
        self.isDeleted = 0

    # Second Constructor that makes all input lower case
    def SetStudent(self, inputFirstName, inputLastName, inputGPA, inputMajor, inputFacultyAdvisor):
        #self.studentID = inputStudentID
        self.firstName = inputFirstName.lower()
        self.lastName = inputLastName.lower()
        self.GPA = inputGPA
        self.major = inputMajor.lower()
        self.facultyAdvisor = inputFacultyAdvisor.lower()
        self.isDeleted = 0


    def ShowMe(self):
        print(self.firstName)
        print(self.lastName)

    def GetStudentTuple(self):
        studentTuple = (str(self.firstName), str(self.lastName), float(self.GPA), str(self.major), str(self.facultyAdvisor))
        return studentTuple
