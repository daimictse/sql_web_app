from flask import Flask, render_template, request, redirect, url_for
import hackbright_app
app = Flask(__name__)

# Code goes here

@app.route("/")
def get_name():
    return render_template("get_student_names.html")

@app.route("/student_name")
def get_student():
    hackbright_app.connect_to_db()
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    rows = hackbright_app.student_grades(first_name, last_name)
    if len(rows) == 0:
        html = render_template("student_info.html", first_name=first_name,
                                                last_name=last_name)
    else:
        grades = []
        for row in rows:
            grades.append((row[2],row[3]))
        html = render_template("student_info.html", first_name=row[0],
                                                    last_name=row[1],
                                                    grades=grades)
    return html

@app.route("/project")
def project_grades():
    hackbright_app.connect_to_db()
    project = request.args.get("project")
    rows = hackbright_app.project_grades(project)
    if len(rows) == 0:
        html = render_template("project_grades.html", project=project)
    else:
        grades = []
        for row in rows:
            grades.append((row[0], row[1], row[2])) #first name, last name, and grade
        html = render_template("project_grades.html", project = project,
                                                        grades=grades)
    return html

@app.route("/new_student", methods=["POST"])
def make_new_student():
    hackbright_app.connect_to_db()
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    student_github = request.form.get("github")
    hackbright_app.make_new_student(first_name, last_name, student_github)
    return redirect("/student_name?first_name=%s&last_name=%s"%(first_name,last_name))

@app.route("/new_project", methods=["POST"])
def make_new_project():
    hackbright_app.connect_to_db()
    project = request.form.get("project")
    description = request.form.get("description")
    max_grade = request.form.get("max_grade")
    hackbright_app.make_new_project(project, description, max_grade)
    return redirect("/project?project=%s"%project)

@app.route("/new_grade", methods=["POST"])
def make_new_grade():
    hackbright_app.connect_to_db()
    github = request.form.get("github")
    project = request.form.get("project")
    grade = request.form.get("grade")
    hackbright_app.make_new_grade(github, project, grade)
    return redirect("/project?project=%s"%project)

if __name__ == "__main__":
    app.run(debug=True)