import requests
import sys
import json
import time
import smtplib
import ssl
import os

# Reads file and converts to JSON
def get_json(path):
    try:
        return json.loads(open(path, "r").read())
    except Exception as e:
        print("Failed to load JSON!", e)
        return None

# POST /api/grades wrapper function
def get_grades(username, password):
    json = { "username": username, "password": password }
    response = ""

    try:
        response = requests.post("http://unipi-students-api:69/api/grades", json=json).json()
    except Exception as e:
        print("Failed to get grades.", e)
        time.sleep(5 * 60)
        exit()

    return response

def send_new_grades(new_grades):
    smtp_config = get_json("/unipi_notify/config/smtp.json")
    
    grades = ""

    for course, grade in new_grades.items():
        grades += course + ": " + grade + "\n"

    message = """\
Subject: Νέοι Βαθμοί

Έχουν δημοσιευθεί {grades_num} νέοι βαθμοί.

{grades}
    """.format(grades_num=len(new_grades), grades=grades).encode('utf-8')

    try: 
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_config["address"], smtp_config["ssl"], context=context) as server:
            server.login(smtp_config["email"], smtp_config["password"])
            server.sendmail(smtp_config["email"], smtp_config["email"], message)
    except Exception as e:
        print("Failed to send e-mail!", e)

# ===!!! TERRIBLE CODE WARNING !!!===
# Get grades and detect if there are new ones
def get_new_grades(username, password):
    old_grades = {}
    new_grades = {}

    old_grades_json = get_json("/unipi_notify/data/grades.json")
    
    # Get old grades    
    for semester in old_grades_json["semesters"]:
        for course in semester["courses"]:
            if course["grade"] != "-":
                old_grades[course["name"]] = course["grade"]

    new_grades_json = get_grades(username, password)

    # Get new grades
    for semester in new_grades_json["semesters"]:
        for course in semester["courses"]:
            if course["grade"] != "-":
                new_grades[course["name"]] = course["grade"]

    # Leave only new grades in new_grades dictionary
    for course, grade in old_grades.items():
        if course in new_grades and grade == new_grades[course]:
            new_grades.pop(course)

    if(len(new_grades) != 0):
        send_new_grades(new_grades)

if __name__ == "__main__":
    time.sleep(30)

    minutes = get_json("/unipi_notify/config/notify.json")["minutes"]

    # I said NO!
    if(minutes < 5):
        no = r"""
 _   _ _____ 
| \ | |  _  |
|  \| | | | |
| . ` | | | |
| |\  \ \_/ /
\_| \_/\___/ 

        """
        print(no)
        exit()

    user_config = get_json("/unipi_notify/config/user.json")
    username = user_config["username"]
    password = user_config["password"]

    if not os.path.exists("/unipi_notify/data/grades.json"):
        res = get_grades(username, password)
        open("/unipi_notify/data/grades.json", "w").write(json.dumps(res))
        time.sleep((minutes / 2) * 60)

    exit()

    try:
        while True:
            get_new_grades(username, password)
            time.sleep(minutes * 60)
    except KeyboardInterrupt:
        print("User has singaled to exit.")
    except Exception as e:
        print("An error has occured!", e)
