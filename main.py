from datetime import datetime

from flask import Flask, jsonify, request

from database import SQL

app = Flask(__name__)
AB=SQL()

def cmd(line):
    AB.command(line)
    print(line)

try:
    AB.create_database("boiler")
    print("Database created")
except:
    print("Database exists")
AB.connect("boiler")
try:
    AB.create_table("log (time VARCHAR(255), value INT)")
    print("log table created")
except:
    print("log table exists")

with open("log.txt", 'w', encoding="utf-8") as write:
    print("Time\t\tTermometer value", file=write)

def rt_temp_check():
    AB.connect("boiler")
    try:
        AB.create_table("rt_temp (active BOOL, userValue INT, meterValue INT)") # meterValue is termometer value
        print("rt_temp table created")
    except:
        print("rt_temp table exists") #rt_temp means real time temperature
    try:
        data=AB.get_all("rt_temp")
        if (data[0][1] < data[0][2]):
            return("rt_record does excist")
    except:
        AB.create_rt_temp_record()

def check():
    rt_temp_check()
    data=AB.get_all("rt_temp")
    print(data)
    if (AB.get_user() < AB.get_meter()):
        line="UPDATE rt_temp SET active = 1;"
        AB.set_active(1)
    else:
        line="UPDATE rt_temp SET active = 0;"
        AB.set_active(0)
    cmd(line)

def data_getter(tp): #tp means type
    rt_temp_check()
    data=request.get_json()[tp]
    line="UPDATE rt_temp SET "+tp+" = "+str(data)
    print(line)
    cmd(line)
    check()
    return(data)

@app.route("/termometer-input", methods=["POST"])
def termometer_input(): #input json{"meterValue" : 22}
    termometer=data_getter("meterValue")
    AB.set_meter(termometer)
    line="INSERT INTO log (currentTime, meterValue) VALUES ('"+str(datetime.now().strftime("%H.%M.%S"))+"', "+str(termometer)+" )" # meterValue is termometer value
    cmd(line)
    with open("log.txt", 'a', encoding="utf-8") as write:
        print(str(datetime.now().strftime("%H.%M.%S"))+"\t"+str(termometer), file=write)
    return(jsonify({"termometerValue" : termometer}))

@app.route("/user-input", methods=["POST"])
def user_input(): #input json{"userValue" : 22}
    user=data_getter("userValue")
    AB.set_user(user)
    return(jsonify({"userValue" : user}))

@app.route("/get-data")
def get_data():
    rt_temp_check()
    data=AB.get_all("rt_temp")
    print(data)
    return(jsonify({"Status" : data[0][0], "User value" : data[0][1], "Termometer value" : data[0][2]}))

@app.route("/get-log")
def get_log():
    data=AB.get_all("log")
    output={}
    for i in range(len(data)):
        output[str(i+1)+" Termometer value"] = data[i][0]
        output[str(i+1)+" Time"] = data[i][1]
    return(jsonify(output))

if (__name__ == "__main__") :
    app.run(debug=True)