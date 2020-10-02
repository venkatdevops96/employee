from flask import Flask, render_template, request
from pymysql import connections
import psycopg2
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
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
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    pri_skill = request.form['pri_skill']
    location = request.form['location']
    cursor = connection.cursor()
    try:

        cursor.execute('''INSERT INTO employee(emp_id, first_name, last_name, pri_skill,
   location) VALUES (emp_id, first_name, last_name, pri_skill, location'''))
        connection.commit()
        emp_name = "" + first_name + " " + last_name
        # Uplaod image file in S3 #
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
