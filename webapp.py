from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)


@app.route("/")
def get_github():
    return render_template("get_github.html")


@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    student_row = hackbright_app.get_student_by_github(student_github)
    grades_rows = hackbright_app.get_grades_by_github(student_github)

    html = render_template("student_info.html", first_name=student_row[0],
                                                last_name=student_row[1],
                                                github=student_row[2],
                                                grades=grades_rows)
    return html


@app.route("/project")
def get_project_grades():
    hackbright_app.connect_to_db()
    print "did this print? before"
    project_title = request.args.get("title")
    project_rows = hackbright_app.get_all_grades_for_project(project_title)
    print "AFTER"

    html = render_template("project_info.html", title=project_title, 
                                                grade=project_rows)
# first_name=project_rows[0],
#                                                 last_name=project_rows[1],
    return html

if __name__ == "__main__":
    app.run(debug=True)

