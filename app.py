from flask import Flask, request
import json
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET"])
def run_scraping():
    process = subprocess.Popen(["python", "data-entry.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    output = ""
    for line in process.stdout:
        output += line
        yield json.dumps({"message": line}) + "\n"

# @app.route("/")
# def index():
    # return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True)
