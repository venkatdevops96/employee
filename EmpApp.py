from flask import Flask, render_template, request
import psycopg2
import os
import boto3
from config import *

app = Flask(__name__)

region = customregion
connection = psycopg2.connect(user = customuser,
                                  password = custompass,
                                  host = customhost,
                                  port = "5432",
                                  database = customdb)
output = {}
table = 'employee'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('AddEmp.html')


@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')


@app.route("/addemp", methods=['POST'])
def AddEmp():
    empid = request.form['emp_id']
    firstname = request.form['first_name']
    lastname = request.form['last_name']
    priskill = request.form['pri_skill']
    locati = request.form['location']
    cursor = connection.cursor()
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    emp_name = "" + firstname + " " + lastname
    try:
        cursor.execute(insert_sql, (empid, firstname, lastname, priskill, locati))
        # Uplaod image file in S3 #
        connection.commit()
        print ( connection.get_dsn_parameters(),"\n")

      # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")   
    print("all modification done...")
    return render_template('AddEmpOutput.html', name=emp_name)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
