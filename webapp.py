from flask import Flask, render_template, request, redirect
import hackbright_app

app = Flask(__name__)


@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/all_students")
def list_all_students():
    hackbright_app.connect_to_db()
    students = hackbright_app.get_all_students()
    html = render_template("all_students.html", students=students)
    return html


#@app.route("/giggles") can have multiple routes for a function, but only one function for a route
@app.route("/student")
def get_student():
    print "in get student"
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    student_row = hackbright_app.get_student_by_github(student_github)

    print "student_row is: " , type(student_row)
    print 'student_row', student_row
    if (student_row == None):
        print "doesn't exist!!!!!!!!"
        html = render_template("github_not_found.html")
        return html
    else:

        grades_rows = hackbright_app.get_grades_by_github(student_github)

        html = render_template("student_info.html", first_name=student_row[0],
                                                    last_name=student_row[1],
                                                    github=student_row[2],
                                                    grades=grades_rows)
        return html


@app.route("/project")
def get_project_grades():
    hackbright_app.connect_to_db()
    project_title = request.args.get("title")
    project_rows = hackbright_app.get_all_grades_for_project(project_title)

    html = render_template("project_info.html", title=project_title, 
                                                grade=project_rows)
    return html

@app.route("/new_student")
def add_student():
    hackbright_app.connect_to_db()
    first_name = request.args.get("first")      #args is a dictionary  
    last_name = request.args.get("last", 'default')
    github = request.args.get("new_github")     # is equal to request.args["new_github"]
    student_info = hackbright_app.make_new_student(first_name, last_name, github)

    #print "student_info is: " , type(student_info)
    #returns NoneType because in the function in hackbright_app we aren't returning any info

    return redirect('/student?github=' + github)

    #JavaScript way of writing the above line of code (which is in flask):
    # html = render_template("added_student.html", new_github=github)
    # return html

@app.route("/new_grade")
def add_grade():
    hackbright_app.connect_to_db()
    project = request.args.get("new_project")
    grade = request.args.get("new_grade")
    github = request.args.get('github', )
    print "github is: " , github
    grade_info = hackbright_app.give_grade_to_student(github, project, grade)

    return redirect('/student?github=' + github)

if __name__ == "__main__":
    app.run(debug=True) #this starts flask

