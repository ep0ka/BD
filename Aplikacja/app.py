from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify, app
import mysql.connector
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import timedelta

#####################################################
# id poszczególnych czujników z bazy danych
id_temperatura = 1
id_cisnienie = 2
id_wilgotnosc = 5
id_co2 = 4
id_smog = 3
id_swiatlo = 9
id_halas = 7
#####################################################


app = Flask(__name__)
#Wykorzystanie mysql.connector, nawiązywanie połączenia z bazą danych
'''
mySQL = mysql.connector.connect(host='raspoka.ddns.net',
                                     database='bazydanych',
                                     user='projekt',
                                     password='bolekilolek')

cur = mySQL.cursor(buffered=True)
'''

#Ustawienie timeout dla sesji (5min)
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

# Index
@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')



# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    mySQL = mysql.connector.connect(host='raspoka.ddns.net',
                                         database='bazydanych',
                                         user='projekt',
                                         password='bolekilolek')

    cur = mySQL.cursor(buffered=True)

    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mySQL.cursor(buffered=True)

        # Execute query
        cur.execute("INSERT INTO user(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mySQL.commit()

        # Close connection
        mySQL.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    mySQL = mysql.connector.connect(host='raspoka.ddns.net',
                                         database='bazydanych',
                                         user='projekt',
                                         password='bolekilolek')

    cur = mySQL.cursor(buffered=True)

    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mySQL.cursor(buffered=True)
        
        # Get user by username
        cur.execute("SELECT * FROM user WHERE username = %s", [username])
        data = cur.fetchone()
        if data != None :
            # Get stored hash
            password = data[4]

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['id'] = data[0]
                session['id_urzadzenia'] = data[0]
                #cur.execute("SELECT * FROM Czujnik WHERE Urzadzenia_idUrzadzenia=%s",[session['id_urzadzenia']])
                #cur.execute("SELECT * FROM Czujnik WHERE Urzadzenia_idUrzadzenia=%s",[session['id_urzadzenia']])

                #Czujniki = cur.fetchall()
                #print("Zmienna Czujniki",Czujniki[1][1])
                # session['liczba_czujnikow'] = len(Czujniki)
                #print("Liczba czujników",session['liczba_czujnikow']," !!!!!!!") # test
                #for i in Czujniki:
               	#id_i_rodzaj = ("1=Temperatura","2=Światło","3=Smog")
               	#session['id_i_rodzaj'] = id_i_rodzaj
               	#print("ID_I_RODZAJ",id_i_rodzaj)
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            mySQL.close()
        else:
            error = 'Username not found'
            mySQL.close()
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
#@app.route('/dashboard')
#@is_logged_in
#def dashboard():
#	return render_template('dashboard.html')
############################################################
#                       Projekt_zespołowy                  #
############################################################
# Strona głowna
@app.route("/dashboard")
@is_logged_in
def dashboard():
	#########################################################################
	# Nawiązywanie połączenia z bazą danych									#
    mySQL_conn = mysql.connector.connect(host='raspoka.ddns.net',			#
                                   database='zespolowy',					#
                                   user='projekt',							#
                                   password='bolekilolek')					#
    cursor = mySQL_conn.cursor(buffered=True)								#
	#########################################################################

    cursor.execute("SELECT value FROM measurement WHERE sensor_id="+str(id_temperatura)+" ORDER BY measure_id DESC")
    temperatura = cursor.fetchone()[0]

    cursor.execute("SELECT value FROM measurement WHERE sensor_id="+str(id_cisnienie)+" ORDER BY measure_id DESC")
    cisnienie = cursor.fetchone()[0]
    
    cursor.execute("SELECT value FROM measurement WHERE sensor_id="+str(id_wilgotnosc)+" ORDER BY measure_id DESC")
    wilgotnosc = cursor.fetchone()[0]

    cursor.execute("SELECT value FROM measurement WHERE sensor_id="+str(id_co2)+" ORDER BY measure_id DESC")
    co2 = cursor.fetchone()[0]

    cursor.execute("SELECT value FROM measurement WHERE sensor_id="+str(id_smog)+" ORDER BY measure_id DESC")
    smog = cursor.fetchone()[0]

    cursor.execute("SELECT value FROM measurement WHERE sensor_id="+str(id_swiatlo)+" ORDER BY measure_id DESC")
    swiatlo = cursor.fetchone()[0]

    cursor.execute("SELECT value FROM measurement WHERE sensor_id="+str(id_halas)+" ORDER BY measure_id DESC")
    halas = cursor.fetchone()[0]
    
    mySQL_conn.close();
    return render_template('dashboard.html', temperatura=temperatura, cisnienie=cisnienie, halas=halas, wilgotnosc=wilgotnosc, swiatlo=swiatlo, smog=smog, co2=co2)


@app.route("/Authenticate")
def Authenticate():
    username = request.args.get('UserName')
    password = request.args.get('Password')
#    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from mysql.user where User='" + username + "' and Password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
        return "Username or Password is wrong"
    else:
        return "Logged in successfully"

# Strona zawierająca tabelkę wraz z danymi z czujnika temperatury
@app.route("/temperatura")
def temperatura():
    if 'logged_in' in session:

        mySQL_conn = mysql.connector.connect(host='raspoka.ddns.net',
                                       database='zespolowy',
                                       user='projekt',
                                       password='bolekilolek')
        cursor = mySQL_conn.cursor()

        cursor.execute("SELECT value,date FROM measurement WHERE sensor_id="+str(id_temperatura))

        value = []
        hour = []

        rows = cursor.fetchall()
        for row in rows:
            value.append(row[0])
            hour.append(str(row[1]))

        legend = 'Dane z czujnika temperatury(1)'
        labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
        values = [10, 9, 8, 7, 6, 4, 7, 8]
        cursor.close()
        mySQL_conn.close();
        return render_template('temperatura.html', values=value, labels=hour, legend=legend)
    else:
        error = 'First log in'
        return render_template('home.html', error=error)
    	#return render_template('home.html')

# Strona zawierająca tabelkę wraz z danymi z czujnika ciśnienia
@app.route("/cisnienie")
def cisnienie():
    mySQL_conn = mysql.connector.connect(host='raspoka.ddns.net',
                                   database='zespolowy',
                                   user='projekt',
                                   password='bolekilolek')
    cursor = mySQL_conn.cursor()

    cursor.execute("SELECT value,date FROM measurement WHERE sensor_id="+str(id_cisnienie))

    value = []
    hour = []

    rows = cursor.fetchall()
    for row in rows:
        value.append(row[0])
        hour.append(str(row[1]))

    legend = 'Dane z czujnika temperatury(1)'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    mySQL_conn.close();
    return render_template('cisnienie.html', values=value, labels=hour, legend=legend)

# Strona zawierająca tabelkę wraz z danymi z czujnika wilgotności
@app.route("/wilgotnosc")
def wilgotnosc():
    mySQL_conn = mysql.connector.connect(host='raspoka.ddns.net',
                                   database='zespolowy',
                                   user='projekt',
                                   password='bolekilolek')
    cursor = mySQL_conn.cursor()

    cursor.execute("SELECT value,date FROM measurement WHERE sensor_id="+str(id_wilgotnosc))

    value = []
    hour = []

    rows = cursor.fetchall()
    for row in rows:
        value.append(row[0])
        hour.append(str(row[1]))

    legend = 'Dane z czujnika temperatury(1)'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    mySQL_conn.close();
    return render_template('wilgotnosc.html', values=value, labels=hour, legend=legend)

# Strona zawierająca tabelkę wraz z danymi z czujnika hałasu
@app.route("/halas")
def halas():
    mySQL_conn = mysql.connector.connect(host='raspoka.ddns.net',
                                   database='zespolowy',
                                   user='projekt',
                                   password='bolekilolek')
    cursor = mySQL_conn.cursor()

    cursor.execute("SELECT value,date FROM measurement WHERE sensor_id="+str(id_halas))

    value = []
    hour = []

    rows = cursor.fetchall()
    for row in rows:
        value.append(row[0])
        hour.append(str(row[1]))

    legend = 'Dane z czujnika temperatury(1)'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    mySQL_conn.close();
    return render_template('halas.html', values=value, labels=hour, legend=legend)

# Strona zawierająca tabelkę wraz z danymi z czujnika światła
@app.route("/swiatlo")
def swiatlo():
    mySQL_conn = mysql.connector.connect(host='raspoka.ddns.net',
                                   database='zespolowy',
                                   user='projekt',
                                   password='bolekilolek')
    cursor = mySQL_conn.cursor()

    cursor.execute("SELECT value,date FROM measurement WHERE sensor_id="+str(id_swiatlo))

    value = []
    hour = []

    rows = cursor.fetchall()
    for row in rows:
        value.append(row[0])
        hour.append(str(row[1]))

    legend = 'Dane z czujnika temperatury(1)'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    mySQL_conn.close();
    return render_template('swiatlo.html', values=value, labels=hour, legend=legend)

# Strona zawierająca tabelkę wraz z danymi z czujnika co2
@app.route("/co2")
def co2():
    mySQL_conn = mysql.connector.connect(host='raspoka.ddns.net',
                                   database='zespolowy',
                                   user='projekt',
                                   password='bolekilolek')
    cursor = mySQL_conn.cursor()

    cursor.execute("SELECT value,date FROM measurement WHERE sensor_id=4")

    value = []
    hour = []

    rows = cursor.fetchall()
    for row in rows:
        value.append(row[0])
        hour.append(str(row[1]))

    legend = 'Dane z czujnika temperatury(1)'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    mySQL_conn.close();
    return render_template('co2.html', values=value, labels=hour, legend=legend)

@app.route("/smog")
def smog():
    mySQL_conn = mysql.connector.connect(host='raspoka.ddns.net',
                                   database='zespolowy',
                                   user='projekt',
                                   password='bolekilolek')
    cursor = mySQL_conn.cursor()

    cursor.execute("SELECT value,date FROM measurement WHERE sensor_id="+str(id_smog))

    value = []
    hour = []

    rows = cursor.fetchall()
    for row in rows:
        value.append(row[0])
        hour.append(str(row[1]))

    legend = 'Dane z czujnika temperatury(1)'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    mySQL_conn.close();
    return render_template('smog.html', values=value, labels=hour, legend=legend)

# Strona służąca do odświeżania wykresów znajdujących się na powyższych stronach /\
@app.route('/val')
def val():
    mySQL_conn = mysql.connector.connect(host='raspoka.ddns.net',
                                   database='zespolowy',
                                   user='projekt',
                                   password='bolekilolek')
    cursor = mySQL_conn.cursor()


    inter = request.args.get('inter')
    id_czujnika = request.args.get('czujnik')
    print(id_czujnika)
    print(inter)

    zmienna = "SELECT value,date FROM measurement WHERE sensor_id="+str(id_czujnika)+" ORDER BY measure_id DESC LIMIT " 
    tmp = zmienna+str(inter)
    cursor.execute(tmp)

    value = []
    hour = []

    rows = cursor.fetchall()
    for row in rows:
        value.append(row[0])
        hour.append(str(row[1]))
    value.reverse()
    hour.reverse()
    mySQL_conn.close();
    return jsonify({'value' : value, 'hour' : hour})

@app.route('/req')
def req():
    tmp_req = request.args.get('inter')
    return '''<h1>reQ: {}</h1>'''.format(tmp_req)

############################################################
############################################################

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(host="192.168.1.108", debug=True)
