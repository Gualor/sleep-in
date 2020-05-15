import os
import sqlite3
import string
from datetime import date
from random import choice, randint

import pandas as pd

import populate.cf as cf
from dbinit import Database
import populate.populateparams as p

path = "database/"
file = "data.db"


def populate_user(db, num):
    name_list = pick_names(num)
    dob_list = pick_dob(num)
    city_list = pick_city(num)
    fc_list = pick_fc(num, name_list, dob_list, city_list)
    spec_list = ["Pulmonologist", "Otolaryngologist",
                 "Cardiologist", "Neurologist"]
    for i in range(0, num):
        usr = create_username(db, name_list[i][0], name_list[i][1])
        pwd = create_password(8)
        if i < 5:
            insert_user(usr, pwd, 'T', None, None,
                        name_list[i][0], name_list[i][1], fc_list[i], dob_list[i], name_list[i][2])
        elif i >= 5 and i < 20:
            insert_user(usr, pwd, 'M', choice(spec_list), "Sleep care",
                        name_list[i][0], name_list[i][1], fc_list[i], dob_list[i], name_list[i][2])
        else:
            insert_user(usr, pwd, 'P', None, None,
                        name_list[i][0], name_list[i][1], fc_list[i], dob_list[i], name_list[i][2])
    print("Inserted {} new users".format(num))
    


def insert_user(usr, pwd, type, spec, unit, name, surname, fc, dob, sex):
    conn = sqlite3.connect(path + file)
    cur = conn.cursor()
    cur.execute('''INSERT INTO User
    (
    Username,
    Password,
    UserType,
    Specialization,
    Unit,
    FirstName,
    Surname,
    FiscalCode,
    DateOfBirth,
    Sex
    )
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (usr, pwd, type, spec, unit, name, surname, fc, dob, sex))
    conn.commit()
    conn.close()


def create_username(db, name, surname):
    """Create a unique username based on personal information."""
    name = name.strip("'").replace(" ", "")
    surname = surname.replace(" ", "")
    username = (name + surname).lower()
    index = 0
    while (db.is_user(username)):
        index += 1
        username += str(index)
    return username


def create_password(num_char):
    """Create a unique password."""
    pwd = ""
    count = 0
    while(count < num_char):
        upper = [choice(string.ascii_uppercase)]
        lower = [choice(string.ascii_lowercase)]
        num = [choice(string.digits)]
        everything = upper + lower + num
        pwd += choice(everything)
        count += 1
    return pwd


def pick_names(num):
    namelist = []
    f1 = open(file="populate/name.csv", mode='r')
    df1 = pd.read_csv(f1, header=None, sep="\t", names=["name", "sex", "id"])
    f2 = open(file="populate/surname.csv", mode='r')
    df2 = pd.read_csv(f2, header=None, sep="\t", names=["surname", "id"])
    i = 0
    while i < num:
        try:
            pos1 = randint(0, min([len(df1), len(df2)]))
            pos2 = randint(0, min([len(df1), len(df2)]))
            if df1["id"][pos1] > 12 and df2["id"][pos2] > 12:
                name = df1["name"][pos1].lower().title()
                surname = df2["surname"][pos2].lower().title()
                if len(name) < 10 and len(surname) < 10:
                    record = (name, surname, df1["sex"][pos1])
                    namelist.append(record)
                    i += 1
        except Exception:
            pass
    return namelist


def pick_dob(num):
    doblist = []
    for i in range(0, num):
        m30 = [4, 6, 9, 11]
        year = randint(a=1930, b=2001)
        month = randint(a=1, b=12)
        if month in m30:
            day = randint(a=1, b=30)
        elif month == 2:
            day = randint(a=1, b=28)
        else:
            day = randint(a=1, b=31)
        dob = date(year, month, day)
        doblist.append(dob)
    return doblist


def pick_city(num):
    citylist = []
    f = open(file="populate/city.csv", mode='r')
    df = pd.read_csv(f, header=None, names=["city"])
    for i in range(0, num):
        pos = randint(a=0, b=len(df))
        citylist.append(df["city"][pos])
    return citylist


def pick_fc(num, namelist, doblist, citylist):
    fclist = []
    for i in range(0, num):
        code = cf.calcola_cf(namelist[i][1], namelist[i][0],
                             doblist[i], namelist[i][2], citylist[i])
        fclist.append(code)
    return fclist


if __name__ == "__main__":

    usr_num = 100
    mDB = Database(path, file)
    mDB.db_init()
    print("Populating User")
    populate_user(mDB, usr_num)

    print("Populating Visit")
    p.populate_visit(200, mDB)

    print("Populating Thresholds")
    p.populate_threshold(mDB)

    print("Populating Blood Pressure")
    p.populate_blood_pressure(mDB)

    print("Populating Body Measure")
    p.populate_body_measure(mDB)

    print("Populating Calories")
    p.populate_calories(mDB)

    print("Populating Activities")
    p.populate_activities(mDB)

    print("Populating Database Accesses")
    p.populate_accesses(750, mDB)

    print("Populating Sleep Efficiency")
    p.populate_sleep_eff(mDB)

    print("Populating Sleep quality")
    p.populate_sleep_qual(mDB)

    print("Populating Visit Parameters")
    p.populate_visit_parameter(mDB)

    print("Done!!")
