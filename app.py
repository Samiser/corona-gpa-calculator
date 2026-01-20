import statistics
from flask import Flask
from flask import json
from flask import request
from flask import render_template

app = Flask(__name__)

def calc_class(gpa):
    if gpa >= 3.75:
        return "1st"
    elif gpa >= 2.75:
        return "2:1"
    elif gpa >= 1.75:
        return "2:2"
    else:
        return "3rd"

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
    data = {"grades": [], "old_gpa": 0, "new_gpa": 0, "old_class":"", "new_class":""}
    sections = {"current": 6}

    if year == "year4":
        sections["old"] = 6

    try:
        for section in sections:
            for i in range(sections[section]):
                data["grades"].append(request.form[section + "_" + str(i)])
        data["old_gpa"] = old_gpa(list(map(float, data["grades"])))
        data["new_gpa"] = new_gpa(list(map(float, data["grades"])))
        data["old_class"] = calc_class(float(data["old_gpa"]))
        data["new_class"] = calc_class(float(data["new_gpa"]))
        return data
    except Exception as e:
        return {"Error": str(e)}

def main():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
