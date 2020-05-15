#!/usr/bin/env python3

"""Create the databse structure with attributes and methods."""

from os import listdir
from os.path import isfile, join, splitext, basename
from datetime import date, datetime, timedelta
import json
from data_process import compute_bmi
import sqlite3

path = "database/"
file = "data.db"


class DBError(Exception):
    """Raised when DB opera tion do not yeild expected results"""
    pass


class User(object):
    """Class to Handle the User-Related data from the DB or client\n"""
    '''
    Constructor: User(param)
    param   can be a tuple containing:
            (ID,Username, Password, UserType, Specialization, Unit, FirstName, Surname, FiscalCode, DateOfBirth, Sex)
            in order, as returned from a SELECT * FROM User query
    param   can be also a dictionary containing the same keynames as the tuple above
    Raises TypeError if tuple is of the wrong lenght, if the dictionary contains an unknown key, or input type is not recongized
    '''

    def __init__(self, user=None):
        self.keyList = ("ID", "Username", "Password", "UserType", "Specialization",
                        "Unit", "FirstName", "Surname", "FiscalCode", "DateOfBirth", "Sex")
        self.userDictionary = {}
        if type(user) == tuple:
            if not len(user) == len(self.keyList):
                raise ValueError

            for i in range(len(user)):
                self.userDictionary[self.keyList[i]] = user[i]

        elif type(user) == dict:
            for i in user:
                if i not in self.keyList:
                    raise ValueError
                self.userDictionary[i] = user[i]
        elif user is not None:
            raise TypeError

    # -------------GETTERS AND SETTERS FOR EVERY KEY
    def getID(self):
        return self.userDictionary.get("ID")

    def setID(self, ID):
        self.userDictionary["ID"] = ID

    def getUsername(self):
        return self.userDictionary.get("Username")

    def setUsername(self, Username):
        self.userDictionary["Username"] = Username

    def getPassword(self):
        return self.userDictionary.get("Password")

    def setPassword(self, Password):
        self.userDictionary["Password"] = Password

    def getUserType(self):
        return self.userDictionary.get("UserType")

    def setUserType(self, UserType):
        self.userDictionary["UserType"] = UserType

    def getSpecialization(self):
        return self.userDictionary.get("Specialization")

    def setSpecialization(self, Specialization):
        self.userDictionary["Specialization"] = Specialization

    def getUnit(self):
        return self.userDictionary.get("Unit")

    def setUnit(self, Unit):
        self.userDictionary["Unit"] = Unit

    def getFirstName(self):
        return self.userDictionary.get("FirstName")

    def setFirstName(self, FirstName):
        self.userDictionary["FirstName"] = FirstName

    def getDateOfBirth(self):
        return self.userDictionary.get("DateOfBirth")

    def setDateOfBirth(self, DateOfBirth):
        self.userDictionary["DateOfBirth"] = DateOfBirth

    def getSurname(self):
        return self.userDictionary.get("Surname")

    def setSurname(self, Surname):
        self.userDictionary["Surname"] = Surname

    def getFiscalCode(self):
        return self.userDictionary.get("FiscalCode")

    def setFiscalCode(self, FiscalCode):
        self.userDictionary["FiscalCode"] = FiscalCode

    def getSex(self):
        return self.userDictionary.get("Sex")

    def setSex(self, Sex):
        self.userDictionary["Sex"] = Sex

    def getDictionary(self):
        return self.userDictionary


class Database(object):
    """Database class for monitoring system for sleep quality."""

    def __init__(self, path, file):
        """Initializate Database class."""
        self.path = path
        self.file = file
        self.fileList = [f for f in listdir(
            self.path) if isfile(join(self.path, f))]
        self.db_init()

    def db_init(self):
        """Check if the database is already present, if not, calls the table creator"""
        if self.file not in self.fileList:
            self._createtables()

    # -----------------------------------TECH ADMIN QUERIES

    def is_user(self, username):
        """Query to Check if username is present in the database.\n
        Keywords:\n
        username:   str     with the username you wisht to search for within the DB

        RETURNS:    bool    True or False
        """
        conn, c = self._connect()
        c.execute('''SELECT count(*) FROM User where Username=?''', (username,))
        count = c.fetchone()[0]
        self._disconnect(conn, c)
        if count:
            return True
        else:
            return False

    def list_all_users(self, userType=None):
        """Returns a list of sql formatted user. Can be filtered by type

        Keywords:

        userType: (optional) char: must be either M, T, or P

        RETURN: (void)"""
        conn, c = self._connect()
        if userType is not None:
            c.execute('''SELECT * FROM User WHERE UserType =?''', (userType,))
        else:
            c.execute('''SELECT * FROM User''')
        res = c.fetchall()
        self._disconnect(conn, c)
        return res

    def retrieve_user(self, userName=None, userID=None):
        """Query to list users

        Keywords:

        userName: Default=None, str containing the User Name as is stored inside the DB

        userID: Default=None, str containing the UserID as is stored inside the DB

        RETURN: list[User.class()] containg all users if UserName=None and userID=None
                (tuple) if UserName = (str) or UserID=(int)
        """
        conn, c = self._connect()
        if (userName is not None) and (userID is not None):
            c.execute("SELECT * FROM User")
            res = c.fetchall()
            userList = []
            for i in res:
                userList.append(User(i))
            res = userList
        elif userName is not None:
            c.execute('''SELECT * FROM User WHERE Username=?''',
                      (userName, ))  # User needs to be a tuple
            res = c.fetchone()
        elif userID is not None:
            c.execute('''SELECT * FROM User WHERE ID=?''',
                      (userID, ))  # User needs to be a tuple
            res = c.fetchone()
        else:
            raise TypeError
        self._disconnect(conn, c)
        return res

    def retrieve_login(self, day=datetime.today(), time_start=None, time_stop=None):
        """Query to list all the Log access within a certain day, or specific timestamps.\n
        Keywords:

        day: datetime.datetime of a specific date i.e. datetime.date(year, month, day). Defaults datetime.date.today()\n
        time_start: datetime.datetime object, specifying the start of the Query\n
        time_stop: datetime.datetimeobject, specifying the end of the Query. Need to specify both start and stop

        RETURN: list[(UserID, Access)]"""

        # if timestamps are inserted, they take precedence
        if (time_start is None) or (time_stop is None):
            # starts the query at 00:00:00
            time_start = datetime.combine(day, datetime.min.time())
            time_stop = datetime.combine(day, datetime.min.time(
            )) + timedelta(days=1) - timedelta(seconds=1)  # ends the query at 23:59:59

        conn, c = self._connect()
        c.execute('''SELECT P.UserID, P.Access, U.UserType FROM Platform as P, User as U where U.ID=P.UserID AND Access between ? and ?''', (time_start, time_stop,))
        res = c.fetchall()
        self._disconnect(conn, c)
        return res

    def add_user(self, user):
        """Adds new user to the access database.  \n
        Keywords:\n
        user: User class Object. Warning: uncomplete fields are NULL Value. Most User Fields are marked as NOT NULL inside the DB

        RETURN: (void)

        Raises DBError if User is already present"""

        # TODO: Add other controls for field completeness??

        conn, c = self._connect()
        if not self.is_user(user.getUsername()):
            c.execute('''INSERT INTO User(Username, Password, UserType, Specialization, Unit, FirstName, Surname, FiscalCode, DateOfBirth, Sex) VALUES(?,?,?,?,?,?,?,?,?,?)''', (user.getUsername(),
                                                                                                                                                                                 user.getPassword(), user.getUserType(), user.getSpecialization(), user.getUnit(), user.getFirstName(), user.getSurname(), user.getFiscalCode(), user.getDateOfBirth(), user.getSex()))
        else:
            raise DBError("Username is already present")
        self._disconnect(conn, c)

    def edit_user(self, user):
        """Adds new user to the access database.  \n
        Keywords:\n
        user: User class Object. Warning: uncomplete fields are NULL Value. Most User Fields are marked as NOT NULL inside the DB

        RETURN: (void)

        Raises DBError if User is not present"""
        conn, c = self._connect()
        c.execute('''UPDATE User
        SET
        Username=?,
        Password=?,
        UserType=?,
        Specialization=?,
        Unit=?,
        FirstName=?,
        Surname=?,
        FiscalCode=?,
        DateOfBirth=?,
        Sex=?
        WHERE
        ID=?
        ''', (user.getUsername(), user.getPassword(), user.getUserType(), user.getSpecialization(), user.getUnit(), user.getFirstName(), user.getSurname(), user.getFiscalCode(), user.getDateOfBirth(), user.getSex(), user.getID()))
        self._disconnect(conn, c)

    def remove_user(self, userID):
        """Deletes from database the selected user and each record bound to them

        Keywords:

        userID: int UserID as stored inside the DB

        RETRUN: (void) """
        conn, c = self._connect()
        c.execute('''DELETE FROM User WHERE ID=?''', (userID,))
        self._disconnect(conn, c)

    # -----------------------------------MEDICIAN QUERIES

    def add_threshold(self, userID, values):
        """ HRMin integer,  HRMax integer,
        SPMin integer,  SPMax integer,
        DPMin integer,  DPMax integer,
        BMIMin DECIMAL(5,2),  BMIMax DECIMAL(5,2),
        ActivityMin integer,  ActivityMax integer,
        StressMin integer,  StressMax integer,
        PSQIMin integer,  PSQIMax integer,
        SleepEffMin integer,  SleepEffMax integer,
        CaloriesMin integer,  CaloriesMax integer,"""

        conn, c = self._connect()
        c.execute('''INSERT INTO Thresholds(PatientID,
        HRMin,  HRMax,
        SPMin,  SPMax,
        DPMin,  DPMax,
        BMIMin,  BMIMax,
        ActivityMin,  ActivityMax,
        StressMin,  StressMax,
        PSQIMin,  PSQIMax,
        SleepEffMin,  SleepEffMax,
        CaloriesMin,  CaloriesMax) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (userID, values['HRMin'],  values['HRMax'], values['SPMin'],  values['SPMax'], values['DPMin'],  values['DPMax'], values['BMIMin'],  values['BMIMax'], values['ActivityMin'],  values['ActivityMax'], values['StressMin'],  values['StressMax'], values['PSQIMin'],  values['PSQIMax'], values['SleepEffMin'],  values['SleepEffMax'], values['CaloriesMin'],  values['CaloriesMax']))

        self._disconnect(conn, c)

    def insert_PSG(self, userID, visitID, filepath):
        """Insert PSG data into the database. Requires the path for the uploaded file

        Keywords:

        userID: int UserID as stored inside the DB

        visitID: int VisitID as stored inside the DB

        filepath: str the path to the uploaded file

        RETURN: (void)"""

        conn, c = self._connect()
        c.execute('''INSERT INTO PSG(
            PatientID,
            VisitID,
            FileLog
        ) VALUES(?,?,?)''', (userID, visitID, filepath))
        self._disconnect(conn, c)

    def insert_stress_level(self, userID, visitID, survey, score):
        """
        Insert stress level survey data and final score into the DB

        Keywords:

        userID: int UserID as stored inside the DB

        visitID: int VisitID as stored inside the DB

        survey: dict dictionary containing the survey structure and answers

        score: final score

        RETURN: (void)
        """
        conn, c = self._connect()

        alert = self.check_threshold(userID, "Stress", score)

        c.execute('''INSERT INTO PercievedStress
        (
        PatientID,
        VisitID,
        SurveyData,
        StressLevel,
        Alert)
        VALUES(?,?,?,?,?)''', (userID, visitID, survey, score, alert))
        self._disconnect(conn, c)

    def retrieve_statistics(self, table, parameter):
        conn, c = self._connect()
        sql = '''SELECT PatientID, AVG(''' + parameter + ''') FROM ''' + \
            table + ''' GROUP BY PatientID'''
        c.execute(sql)
        res = c.fetchall()
        self._disconnect(conn, c)
        return res

    def retrieve_parameters(self, parameter, patient=None, last=False, time_start=None, time_stop=None):
        """returns a list of the selected physiological parameter for the selected user inside the chosen timeframe

        Keywords:

        parameter: str Name of the physiological parameter to retrieve. MUST be either Activity, BloodPressure, BodyMeasure, Calories, PSG, PercievedStress, SleepQuality

        patient: Default=None, if (int) inserted the data is specific to a single user, else, all users are taken in consideration

        last: bool Default= False. If true returns only the last parameter updated for the selected user (if any) or everyone (otherwhise)

        time_start: datetime object. start of the timeframe

        time_stop: datetime object. stop of the timeframe: BOTH START AND STOP MUST BE INSERTED, OTHERWISE IT DEFAULTS TO ALL RECORDS

        RETURNS: [(DEPENDS ON THE TABLE CHOSEN)]
        """
        conn, c = self._connect()
        if last:
            if patient is None:
                sql = '''SELECT * FROM ''' + parameter + \
                    ''' WHERE Recorded IN (SELECT MAX(Recorded) FROM ''' + \
                    parameter + ''' GROUP BY PatientID)'''
                c.execute(sql)
            else:
                sql = '''SELECT * FROM ''' + parameter + \
                    ''' WHERE PatientID=? AND Recorded IN (SELECT MAX(Recorded) FROM ''' + \
                    parameter + ''' GROUP BY PatientID)'''
                c.execute(sql, (patient,))
        else:
            if (time_start is None) or (time_stop is None):
                if patient is None:
                    # Returns ALL The thingssss!!!
                    sql = '''SELECT * FROM ''' + parameter
                    c.execute(sql)
                else:
                    sql = '''SELECT * FROM ''' + parameter + ''' WHERE PatientID=?'''
                    c.execute(sql, (patient, ))
            else:
                if patient is None:
                    sql = '''SELECT * FROM ''' + parameter + ''' WHERE Recorded BETWEEN ? and ?'''
                    c.execute(sql, (time_start, time_stop))
                else:
                    sql = '''SELECT * FROM ''' + parameter + \
                        ''' WHERE PatientID=? and (Recorded BETWEEN ? and ?)'''
                    c.execute(sql, (patient, time_start, time_stop))

        res = c.fetchall()
        self._disconnect(conn, c)
        return res

    def book_visit(self, patient, medician, visitDate, PSG=False):
        """Book a visit for the specified patient"""
        conn, c = self._connect()

        if not PSG:
            c.execute('''INSERT INTO Visit(
                PatientID,
                MedicianID,
                VisitDate,
                Complete
            ) VALUES(?,?,?,?)''', (patient, medician, visitDate, 0))
        else:
            c.execute('''INSERT INTO Visit(
                PatientID,
                MedicianID,
                VisitDate,
                PSG,
                Complete
            ) VALUES(?,?,?,?,?)''', (patient, medician, visitDate, PSG, 0))
        self._disconnect(conn, c)

    def edit_visit(self, VisitID, PatientID, MedicianID, VisitDate, PSG, Complete, Anamnesis, Diagnosis, Notes, Prescription):
        conn, c = self._connect()
        c.execute('''UPDATE Visit
        SET
        PatientID=?,
        MedicianID=?,
        VisitDate=?,
        PSG=?,
        Complete=?,
        Anamnesis=?,
        Diagnosis=?,
        Notes=?,
        Prescription=?
        WHERE
        ID=?
        ''', (PatientID, MedicianID, VisitDate, PSG, Complete, Anamnesis, Diagnosis, Notes, Prescription, VisitID))
        self._disconnect(conn, c)

    def list_patient(self):
        """List all patient and the last visit they participated in

        RETURNS: [(userID,FirstName,Surname,LastVisit)]"""
        conn, c = self._connect()
        c.execute('''SELECT U.ID, U.FirstName, U.Surname,  max(V.VisitDate) FROM Visit AS V, User AS U WHERE U.ID=V.PatientID AND V.Complete=1 GROUP BY V.PatientID''')
        res = c.fetchall()
        self._disconnect(conn, c)
        return res

    def retrieve_count_abnormal(self, parameter, patient, time_start=None, time_stop=None):
        """returns a list of the selected physiological parameter for the selected user inside the chosen timeframe

        Keywords:

        parameter: str Name of the physiological parameter to retrieve. MUST be either Activity, BloodPressure, BodyMeasure, Calories, PercievedStress, SleepQuality

        patient: int UserID corresponding to the patient

        time_start: datetime object. start of the timeframe

        time_stop: datetime object. stop of the timeframe: BOTH START AND STOP MUST BE INSERTED, OTHERWISE IT DEFAULTS TO ALL RECORDS

        RETURNS: [(DEPENDS ON THE TABLE CHOSEN)]
        """
        conn, c = self._connect()
        if (time_start is None) or (time_stop is None):
            c.execute('''SELECT count(*) FROM ''' + parameter +
                      ''' WHERE PatientID=? AND Alert=1''', (patient, ))
        else:
            c.execute('''SELECT count(*) FROM ''' + parameter +
                      ''' WHERE PatientID=? AND Alert=1 AND (Recorded BETWEEN ? and ?)''', (patient, time_start, time_stop))

        res = c.fetchone()
        self._disconnect(conn, c)
        return res

    # -----------------------------------PATIENT QUERIES

    def insert_calories(self, userID, calories):
        alert = self.check_threshold(userID, "Calories", int(calories))
        conn, c = self._connect()
        c.execute('''INSERT INTO Calories(
        PatientID,
        Recorded,
        DailyCalories,
        Alert) VALUES(?,?,?,?)''', (userID, datetime.today(), calories, alert))
        self._disconnect(conn, c)

    def insert_PSQI(self, userID, survey, PSQI):
        alert = self.check_threshold(userID, "PSQI", PSQI)
        conn, c = self._connect()
        c.execute('''INSERT INTO SleepQuality
            (
            PatientID,
            SurveyData,
            Recorded,
            PSQI,
            Alert)
            VALUES(?,?,?,?,?)''', (userID, survey, datetime.today(), PSQI, alert))
        self._disconnect(conn, c)

    def insert_sleep_efficiency(self, userID, survey, efficiency, subjective):
        alert = self.check_threshold(userID, "SleepEff", efficiency)
        conn, c = self._connect()
        c.execute('''INSERT INTO SleepEfficiency
            (
            PatientID,
            SurveyData,
            Recorded,
            Efficiency,
            SubjectiveSleep,
            Alert)
            VALUES(?,?,?,?,?,?)''', (userID, survey, datetime.today(), efficiency, subjective, alert))
        # TODO: add SubjectiveSleep field
        self._disconnect(conn, c)

    def insert_activity(self, userID, hours, filepath):
        """Insert Activity data into the database. Requires the path for the uploaded file

        Keywords:

        userID: int UserID as stored inside the DB

        filepath: str the path to the uploaded file"""

        alert = self.check_threshold(userID, "Activity", hours)

        conn, c = self._connect()
        c.execute('''INSERT INTO Activity(
            PatientID,
            Recorded,
            Hours,
            ActivityData,
            Alert
        )
        ''', (userID, datetime.today(), hours, filepath, alert))
        self._disconnect(conn, c)

    # -----------------------------------MED-PATIENT MIXED QUERIES

    def edit_threshold(self, userID, values):
        conn, c = self._connect()
        c.execute('''UPDATE Thresholds
        SET
        HRMin=?,  HRMax=?,
        SPMin=?,  SPMax=?,
        DPMin=?,  DPMax=?,
        BMIMin=?,  BMIMax=?,
        ActivityMin=?,  ActivityMax=?,
        StressMin=?,  StressMax=?,
        PSQIMin=?,  PSQIMax=?,
        SleepEffMin=?,  SleepEffMax=?,
        CaloriesMin=?,  CaloriesMax=?
        WHERE
        PatientID=?''', (values["HRMin"], values["HRMax"], values["SPMin"], values["SPMax"], values["DPMin"], values["DPMax"], values["BMIMin"], values["BMIMax"], values["ActivityMin"], values["ActivityMax"], values["StressMin"], values["StressMax"], values["PSQIMin"], values["PSQIMax"], values["SleepEffMin"], values["SleepEffMax"], values["CaloriesMin"], values["CaloriesMax"], userID))
        self._disconnect(conn, c)

    def check_threshold(self, patientID, parameter, value):
        """ HRMin integer,  HRMax integer,
        SPMin integer,
        DPMin integer,
        BMIMin DECIMAL(5,2),
        ActivityMin integer,
        StressMin integer,
        PSQIMin"""

        conn, c = self._connect()
        sql = '''SELECT ''' + parameter + '''Max, ''' + \
            parameter + '''Min FROM Thresholds WHERE PatientID=?'''
        c.execute(sql, (patientID,))
        res = c.fetchone()
        self._disconnect(conn, c)

        if (res[0] is None or value < res[0]) and (res[1] is None or value > res[1]):
            return 0
        else:
            return 1

    def retrieve_threshold(self, patientID):
        conn, c = self._connect()
        c.execute('''SELECT * FROM Thresholds WHERE PatientID=?''', (patientID, ))
        res = c.fetchall()
        self._disconnect(conn, c)
        return res

    def insert_BP(self, userID, DP, SP, HR, visitID=None, date=None):
        """Insert Into table Blood Pressure value

        Keywords:

        userID: int UserID as stored inside the DB

        DP: int Dyastolic pressure
        SP: int Systolic  pressure
        HR: inr Heart Rate

        RETURN: (Void)

        """

        alert = (self.check_threshold(userID, "HR", HR) or self.check_threshold(
            userID, "DP", DP) or self.check_threshold(userID, "SP", SP))

        conn, c = self._connect()
        if (visitID is not None) and (date is not None):
            c.execute('''INSERT INTO BloodPressure(
            PatientID ,
            VisitID,
            Recorded,
            SystolicBP,
            DyastolicBP,
            HeartRate,
            Alert) VALUES(?,?,?,?,?,?,?)''', (userID, visitID, date, SP, DP, HR, alert))
        else:
            c.execute('''INSERT INTO BloodPressure(
            PatientID ,
            Recorded,
            SystolicBP,
            DyastolicBP,
            HeartRate,
            Alert) VALUES(?,?,?,?,?,?)''', (userID, datetime.today(), SP, DP, HR, alert))
        self._disconnect(conn, c)

    def insert_body_measure(self, userID, height, weight, visitID=None, date=None):
        BMI = compute_bmi(int(height), int(weight))
        alert = self.check_threshold(userID, "BMI", BMI)
        conn, c = self._connect()
        if (visitID is not None) and (date is not None):
            c.execute('''INSERT INTO BodyMeasure(
            PatientID,
            VisitID,
            Recorded,
            Height,
            Weight,
            BMI,
            Alert) VALUES(?,?,?,?,?,?,?)''', (userID, visitID, date, height, weight, BMI, alert))
        else:
            c.execute('''INSERT INTO BodyMeasure(
            PatientID,
            Recorded,
            Height,
            Weight,
            BMI,
            Alert) VALUES(?,?,?,?,?,?)''', (userID, datetime.today(), height, weight, BMI, alert))
        self._disconnect(conn, c)

    def retrieve_visit(self, user, future=False, all=False, day=datetime.today(), time_start=None, time_stop=None, visitID=None):
        """Query to list all the visits access booked on a certain day, or within specific timestamps.
        Keywords:

        user: specifies the ID of one of the two actors of the visit (can use this function for both medician and patient) REQUIRED

        future: Boolean flag, if true returns all the visits from the day on. False by Default REQUIRES day

        all: Boolean flag, if true returns every visit booked by or for the user. Defaults at True other parameters are absent. If forced True, ignores other parameters

        day: datetime.datetime of a specific date i.e. datetime.date(year, month, day).

        time_start: datetime.datetime object, specifying the start of the Query. Overrides day

        time_stop: datetime.datetimeobject, specifying the end of the Query. Need to specify both start and stop"""

        conn, c = self._connect()
        if visitID is None:
            if all:
                c.execute('''SELECT
                        P.ID, P.FirstName, P.Surname,
                        M.ID, M.FirstName, M.Surname, M.Specialization, M.Unit,
                        V.ID, V.VisitDate, V.PSG
                        FROM
                        User as P, User as M, Visit as V
                        WHERE V.PatientID=P.ID and V.MedicianID=M.ID and (V.PatientID= ? or V.MedicianID= ?)
                        ORDER BY V.VisitDate ASC''', (user, user))
                res = c.fetchall()
            else:
                if time_start is None or time_stop is None:  # if timestamps are inserted, they take precedence
                    # starts the query at 00:00:00
                    time_start = datetime.combine(day, datetime.min.time())
                    if not future:
                        time_stop = datetime.combine(day, datetime.min.time(
                        )) + timedelta(days=1) - timedelta(seconds=1)  # ends the query at 23:59:59
                        c.execute('''SELECT
                        P.ID, P.FirstName, P.Surname,
                        M.ID, M.FirstName, M.Surname, M.Specialization, M.Unit,
                        V.ID, V.VisitDate, V.PSG
                        FROM
                        User as P, User as M, Visit as V
                        WHERE V.PatientID=P.ID and V.MedicianID=M.ID and (V.PatientID= ? or V.MedicianID= ?) and (V.VisitDate between ? and ?)
                        ORDER BY V.VisitDate ASC''', (user, user, time_start, time_stop))
                        res = c.fetchall()
                    else:
                        c.execute('''SELECT
                        P.ID, P.FirstName, P.Surname,
                        M.ID, M.FirstName, M.Surname, M.Specialization, M.Unit,
                        V.ID, V.VisitDate, V.PSG
                        FROM
                        User as P, User as M, Visit as V
                        WHERE V.PatientID=P.ID and V.MedicianID=M.ID and (V.PatientID= ? or V.MedicianID= ?) and (V.VisitDate > ?)
                        ORDER BY V.VisitDate ASC''', (user, user, time_start))
                        res = c.fetchall()
        else:
            c.execute('''SELECT * FROM Visit WHERE ID=?''', (visitID, ))
            res = c.fetchone()
        self._disconnect(conn, c)
        return res

    # -----------------------------------GENERAL USER FUNCTIONS

    def log_user_in(self, username, password):
        conn, c = self._connect()
        c.execute(
            '''SELECT * FROM User WHERE Username = ? AND Password=?''', (username, password))
        try:
            value = c.fetchone()
            c.execute('''INSERT INTO Platform(UserID,Access) VALUES(?,?)''',
                      (value[0], datetime.today()))
            self._disconnect(conn, c)
            return value  # template lul ---- Maybe Generate cookies?
        except TypeError:
            self._disconnect(conn, c)
            return False

    def _connect(self):
        conn = sqlite3.connect(self.path + self.file)
        c = conn.cursor()
        return conn, c

    def _disconnect(self, conn, c):
        conn.commit()
        c.close()

    def _createtables(self):
        """Table Creator"""

        conn, c = self._connect()

        c.execute('''CREATE TABLE IF NOT EXISTS User
        (
        ID integer PRIMARY KEY,
        Username varchar(255) NOT NULL UNIQUE,
        Password varchar(255) NOT NULL,
        UserType char NOT NULL,
        Specialization varchar(255),
        Unit varchar(255),
        FirstName varchar(255) NOT NULL,
        Surname varchar(255) NOT NULL,
        FiscalCode varchar(16) NOT NULL UNIQUE,
        DateOfBirth date NOT NULL,
        Sex char
        )
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS Visit
        (
        ID integer PRIMARY KEY,
        PatientID integer NOT NULL ,
        MedicianID integer NOT NULL,
        VisitDate timestamp,
        PSG Boolean,
        Complete Boolean,
        Anamnesis text,
        Diagnosis text,
        Notes text,
        Prescription text,
        UNIQUE(PatientID,MedicianID,VisitDate),
        FOREIGN KEY (PatientID) REFERENCES User(ID) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (MedicianID) REFERENCES User(ID) ON UPDATE CASCADE ON DELETE CASCADE
        )
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS Thresholds
        (
        ID integer PRIMARY KEY,
        PatientID integer NOT NULL ,
        HRMin integer,  HRMax integer,
        SPMin integer,  SPMax integer,
        DPMin integer,  DPMax integer,
        BMIMin DECIMAL(5,2),  BMIMax DECIMAL(5,2),
        ActivityMin integer,  ActivityMax integer,
        StressMin integer,  StressMax integer,
        PSQIMin integer,  PSQIMax integer,
        SleepEffMin integer,  SleepEffMax integer,
        CaloriesMin integer,  CaloriesMax integer,
        FOREIGN KEY (PatientID) REFERENCES User(ID) ON UPDATE CASCADE ON DELETE CASCADE
        )
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS BloodPressure
        (
        ID integer PRIMARY KEY,
        PatientID integer,
        VisitID integer,
        Recorded timestamp,
        SystolicBP integer,
        DyastolicBP integer,
        HeartRate integer,
        Alert boolean,
        FOREIGN KEY (PatientID) references User(ID) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (VisitID) references Visit(ID) ON UPDATE CASCADE ON DELETE CASCADE
        )
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS PSG
        (
        ID integer PRIMARY KEY,
        PatientID integer,
        VisitID integer,
        FileLog varchar,
        FOREIGN KEY (PatientID) references User(ID) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (VisitID) references Visit(ID) ON UPDATE CASCADE ON DELETE CASCADE
        )
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS Activity
        (
        ID integer PRIMARY KEY,
        PatientID integer,
        Recorded timestamp,
        Hours integer,
        ActivityData varchar,
        Alert boolean,
        FOREIGN KEY (PatientID) references User(ID) ON UPDATE CASCADE ON DELETE CASCADE
        )
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS BodyMeasure
        (
        ID integer PRIMARY KEY,
        PatientID integer,
        VisitID integer,
        Recorded timestamp,
        Height DECIMAL(5,2),
        Weight DECIMAL(5,2),
        BMI DECIMAL(5,2),
        Alert boolean,
        FOREIGN KEY (PatientID) references User(ID) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (VisitID) references Visit(ID) ON UPDATE CASCADE ON DELETE CASCADE
        )
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS PercievedStress
        (
        ID integer PRIMARY KEY,
        PatientID integer,
        VisitID integer,
        SurveyData text,
        StressLevel  integer,
        Alert boolean,
        FOREIGN KEY (PatientID) references User(ID) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (VisitID) references Visit(ID) ON UPDATE CASCADE ON DELETE CASCADE
        )
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS SleepQuality
        (
        ID integer PRIMARY KEY,
        PatientID integer,
        SurveyData text,
        Recorded timestamp,
        PSQI integer,
        Alert boolean,
        FOREIGN KEY (PatientID) references User(ID) ON UPDATE CASCADE ON DELETE CASCADE
        )
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS SleepEfficiency
        (
        ID integer PRIMARY KEY,
        PatientID integer,
        SurveyData text,
        Recorded timestamp,
        Efficiency integer,
        SubjectiveSleep integer,
        Alert boolean,
        FOREIGN KEY (PatientID) references User(ID) ON UPDATE CASCADE ON DELETE CASCADE
        )
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS Calories
        (
        ID integer PRIMARY KEY,
        PatientID integer,
        Recorded timestamp,
        DailyCalories integer,
        Alert boolean,
        FOREIGN KEY (PatientID) references User(ID) ON UPDATE CASCADE ON DELETE CASCADE
        )''')

        c.execute('''CREATE TABLE IF NOT EXISTS Platform
        (
        ID integer PRIMARY KEY,
        UserID integer,
        Access timestamp,
        FOREIGN KEY (UserID) references User(ID) ON UPDATE CASCADE ON DELETE CASCADE
        )
        ''')

        self._disconnect(conn, c)


if __name__ == "__main__":

    mDB = Database(path, file)
    mDB.db_init()
