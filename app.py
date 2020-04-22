import statistics
from flask import Flask
from flask import json
from flask import request
from flask import render_template

app = Flask(__name__)

def old_gpa(grades):
    return "{:.2f}".format(statistics.mean(grades))

def new_gpa(grades):
    grades.remove(min(grades))
    grades.remove(min(grades))
    return "{:.2f}".format(statistics.mean(grades))

@app.route('/')
@app.route('/<year>')
def form(year=None):
    return render_template('index.html', year=year)

@app.route('/<year>', methods=['POST'])
def form_post(year=None):
    data = {"grades": [], "wanted_grades": [], "old_gpa": 0, "new_gpa": 0}
    sections = {"current": 3}

    if year == "year4":
        sections["old"] = 6

    try:
        for section in sections:
            for i in range(sections[section]):
                data["grades"].append(request.form[section + "_" + str(i)])
        for i in range(3):
            data["wanted_grades"].append(request.form["want_" + str(i)])
        data["old_gpa"] = old_gpa(list(map(float, data["grades"] + data["wanted_grades"])))
        data["new_gpa"] = new_gpa(list(map(float, data["grades"] + data["wanted_grades"])))
        return data
    except Exception as e:
        return {"Error": str(e)}
