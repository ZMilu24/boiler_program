from datetime import datetime

from flask import Flask, jsonify, request

from database import SQL

app = Flask(__name__)
AB=SQL()
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
try:
    AB.create_table("rt_temp (active BOOL, userValue INT, meterValue INT)")
    print("rt_temp table created")
except:
    print("rt_temp table exists") #rt_temp means real time temperature
asd="INSERT INTO rt_temp (active, userValue, meterValue) VALUES (0, 0, 0)" # meterValue is termometer value
AB.command(asd)

def check():
    data=AB.get_all("rt_temp")
    if (data[0][1] > data[0][2]):
        cmd="UPDATE rt_temp SET active = 1"
    else:
        cmd="UPDATE rt_temp SET active = 0"
    AB.command(cmd)

def data_getter(tp): #tp means type
    data=request.get_json()[tp]
    cmd="UPDATE rt_temp SET "+tp+" = "+str(data)
    print(cmd)
    AB.command(cmd)
    #check()
    return(data)

@app.route("/termometer-input", methods=["POST"])
def termometer_input(): #input json{"meterValue" : 22}
    termometer=data_getter("meterValue")
    cmd="INSERT INTO log (currentTime, meterValue) VALUES ('"+str(datetime.now().strftime("%H.%M.%S"))+"', "+str(termometer)+" )" # meterValue is termometer value
    AB.command(cmd)
    return(jsonify({"termometerValue" : termometer}))

@app.route("/user-input", methods=["POST"])
def user_input(): #input json{"userValue" : 22}
    user=data_getter("userValue")
    return(jsonify({"userValue" : user}))

@app.route("/get-data")
def get_data():
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