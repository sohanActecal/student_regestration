from flask import Flask, redirect, url_for, request, render_template, session
import json
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'your secret key'
database_conn= open("config.json", 'r')
configuration= json.load(database_conn)
app.config['MYSQL_HOST'] = configuration['host']
app.config['MYSQL_USER'] = configuration['user']
app.config['MYSQL_PASSWORD'] = configuration['password']

app.config['MYSQL_DB'] = configuration['database']
mysql = MySQL(app)


# -----------------student registration -----------------------------
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

#----------------student detail---------------
@app.route('/')
def studentDetail():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from signin_detail")
    result = cur.fetchall()  
    return render_template("detail.html", result=result)
#-----------fee------------
@app.route('/fee')
def fee():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from signin_detail")
    result = cur.fetchall()
    return render_template("fee.html", result=result)

#-------------admin login--------------------- 
@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST' and 'user_name' in request.form and 'password' in request.form:
        username = request.form['user_name']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admin_login WHERE user_name = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True 
           
            return render_template('login.html',mag=msg)
            
        else:
            msg="login Successfully"
            return render_template('login.html',mag=msg)
    return render_template('login.html')
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
 
if __name__ == '__main__':
	app.run(debug=True)
