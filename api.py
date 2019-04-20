from flask import Flask, jsonify
from flask import request, render_template
import mysql.connector
import datetime

app = Flask(__name__)
now = datetime.datetime.now()
date = str(now.year)+"-"+str(now.month)+"-"+str(now.day)+" "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)


mydb =  mysql.connector.connect(
host="db-intern.ciupl0p5utwk.us-east-1.rds.amazonaws.com",
user="dummyUser",
passwd="dummyUser01",
database="db_intern",
port=3306
)

a = {'name':'da'}

mycursor = mydb.cursor()


# instruction page
@app.route('/')
def rt():
    return render_template('instruction.html')


# Web form
@app.route('/form')
def show_home():
    return render_template('homePage.html')

@app.route('/form', methods=['POST'])
def getValue():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    phone = request.form['phone']
    print(username)
    print(password)
    print(email)
    print(phone)
    dicti = {'emaiil':email}
    mycursor.execute("select * from userData where emailId=%(emaiil)s",dicti)
    records = mycursor.fetchall()
    print(records)
    if records:
        er = (username,phone,password,date,email)
        query = """update userData set userName = %s, phoneNo = %s, password = %s, dateTime = %s where emailId = %s"""
        mydb.cursor().execute(query,er)
        print("UPDATED")
        mydb.commit()
        return jsonify({'success':'Database Updated'})
    else:
        query = "INSERT INTO userData VALUES(%s,%s,%s,%s,%s)"
        user = (username, email, phone, password, date)
        mycursor.execute(query, user)
        print("Successfully")
        mydb.commit()
        return jsonify({'success':'New values are added in database'})

# for searching record

@app.route('/search')
def get():
    return render_template('Search.html')


@app.route('/search', methods=['POST'])

def getv():
    checkEmail = request.form['checkEmail']
    print(checkEmail)
    dict = {'emailll':checkEmail}
    mycursor.execute("select * from userData where emailId=%(emailll)s",dict)
    row = mycursor.fetchall()
    if row:
        username = row[0][0]
        email = row[0][1]
        phone = row[0][2]
        password = row[0][3]
        datee = row[0][4]
        tt = {'username':username,'email':email,'phone':phone,'password':password,'datetimee':datee}
        if row:
            t = {'data':tt}
        else:
            t = {'data':'not found'}
        return jsonify(t)
    else:
        return jsonify({'error':'No data found with entered email'})


#for deletingrecord


@app.route('/delete')
def gete():
    return render_template('Delete.html')

@app.route('/delete',methods=['POST'])
def deletee():
    checkemail = request.form['checkEmail']
    di = {'emaial':checkemail}
    mycursor.execute("select * from userData where emailId = %(emaial)s",di)
    reco = mycursor.fetchall()
    if reco:
        mycursor.execute("delete from userData where emailId =%(emaial)s",di)
        mydb.commit()
        return jsonify({'success':'Record Deleted'})
    else:
        return jsonify({'error':'No data found with entered email'})


app.run(port=5003)
