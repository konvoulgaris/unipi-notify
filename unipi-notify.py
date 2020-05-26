import requests
import sys
import json
import jsonschema
import time
import smtplib
import ssl
import os

PATH_PREFIX = str(os.getenv("PATH_PREFIX", ""))
URL = str(os.getenv("API_URL", "localhost"))
REFRESH = int(os.getenv("REFRESH", "30"))

SMTP_SCHEMA = {
    "address": { "type": "string" },
    "ssl_port": { "type": "number" },
    "email": { "type": "string" },
    "password": { "type": "string" },
}

SMTP = None

USER_SCHEMA = {
    "username": { "type": "string" },
    "password": { "type": "string" }
}

USER = None

# Load JSON and validate against schema
def get_json(path, schema=None):
    data = None

    try:
        with open(PATH_PREFIX + path, "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data)

            if not schema is None:
                jsonschema.validate(data, schema)
    except Exception as e:
        print("Failed to get JSON!\n", e)
        return None
    
    return data

# Get latest grades
def get_grades():
    data = None

    try:
        response = requests.post("http://" + URL + ":8080/api/grades", json=USER)
        data = response.json()
    except Exception as e:
        print("Failed to get grades!\n", e)
        return None

    return data

# Get last grades; if there aren't any, get them
def get_last_grades():
    if not os.path.exists("data/grades.json"):
        return None

    data = get_json("data/grades.json")
    return data

def send_email(subject, message):
    if SMTP is None:
        print("SMTP configuration isn't loaded!")
        return False

    server_address = SMTP["address"]
    server_ssl = SMTP["ssl_port"]
    server_context = ssl.create_default_context()
    email = SMTP["email"]
    password = SMTP["password"]

    msg = """\
Subject: {sub}

{mes}
    """.format(sub=subject, mes=message).encode('utf-8')

    try: 
        with smtplib.SMTP_SSL(server_address, server_ssl, context=server_context) as server:
            server.login(email, password)
            server.sendmail(email, email, msg)
    except Exception as e:
        print("Failed to send e-mail!\n", e)
        return False

    return True

def check_grades(last_grades):
    new_grades = get_grades()

    if new_grades is None:
        print("Failed to get new grades!")
        return None

    print("Got new grades")

    # I AM FULLY AWARE THAT THE FOLLOWING BLOCK IS NOT OPTIMAL!    
    last_grades_formatted = {}

    # Clean last grades
    for semester in last_grades["semesters"]:
        for course in semester["courses"]:
            if course["grade"] != "-":
                last_grades_formatted[course["name"]] = course["grade"]

    new_grades_formatted = {}

    # Clean new grades
    for semester in new_grades["semesters"]:
        for course in semester["courses"]:
            if course["grade"] != "-":
                new_grades_formatted[course["name"]] = course["grade"]

    # Actually get new grades
    for course, grade in last_grades_formatted.items():
        if course in new_grades_formatted and grade == new_grades_formatted[course]:
            new_grades_formatted.pop(course)

    if len(new_grades_formatted) <= 0:
        return last_grades

    print("There are new grades.\nSending mail!")

    grades = ""

    for course, grade in new_grades_formatted.items():
        grades += "- " + course + ": " + grade + "\n"

    message = "Έχουν δημοσιευθεί {gn} νέες(α) βαθμολογίες(α)!\n\n{g}".format(gn=str(len(new_grades_formatted)), g=grades)

    send_email("Νέες βαθμολογίες!", message)

    try:
        with open(PATH_PREFIX + "data/grades.json", "w") as file:
            data = json.dumps(new_grades)
            file.write(data)
    except Exception as e:
        print("Failed to write grades.json!")
        return None

    return new_grades


if __name__ == "__main__":
    time.sleep(30)

    SMTP = get_json("config/smtp.json", SMTP_SCHEMA)

    if SMTP is None:
        print("Failed to load SMTP configuration!")
        exit(1)

    print("Loaded SMTP configuration")

    USER = get_json("config/user.json", USER_SCHEMA)

    if USER is None:
        print("Failed to load user configuration!")
        exit(1)

    print("Loaded USER configuration")

    last_grades = get_last_grades()    

    if last_grades is None:
        print("First time setup.\nGetting grades...")
        last_grades = get_grades()
        
        while last_grades is None:
            print("Failed to get grades!\nWaiting before trying again...")
            time.sleep(REFRESH * 60)
            last_grades = get_grades()

        try:
            with open(PATH_PREFIX + "data/grades.json", "w") as file:
                data = json.dumps(last_grades)
                file.write(data)
        except Exception as e:
            print("Failed to write grades.json!")
            exit(1)

        print("Got grades!\nWaiting to refresh...")
        time.sleep(REFRESH * 60)

    print("Starting to check for new grades")

    try:
        while True:
            last_grades = check_grades(last_grades)
            
            if last_grades is None:
                print("An error has occured!")
                exit(1)

            print("Checked grades!\nWaiting to refresh...")
            time.sleep(REFRESH * 60)
    except KeyboardInterrupt:
        print("User has signaled to exit")
