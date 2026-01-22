from flask import Flask, jsonify, request
from flask_cors import CORS # importerer cors for å tillate kobling fra andre domener
from dotenv import load_dotenv # importerer dotenv for å lese det som står i .env filen og for å gjøre det tigjengelig i Python
import os # importeres for å hente ting skrevet i .env filen
import mariadb # importeres for å kunne snakke med DB
from flask import Flask , render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/auth")
def auth():
    return render_template("auth.html")


if __name__ == "__main__":
    app.run(debug=True)

load_dotenv()
 
app = Flask(__name__)
CORS(app)
 
def db_connection(): # funskjonen for å koble til DB
        return mariadb.connect( # kobler på DB ved å bruke .env info
           host=os.getenv('DB_HOST'), # host
           user=os.getenv('DB_USER'), # bruker
           password=os.getenv('DB_PASS'), # passord
           database=os.getenv('DB_NAME') # database navn
           
        )
 
 