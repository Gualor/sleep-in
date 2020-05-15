from random import randint
from datetime import datetime, timedelta
from dbinit import Database
from data_process import compute_bmi

path = "../server/database/"
file = "data.db"
def home_p():
    return randint(101,200)

def populate_visit(number, DB):
    d = datetime.today().replace(hour=8, minute=0, second=0, microsecond=0)
    l = []
    for i in range(number):
        rnd_patient = randint(21, 100)
        rnd_medician = randint(6, 20)
        hourplus = randint(0, 10)
        minuteplus = randint(0, 1) * 30
        dayplus = randint(-100, 90)
        psg = randint(0, 1)
        plus = timedelta(days=dayplus, seconds=(minuteplus * 60 + hourplus * 3600))
        complete = 0
        if d + plus < datetime.today():
            complete = 1
        l.append((rnd_patient, rnd_medician, d + plus, complete, psg))
    duplicates = 0
    try:
        conn, c = DB._connect()
        c.executemany('''INSERT INTO Visit(
                PatientID,
                MedicianID,
                VisitDate,
                Complete,
                PSG
            ) VALUES(?,?,?,?,?)''', l)
        DB._disconnect(conn, c)
    except Exception as e:
        print("{} encountered.".format(e))
        duplicates += 1
        pass

    print("\t Inserted {} records".format(len(l) - duplicates))


def populate_threshold(DB):
    conn, c = DB._connect()
    for patient in range(21, 101):
        c.execute('''INSERT INTO Thresholds(PatientID,
        HRMin,  HRMax,
        SPMin,  SPMax,
        DPMin,  DPMax,
        BMIMin,  BMIMax,
        ActivityMin,  ActivityMax,
        StressMin,  StressMax,
        PSQIMin,  PSQIMax,
        SleepEffMin,  SleepEffMax,
        CaloriesMin,  CaloriesMax) VALUES(?,60,80,110,139,75,89,18.5,24.9,0,NULL,0,20,0,13,50,NULL,2000,3000)''', (patient,))
    DB._disconnect(conn, c)
    print("\t Inserted {} records".format(len(range(21, 101))))


def populate_blood_pressure(DB):
    l = []
    for patient in range(21, 101):
        d = datetime.today()
        home_param = home_p()
        for i in range(home_param, 0, -1):
            hr = randint(55, 85)
            sp = randint(109, 140)
            dp = randint(74, 90)
            alert = DB.check_threshold(patient, "HR", hr) or DB.check_threshold(
                patient, "SP", sp) or DB.check_threshold(patient, "DP", dp)
            l.append((patient, d - timedelta(days=i), sp, dp, hr, alert))
    conn, c = DB._connect()
    c.executemany('''INSERT INTO BloodPressure(
        PatientID ,
        Recorded,
        SystolicBP,
        DyastolicBP,
        HeartRate,
        Alert) VALUES(?,?,?,?,?,?)''', l)
    DB._disconnect(conn, c)
    print("\t Inserted {} records".format(len(l)))


def populate_body_measure(DB):
    l = []
    for patient in range(21, 101):
        d = datetime.today()
        home_param = home_p()
        height = randint(160, 190)
        weight = randint(50, 80)
        for i in range(home_param, 0, -1):
            weight += (randint(-1, 1) / 10)
            BMI = compute_bmi(int(height), weight)
            alert = DB.check_threshold(patient, "BMI", BMI)
            l.append((patient, d - timedelta(days=i),
                      height / 100, int(weight), BMI, alert))
    conn, c = DB._connect()
    c.executemany('''INSERT INTO BodyMeasure(
        PatientID,
        Recorded,
        Height,
        Weight,
        BMI,
        Alert) VALUES(?,?,?,?,?,?)''', l)
    DB._disconnect(conn, c)
    print("\t Inserted {} records".format(len(l)))


def populate_calories(DB):
    l = []
    for patient in range(21, 101):
        d = datetime.today()
        home_param = home_p()
        for i in range(home_param, 0, -1):
            calories = randint(1900, 3100)
            alert = DB.check_threshold(patient, "Calories", calories)
            l.append((patient, d - timedelta(days=i), calories, alert))
    conn, c = DB._connect()
    c.executemany('''INSERT INTO Calories(
        PatientID,
        Recorded,
        DailyCalories,
        Alert) VALUES(?,?,?,?)''', l)
    DB._disconnect(conn, c)
    print("\t Inserted {} records".format(len(l)))


def populate_activities(DB):
    l = []
    for patient in range(21, 101):
        d = datetime.today()
        home_param = home_p()
        for i in range(home_param, 0, -1):
            activities = randint(0, 5)
            alert = DB.check_threshold(patient, "Activity", activities)
            l.append((patient, d - timedelta(days=i), activities, alert))

    conn, c = DB._connect()
    c.executemany('''INSERT INTO Activity(
        PatientID,
        Recorded,
        Hours,
        Alert) VALUES(?,?,?,?)''', l)
    DB._disconnect(conn, c)
    print("\t Inserted {} records".format(len(l)))


def populate_accesses(number, DB):
    l = []
    for i in range(number):
        user = randint(1, 100)
        day = randint(-1, 200) * -1
        hour = randint(0, 23)
        sec = randint(0, 3599)
        d = datetime.combine(datetime.today(), datetime.min.time(
        )) + timedelta(days=day, hours=hour, seconds=sec)
        l.append((user, d))
    conn, c = DB._connect()
    c.executemany('''INSERT INTO Platform(UserID, Access) VALUES(?,?) ''', l)
    DB._disconnect(conn, c)
    print("\t Inserted {} records".format(len(l)))


def populate_sleep_eff(DB):
    l = []
    for patient in range(21, 101):
        d = datetime.today()
        home_param = home_p()
        for i in range(home_param, 0, -1):
            eff = randint(48, 100)
            subj = randint(1, 5)
            alert = DB.check_threshold(patient, "SleepEff", eff)
            l.append((patient, d - timedelta(days=i), eff, subj, alert))

    conn, c = DB._connect()
    c.executemany('''INSERT INTO SleepEfficiency(
        PatientID,
        Recorded,
        Efficiency,
        SubjectiveSleep,
        Alert) VALUES(?,?,?,?,?)''', l)
    DB._disconnect(conn, c)
    print("\t Inserted {} records".format(len(l)))


def populate_sleep_qual(DB):
    l = []
    for patient in range(21, 101):
        d = datetime.today()
        home_param = randint(1, 11)
        for i in range(home_param, 0, -1):
            psqi = randint(0, 14)
            alert = DB.check_threshold(patient, "PSQI", psqi)
            l.append((patient, d - timedelta(days=i * 30), psqi, alert))

    conn, c = DB._connect()
    c.executemany('''INSERT INTO SleepQuality(
        PatientID,
        Recorded,
        PSQI,
        Alert) VALUES(?,?,?,?)''', l)
    DB._disconnect(conn, c)
    print("\t Inserted {} records".format(len(l)))


def populate_visit_parameter(DB):
    conn, c = DB._connect()
    c.execute('''SELECT ID, PatientID, VisitDate FROM Visit WHERE Complete=1''')
    visits = c.fetchall()
    print("\t For {} visits: Populating stress, bp and bodymeasure".format(len(visits)))
    for i in visits:
        stress = randint(0, 25)
        populate_stress(
            DB, (i[1], i[0], stress, DB.check_threshold(i[1], "Stress", stress)), c)
        populate_visit_body(DB, i[0], i[2], i[1], c)
        populate_visit_bp(DB, i[1], i[0], i[2], c)
    DB._disconnect(conn, c)


def populate_visit_body(DB, visitID, visitDate, patientID, c):
    print("{},{},{}".format(visitID, visitDate, patientID))
    c.execute('''SELECT Height, Weight, Recorded FROM BodyMeasure WHERE Recorded < ? AND PatientID=? ORDER BY Recorded DESC ''',
              (visitDate, patientID))
    res = c.fetchone()
    height = res[0]
    weight = int(res[1] + (randint(-1, 1) / 100))
    BMI = compute_bmi(int(height), weight)
    alert = DB.check_threshold(patientID, "BMI", BMI)
    c.execute('''INSERT INTO BodyMeasure(
        PatientID,
        VisitID,
        Recorded,
        Height,
        Weight,
        BMI,
        Alert) VALUES(?,?,?,?,?,?,?)''', (patientID, visitID, visitDate, height, weight, BMI, alert))


def populate_visit_bp(DB, patient, visitID, visitDate, c):
    hr = randint(55, 85)
    sp = randint(109, 140)
    dp = randint(74, 90)
    alert = DB.check_threshold(patient, "HR", hr) or DB.check_threshold(
        patient, "SP", sp) or DB.check_threshold(patient, "DP", dp)
    c.execute('''INSERT INTO BloodPressure(
        PatientID ,
        VisitID,
        Recorded,
        SystolicBP,
        DyastolicBP,
        HeartRate,
        Alert) VALUES(?,?,?,?,?,?,?)''', (patient, visitID, visitDate, sp, dp, hr, alert))


def populate_stress(DB, tup, c):
    c.execute('''INSERT INTO PercievedStress(
        PatientID,
        VisitID,
        StressLevel,
        Alert) VALUES(?,?,?,?)''', tup)


if __name__ == "__main__":

    visit = 100
    mDB = Database(path, file)
    populate_visit(visit, mDB)
