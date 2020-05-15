from flask import Flask, g, redirect, render_template, request, make_response, flash, url_for
import sqlite3
from dbinit import Database, User, DBError
from data_process import adduser_dict, TestPSQI, TestEff, count_login, table_login, format_date, eff_graph, table_visit, table_patient, table_daily, vizstats_dict, allstats_dict, datetime_format, format_datetime, reverse_datetime
import json
import os
from datetime import datetime, timedelta, date
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploaded'

path = "database/"
file = "data.db"
mDB = Database(path, file)
user_dict = {}

# Create app
app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'super-secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# ################### Security function ############### #
def check_cook(id, userType):
    user = user_dict.get(id)
    if user is not None:
        if user.getUserType() == userType:
            return 1
    return 0


# #################### Login page #################### #
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
        userdetails = request.form
        username = userdetails['username']
        password = userdetails['password']
        temp = mDB.log_user_in(username, password)
        try:
            id = str(temp[0])
            username = str(temp[1])
            password = str(temp[2])
            usertype = str(temp[3])
            specialization = str(temp[4])
            unit = str(temp[5])
            firstname = str(temp[6])
            surname = str(temp[7])
            fiscalcode = str(temp[8])
            dateofbirth = str(temp[9])
            sex = str(temp[10])
            user = User({'ID': id, 'Username': username, 'Password': password, 'UserType': usertype, 'Specialization': specialization,
                         'Unit': unit, 'FirstName': firstname, 'Surname': surname, 'FiscalCode': fiscalcode, 'DateOfBirth': dateofbirth, 'Sex': sex})
            user_dict[id] = user

            if usertype == "M":
                user_obj = user_dict[id]
                all_patients = table_patient(mDB.list_patient())
                daily_patients = table_daily(mDB.retrieve_visit(id))
                fcode = user_obj.getFiscalCode()
                dob = format_date(user_obj.getDateOfBirth())
                spec = user_obj.getSpecialization()
                unit = user_obj.getUnit()
                resp = make_response(render_template(
                    "/medician.html", first=firstname, sur=surname, fcode=fcode, dob=dob, spec=spec, unit=unit, all_pat=all_patients, daily=daily_patients))
                resp.set_cookie('session', id)
                return resp

            if usertype == "T":
                stop_date = datetime.today()
                start_date = stop_date - timedelta(days=7)
                log = mDB.retrieve_login(time_start=start_date, time_stop=stop_date)
                log_dict = count_login(log)
                n_login = table_login(mDB.retrieve_login())
                n_users = len(mDB.list_all_users(userType=None))
                n_patients = len(mDB.list_all_users(userType="P"))
                n_medicians = len(mDB.list_all_users(userType="M"))
                n_techs = len(mDB.list_all_users(userType="T"))
                resp = make_response(render_template("/techadmin.html", log_dict=log_dict, login=n_login,
                                                     users=n_users, pat=n_patients, med=n_medicians, tech=n_techs, first=firstname, sur=surname))
                resp.set_cookie('session', id)
                return resp

            if usertype == "P":
                stop_date = datetime.today()
                start_date = stop_date - timedelta(days=7)
                eff_list = mDB.retrieve_parameters(
                    "SleepEfficiency", patient=id, time_start=start_date, time_stop=stop_date)
                eff_dict = eff_graph(eff_list, days=7)
                user_obj = user_dict[id]
                fcode = user_obj.getFiscalCode()
                dob = format_date(user_obj.getDateOfBirth())
                param = mDB.retrieve_parameters("BodyMeasure", patient=id, last=True)
                if len(param) > 0:
                    height = str(param[0][4]) + " cm"
                    weight = str(param[0][5]) + " Kg"
                else:
                    height = "No data"
                    weight = "No data"
                vis = mDB.retrieve_visit(id, future=True)
                n_visit = table_visit(vis)
                resp = make_response(render_template("/patient.html", fcode=fcode,
                                                     dob=dob, height=height, weight=weight, eff_dict=eff_dict, visit=n_visit, first=firstname, sur=surname))
                resp.set_cookie('session', id)
                return resp

        except Exception as e:
            print(e)
            flash('Login Failed!', 'danger')
            return redirect(url_for('login'))


# #################### Tech-admin's page #################### #
@app.route('/techadmin', methods=['GET', 'POST'])
def techadmin():
    if request.method == 'GET':
        stop_date = datetime.today()
        start_date = stop_date - timedelta(days=7)
        log = mDB.retrieve_login(time_start=start_date, time_stop=stop_date)
        log_dict = count_login(log)
        n_login = table_login(mDB.retrieve_login())
        n_users = len(mDB.list_all_users(userType=None))
        n_patients = len(mDB.list_all_users(userType="P"))
        n_medicians = len(mDB.list_all_users(userType="M"))
        n_techs = len(mDB.list_all_users(userType="T"))
        id = request.cookies.get('session')
        if check_cook(id, 'T'):
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            return render_template("/techadmin.html", log_dict=log_dict, login=n_login, users=n_users, pat=n_patients, med=n_medicians, tech=n_techs, first=firstname, sur=surname)
        else:
            return redirect("login")


# Tech-admin Function addUser
@app.route('/addUser', methods=['GET', 'POST'])
def add_user():

    if request.method == 'GET':
        id = request.cookies.get('session')
        user_obj = user_dict[id]
        firstname = user_obj.getFirstName()
        surname = user_obj.getSurname()
        return render_template("addUser.html", first=firstname, sur=surname)

    if request.method == 'POST':
        try:
            dict_usr = adduser_dict(mDB, request.form)
            mDB.add_user(User(dict_usr))
            return redirect("techadmin")
        except ValueError:

            return redirect("addUser")

# Tech-admin Function select User


@app.route('/selectUser', methods=['GET', 'POST'])
def select_user():
    if request.method == 'GET':
        res = mDB.list_all_users()
        id = request.cookies.get('session')
        if check_cook(id, 'T'):
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            return render_template("selectUser.html", user=res, first=firstname, sur=surname)
        else:
            return redirect("login")

    if request.method == 'POST':
        userdetails = request.form
        username = userdetails['username']
        user = mDB.retrieve_user(username)
        dict = User(user).getDictionary()
        dict['DateOfBirth'] = format_date(dict['DateOfBirth'])
        return redirect(url_for("edit_user", user=json.dumps(dict), sort_keys=True))


# Tech-admin Function edit User
@app.route('/editUser', methods=['GET', 'POST'])
def edit_user():
    if request.method == 'GET':
        user = json.loads(request.args['user'])
        id = request.cookies.get('session')
        if check_cook(id, 'T'):
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            return render_template("editUser.html", user=user, first=firstname, sur=surname)
        else:
            return redirect("login")

    if request.method == 'POST':
        if request.form['nome'] == 'EDIT USER':
            userdetails = request.form
            id = userdetails['id']
            username = userdetails['username']
            password = userdetails['password']
            usertype = userdetails['usertype']
            specialization = userdetails['specialization']
            unit = userdetails['unit']
            firstname = userdetails['firstname']
            surname = userdetails['surname']
            fc = userdetails['fc']
            d = int(userdetails['dob'][0:2])
            m = int(userdetails['dob'][3:5])
            y = int(userdetails['dob'][6:])
            dateofbirth = date(day=d, month=m, year=y)
            sex = userdetails['sex']
            if not usertype == "M":
                specialization = None
                unit = None
            user = {'ID': id, 'Username': username, 'Password': password, 'UserType': usertype, 'Specialization': specialization,
                    'Unit': unit, 'FirstName': firstname, 'Surname': surname, 'FiscalCode': fc, 'DateOfBirth': dateofbirth, 'Sex': sex}
            mUser = User(user)
            mDB.edit_user(mUser)
            return redirect("techadmin")

        if request.form['nome'] == 'DELETE USER':
            userdetails = request.form
            id = userdetails['id']
            mDB.remove_user(id)
            return redirect("techadmin")


# #################### Patient's page #################### #
@app.route('/patient', methods=['GET', 'POST'])
def patient():
    if request.method == 'GET':
        id = request.cookies.get('session')
        stop_date = datetime.today()
        start_date = stop_date - timedelta(days=7)
        eff_list = mDB.retrieve_parameters(
            "SleepEfficiency", patient=id, time_start=start_date, time_stop=stop_date)
        eff_dict = eff_graph(eff_list, days=7)
        if check_cook(id, 'P'):
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            fcode = user_obj.getFiscalCode()
            dob = format_date(user_obj.getDateOfBirth())
            param = mDB.retrieve_parameters("BodyMeasure", patient=id, last=True)
            if len(param) > 0:
                height = str(param[0][4]) + " cm"
                weight = str(param[0][5]) + " Kg"
            else:
                height = "No data"
                weight = "No data"
            vis = mDB.retrieve_visit(id, future=True)
            n_visit = table_visit(vis)

            return render_template("patient.html", fcode=fcode, dob=dob, height=height, weight=weight, eff_dict=eff_dict, visit=n_visit, first=firstname, sur=surname)

        else:
            return redirect("login")


# Patient Function psqi
@app.route('/psqi', methods=['GET', 'POST'])
def psqi():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'P'):
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            return render_template("psqi.html", first=firstname, sur=surname)
        else:
            return redirect("login")

    if request.method == 'POST':
        id = request.cookies.get('session')
        psqi = TestPSQI(request.form)
        mDB.insert_PSQI(id, json.dumps(psqi.test), psqi.score)
        return redirect("patient")


# Patient Function sleep efficiency
@app.route('/sleepEff', methods=['GET', 'POST'])
def sleep_eff():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'P'):
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            return render_template("sleepEff.html", first=firstname, sur=surname)
        else:
            return redirect("login")

    if request.method == 'POST':
        id = request.cookies.get('session')
        eff = TestEff(request.form)
        subj = request.form['subj']
        mDB.insert_sleep_efficiency(id, json.dumps(eff.test), int(eff.score), int(subj))
        return redirect("patient")


# Patient Function insert Parameter at Home
@app.route('/insertParamHome', methods=['GET', 'POST'])
def insert_param_home():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'P'):
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            return render_template("insertParamHome.html", first=firstname, sur=surname)
        else:
            return redirect("login")

    if request.method == 'POST':
        id = request.cookies.get('session')
        userdetails = request.form
        height = userdetails['height']
        weight = userdetails['weight']
        foodcalories = userdetails['foodcalories']
        hoursofactivity = userdetails['hoursofactivity']
        file = request.files['file']
        tmp = file.read().decode()
        tmp = tmp.split(", ")
        hr = int(tmp[0])
        dbp = int(tmp[1])
        sbp = int(tmp[2])
        mDB.insert_BP(id, dbp, sbp, hr)
        mDB.insert_activity(id, int(hoursofactivity))
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if not (height == "" or weight == ""):
            mDB.insert_body_measure(id, height, weight, visitID=None)
        if not foodcalories == "":
            mDB.insert_calories(id, foodcalories)
        return redirect("patient")


# Patient Function visualize statistics
@app.route('/visualizeStatistics', methods=['GET', 'POST'])
def visualize_statistics():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'P'):
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            hr, sbp, dbp, bmi, cal, act, psq, qua, eff, psl, dict_tresh = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
            return render_template("visualizeStatistics.html", thresh=dict_tresh, first=firstname, sur=surname, hr=hr, sbp=sbp, dbp=dbp, bmi=bmi, cal=cal, act=act, psq=psq, qua=qua, eff=eff, psl=psl, sort_keys=True)
        else:
            return redirect("login")

    if request.method == 'POST':
        id = request.cookies.get('session')
        print(request.form)
        user_obj = user_dict[id]
        firstname = user_obj.getFirstName()
        surname = user_obj.getSurname()

        try:
            vizdict = vizstats_dict(mDB, id, request.form)
            tresh = mDB.retrieve_threshold(id)

            dict_tresh = {}
            keys = ["ID", "PatientID", "HRMin", "HRMax", "SPMin", "SPMax", "DPMin", "DPMax", "BMIMin", "BMIMax", "ActivityMin",
                    "ActivityMax", "StressMin", "StressMax", "PSQIMin", "PSQIMax", "SleepEffMin", "SleepEffMax", "CaloriesMin", "CaloriesMax"]

            for i in range(len(keys)):
                dict_tresh[keys[i]] = tresh[0][i]
            return render_template("visualizeStatistics.html", thresh=dict_tresh, first=firstname, sur=surname, hr=vizdict['hr'], sbp=vizdict['sbp'], dbp=vizdict['dbp'], bmi=vizdict['bmi'], cal=vizdict['cal'], act=vizdict['act'], psq=vizdict['psq'], qua=vizdict['qua'], eff=vizdict['eff'], psl=vizdict['psl'], sort_keys=True)
        except IndexError:
            hr, sbp, dbp, bmi, cal, act, psq, qua, eff, psl, dict_tresh = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
            return render_template("visualizeStatistics.html", thresh=dict_tresh, first=firstname, sur=surname, hr=hr, sbp=sbp, dbp=dbp, bmi=bmi, cal=cal, act=act, psq=psq, qua=qua, eff=eff, psl=psl, sort_keys=True)


# #################### Medician's page #################### #
@app.route('/medician', methods=['GET', 'POST'])
def medician():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'M'):
            user_obj = user_dict[id]
            all_patients = table_patient(mDB.list_patient())
            daily_patients = table_daily(mDB.retrieve_visit(user=id))
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            fcode = user_obj.getFiscalCode()
            dob = format_date(user_obj.getDateOfBirth())
            spec = user_obj.getSpecialization()
            unit = user_obj.getUnit()
            return render_template("medician.html", first=firstname, sur=surname, fcode=fcode, dob=dob, spec=spec, unit=unit, all_pat=all_patients, daily=daily_patients)
        else:
            return redirect("login")


# Medician Function select patient for booking a visit
@app.route('/selectUserBook', methods=['GET', 'POST'])
def select_user_book():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'M'):

            res = mDB.list_all_users(userType="P")
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            return render_template("selectUserBook.html", user=res, first=firstname, sur=surname)
        else:
            return redirect("login")

    if request.method == 'POST':
        userdetails = request.form
        patient_id = userdetails['username']
        medician_id = request.cookies.get('session')
        dict_id = {'PatientID': patient_id, 'MedicianID': medician_id}
        return redirect(url_for("book_visit", user=json.dumps(dict_id, sort_keys=True)))


# Medician Function book visit for a patient
@app.route('/bookVisit', methods=['GET', 'POST'])
def book_visit():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'M'):
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            user = json.loads(request.args['user'])
            return render_template("bookVisit.html", user=user, first=firstname, sur=surname)
        else:
            return redirect("login")

    if request.method == 'POST':
        userdetails = request.form
        pat = userdetails['PatientID']
        med = userdetails['MedicianID']
        date = userdetails['date']
        date = date.split()
        days = date[0]
        hour = date[1]
        xm = date[2]
        h = hour.split(':')[0]
        mi = hour.split(':')[1]

        tmp = days.split('/')
        m = tmp[0]
        d = tmp[1]
        y = tmp[2]

        if xm == "PM":
            if not int(h) == 12:
                h = int(h) + 12

        elif xm == "AM":
            if int(h) == 12:
                h = int(h) - 12

        date = datetime(int(y), int(m), int(d), int(h), int(mi), 00, 000)

        psg = userdetails['psg']
        mDB.book_visit(pat, med, date, PSG=int(psg))

        return redirect("medician")


# Medician Function select patient for edit a visit
@app.route('/selectVisit', methods=['GET', 'POST'])
def select_visit():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'M'):
            res = mDB.retrieve_visit(user=id, all=True)
            tmp_list = []
            for i in range(0, len(res)):
                tmp = list(res[i])
                tmp[9] = format_datetime(tmp[9])
                tmp_list.append(tuple(tmp))
            res = tmp_list
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            return render_template("selectVisit.html", visit=res, first=firstname, sur=surname)
        else:
            return redirect("login")

    if request.method == 'POST':
        userdetails = request.form
        visit_id = userdetails['username']
        return redirect(url_for("edit_visit", user=visit_id))


# Medician Function edit booked visit
@app.route('/editVisit', methods=['GET', 'POST'])
def edit_visit():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'M'):
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            visit_id = json.loads(request.args['user'])
            vis = mDB.retrieve_visit(1, visitID=visit_id)
            tmp = list(vis)
            tmp[3] = format_datetime(tmp[3])
            vis = tuple(tmp)
            return render_template("editVisit.html", first=firstname, sur=surname, visit=vis)
        else:
            return redirect("login")

    if request.method == 'POST':
        if request.form['nome'] == 'SAVE':
            userdetails = request.form
            print(userdetails)
            medician_id = userdetails['medicianID']
            visit_id = userdetails['visitID']
            patient_id = userdetails['patientID']
            visit_date = reverse_datetime(userdetails['visitDate'])
            if 'comp' in userdetails.keys():
                if userdetails['comp'] == '0':
                    print("dentro")
                    bps = userdetails['bps']
                    bpd = userdetails['bpd']
                    psg = userdetails['psg']
                    psgdiag = userdetails['psgdiagn']
                    comp = userdetails['comp']
                    anam = userdetails['anam']
                    diag = userdetails['dia']
                    note = userdetails['notes']
                    pres = userdetails['pres']
                    height = userdetails['height']
                    weight = userdetails['weight']
                    file_hr = request.files['hr']

                    comp = 1

                    hr = int(file_hr.read().decode())
                    filename_hr = secure_filename(file_hr.filename)

                    file_hr.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_hr))

                    mDB.insert_body_measure(patient_id, height, weight,
                                            visitID=visit_id, date=visit_date)
                    mDB.insert_BP(patient_id, int(bpd), int(bps), int(hr),
                                  visitID=visit_id, date=visit_date)
                    mDB.edit_visit(visit_id, patient_id, medician_id,
                                   visit_date, psg, comp, anam, diag, note, pres)

                    if psg == '1':
                        file_psg = request.files['psgres']
                        filename_psg = secure_filename(file_psg.filename)
                        file_psg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_psg))
                        file_path_psg = os.path.join(app.config['UPLOAD_FOLDER'], filename_psg)
                        mDB.insert_PSG(patient_id, visit_id, file_path_psg)

                elif userdetails['comp'] == '1':
                    note = userdetails['notes']
                    mDB.edit_visit(visit_id, None, None,
                                   None, None, None, None, None, note, None, Full=False)

            else:
                note = userdetails['notes']
                mDB.edit_visit(visit_id, None, None,
                               None, None, None, None, None, note, None, Full=False)

            return redirect(url_for('medician'))
        if request.form['nome'] == 'PSL':
            userdetails = request.form
            visit_id = userdetails['visitID']
            patient_id = userdetails['patientID']
            dict_id = {'VisitID': visit_id, 'PatientID': patient_id}
            return redirect(url_for("psl", user=json.dumps(dict_id, sort_keys=True)))

        if request.form['nome'] == 'BOOK':
            userdetails = request.form
            medician_id = userdetails['medicianID']
            patient_id = userdetails['patientID']
            dict_id = {'PatientID': patient_id, 'MedicianID': medician_id}
            return redirect(url_for("book_visit", user=json.dumps(dict_id, sort_keys=True)))


# Medician Function select patient for setting thresholds
@app.route('/selectUserThresh', methods=['GET', 'POST'])
def select_thresh():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'M'):
            res = mDB.list_all_users(userType="P")
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            return render_template("selectUserThresh.html", users=res, first=firstname, sur=surname)
        else:
            return redirect("login")

    if request.method == 'POST':
        userdetails = request.form
        user_id = userdetails['username']

        try:
            tresh = mDB.retrieve_threshold(user_id)
            dict_tresh = {}
            keys = ["ID", "PatientID", "HRMin", "HRMax", "SPMin", "SPMax", "DPMin", "DPMax", "BMIMin", "BMIMax", "ActivityMin",
                    "ActivityMax", "StressMin", "StressMax", "PSQIMin", "PSQIMax", "SleepEffMin", "SleepEffMax", "CaloriesMin", "CaloriesMax"]

            for i in range(len(keys)):
                dict_tresh[keys[i]] = tresh[0][i]

            return redirect(url_for("set_thresholds", user=json.dumps(dict_tresh, sort_keys=True)))
        except IndexError:
            return redirect(url_for("add_thresholds", user=json.dumps(user_id)))


# Medician Function add new Thresholds for patients
@app.route('/addThresholds', methods=['GET', 'POST'])
def add_thresholds():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'M'):
            user = json.loads(request.args['user'])
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            return render_template("addThresholds.html", user=user, first=firstname, sur=surname)
        else:
            return redirect("login")

    if request.method == 'POST':
        userdetails = request.form
        patient_id = userdetails['PatientID']
        hrmin = userdetails['HRMin']
        hrmax = userdetails['HRMax']
        spmin = userdetails['SPMin']
        spmax = userdetails['SPMax']
        dpmin = userdetails['DPMin']
        dpmax = userdetails['DPMax']
        bmimin = userdetails['BMIMin']
        bmimax = userdetails['BMIMax']
        actmin = userdetails['ActivityMin']
        actmax = userdetails['ActivityMax']
        stressmin = userdetails['StressMin']
        stressmax = userdetails['StressMax']
        psqimin = userdetails['PSQIMin']
        psqimax = userdetails['PSQIMax']
        effmin = userdetails['SleepEffMin']
        effmax = userdetails['SleepEffMax']
        calmin = userdetails['CaloriesMin']
        calmax = userdetails['CaloriesMax']

        tresh = {'PatientID': patient_id, 'HRMin': hrmin, 'HRMax': hrmax, 'SPMin': spmin, 'SPMax': spmax, 'DPMin': dpmin, 'DPMax': dpmax, 'BMIMin': bmimin, 'BMIMax': bmimax, 'ActivityMin': actmin,
                 'ActivityMax': actmax, 'StressMin': stressmin, 'StressMax': stressmax, 'PSQIMin': psqimin, 'PSQIMax': psqimax, 'SleepEffMin': effmin, 'SleepEffMax': effmax, 'CaloriesMin': calmin, 'CaloriesMax': calmax}

        mDB.add_threshold(patient_id, tresh)
        return redirect("medician")


# Medician Function set Thresholds
@app.route('/setThresholds', methods=['GET', 'POST'])
def set_thresholds():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'M'):
            user = json.loads(request.args['user'])
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            return render_template("setThresholds.html", user=user, first=firstname, sur=surname)
        else:
            return redirect("login")

    if request.method == 'POST':
        userdetails = request.form
        patient_id = userdetails['PatientID']
        hrmin = userdetails['HRMin']
        hrmax = userdetails['HRMax']
        spmin = userdetails['SPMin']
        spmax = userdetails['SPMax']
        dpmin = userdetails['DPMin']
        dpmax = userdetails['DPMax']
        bmimin = userdetails['BMIMin']
        bmimax = userdetails['BMIMax']
        actmin = userdetails['ActivityMin']
        actmax = userdetails['ActivityMax']
        stressmin = userdetails['StressMin']
        stressmax = userdetails['StressMax']
        psqimin = userdetails['PSQIMin']
        psqimax = userdetails['PSQIMax']
        effmin = userdetails['SleepEffMin']
        effmax = userdetails['SleepEffMax']
        calmin = userdetails['CaloriesMin']
        calmax = userdetails['CaloriesMax']

        tresh = {'PatientID': patient_id, 'HRMin': hrmin, 'HRMax': hrmax, 'SPMin': spmin, 'SPMax': spmax, 'DPMin': dpmin, 'DPMax': dpmax, 'BMIMin': bmimin, 'BMIMax': bmimax, 'ActivityMin': actmin,
                 'ActivityMax': actmax, 'StressMin': stressmin, 'StressMax': stressmax, 'PSQIMin': psqimin, 'PSQIMax': psqimax, 'SleepEffMin': effmin, 'SleepEffMax': effmax, 'CaloriesMin': calmin, 'CaloriesMax': calmax}

        mDB.edit_threshold(patient_id, tresh)
        return redirect("medician")


# Medician Function PercievedStress level
@app.route('/psl', methods=['GET', 'POST'])
def psl():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'M'):
            user = json.loads(request.args['user'])
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            return render_template("psl.html", user=user, first=firstname, sur=surname)
        else:
            return redirect("login")

    if request.method == 'POST':
        userdetails = request.form
        survey = {}

        patient_id = userdetails['PatientID']
        visit_id = userdetails['VisitID']
        q1 = int(userdetails['quest1'])
        q2 = int(userdetails['quest2'])
        q3 = int(userdetails['quest3'])
        q4 = int(userdetails['quest4'])
        q5 = int(userdetails['quest5'])
        q6 = int(userdetails['quest6'])
        q7 = int(userdetails['quest7'])
        q8 = int(userdetails['quest8'])
        q9 = int(userdetails['quest9'])
        q10 = int(userdetails['quest10'])

        survey["quest1"] = q1
        survey["quest2"] = q2
        survey["quest3"] = q3
        survey["quest4"] = q4
        survey["quest5"] = q5
        survey["quest6"] = q6
        survey["quest7"] = q7
        survey["quest8"] = q8
        survey["quest9"] = q9
        survey["quest10"] = q10

        q4 = abs(q4 - 4)
        q5 = abs(q5 - 4)
        q7 = abs(q7 - 4)
        q8 = abs(q8 - 4)

        score = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9 + q10
        mDB.insert_stress_level(patient_id, visit_id, json.dumps(survey), score)

        return redirect('medician')


# Medician Function select patient to check abnormalities
@app.route('/selectPatAbno', methods=['GET', 'POST'])
def select_pat_abonrmal():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'M'):
            res = mDB.list_all_users(userType="P")
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            return render_template("selectPatAbno.html", user=res, first=firstname, sur=surname)
        else:
            return redirect("login")

    if request.method == 'POST':
        userdetails = request.form
        id = userdetails['username']
        return redirect(url_for("abnormal", user=id))


# Medician Function retrieve abnormalities
@app.route('/abnormal', methods=['GET'])
def abnormal():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'M'):
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            patient = json.loads(request.args['user'])
            activity = mDB.retrieve_count_abnormal("Activity", patient)[0]
            bp = mDB.retrieve_count_abnormal("BloodPressure", patient)[0]
            bm = mDB.retrieve_count_abnormal("BodyMeasure", patient)[0]
            cal = mDB.retrieve_count_abnormal("Calories", patient)[0]
            stress = mDB.retrieve_count_abnormal("PercievedStress", patient)[0]
            sleepqual = mDB.retrieve_count_abnormal("SleepQuality", patient)[0]
            sleepeff = mDB.retrieve_count_abnormal("SleepEfficiency", patient)[0]

            return render_template("abnormal.html", first=firstname, sur=surname, act=activity, bp=bp, bm=bm, cal=cal, stress=stress, sq=sleepqual, se=sleepeff)
        else:
            return redirect("login")


# Medician Function select patient's parameter
@app.route('/selectUserParam', methods=['GET', 'POST'])
def select_user_param():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'M'):
            res = mDB.list_all_users(userType="P")
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            return render_template("selectUserParam.html", user=res, first=firstname, sur=surname)
        else:
            return redirect("login")

    if request.method == 'POST':
        if request.form['nome'] == 'SELECT':
            userdetails = request.form
            patient_id = userdetails['username']
            patient_name = userdetails['search']
            dict_id = {'PatientID': patient_id, 'PatientName': patient_name}
            return redirect(url_for("select_param", user=json.dumps(dict_id, sort_keys=True)))
        if request.form['nome'] == 'ALL':
            return redirect("allParam")


# Medician Function select parameter to visualize across all patients list
@app.route('/allParam', methods=['GET'])
def all_param():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'M'):
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            all_dict = allstats_dict(mDB)
            dict_thresh = {}

            return render_template("allParam.html",  thresh=dict_thresh, first=firstname, sur=surname, hr=all_dict['HeartRate'], sbp=all_dict['SystolicBP'], dbp=all_dict['DyastolicBP'], bmi=all_dict['BMI'], cal=all_dict['DailyCalories'], act=all_dict['Hours'], psq=all_dict['PSQI'], qua=all_dict['SubjectiveSleep'], eff=all_dict['Efficiency'], psl=all_dict['StressLevel'], sort_keys=True)

        else:
            return redirect("login")


# Medician Function select parameter to visualize from the patient chosen before
@app.route('/selectParam', methods=['GET', 'POST'])
def select_param():
    if request.method == 'GET':
        id = request.cookies.get('session')
        if check_cook(id, 'M'):
            user = json.loads(request.args['user'])
            user_obj = user_dict[id]
            firstname = user_obj.getFirstName()
            surname = user_obj.getSurname()
            hr, sbp, dbp, bmi, cal, act, psq, qua, eff, psl, dict_tresh = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
            return render_template("selectParam.html", thresh=dict_tresh, first=firstname, sur=surname, user=user, hr=hr, sbp=sbp, dbp=dbp, bmi=bmi, cal=cal, act=act, psq=psq, qua=qua, eff=eff, psl=psl, sort_keys=True)

        else:
            return redirect("login")

    if request.method == 'POST':
        pat_id = request.form['patientID']
        pat_name = request.form['patientName']
        id = request.cookies.get('session')
        user_obj = user_dict[id]
        firstname = user_obj.getFirstName()
        surname = user_obj.getSurname()
        vizdict = vizstats_dict(mDB, pat_id, request.form)
        try:

            dict_id = {}
            tresh = mDB.retrieve_threshold(pat_id)
            dict_tresh = {}
            keys = ["ID", "PatientID", "HRMin", "HRMax", "SPMin", "SPMax", "DPMin", "DPMax", "BMIMin", "BMIMax", "ActivityMin",
                    "ActivityMax", "StressMin", "StressMax", "PSQIMin", "PSQIMax", "SleepEffMin", "SleepEffMax", "CaloriesMin", "CaloriesMax"]

            for i in range(len(keys)):
                dict_tresh[keys[i]] = tresh[0][i]
            return render_template("selectParam.html", thresh=dict_tresh, first=firstname, sur=surname, user=dict_id, hr=vizdict['hr'], sbp=vizdict['sbp'], dbp=vizdict['dbp'], bmi=vizdict['bmi'], cal=vizdict['cal'], act=vizdict['act'], psq=vizdict['psq'], qua=vizdict['qua'], eff=vizdict['eff'], psl=vizdict['psl'], sort_keys=True)
        except IndexError:
            dict_tresh = {}
            return render_template("selectParam.html", thresh=dict_tresh, first=firstname, sur=surname, user=dict_id, hr=vizdict['hr'], sbp=vizdict['sbp'], dbp=vizdict['dbp'], bmi=vizdict['bmi'], cal=vizdict['cal'], act=vizdict['act'], psq=vizdict['psq'], qua=vizdict['qua'], eff=vizdict['eff'], psl=vizdict['psl'], sort_keys=True)


# ########################## CONTACTS
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'GET':
        tech = mDB.list_all_users(userType="T")
        return render_template("contacts.html", tech=tech)


if __name__ == "__main__":
    app.run()
