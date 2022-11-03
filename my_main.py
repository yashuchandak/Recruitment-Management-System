from flask import Flask, render_template, redirect, session, request, url_for

import mysql.connector as connector

import smtplib

app = Flask(__name__)

db = connector.connect(host = "localhost", user = "root", password = "Mysqlroot", database = "tempproj")

command_handler = db.cursor(buffered=True)

@app.route('/', methods =['GET', 'POST'])
def login():
    
    if request.method=="POST" and 'regemp' in request.form:
        return redirect(url_for('registration'))

    
    if request.method=='POST' and ('pass' and 'email' in request.form):
        
        email = request.form['email']
        passw = request.form['pass']
        lis = [email, passw]
        
    
    
        if request.form.get('exampleRadios')=="option1":
            command_handler.execute("SELECT name, id FROM employer WHERE email_id=%s AND password=%s", lis)
            present=command_handler.fetchone()
            if present:
                session['admin'] = 'admin'
                return redirect(url_for('employer_dashboard', name=present[0], eid=present[1]))
        else:
            command_handler.execute("SELECT name, id FROM job_seeker WHERE email_id=%s and password=%s", (email, passw,))
            present=command_handler.fetchone()
            if present:
                session['admin'] = 'admin'
                return redirect(url_for('job_seeker_dashboard', name=present[0], jsid=present[1]))
    
    
    return render_template('login.html')

@app.route('/employer_dashboard<name><eid>', methods=['GET', 'POST'])
def employer_dashboard(name,eid):
    # print(name)
    fulljob=[]
    profile=[]
    if 'admin' not in session:
        return redirect(url_for('login'))
    command_handler.execute("SELECT id, role, available FROM job WHERE eid=%s", (eid,))
    lis=command_handler.fetchall()
    # print(lis)
    if request.method=='POST' and 'jobid' in request.form:
        jobid=request.form['jobid']
        command_handler.execute("SELECT * FROM job WHERE id=%s", (jobid,))
        fulljob = command_handler.fetchone()
        # print(fulljob)

        if request.method == 'POST' and 'sub2' in request.form:
            fetch = ['available','timing','requirement','city','role','salary','work_location']
            query_vals = []
            
            for i in range(0, len(fetch)):
                query_vals.append(request.form[fetch[i]])
        
            command_handler.execute("UPDATE job SET available=%s, timing=%s, requirement=%s,city=%s,role=%s,salary=%s,work_location=%s", query_vals)
            db.commit()
            
            command_handler.execute("SELECT * FROM job WHERE id = %s",(jobid,))
            fulljob = command_handler.fetchone()
        
    if request.method == 'POST' and 'sub3' in request.form:
        fetch = ['ntiming', 'nrequirement', 'ncity', 'nrole', 'nsalary', 'nwork_location']

        query_vals = []
    
        for i in range(len(fetch)):
            query_vals.append(request.form[fetch[i]])
        query_vals.append(eid)

        command_handler.execute("INSERT INTO job (available, timing, requirement, city, role, salary, work_location, eid) VALUES (1, %s, %s, %s, %s, %s,  %s, %s)", query_vals)

        db.commit()

    command_handler.execute("SELECT * FROM employer where id=%s", (eid,))
    profile=command_handler.fetchone()
    # print(profile)

    if request.method == 'POST' and 'sub4' in request.form:
        
        fetch = ['name', 'age', 'gender', 'education', 'mobile', 'area', 'city', 'email_id', 'password']

        query_vals = []
    
        for i in range(len(fetch)):
            query_vals.append(request.form[fetch[i]])
        # query_vals.append(eid)

        command_handler.execute("UPDATE employer SET name=%s, age=%s, gender=%s, education=%s, mobile=%s, area=%s, city=%s, email_id=%s, password=%s", query_vals)

        db.commit()

    return render_template('employer_dashboard.html', name=name, jobs=lis, fulljob=fulljob, profile=profile)


@app.route('/job_seeker_dashboard<name><jsid>', methods=['GET', 'POST'])
def job_seeker_dashboard(name, jsid):
    # print(name)
    # fulljob=[]
    profile=[]
    if 'admin' not in session:
        return redirect(url_for('login'))
    # command_handler.execute("SELECT id, role, available FROM job WHERE eid=%s", (eid,))
    # lis=command_handler.fetchall()
    # # print(lis)
    # if request.method=='POST' and 'jobid' in request.form:
    #     jobid=request.form['jobid']
    #     command_handler.execute("SELECT * FROM job WHERE id=%s", (jobid,))
    #     fulljob = command_handler.fetchone()
    #     # print(fulljob)

    #     if request.method == 'POST' and 'sub2' in request.form:
    #         fetch = ['available','timing','requirement','city','role','salary','work_location']
    #         query_vals = []
            
    #         for i in range(0, len(fetch)):
    #             query_vals.append(request.form[fetch[i]])
        
    #         command_handler.execute("UPDATE job SET available=%s, timing=%s, requirement=%s,city=%s,role=%s,salary=%s,work_location=%s", query_vals)
    #         db.commit()
            
    #         command_handler.execute("SELECT * FROM job WHERE id = %s",(jobid,))
    #         fulljob = command_handler.fetchone()
        
    # if request.method == 'POST' and 'sub3' in request.form:
    #     fetch = ['ntiming', 'nrequirement', 'ncity', 'nrole', 'nsalary', 'nwork_location']

    #     query_vals = []
    
    #     for i in range(len(fetch)):
    #         query_vals.append(request.form[fetch[i]])
    #     query_vals.append(eid)

    #     command_handler.execute("INSERT INTO job (available, timing, requirement, city, role, salary, work_location, eid) VALUES (1, %s, %s, %s, %s, %s,  %s, %s)", query_vals)

    #     db.commit()

    command_handler.execute("SELECT * FROM job_seeker where id=%s", (jsid,))
    profile=command_handler.fetchone()
    # print(profile)

    if request.method == 'POST' and 'sub4' in request.form:
        
        fetch = ['name', 'age', 'gender', 'education', 'mobile', 'area', 'city', 'email_id', 'password']

        query_vals = []
    
        for i in range(len(fetch)):
            query_vals.append(request.form[fetch[i]])
        # query_vals.append(eid)

        command_handler.execute("UPDATE job_seeker SET name=%s, age=%s, gender=%s, education=%s, mobile=%s, area=%s, city=%s, email_id=%s, password=%s", query_vals)

        db.commit()

    return render_template('job_seeker_dashboard.html', name=name, profile=profile)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method=='POST' and 'name' in request.form:
        fetch = ['name', 'age', 'gender', 'education', 'mobile', 'area', 'city', 'password', 'email_id']

        query_vals = []
    
        for i in range(len(fetch)):
            query_vals.append(request.form[fetch[i]])

        if request.form.get('who')=="emp":
            command_handler.execute("INSERT INTO employer (name, age, gender, education, mobile, area, city, password, email_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", query_vals)
        else:
            command_handler.execute("INSERT INTO job_seeker (name, age, gender, education, mobile, area, city, password, email_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", query_vals)

        db.commit()
    
    return render_template("registration.html")


# @app.route('/add_job', methods=['GET', 'POST'])
# def add_job():
#     if request.method=='POST' and 'role' in request.form:
#         fetch = ['timing', 'requirement', 'city', 'role', 'eid', 'salary', 'work_location']

#         query_vals = []
    
#         for i in range(len(fetch)):
#             query_vals.append(request.form[fetch[i]])

#         command_handler.execute("INSERT INTO job (available, timing, requirement, city, role, eid, salary, work_location) VALUES (1, %s, %s, %s, %s, %s, %s, %s, %s)", query_vals)

#         db.commit()
    
#     return render_template("add_job.html")

    
if __name__ == "__main__":
    app.secret_key = 'seckey' #necessaryforsession
    app.run(host = "localhost", port = int("5000"), debug = True)