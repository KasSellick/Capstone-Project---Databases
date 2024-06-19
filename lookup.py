'''Program to read student data and save information to JSON or XML files.

Access database.
Present menu to the user.
Options to:
    view all students
    view subjects taken by a student
    lookup address for a given firstname and surname
    list reviews for a given student_id
    list all courses taken by teacher_id
    list all students who haven't completed their course
    list all students who have completed their course and achieved 30 or below
    exit program
Give option after each query to save data as XML or JSON file.

Functions:
-------
    usage_is_incorrect:
        Parameters:
            input (list) : input from user with command and arguments
            num_args (int) : number of arguments required for command

    store_data_as_json:
        Parameters:
            data : SQLite query result
            filename (str) : Name of file given by user

    store_data_as_xml:
        Parameters:
            data : SQLite query result
            filename (str) : Name of file given by user
            table (str) : table name of data

    offer_to_store:
        Parameters:
            data : SQLite query result
            table (str) : table name of data
'''



#=======Importing Libraries=======

import sqlite3
import json
import xml.etree.ElementTree as ET
import os.path


#=======Connecting Database=======

# connect to SQLite database
try:
    conn = sqlite3.connect("HyperionDev.db")
except sqlite3.Error:
    print("Please store your database as HyperionDev.db")
    quit()

# get cursor object
cur = conn.cursor()



#=======Functions=======


# check user input
def usage_is_incorrect(input, num_args):
    '''Check user has input correct number of arguements.

    Returns:
    -------
        True or False
    
    Parameters:
    -------
        input (list) : input from user with command and arguments
        num_args (int) : number of arguments required for command
    '''
    
    if len(input) != num_args + 1:
        print(f"The {input[0]} command requires {num_args} arguments.")
        return True
    return False


# save data as JSON
def store_data_as_json(data, filename):
    '''Save data as a JSON file.
    
    Create a list of information for each object.
    Create a list of information headings.
    Create dictionary of headings and inforamtion.
    Convert dictionary to JSON format.
    Save JSON file.
    
    Parameters:
    -------
        data : SQLite query result
        filename (str) : Name of file given by user
    '''
    
    #fetch all rows from the last executed statement
    rows = cur.fetchall()
    
    # get column names
    columns = [description[0] for description in cur.description]
    
    # convert query results to a list of dictionaries
    data_dict = [dict(zip(columns, row)) for row in rows]
    
    # convert data to JSON
    json_data = json.dumps(data_dict, indent=4)
    
    # save data to JSON file
    with open(filename, 'w') as outfile:
        outfile.write(json_data)


# save data as XML
def store_data_as_xml(data, filename, table):
    '''Save data as an XML file.
    
    Create a list of information for each object.
    Create a list of information headings.
    Convert data to XML structure.
    Save XML file.
    
    Parameters:
    -------
        data : SQLite query result
        filename (str) : Name of file given by user
        table (str) : table name of data
    '''
    
    # root element name
    tree_name = filename.strip('.xml')
    
    # fetch all rows from the last executed statement
    rows = cur.fetchall()

    # get column names
    columns = [description[0] for description in cur.description]

    # create the root element for the XML
    root = ET.Element(tree_name)

    # iterate over rows to create XML structure
    for row in rows:
        row_element = ET.SubElement(root, table)
        for i, value in enumerate(row):
            col_element = ET.SubElement(row_element, columns[i])
            col_element.text = str(value)

    # convert the XML tree to a string
    tree = ET.ElementTree(root)

    # save XML to file
    tree.write(filename, encoding='utf-8', xml_declaration=True)
    

# ask to save data
def offer_to_store(data, table):
    '''Asks user if they'd like to store information in a file.

    If yes:
        Ask for file name with .xml or .json extension.
        If .xml:
            call function store_data_as_xml.
        If .json:
            call function store_data_as_json.
            
    Parameters:
    -------
        data : SQLite query result
        table (str) : table name of data
    '''

    # get user input
    while True:
        print("\nWould you like to store this result?")
        choice = input("Y/[N]? : ").strip().lower()

        # if yes, get file from user name and call appropriate function
        if choice == "y":
            while True:
                filename = input("\nSpecify filename. Must end in .xml or .json: ")
                # check if file exists
                check_file = os.path.isfile(filename)
                # if exists, loop back to rename
                if check_file == True:
                    print(f"\nFile name {filename} already exists. Please try again.")
                
                # if new file name, check extension
                else:
                    ext = filename.split(".")[-1]
                    if ext == 'xml':
                        store_data_as_xml(data, filename, table) # save as xml
                        break
                    elif ext == 'json':
                        store_data_as_json(data, filename) # save as json
                        break
                    # if incorrect extension, loop back to rename
                    else:
                        print("\nInvalid file extension. Please use .xml or .json")
            break
        
        # if no, exit function
        elif choice == 'n':
            break
        
        # invalid input
        else:
            print("\nInvalid choice. Please try again.")



#=======Menu=======

usage = '''
What would you like to do?

va                         - view all students
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program

Type your option here: '''

print("Welcome to the data querying app!")



#=======Queries=======

while True:
    
    print()
    # Get input from user
    user_input = input(usage).split(" ")
    print()

    # Parse user input into command and args
    command = user_input[0]
    if len(user_input) > 1:
        args = user_input[1:]


    if command == 'va': # print all student names and surnames
        
        # execute query
        try:
            data = cur.execute("""SELECT * FROM Student""")
            
            # print all student names and surnames
            print("\n\033[1mList of all students:\033[0m")
            print("\n_____________\n")
            for _, firstname, surname, _, _ in data:
                print(f"{firstname} {surname}")
            print("\n_____________")

            # table name for XML file
            table = 'Student'

            # option to save to file
            offer_to_store(data,table)

        except:
            print("Could not complete request. Please try again.")
    
    
        
    elif command == 'vs': # view subjects by student_id
        
        # check number of arguments
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        
        # execute query
        try: 
            data_for_display = cur.execute('''SELECT Course.course_name,
            Student.first_name, Student.last_name
            FROM Course
            INNER JOIN StudentCourse
            ON Course.course_code = StudentCourse.course_code
            INNER JOIN Student
            ON StudentCourse.student_id = Student.student_id
            WHERE Student.student_id = ?
            ''', (student_id,))
            
            # fetch all rows from query
            courses = cur.fetchall()
            
            # print results
            print(f"\n\033[1mCourses taken by {courses[0][1]} {courses[0][2]}: \033[0m")
            print("\n_____________\n")
            for  course in courses:
                print(course[0])
            print("\n_____________")

            # get all data for file
            data = cur.execute('''SELECT *
            FROM Course
            INNER JOIN StudentCourse
            ON Course.course_code = StudentCourse.course_code
            INNER JOIN Student
            ON StudentCourse.student_id = Student.student_id
            WHERE Student.student_id = ?
            ''', (student_id,))
            
            # table name for XML file
            table = 'Course'

            # option to save to file
            offer_to_store(data,table)
        
        except:
            print("Invalid student number. Please try again.")




    elif command == 'la':# list address by name and surname
    
        # check number of arguments
        if usage_is_incorrect(user_input, 2):
            continue
        firstname, surname = args[0], args[1]
        
        # execute query
        try:
            data_for_display = cur.execute('''SELECT Address.street,
            Address.city, Student.student_id
            FROM Address
            LEFT JOIN Student
            ON Address.address_id = Student.address_id
            LEFT JOIN Teacher
            ON Address.address_id = Teacher.address_id
            WHERE (Student.first_name = ? AND Student.last_name = ?) OR (Teacher.first_name = ? AND Teacher.last_name = ?)
            ''', (firstname,surname,firstname,surname))
            
            # fetch all rows from query
            address = cur.fetchall()

            # print results
            print(f"""
\033[1mAddress of {firstname} {surname}:\033[0m
_____________
Street: {address[0][0]}
City: \t{address[0][1]}
_____________
""")

            #print(address[0][2])
            
            # table name for XML file
            table = 'Address'
            
            # get all data for file
            # separate to avoid null results
            if address[0][2] == None : # is not a student
                data = cur.execute('''SELECT *
                FROM Address
                INNER JOIN Teacher
                ON Address.address_id = Teacher.address_id
                WHERE Teacher.first_name = ? AND Teacher.last_name = ?
                ''', (firstname,surname))
            
            else:
                data = cur.execute('''SELECT *
                FROM Address
                INNER JOIN Student
                ON Address.address_id = Student.address_id
                WHERE Student.first_name = ? AND Student.last_name = ?
                ''', (firstname,surname))
            
            # option to save to file
            offer_to_store(data, table)
        
        except:
            print("Invalid name. Please try again.")



    elif command == 'lr':# list reviews by student_id
    
        # check number of arguments
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        
        # execute query
        try:
            data_for_display = cur.execute('''SELECT Course.course_name, Review.completeness,
            Review.efficiency, Review.style, Review.documentation, Review.review_text,
            Student.first_name, Student.last_name
            FROM Review
            INNER JOIN StudentCourse
            ON Review.student_id = StudentCourse.student_id AND
            Review.course_code = StudentCourse.course_code
            LEFT JOIN Student
            ON StudentCourse.student_id = Student.student_id
            LEFT JOIN Course
            ON Course.course_code =StudentCourse.course_code
            WHERE Student.student_id = ?
            ''', (student_id,))
            
            # fetch all rows from query
            reviews = cur.fetchall()

            # print results
            print(f"\n\033[1mReviews for {reviews[0][6]} {reviews[0][7]}:\033[0m")
            for review in reviews:
                print("\n_____________\n")
                print(f"""
\033[1mCourse: {review[0]}\033[0m

Completeness: \t{review[1]}
Efficiency: \t{review[2]}
Style: \t\t{review[3]}
Documentation: \t{review[4]}
Comments: \t{review[5]}
                """)
                print("\n_____________")

            # get all data for file
            data = cur.execute('''SELECT *
            FROM Review
            INNER JOIN StudentCourse
            ON Review.student_id = StudentCourse.student_id AND
            Review.course_code = StudentCourse.course_code
            LEFT JOIN Student
            ON StudentCourse.student_id = Student.student_id
            LEFT JOIN Course
            ON Course.course_code =StudentCourse.course_code
            WHERE Student.student_id = ?
            ''', (student_id,))
            
            # table name for XML file
            table = 'Review'

            # option to save to file
            offer_to_store(data, table)
                
        except:
            print("Invalid student number. Please try again.")




    elif command == 'lc': # list all courses taken by teacher_id
    
        # check number of arguments
        if usage_is_incorrect(user_input, 1):
            continue
        teacher_id = args[0]
        
        # execute query
        try:
            data_for_display = cur.execute('''SELECT Course.course_name, Teacher.first_name,
            Teacher.last_name
            FROM Course
            INNER JOIN Teacher
            ON Teacher.teacher_id = Course.teacher_id
            WHERE Teacher.teacher_id = ?
            ''', (teacher_id,))

            # fetch all rows from query
            courses = cur.fetchall()

            # print results
            print(f"\n\033[1mCourses given by {courses[0][1]} {courses[0][2]}: \033[0m")
            print("\n_____________\n")
            for  course in courses:
                print(course[0])
            print("\n_____________")

            # get all data for file
            data = cur.execute('''SELECT *
            FROM Course
            INNER JOIN Teacher
            ON Teacher.teacher_id = Course.teacher_id
            WHERE Teacher.teacher_id = ?
            ''', (teacher_id,))
            
            # table name for XML file
            table = 'Course'

            # option to save to file
            offer_to_store(data, table)

        except:
            print("Invalid teacher ID. Please try again.")



    elif command == 'lnc': # list all students who haven't completed their course
    
        # execute query
        try:
            data_for_display = cur.execute('''SELECT Student.student_id, Student.first_name,
            Student.last_name, Student.email, Course.course_name
            FROM Student
            INNER JOIN StudentCourse
            ON Student.student_id = StudentCourse.student_id
            INNER JOIN Course
            ON StudentCourse.course_code = Course.course_code
            WHERE StudentCourse.is_complete = ?
            ''', ('0'))
            
            # fetch all rows from query
            incomplete = cur.fetchall()
            
            # print results
            print("\n\033[1mList of all students with incomplete courses:\033[0m")
            for student in incomplete:
                print("\n_____________\n")
                print(f"""
Student number: {student[0]}
First name: \t{student[1]}
Surname: \t{student[2]}
Email: \t\t{student[3]}
Course: \t{student[4]}
""")
                print("\n_____________")

            # get all data for file
            data = cur.execute('''SELECT Student.student_id, Student.first_name,
            Student.last_name, Student.email, Course.course_name
            FROM Student
            INNER JOIN StudentCourse
            ON Student.student_id = StudentCourse.student_id
            INNER JOIN Course
            ON StudentCourse.course_code = Course.course_code
            WHERE StudentCourse.is_complete = ?
            ''', ('0'))
            
            # table name for XML file
            table = 'Student'

            # option to save to file
            offer_to_store(data, table)
        
        except:
            print("Could not complete request. Please try again.")
    
    
    
    elif command == 'lf': # list all students who have completed their course and got a mark <= 30
    
        # execute query
        try:
            data_for_display = cur.execute('''SELECT Student.student_id, Student.first_name,
            Student.last_name, Student.email, Course.course_name, StudentCourse.mark
            FROM Student
            INNER JOIN StudentCourse
            ON Student.student_id = StudentCourse.student_id
            INNER JOIN Course
            ON StudentCourse.course_code = Course.course_code
            WHERE StudentCourse.is_complete = ? AND StudentCourse.mark <= ?
            ''', ('1','30'))
            
            # fetch all rows from query
            completed_fail = cur.fetchall()
            
            # print results
            print("\n\033[1mList of all students with complete courses with a mark of 30 or below:\033[0m")
            for student in completed_fail:
                print("\n_____________\n")
                print(f"""
Student number: {student[0]}
First name: \t{student[1]}
Surname: \t{student[2]}
Email: \t\t{student[3]}
Course: \t{student[4]}
Mark: \t\t{student[5]}
""")
                print("\n_____________")
            
            # get all data for file
            data = cur.execute('''SELECT *
            FROM Student
            INNER JOIN StudentCourse
            ON Student.student_id = StudentCourse.student_id
            INNER JOIN Course
            ON StudentCourse.course_code = Course.course_code
            WHERE StudentCourse.is_complete = ? AND StudentCourse.mark <= ?
            ''', ('1','30'))
            
            # table name for XML file
            table = 'Student'

            # option to save to file
            offer_to_store(data, table)
        
        except:
            print("Could not complete request. Please try again.")



    elif command == 'e': # exit this program
        
        # close connection
        conn.close()
        print("\nProgramme exited successfully!")
        break
    
    else: # invalid input
        
        print(f"\nI\033[1mncorrect command:\033[0m '{command}'")
    

    
