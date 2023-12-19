import time
from datetime import datetime
from multiprocessing import Process
from threading import Timer

from flask import Flask, jsonify, request

from database import SQL

app = Flask(__name__)
AB=SQL()
AB.connect("boiler")

def logging():
    data=AB.get_all("rt_temp")
    cmd="INSERT INTO log (currentTime, meterValue) VALUES ('"+str(datetime.now().strftime("%H.%M.%S"))+"', "+str(data[0][2])+" )" # meterValue is termometer value
    AB.command(cmd)
    Timer(5*60, logging).start()

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
    AB.command(cmd)
    check()
    return(data)

@app.route("/termometer-input", methods=["POST"])
def termometer_input():
    termometer=data_getter("meterValue")
    return(jsonify({"termometerValue" : termometer}))

@app.route("/user-input", methods=["POST"])
def user_input():
    user=data_getter("userValue")
    return(jsonify({"userValue" : user}))

@app.route("/get-data")
def get_data():
    data=AB.get_all("rt_temp")
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
    Timer(1, logging).start()
    app.run(debug=True)