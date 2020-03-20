# Filip Augustowski
# 002287932
# 3/18/2020
# CPSC408 CRUDApp

import Student
import sqlite3

# Must always connect to our database first
conn = sqlite3.connect('StudentDB.sqlite')
# allows python code to execute 50L statements
c = conn.cursor()

# Helper Functions

# Returns true if the input is correct, false if not
def CheckInput(type, check):
    if type == 'str' and isinstance(check, str) and check != '':
        return True
    elif type == 'float':
        try:
            checkFloat = float(check)
            return True
        except ValueError:
            print('Input number properly')
    elif type == 'int':
        try:
            checkInt = int(check)
            return True
        except ValueError:
            print('Input number properly')
    else:
        print("Input Error or Empty line")
        return False;

def Create():
    # All of this information is required on creation
    firstName = input('\tEnter First Name: ')
    if CheckInput('str', firstName):
        lastName = input('\tEnter Last Name: ')
        if CheckInput('str', lastName):
            GPA = input('\tEnter GPA: ')
            if CheckInput('float', GPA):
                major = input('\tEnter Major: ')
                if CheckInput('str', major):
                    facultyAdvisor = input('\tEnter Faculty Advisor: ')
                    if CheckInput('str', facultyAdvisor):
                        # Create our student object and assign proper values.
                        newStudent = Student.Student()
                        newStudent.SetStudent(firstName, lastName, GPA, major, facultyAdvisor)
                        # Feed our DB the new entry, rows are case sensitive
                        c.execute("INSERT INTO Student('FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor')" 
                                 "VALUES (?, ?, ?, ?, ?)", newStudent.GetStudentTuple())
                        conn.commit()

def Display():
    # Find all students that are not deleted
    studentTable = c.execute('SELECT * FROM Student WHERE isDeleted != 1')
    displayResults = c.fetchall()
    # README 3, displays results in a pretty manner
    for result in displayResults:
        print('\t' + ' '.join(map(str, result)))

def Update():
    print('Leave input blank to not change')
    inputID = input('Enter StudentID: ')

    # Here we allow user to choose what to update
    if CheckInput('int', inputID):
        inputMajor = input('\tEnter New Major: ')
        if CheckInput('str', inputMajor):
            inputAdvisor = input('\tEnter New Advisor: ')
            # Update both
            if CheckInput('str', inputAdvisor):
                # Catch SQL Error, README 4)
                try:
                    c.execute('UPDATE Student Set Major = ?, FacultyAdvisor = ? WHERE StudentID = ?',
                              (inputMajor, inputAdvisor, inputID,))
                    conn.commit()
                except Exception as e:
                    print("Exception in query: %s" % e)

            # Just update major
            else:
                try:
                    c.execute('UPDATE Student Set Major = ? WHERE StudentID = ?', (inputMajor, inputID,))
                    conn.commit()
                except Exception as e:
                    print("Exception in query: %s" % e)

        else:
            inputAdvisor = input('Enter New Advisor: ')
            # Only update advisor
            if CheckInput('str', inputAdvisor):
                try:
                    c.execute('UPDATE Student Set FacultyAdvisor = ? WHERE StudentID = ? ', (inputAdvisor, inputID,))
                    conn.commit()

                except Exception as e:
                    print("Exception in query: %s" % e)
            # No Changes due to bad input or no input on both
            else:
                print('No change made')

def Delete():
    print('Leave input blank to not change')
    inputID = input('\tEnter StudentID: ')
    # Attempt to resolveID
    if CheckInput('int', inputID):
        try:
            # Soft delete
            c.execute('UPDATE Student Set isDeleted= ? WHERE StudentID = ?', (1, inputID))
            conn.commit()
        except Exception as e:
            print("Exception in query: %s" % e)

# Creates a like term for sqlite
def CreateLikeTerm(term):
    term = '%'+term+'%'
    return term

def Search():
    print('\t1-----Search by GPA--------')
    print('\t2-----Search by Major------')
    print('\t3-----Search by Advisor----')
    userChoice = input('\tChose Search Option: ')

    if userChoice == '1':
        searchTerm = input('\tInput GPA: ')
        if CheckInput('float', searchTerm):
            c.execute('SELECT * FROM Student WHERE isDeleted != ? AND GPA = ?', (1, searchTerm))
            displayResults = c.fetchall()
            # README 3, displays results in a pretty manner
            for result in displayResults:
                print('\t' + ' '.join(map(str, result)))
    if userChoice == '2':
        searchTerm = input('\tInput Major: ')
        if CheckInput('str', searchTerm):
            c.execute('SELECT * FROM Student WHERE isDeleted != ? AND Major LIKE ?', (1, CreateLikeTerm(searchTerm)))
            displayResults = c.fetchall()
            # README 3, displays results in a pretty manner
            for result in displayResults:
                print('\t' + ' '.join(map(str, result)))
    if userChoice == '3':
        searchTerm = input('\tInput Advisor: ')
        if CheckInput('str', searchTerm):
            c.execute('SELECT * FROM Student WHERE isDeleted != ? AND FacultyAdvisor LIKE ?', (1, CreateLikeTerm(searchTerm)))
            displayResults = c.fetchall()
            # README 3, displays results in a pretty manner
            for result in displayResults:
                print('\t' + ' '.join(map(str, result)))

# Keep looping until quit
while True:
    print('1-----Display Students-----')
    print('2-----Create Student-------')
    print('3-----Update Student Info--')
    print('4-----Delete Student Info--')
    print('5-----Search Students------')
    print('Q-----Quit-----------------')
    userChoice = input('\tChoose What To Do: ')

    if userChoice == '1':
        Display()

    if userChoice == '2':
        Create()

    if userChoice == '3':
        Update()

    if userChoice == '4':
        Delete()

    if userChoice == '5':
        Search()

    elif userChoice.lower() == 'q' or userChoice.lower() == 'quit':
        c.close()
        conn.close()
        break
