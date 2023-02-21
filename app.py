from flask import Flask, redirect, url_for, request, render_template
import json
from flask_mysqldb import MySQL

app = Flask(__name__)


database_conn= open("config.json", 'r')
configuration= json.load(database_conn)
app.config['MYSQL_HOST'] = configuration['host']
app.config['MYSQL_USER'] = configuration['user']
app.config['MYSQL_PASSWORD'] = configuration['password']

app.config['MYSQL_DB'] = configuration['database']
mysql = MySQL(app)



@app.route('/add-student',methods=['GET','POST'])
def storeData():
    cur = mysql.connection.cursor()
     
    if request.method == 'POST' :
        #passing HTML form data into python variable
         
        student_name=request.form['student_name']
        r_no=request.form['registration_no']
        course_name=request.form['course_name']
        date= request.form['date']
        duration= request.form['duration']
        mobile_no= request.form['mobile_no']
        email=request.form ['email']
        address= request.form['address']
        cur.execute('INSERT INTO  signin_detail(student_name, registration_No, course, date_of_registration, duration, mobile_no, email, address) values("{}","{}","{}","{}","{}","{}","{}","{}")'.format(student_name,r_no,course_name,date,duration,mobile_no,email,address))
        mysql.connection.commit()
        return render_template("detail.html")
            
    return render_template("form.html")


@app.route('/')
def studentDetail():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from signin_detail")
    result = cur.fetchall()



    
    return render_template("detail.html", result=result)

@app.route('/fee')
def fee():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from signin_detail")
    result = cur.fetchall()
    return render_template("fee.html", result=result)
 
if __name__ == '__main__':
	app.run(debug=True)
