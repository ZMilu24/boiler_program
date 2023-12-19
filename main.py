from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/termometer-input")
def termometer_input():
    termometer=request.get_json()["termoValue"]
    return(jsonify({"termometerValue" : termometer}))

@app.route("/user-input")
def user_input():
    user=request.get_json()["userValue"]
    return(jsonify({"userValue" : user}))

@app.route("/get-data")
def get_data():
    data=request.get_json()["termoValue"]
    return(jsonify({"userValue" : data}))

if (__name__ == "__main__") :
    app.run(debug=True)