import mysql.connector

def ConnectToDatabase(host):
    db = mysql.connector.connect(
            host=host,
            db="GCDB",
            user="webuser",
            passwd="password"
        )

    return db

def TestConnection(con):

    cursor = con.cursor()

    cursor.execute("SELECT VERSION()")

    results = cursor.fetchone()

    if results:
        return True
    else:
        return False


def ExecQuery(con, query):
    if(con == None):
        return

    cursor = con.cursor()

    cursor.execute(query)

    for x in cursor:
        print(x)

def GetLaunchID(con, desc):
    dbCursor = con.cursor()

    LaunchID = dbCursor.execute("SELECT max(l_id) FROM LAUNCH WHERE l_description = \"" + desc + "\"")

    for x in dbCursor:
        return x[0]

def LoadLaunchID(con):
    dbCursor = con.cursor()

    user_in = input("Enter Launch ID: ")
    dbCursor.execute("SELECT l_id FROM LAUNCH WHERE l_id = "+user_in)

    for x in dbCursor:
        return x[0]

    return 0;


def InstertIntoLaunch(con, separation, end, desc):
    sqlString = "CALL usp_AddLaunch( NOW(), "+ separation+", "+ end+", \""+desc+"\")"

    dbCursor = con.cursor()
    dbCursor.execute(sqlString)
    con.commit()

    LaunchID = GetLaunchID(con, desc)

    return LaunchID

def InsertIntoTelemetryNosecone(con, launchID, GPSx, GPSy, altitude):
    sqlString = "CALL usp_AddTelemetry_Nosecone( "+str(launchID)+", "+GPSx+", "+GPSy+", "+altitude+")"

    dbCursor = con.cursor()
    dbCursor.execute(sqlString)
    con.commit()

def InsertIntoTelemetryVehicle(con, launchID, velocity, GPSx, GPSy, altitude, voltage, temp):
    sqlString = "CALL usp_AddTelemetry_Vehicle( "+str(launchID)+", "+velocity+", "+GPSx+", "+GPSy+", "+altitude+", "+voltage+", "+temp+")"

    dbCursor = con.cursor()
    dbCursor.execute(sqlString)
    con.commit()

def Main():
    IP = "192.168.0.101"
    LAUNCH_ID = 0

    print("River City Rocketry");
    print("Ground Computer Database Client")
    print("Written by: Tom Sarver")

    user_in = -1

    while(user_in != "0"):
        print("\n1) Set Connection Variables")
        print("2) Get Connection Variables")
        print("3) Test Database Connection")
        print("4) Query Database")
        print("5) New Launch")
        print("6) Load Launch")
        print("t) Execute Test Function")
        print("0) Exit")

        user_in = input("Option: ")
        if(user_in == "t"):
            testfxn()
        elif(user_in == "1"):
            option = input("Use Default Connection?(y/n): ")
            if(option.upper() == "Y"):
                IP = "192.168.0.101"
            else:
                user_ip = input("Host IP: ")
                IP = user_ip
        elif(user_in == "2"):
            print("\nHost: "+IP)
            print("Database: GCDB")
            print("User: webuser")

            print("\nLaunch ID: "+str(LAUNCH_ID))

        elif(user_in == "3"):
            test = TestConnection(ConnectToDatabase(IP))

            if(test == True):
                print("\nConnection Succeeded")
            else:
                print("\nConnection Failed")
        elif(user_in == "4"):
            q = input("db> ")

            db = ConnectToDatabase(IP)

            ExecQuery(db, q)
        elif(user_in == "5"):
            desc = input("Launch Description: ")

            db = ConnectToDatabase(IP)
            LAUNCH_ID = InstertIntoLaunch(db, "NULL", "NULL", desc)
        elif(user_in == "6"):
            db = ConnectToDatabase(IP)

            LAUNCH_ID = LoadLaunchID(db)

def testfxn():
    IP = "192.168.1.126"
    LAUNCH_ID = 0

    print("New Launch")

    db = ConnectToDatabase(IP)

    desc = input("Launch Description: ")
    LAUNCH_ID = InstertIntoLaunch(db, "NULL", "NULL", desc)
    print("LAUNCH_ID: "+str(LAUNCH_ID))

    #Insert Dummy Data
    InsertIntoTelemetryNosecone(db, LAUNCH_ID, "0.0", "0.0", "0.0")
    InsertIntoTelemetryNosecone(db, LAUNCH_ID, "0.0", "0.0", "0.0")
    InsertIntoTelemetryNosecone(db, LAUNCH_ID, "0.0", "0.0", "0.0")
    InsertIntoTelemetryNosecone(db, LAUNCH_ID, "0.0", "0.0", "0.0")
    InsertIntoTelemetryNosecone(db, LAUNCH_ID, "0.0", "0.0", "0.0")

    InsertIntoTelemetryVehicle(db, LAUNCH_ID, "0.0", "0.0", "0.0", "0.0", "0.0", "0.0")
    InsertIntoTelemetryVehicle(db, LAUNCH_ID, "0.0", "0.0", "0.0", "0.0", "0.0", "0.0")
    InsertIntoTelemetryVehicle(db, LAUNCH_ID, "0.0", "0.0", "0.0", "0.0", "0.0", "0.0")
    InsertIntoTelemetryVehicle(db, LAUNCH_ID, "0.0", "0.0", "0.0", "0.0", "0.0", "0.0")
    InsertIntoTelemetryVehicle(db, LAUNCH_ID, "0.0", "0.0", "0.0", "0.0", "0.0", "0.0")

Main()
#testfxn()