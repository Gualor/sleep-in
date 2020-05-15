#!/bin/env python3

from random import choice
import sqlite3
import string
import sys
import itertools as it
import operator
from functools import partial
from datetime import date, datetime, timedelta
import json

MESI = "ABCDEHLMPRST"
DISPARI = [1, 0, 5, 7, 9, 13, 15, 17, 19, 21, 2, 4, 18,
           20, 11, 3, 6, 8, 12, 14, 16, 10, 22, 25, 24, 23]
ORD_0 = ord("0")
ORD_A = ord("A")
vocale_pred = partial(operator.contains, set("AEIOUÀÈÉÌÒÙ"))


def create_username(name, surname):
    """Create a unique username based on personal information."""
    name = name.strip("'").replace(" ", "")
    surname = surname.strip("'").replace(" ", "")
    username = (name + surname).lower()
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


def calculate_fc(name, surname, sex, dob, city):
    """Calculate fiscal code."""
    code = calcola_cf(surname, name, dob, sex, city)
    return code


def pari(char):
    return ord(char) - (ORD_0 if char.isdigit() else ORD_A)


def dispari(char):
    return DISPARI[ord(char) - (ORD_0 if char.isdigit() else ORD_A)]


def calcola_ultimo_carattere(resto):
    return chr(ORD_A + resto)


def partition(pred, iterable):
    partitions = [], []
    for element in iterable:
        partitions[int(pred(element))].append(element)
    return partitions


def codifica_nome(nome, is_cognome=True):
    nome = nome.upper().replace(" ", "")

    consonanti, vocali = partition(vocale_pred, nome)

    if not is_cognome and len(consonanti) > 3:
        del consonanti[1]

    nome = "".join(consonanti + vocali)[:3]
    return nome.ljust(3, "X")


def codifica_data(data, sesso):
    offset = 40 if sesso in "fF" else 0
    return "{:>02}{}{:>02}".format(data.year % 100,
                                   MESI[data.month - 1],
                                   data.day + offset)


def codifica_comune(nome_comune):
    try:
        nome_comune = nome_comune.upper()
        conn = sqlite3.connect("comuni.db")
        result_set = conn.execute("select code from comuni where name = ?", [nome_comune])
        result = result_set.fetchone()
        return result[0]
    except TypeError:  # result is None
        raise ValueError("Comune non trovato!")


def calcola_codice_controllo(code):
    acc_d = sum(dispari(x) for x in code[::2])
    acc_p = sum(pari(x) for x in code[1::2])
    return calcola_ultimo_carattere((acc_d + acc_p) % 26)


def calcola_cf(cognome, nome, data, sesso, comune):
    codice = "{}{}{}{}".format(codifica_nome(cognome),
                               codifica_nome(nome, is_cognome=False),
                               codifica_data(data, sesso),
                               codifica_comune(comune))
    return "".join([codice, calcola_codice_controllo(codice)])


def compute_bmi(height, weight):
    """Compute BMI index."""
    tmp_h = int(height) / 100
    tmp_w = int(weight)
    bmi = tmp_w / (tmp_h ** 2)
    return round(bmi, 2)


def compute_psl(stress_survey):
    """Compute the perceived stress scale."""
    dict = json.loads(stress_survey)
    scale = 4
    psl = 0
    for key in dict:
        value = scale - dict[key]
        psl += value
    return psl


class TestEff(object):
    """Sleep efficiency test class."""

    def __init__(self, sleep_survey):
        self.test = self.convert_dict(sleep_survey)
        self.score = self.compute_efficiency(sleep_survey)

    def convert_dict(self, dict):
        survey = {}
        survey["quest1"] = int(dict["quest1"])
        survey["quest2"] = int(dict["quest2"])
        survey["quest3"] = int(dict["quest3"])
        survey["quest4"] = int(dict["quest4"])
        survey["quest6"] = int(dict["quest6"])
        survey["quest7"] = int(dict["quest7"])
        return survey

    def compute_efficiency(self, form):
        """Compute sleep efficiency."""

        gobed = int(form['quest1'])
        offlights = int(form['quest2'])
        asleep = int(form['quest3'])
        n = int(form['quest4'])
        totalawake = int(form['quest5'])
        stay = int(form['quest6'])
        gotup = int(form['quest7'])
        if(gobed <= 24) and (gobed >= 17):
            A = (abs((gobed - gotup) - 24)) * 60  # in minutes
        elif(gobed < 17):
            A = (gotup - gobed) * 60  # in minutes
        B = offlights + asleep + totalawake + stay
        sleep_eff = ((A - B) / A) * 100
        return sleep_eff


class TestPSQI(object):
    """PSQI test class."""

    def __init__(self, sleep_survey):
        self.test = self.convert_dict(sleep_survey)
        self.components = self.get_components()
        self.score = self.psqi_score()

    def convert_dict(self, dict):
        survey = {}
        survey["quest1"] = int(dict["quest1"])
        survey["quest2"] = int(dict["quest2"])
        survey["quest3"] = int(dict["quest3"])
        survey["quest4"] = int(dict["quest4"])
        survey["quest51"] = int(dict["quest51"])
        survey["quest52"] = int(dict["quest52"])
        survey["quest53"] = int(dict["quest53"])
        survey["quest54"] = int(dict["quest54"])
        survey["quest55"] = int(dict["quest55"])
        survey["quest56"] = int(dict["quest56"])
        survey["quest57"] = int(dict["quest57"])
        survey["quest58"] = int(dict["quest58"])
        survey["quest59"] = int(dict["quest59"])
        survey["quest510"] = int(dict["quest510"])
        survey["quest6"] = int(dict["quest6"])
        survey["quest7"] = int(dict["quest7"])
        survey["quest8"] = int(dict["quest8"])
        survey["quest9"] = int(dict["quest9"])
        return survey

    def get_components(self):
        comp_list = []
        comp_list.append(self.get_comp1())
        comp_list.append(self.get_comp2())
        comp_list.append(self.get_comp3())
        comp_list.append(self.get_comp4())
        comp_list.append(self.get_comp5())
        comp_list.append(self.get_comp6())
        comp_list.append(self.get_comp7())
        return comp_list

    def psqi_score(self):
        score = sum(self.components)
        return score

    def get_comp1(self):
        score = self.test["quest9"]
        return score

    def get_comp2(self):
        score = 0
        if self.test["quest2"] <= 15:
            score += 0
        elif self.test["quest2"] >= 16 and self.test["quest2"] <= 30:
            score += 1
        elif self.test["quest2"] >= 31 and self.test["quest2"] <= 60:
            score += 2
        elif self.test["quest2"] > 60:
            score += 3
        score += self.test["quest51"]
        if score == 0:
            score = 0
        elif score >= 1 and score <= 2:
            score = 1
        elif score >= 3 and score <= 4:
            score = 2
        elif score >= 5 and score <= 6:
            score = 3
        return score

    def get_comp3(self):
        self.test["quest4"]
        if self.test["quest4"] > 7:
            score = 0
        elif self.test["quest4"] >= 6 and self.test["quest4"] <= 7:
            score = 1
        elif self.test["quest4"] >= 5 and self.test["quest4"] <= 6:
            score = 2
        elif self.test["quest4"] < 5:
            score = 3
        return score

    def get_comp4(self):
        try:
            score = (self.test["quest4"] / (self.test["quest2"] + self.test["quest4"])) * 100
        except ZeroDivisionError:
            return 3

        if score > 85:
            score = 0
        elif score >= 75 and score <= 84:
            score = 1
        elif score >= 65 and score <= 74:
            score = 2
        elif score <= 64:
            score = 3
        return score

    def get_comp5(self):
        score = 0
        for i in self.test.keys():
            if i in ["quest52", "quest53", "quest54", "quest55", "quest56", "quest57", "quest58", "quest59", "quest510"]:
                score += self.test[i]
        if score == 0:
            score = 0
        elif score >= 1 and score <= 9:
            score = 1
        elif score >= 10 and score <= 18:
            score = 2
        elif score >= 19 and score <= 27:
            score = 3
        return score

    def get_comp6(self):
        score = self.test["quest6"]
        return score

    def get_comp7(self):
        score = self.test["quest7"] + self.test["quest8"]
        if score == 0:
            score = 0
        elif score >= 1 and score <= 2:
            score = 1
        elif score >= 3 and score <= 4:
            score = 2
        elif score >= 5 and score <= 6:
            score = 3
        return score


def adduser_dict(db, form):
    firstname = str(form['firstname'])
    surname = str(form['surname'])
    usertype = str(form['usertype'])
    specialization = str(form['specialization'])
    unit = str(form['unit'])
    city = str(form['city'])
    d = int(form['dob'][0:2])
    m = int(form['dob'][3:5])
    y = int(form['dob'][6:])
    dateofbirth = date(day=d, month=m, year=y)
    sex = str(form['sex'])
    index = 0
    username = create_username(firstname, surname)
    tmp = username
    while(db.is_user(tmp)):
        index += 1
        tmp = username + str(index)
    username = tmp
    password = create_password(8)
    fiscalcode = calculate_fc(firstname, surname, sex, dateofbirth, city)
    user = {'Username': username, 'Password': password, 'UserType': usertype, 'Specialization': specialization, 'Unit': unit,
            'FirstName': firstname, 'Surname': surname, 'FiscalCode': fiscalcode, 'DateOfBirth': dateofbirth, 'Sex': sex}
    return user


def count_login(log):
    log_dict = {}
    for x in log:
        tmp = x[1].replace(" ", "_")
        tmp = tmp.split("_")[0]
        tmp = tmp.split("-")
        y = str(tmp[0])
        if len(y) < 2:
            y = "0" + y
        m = str(tmp[1])
        if len(m) < 2:
            m = "0" + m
        d = str(tmp[2])
        if len(d) < 2:
            d = "0" + d
        day = d + "/" + m
        if day not in log_dict.keys():
            log_dict[day] = 0
        else:
            log_dict[day] += 1
    return log_dict


def table_login(log):
    res = []
    for i in range(0, len(log)):
        date = log[i][1].split(" ")[0]
        time = log[i][1].split(" ")[1]
        y = date[0:4]
        m = date[5:7]
        d = date[8:10]
        if len(m) < 2:
            m = "0" + m
        if len(d) < 2:
            d = "0" + d
        date = d + "-" + m + "-" + y
        time = time[0:8]
        string = date + " , " + time
        res.append((log[i][0], string))
    return res


def table_patient(pat):
    res = []
    for i in range(0, len(pat)):
        date = pat[i][3].split(" ")[0]
        time = pat[i][3].split(" ")[1]
        y = date[0:4]
        m = date[5:7]
        d = date[8:10]
        if len(m) < 2:
            m = "0" + m
        if len(d) < 2:
            d = "0" + d
        date = d + "-" + m + "-" + y
        time = time[0:5]
        string = date + " , " + time[0:6]
        res.append((pat[i][1], pat[i][2], string))
    return res


def table_daily(pat):
    res = []
    for i in range(0, len(pat)):
        time = pat[i][9].split(" ")[1]
        time = time[0:5]
        if pat[i][10] == 1:
            psg = "yes"
        else:
            psg = "no"
        res.append((pat[i][1], pat[i][2], time, psg))
    return res


def format_date(date, full=True, sep="-"):
    tmp = str(date)
    y = tmp[0:4]
    m = tmp[5:7]
    d = tmp[8:10]
    if len(m) < 2:
        m = "0" + m
    if len(d) < 2:
        d = "0" + d
    if full:
        date = d + sep + m + sep + y
    else:
        date = d + sep + m
    return date


def format_datetime(date, sep="-"):
    tmp = str(date)
    y = tmp[0:4]
    m = tmp[5:7]
    d = tmp[8:10]
    if len(m) < 2:
        m = "0" + m
    if len(d) < 2:
        d = "0" + d
    date = d + sep + m + sep + y
    time = tmp[11:16]
    return date + " " + time


def reverse_datetime(date):
    tmp = date.split(" ")
    date = tmp[0]
    time = tmp[1]
    d = int(date.split("-")[0])
    m = int(date.split("-")[1])
    y = int(date.split("-")[2])
    h = int(time.split(":")[0])
    mi = int(time.split(":")[1])
    date = datetime(int(y), int(m), int(d), int(h), int(mi), 00, 000)
    return date


def eff_graph(eff, days):
    dict = {}
    for x in eff:
        tmp = x[3].replace(" ", "_")
        tmp = tmp.split("_")[0]
        tmp = tmp.split("-")
        y = str(tmp[0])
        if len(y) < 2:
            y = "0" + y
        m = str(tmp[1])
        if len(m) < 2:
            m = "0" + m
        d = str(tmp[2])
        if len(d) < 2:
            d = "0" + d
        day = d + "/" + m
        dict[day] = x[4]
    n = len(dict) - days
    if n >= 0:
        return {k: dict[k] for k in list(dict.keys())[n:]}
    else:
        return dict


def table_visit(vis):
    res = []
    for i in range(0, len(vis)):
        date = vis[i][9].split(" ")[0]
        time = vis[i][9].split(" ")[1]
        y = date[0:4]
        m = date[5:7]
        d = date[8:10]
        if len(m) < 2:
            m = "0" + m
        if len(d) < 2:
            d = "0" + d
        date = d + "-" + m + "-" + y
        time = time[0:8]
        if vis[i][10] == 1:
            psg = "yes"
        else:
            psg = "no"
        res.append((vis[i][5], date, time[0:5], psg))
    return res


def datetime_format(date, lastday=False):
    date = date.split("/")
    d = int(date[1])
    m = int(date[0])
    y = int(date[2])
    if not lastday:
        return datetime(year=y, month=m, day=d)
    else:
        return datetime(year=y, month=m, day=d) + timedelta(days=1)


def pick_date(form):
    list = form['dates']
    start = datetime_format(list.split(",")[0], lastday=False)
    stop = datetime_format(list.split(",")[1], lastday=True)
    return start, stop


def hrbp_dict(db, id, start, stop):
    hr = {}
    sbp = {}
    dbp = {}
    list = db.retrieve_parameters(parameter="BloodPressure", patient=id,
                                  time_start=start, time_stop=stop)
    for x in list:
        hr[format_date(x[3], full=False, sep="/")] = x[6]
        sbp[format_date(x[3], full=False, sep="/")] = x[4]
        dbp[format_date(x[3], full=False, sep="/")] = x[5]
    return hr, sbp, dbp


def bmi_dict(db, id, start, stop):
    bmi = {}
    list = db.retrieve_parameters(parameter="BodyMeasure", patient=id,
                                  time_start=start, time_stop=stop)
    for x in list:
        bmi[format_date(x[3], full=False, sep="/")] = x[6]
    return bmi


def cal_dict(db, id, start, stop):
    cal = {}
    list = db.retrieve_parameters(parameter="Calories", patient=id,
                                  time_start=start, time_stop=stop)
    for x in list:
        cal[format_date(x[2], full=False, sep="/")] = x[3]
    return cal


def act_dict(db, id, start, stop):
    act = {}
    list = db.retrieve_parameters(parameter="Activity", patient=id,
                                  time_start=start, time_stop=stop)
    for x in list:
        act[format_date(x[2], full=False, sep="/")] = x[3]
    return act


def psq_dict(db, id, start, stop):
    psq = {}
    list = db.retrieve_parameters(parameter="SleepQuality", patient=id,
                                  time_start=start, time_stop=stop)
    for x in list:
        psq[format_date(x[3], full=False, sep="/")] = x[4]
    return psq


def qua_dict(db, id, start, stop):
    qua = {}
    list = db.retrieve_parameters(parameter="SleepEfficiency", patient=id,
                                  time_start=start, time_stop=stop)
    for x in list:
        qua[format_date(x[3], full=False, sep="/")] = x[5]
    return qua


def eff_dict(db, id, start, stop):
    eff = {}
    list = db.retrieve_parameters(parameter="SleepEfficiency", patient=id,
                                  time_start=start, time_stop=stop)
    for x in list:
        eff[format_date(x[3], full=False, sep="/")] = x[4]
    return eff


def psl_dict(db, id, start, stop):
    psl = {}
    list = db.retrieve_stress(id, start, stop)
    for x in list:
        psl[format_date(x[2], full=False, sep="/")] = x[1]
    return psl


def vizstats_dict(db, id, form):
    start, stop = pick_date(form)
    hr, sbp, dbp = hrbp_dict(db, id, start, stop)
    bmi = bmi_dict(db, id, start, stop)
    cal = cal_dict(db, id, start, stop)
    act = act_dict(db, id, start, stop)
    psq = psq_dict(db, id, start, stop)
    qua = qua_dict(db, id, start, stop)
    eff = eff_dict(db, id, start, stop)
    psl = psl_dict(db, id, start, stop)
    dict = {'hr': hr, 'sbp': sbp, 'dbp': dbp, 'bmi': bmi,
            'cal': cal, 'act': act, 'psq': psq, 'qua': qua, 'eff': eff, 'psl': psl}
    return dict


def all_dict(list):
    dict = {}
    for i in list:
        dict[i[0]] = i[1]

    return dict


def allstats_dict(db):
    table = {'Activity': 'Hours', 'BloodPressure': ['SystolicBP', 'DyastolicBP', 'HeartRate'], 'BodyMeasure': 'BMI', 'Calories': 'DailyCalories', 'PercievedStress': 'StressLevel', 'SleepEfficiency': ['Efficiency', 'SubjectiveSleep'], 'SleepQuality': 'PSQI'}
    par = {}
    for i in table.keys():

        if type(table[i]) == list:
            for k in table[i]:
                tmp = db.retrieve_statistics(i, k)
                par[k] = all_dict(tmp)

        else:
            tmp = db.retrieve_statistics(i, table[i])

            par[table[i]] = all_dict(tmp)
    return par
