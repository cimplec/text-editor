from flask import Flask, request, render_template, redirect, jsonify
import os
import time
import subprocess


app = Flask(__name__)

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = "my-secret-key"
app.config["SESSION_TYPE"] = "filesystem"

@app.route("/", methods=['GET'])
def index():

    if request.method == "GET":
        return render_template("index.html")

@app.route("/compile", methods=['POST'])
def compile():

    if request.method == "POST":
        simc_code = request.form['simc_code']

        filename = str(int(time.time()))
        simc_filename = os.path.join("static/code/", filename + ".simc")
        c_filename = os.path.join("static/code/", filename + ".c")

        with open(simc_filename, "w") as file:
            file.write(simc_code)

        output = subprocess.getoutput(f"simc {simc_filename}")
        print(output)

        if "simc: not found" in output:
            return jsonify({"status": "error", "message": "simC not installed, ask an admin to do so!"})
        
        if "[Line" in output:
            return jsonify({"status": "error", "message": output})

        try:
            with open(c_filename, "r") as file:
                c_code = file.read()
        except:
            return jsonify({"status": "error", "message": "Unknown error!"})

        return jsonify({"status": "success", "message": c_code})

@app.route("/update-simc", methods=['GET'])
def update_simc():

    if request.method == "GET":
        _ = subprocess.getoutput("pip uninstall simc -y")
        _ = subprocess.getoutput("pip install git+https://github.com/cimplec/sim-c")

        return jsonify({"status": "sim-C upgraded successfully!"})