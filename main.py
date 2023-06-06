from flask import Flask, render_template,redirect, url_for, request,jsonify,session,flash,json
from flaskext.mysql import MySQL
from flask_mysqldb import MySQL,MySQLdb 
import MySQLdb.cursors
from werkzeug.utils import secure_filename
import os
#import magic
import urllib.request
from datetime import datetime



 
app = Flask(__name__)
       
app.secret_key = "caircocoders-ednalan-2020"
       
app.config['MYSQL_HOST'] = 'p3nlmysql85plsk.secureserver.net'
app.config['MYSQL_USER'] = 'gymdbuid'
app.config['MYSQL_PASSWORD'] = '!Bsg15a8'
app.config['MYSQL_DB'] = 'gymdb'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
 
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  
ALLOWED_EXTENSIONS = set(['WMV','AVI','3G2','mp4'])
ALLOWED_EXTENSIONS1 = set(['png', 'jpg', 'jpeg', 'gif','pdf'])

  
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def allowed_file1(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS1






 



  
#######index page#######


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        print("Its in get")
        print("1")
        return render_template("index.html")
    else:
        print("2")
        return render_template('Dashboard.html')






 ###########about page########################   
    
@app.route('/about', methods = ['GET', 'POST'])
def about():
    print("page open")
    return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template("contact.html")


@app.route('/gallery')
def gallery():
    return render_template("gallery.html")


@app.route('/plans')
def plans():
    return render_template("plans.html")



@app.route('/sports')
def sports():
    return render_template("sports.html")





##########   Login ###################
	
@app.route('/login',methods=['GET','POST'])
def log():
    msg = ''
    if request.method == 'POST': 
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM signup WHERE username = %s AND password = %s', (username, password, ))
        abc = cursor.fetchone()
        if abc:
            session['loggedin'] = True
            session['id'] = abc['id']
            session['username'] = abc['username']
            msg = 'Logged in successfully !'
            return render_template('UI/Student/dashboard.html', msg = msg)
        else:
            msg = 'Wrong Credential !'
            return render_template('login.html', msg = msg)
    else:
        return render_template("login.html")
    
################# Admin Login ####################

@app.route("/admin",methods=['GET','POST'])
def admin_login():
        msg = ''
        if request.method == 'POST': 
            username = request.form['username']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password, ))
            abc = cursor.fetchone()
            if abc:
                session['loggedin'] = True
                session['id'] = abc['id']
                session['username'] = abc['username']
                msg = 'Logged in successfully !'
                return render_template('UI/Admin/dashboard.html', msg = msg)
            else:
                msg = 'Wrong Credential !'
                return render_template('admin_login.html', msg = msg)
        else:
            return render_template("admin_login.html")
        


################# Coach Login ####################

@app.route("/coach",methods=['GET','POST'])
def coach_login():
        msg = ''
        if request.method == 'POST': 
            username = request.form['username']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM coach_regis WHERE username = %s AND password = %s', (username, password, ))
            abc = cursor.fetchone()
            if abc:
                session['loggedin'] = True
                session['id'] = abc['id']
                session['username'] = abc['username']
                msg = 'Logged in successfully !'
                return render_template('UI/Coach/dashboard.html', msg = msg)
            else:
                msg = 'Wrong Credential !'
                return render_template('coach_login.html', msg = msg)
        else:
            return render_template("coach_login.html")
        
        





############# signup ########

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        mobile=request.form['mobile']
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO signup (name,email,mobile,username,password) VALUES (%s,%s,%s,%s,%s)",(name,email,mobile,username,password))
        mysql.connection.commit()
        msg="Data Inserted Successfully"
        
        
        
        
        return render_template("login.html",msg=msg)
    else:
        
        return render_template("signup.html")
    
    

##################  Admin Dashboard ###############



@app.route('/UI/Admin/dashboard',methods=['GET','POST'])
def admin_dashboard():
    return render_template("UI/Admin/dashboard.html")

####################  Coach Dashboard ############

@app.route('/UI/Coach/dashboard',methods=['GET','POST'])
def coach_dashboard():
    if 'loggedin' in session:
        if request.method=='GET':
        
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT file_name FROM coach_regis WHERE id = % s', (session['id'], ))
            coach_regis = cursor.fetchone()   
    
    return render_template("UI/Coach/dashboard.html",coach_regis=coach_regis)


########### student dashboard ################

@app.route('/UI/Student/dashboard',methods=['GET','POST'])
def student_dashboard():
    return render_template("UI/Student/dashboard.html")



#############  coach registration ################
# @app.route("/UI/admin/coach_entry",methods=['GET','POST'])
# def coach_entry():
#     if request.method=='POST':
#         name=request.form['name']
#         email=request.form['email']
#         dateofbirth=request.form['dateofbirth']
#         phone=request.form['phone']
        
#         state=request.form['state']
#         district=request.form['district']
#         locality=request.form['locality']
#         gender=request.form['gender']
        
#         experience=request.form['experience']
        
#         username=request.form['username']
#         password=request.form['password']
#         cursor=mysql.connection.cursor()
        
        
#         cursor.execute("INSERT INTO coach_regis (name,email,dateofbirth,phone,state,district,locality,gender,experience,username,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,email,dateofbirth,phone,state,district,locality,gender,experience,username,password))
#         mysql.connection.commit()
#         msg="Data Inserted Successfully"
#         # cursor=mysql.connection.cursor()
#         # cursor.execute("SELECT * FROM coach_regis")
#         # coach_entry=cursor.fetchall()
        
#         return render_template("UI/Admin/coach_Registration.html",msg=msg)
#     else:
#         # cursor=mysql.connection.cursor()
#         # cursor.execute("SELECT * FROM coach_regis")
#         # coach_entry=cursor.fetchall()
#         return render_template("UI/Admin/coach_Registration.html")
    
    
    
###################  coach regitration with  image #################### 
    
@app.route("/UI/admin/coach_entry",methods=['GET','POST'])
def coach_entry():
    
    if request.method=='GET':
        
            
        return render_template("UI/Admin/coach_Registration.html")
    else:
        
        cursor = mysql.connection.cursor()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        now = datetime.now()
        if request.method=='POST':
            name=request.form['name']
            email=request.form['email']
            dateofbirth=request.form['dateofbirth']
            phone=request.form['phone']
            
            state=request.form['state']
            district=request.form['district']
            locality=request.form['locality']
            gender=request.form['gender']
            
            experience=request.form['experience']
            
            username=request.form['username']
            password=request.form['password']
            cursor=mysql.connection.cursor()
            
            files1 = request.files.getlist('files1[]')
            
            cursor=mysql.connection.cursor()
            print("files")
            for file in files1:
                if file and allowed_file1(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
                    cursor.execute("INSERT INTO coach_regis (name,email,dateofbirth,phone,state,district,locality,gender,experience,username,password,file_name,uploaded_on) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,email,dateofbirth,phone,state,district,locality,gender,experience,username,password,filename,now))
                    
                    cursor=mysql.connection.cursor()
                    
                    mysql.connection.commit()
                print("file")
            msg="Data Inserted Successfully"
                    
            # cursor=mysql.connection.cursor()
            # cursor.execute("SELECT id,coach_id,coach_name,student_id,name,email,dateofbirth,height,phone,state,district,locality,username,weight,bmi,gender,experience FROM student_registration")
            # student_registration=cursor.fetchall()
                
        return render_template("UI/Admin/coach_Registration.html",msg=msg)
    
    
    



#############  student registration ################
@app.route("/UI/Admin/student_registration",methods=['GET','POST'])
def studentregistration():
    if request.method=='GET':
        return render_template("UI/Admin/student_Registration.html")
    else:
        
        cursor = mysql.connection.cursor()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        now = datetime.now()
        if request.method=='POST':
            coach_id=request.form['coach_id']
            coach_name=request.form['coach_name']
            student_id=request.form['student_id']
            name=request.form['name']
            email=request.form['email']
            dateofbirth=request.form['dateofbirth']
            phone=request.form['phone']
            state=request.form['state']
            district=request.form['district']
            locality=request.form['locality']
            gender=request.form['gender']
            height=request.form['height']
            weight=request.form['weight']
            bmi=request.form['bmi']
            experience=request.form['experience']
            username=request.form['username']
            password=request.form['password']
            files1 = request.files.getlist('files1[]')
            
            cursor=mysql.connection.cursor()
            print("files")
            for file in files1:
                if file and allowed_file1(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            
                    cursor.execute("INSERT INTO student_registration (coach_id,coach_name,student_id,name,email,dateofbirth,phone,state,district,locality,gender,height,weight,experience,bmi,username,password,file_name,uploaded_on) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(coach_id,coach_name,student_id,name,email,dateofbirth,phone,state,district,locality,gender,height,weight,experience,bmi,username,password,filename,now))
                    cursor=mysql.connection.cursor()
                    cursor.execute("SELECT id,coach_id,coach_name,student_id,name,email,dateofbirth,height,phone,state,district,locality,username,weight,bmi,gender,experience FROM student_registration")
                    student_registration=cursor.fetchall()
                    mysql.connection.commit()
                print("file")
            msg="Data Inserted Successfully"
                    
            # cursor=mysql.connection.cursor()
            # cursor.execute("SELECT id,coach_id,coach_name,student_id,name,email,dateofbirth,height,phone,state,district,locality,username,weight,bmi,gender,experience FROM student_registration")
            # student_registration=cursor.fetchall()
                
        return render_template("UI/Coach/report_Student.html",msg=msg,student_registration=student_registration)
    
    
 
 



##################### coach report ##########################
    
@app.route('/UI/Admin/report_Coach',methods=['GET','POST'])
def coach_report():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM coach_regis")
    coach_entry=cursor.fetchall()
        
    return render_template("UI/Admin/report_Coach.html",coach_regis=coach_entry)





################### report student registration ################################           

@app.route("/UI/Admin/studentreport",methods=['GET','POST'])
def studentreport():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT id,coach_id,coach_name,student_id,name,email,dateofbirth,height,phone,state,district,locality,username,weight,bmi,gender,experience FROM student_registration")
    student_registration=cursor.fetchall()
    return render_template("UI/Admin/report_Student.html",student_registration=student_registration)

    
####################  ai tracker########################  

@app.route("/UI/Admin/aitracker",methods=['GET','POST'])
def aitracker():
    # cursor=mysql.connection.cursor()
    # cursor.execute("SELECT * FROM student_registration")
    # student_registration=cursor.fetchall()
    return render_template("UI/Admin/ai_Tracker.html")
  
  
################# package ############





@app.route("/UI/Admin/package",methods=['GET','POST'])
def package():
    if request.method=='GET':
        
        
        return render_template("UI/Admin/package.html")

    else:
        cur = mysql.connection.cursor()
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # now = datetime.now()
        if request.method == 'POST':
            
            
            title=request.form['title']
            duration=request.form['duration']
            description=request.form['description']
            cur.execute("INSERT INTO package (title,duration,discription) VALUES (%s,%s,%s)",[title,duration,description])
            return render_template('UI/Admin/package.html')
            # files1 = request.files.getlist('files1[]')
            # print("files")
            # for file in files1:
            #     if file and allowed_file1(file.filename):
            #         filename = secure_filename(file.filename)
            #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #         cur.execute("INSERT INTO package (file_name, uploaded_on,title,duration,discription) VALUES (%s,%s,%s,%s,%s,)",[filename, now,title,duration,description])
            #         mysql.connection.commit()
            #     print(file)
           
            # flash('File(s) successfully uploaded')    
        


    

################# workout ##################

@app.route('/UI/Admin/workout',methods=['GET','POST'])
def workout():
    if request.method=='POST':
        workout_id=request.form['workout_id']
        workout=request.form['workout']
        discription=request.form['discription']
        
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO exersize_name (workout,workout_id,discription) VALUES (%s,%s,%s)",[workout,workout_id,discription])
        # cursor=mysql.connection.cursor()
        # cursor.execute("SELECT * FROM exersize_name")
        # exersize_name=cursor.fetchall()
        mysql.connection.commit()
        msg="Data Inserted Successfully"
        
        return render_template("UI/Admin/workout.html")
    else:
        # cursor=mysql.connection.cursor()
        # cursor.execute("SELECT * FROM exersize_name")
        # exersize_name=cursor.fetchall()
        return render_template("UI/Admin/workout.html")
    
################## upload video  in coach ########################   
    
@app.route('/UI/Coach/uploadvideo/<int:id>',methods=['GET','POST'])
def capture(id):
   
        # if 'loggedin' in session:
            if request.method=='GET':
                
                cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
                # cur.execute("SELECT id FROM coach_registration WHERE username=%s",(session['username'],))
                # ghi=cur.fetchone()
                cur.execute("SELECT * FROM exersize_name")
                abc=cur.fetchall()
                # cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query=("SELECT student_id,name,coach_id,coach_name FROM student_registration WHERE id=%s")
                cur.execute(query, (id,))
                student_registration=cur.fetchone()
               

                return render_template("UI/Coach/upload_video.html",exersize_name=abc,student_registration=student_registration)
            else:
                cur = mysql.connection.cursor()
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                now = datetime.now()
                if request.method == 'POST':
                    coach_id=request.form['coach_id']
                    coach_name=request.form['coach_name']
                    student_id=request.form['student_id']
                    name=request.form['name']
                    
                    workout=request.form['workout']
                    files = request.files.getlist('files[]')
                    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
                    
                    # print(files)
                    for file in files:
                        if file and allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            cur.execute("INSERT INTO capture_form (coach_id,coach_name,student_id,name,workout,file_name, uploaded_on) VALUES (%s, %s,%s,%s,%s,%s,%s)",[coach_id,coach_name,student_id,name,workout,filename, now])
                            mysql.connection.commit()
                        print(file)
                    cur.close()   
                       
                return render_template("UI/Coach/upload_video.html")
###################  student report in coach ######################            
            
@app.route("/UI/Coach/studentreport",methods=['GET','POST'])
def studentreport1():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT id,coach_id,coach_name,student_id,name,email,dateofbirth,height,phone,state,district,locality,username,weight,bmi,gender,experience FROM student_registration")
    student_registration=cursor.fetchall()
    return render_template("UI/Coach/report_Student.html",student_registration=student_registration)


#################   student registration in coach #############


@app.route("/UI/Coach/student_registration",methods=['GET','POST'])
def studentregistration1():
    if request.method=='GET':
        return render_template("UI/Coach/student_Registration.html")
    else:
        
        cursor = mysql.connection.cursor()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        now = datetime.now()
        if request.method=='POST':
            coach_id=request.form['coach_id']
            coach_name=request.form['coach_name']
            student_id=request.form['student_id']
            name=request.form['name']
            email=request.form['email']
            dateofbirth=request.form['dateofbirth']
            phone=request.form['phone']
            state=request.form['state']
            district=request.form['district']
            locality=request.form['locality']
            gender=request.form['gender']
            height=request.form['height']
            weight=request.form['weight']
            bmi=request.form['bmi']
            experience=request.form['experience']
            username=request.form['username']
            password=request.form['password']
            files1 = request.files.getlist('files1[]')
            
            cursor=mysql.connection.cursor()
            print("files")
            for file in files1:
                if file and allowed_file1(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            
                    cursor.execute("INSERT INTO student_registration (coach_id,coach_name,student_id,name,email,dateofbirth,phone,state,district,locality,gender,height,weight,experience,bmi,username,password,file_name,uploaded_on) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(coach_id,coach_name,student_id,name,email,dateofbirth,phone,state,district,locality,gender,height,weight,experience,bmi,username,password,filename,now))
                    cursor=mysql.connection.cursor()
                    cursor.execute("SELECT id,coach_id,coach_name,student_id,name,email,dateofbirth,height,phone,state,district,locality,username,weight,bmi,gender,experience FROM student_registration")
                    student_registration=cursor.fetchall()
                    mysql.connection.commit()
                print("file")
            msg="Data Inserted Successfully"
                    
            # cursor=mysql.connection.cursor()
            # cursor.execute("SELECT id,coach_id,coach_name,student_id,name,email,dateofbirth,height,phone,state,district,locality,username,weight,bmi,gender,experience FROM student_registration")
            # student_registration=cursor.fetchall()
                
        return render_template("UI/Coach/report_Student.html",msg=msg,student_registration=student_registration)
    
    
 
 


#####################  upload video Report ##############   
@app.route("/UI/Coach/uploadvideo_report",methods=['GET','POST'])
def uploadreport_form():
     cur=mysql.connection.cursor()
     cur.execute("SELECT id,coach_id,coach_name,student_id,name,workout,file_name FROM capture_form")
     capture_form=cur.fetchall()
     return render_template("UI/Coach/uploadVideoReport.html",capture_form=capture_form)


    
########################   Ai Tracker in Coach  ##################### 

@app.route("/UI/Coach/aitracker", methods=['GET','POST']) 
def aitrackerCoach():
    return render_template("UI/Coach/ai_Tracker.html")

################# Counselling in coach panel  ################

@app.route("/UI/Coach/counselling", methods=['GET','POST']) 
def counselling():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM counselling")
    counselling =cur.fetchall()
    return render_template("UI/Coach/counselling.html",counselling=counselling)


################ create counselling in coach ###################


@app.route("/UI/Coach/createcounselling", methods=['GET','POST']) 
def createcounselling():
    if request.method=='GET':
        
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cur.execute("SELECT name FROM student_registration")
        student_registration=cur.fetchall()
        return render_template("UI/Coach/createcounselling.html",student_registration=student_registration)
    
    else:
        now = datetime.now()
        if request.method=='POST':
        
            name=request.form['name']
            
            student_id=request.form['student_id']
            remark =request.form['remark']
            dateofbirth=request.form['dateofbirth']
            
            cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT name FROM student_registration")
            student_registration=cur.fetchall()
            
            
            
            
            cur.execute("INSERT INTO counselling (name,student_id,remark,date,uploaded_on) VALUES(%s,%s,%s,%s,%s)" ,(name,student_id,remark,dateofbirth,now))
            

            msg="successfully insert"
            mysql.connection.commit()
            
            return render_template("UI/Coach/counselling.html" ,msg=msg,student_registration=student_registration)
        
    
#############  create dependent dropdown ###############

# @app.route("/adgen",methods=["POST","GET"])
# def adgen(): 
    
#     # cur = mysql.connection.cursor()
#     # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     if request.method == 'POST':
        
#         category_id = request.form['category_id'] 
#         print(category_id) 
#         cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
#         cur.execute("SELECT * FROM addfeetitle WHERE name = %s ORDER BY student_id ASC", [category_id] )
#         student_registration = cur.fetchall()
#         cur=mysql.connection.cursor()
        
#         OutputArray = []
#         for row in student_registration:
#             outputObj = {
#                 'id': row['student_id'],
#                 'name': row['student_id']}
#             OutputArray.append(outputObj)
#     return jsonify(OutputArray)


# @app.route("/addfeetitle",methods=["POST","GET"])
# def abc():  
#     cur = mysql.connection.cursor()
#     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     if request.method == 'POST':
#         category_id = request.form['category_id'] 
#         print(category_id) 
#         cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
#         cur.execute("SELECT * FROM student_registration WHERE name = %s ORDER BY student_id ASC", [category_id] )
#         student_registration = cur.fetchall()  
#         OutputArray = []
#         for row in student_registration:
#             outputObj = {
#                 'id': row['student_id'],
#                 'name': row['student_id']}
#             OutputArray.append(outputObj)
#     return jsonify(OutputArray)



############## Add Nutrition #################################


@app.route("/UI/Coach/nutrition",methods=['GET','POST'])
def nutrition():
    if request.method=='POST':
        title=request.form['title']
        time=request.form['time']
        desc=request.form['desc']
        
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO nutrition (title,time,description) VALUES (%s,%s,%s)",(title,time,desc))
        
        
        mysql.connection.commit()
        msg="Data Inserted Successfully"
        
        
        
        
        return render_template("UI/Coach/nutrition.html",msg=msg,)
    else:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT uploaded_on  FROM counselling")
        nutrition=cur.fetchall()
        
        
        return render_template("UI/Coach/nutrition.html",counselling=nutrition)
    
    

    
        




  




            





            
    
if __name__ == "__main__":
    app.run(debug=True)