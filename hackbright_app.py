import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def get_projects_by_title(title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    rows = DB.fetchall()
    for row in rows:
        print """\
    Project: %s
    Description: %s
    Maximum Grade: %d"""%(row[0], row[1], row[2])

def student_project_grade(first_name, last_name, project):
    query="""SELECT *
    FROM GradesView 
    WHERE Gradesview.first_name = ? AND GradesView.last_name = ? AND GradesView.project_title = ?"""
    DB.execute(query, (first_name, last_name, project,))
    rows = DB.fetchall()
    for row in rows:
        print """\
    %s %s received %d on %s."""%(row[0], row[1], row[3], row[2]) 

def student_grades(first_name, last_name):
    query="""SELECT * FROM GradesView AS gv
    WHERE gv.first_name = ? AND gv.last_name = ?"""
    DB.execute(query, (first_name, last_name,))
    rows = DB.fetchall()
    return rows 

def project_grades(project):
    query="""SELECT gv.first_name, gv.last_name, gv.grade
    FROM GradesView AS gv
    WHERE gv.project_title = ?"""
    DB.execute(query, (project,))
    rows = DB.fetchall()
    return rows 


def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students (first_name, last_name, github) values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    return True

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) values (?,?,?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s"%title

def make_new_grade(student_github, project_title, grade):
    query = """INSERT into Grades (student_github, project_title, grade) values (?, ?, ?)"""
    DB.execute(query, (student_github, project_title, grade))
    CONN.commit()
    return project_title

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split("|")
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "project":
            get_projects_by_title(*args)
        elif command == "project_grade":
            student_project_grade(*args)
        elif command == "grades":
            student_grades(*args)
        elif command == "new_student":
            make_new_student(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "new_grade":
            make_new_grade(*args)

    CONN.close()

if __name__ == "__main__":
    main()