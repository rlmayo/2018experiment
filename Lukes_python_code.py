
from bottle import route, template, request, response, run
import random
import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS data
    (id INT PRIMARY KEY,
    treatment INT,
    amount FLOAT,
    age STRING,
    gender STRING,
    marital_status STRING,
    income STRING,
    code INT)''')
c.close()

#Page: Consent
@route('/consent')
def consent():
    subject = request.get_cookie('subjnum')
    if not subject:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("INSERT INTO data(id, treatment, amount, age, gender, marital_status, income, code) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (0, 0, 0, '0', '0', '0', '0', 0))
        key = c.lastrowid
        response.set_cookie('subjnum', key, secret = 'None', max_age = 3600)
        treatment = random.randint(1,3)
        code = random.randint(1,99999)
        c.execute("INSERT OR REPLACE INTO data(id, treatment, code) VALUES(?, ?, ?)", (key, treatment, code))
        conn.commit()
        c.close()
    return template() #consent tpl file


#Page: Attention Test
@route('/attention')
def attention():
    return template() #attention tpl file


#Page: Question
@route('/question', method = 'GET')
def treatment():
    subject = request.get_cookie('subjnum')
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    treatment = c.execute("SELECT treatment FROM data WHERE id=?", (subject,))
    if request.GET.save:
        amount = request.forms.get('amount')
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO data(id, amount) VALUES(?, ?)", (subject, amount))
        conn.commit()
        c.close()

    return template() #question tpl file, treatment


#Page: Survey
@route('/survey', method = 'GET')
def survey():
    subject = request.get_cookie('subjnum')
    if request.GET.save:
        age = request.GET.age.strip()
        gender = request.GET.gender.strip()
        marital_status = request.GET.marital_status.strip()
        income = request.GET.income.strip()
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO data(id, age, gender, marital_status, income) VALUES(?, ?, ?, ?, ?)", (subject, age, gender, marital_status, income))
        conn.commit()
        c.close()

    else:
        return template() #survey tpl file,


#Page: Earnings
@route('/earnings')
def earnings():
    subject = request.get_cookie('subjnum')
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    donation = c.execute("SELECT amount FROM data WHERE id=?", (subject,))
    earnings = 1-donation
    code = c.execute("SELECT code FROM data WHERE id=?", (subject,))

    return template() #earnings template, earnings, code

    run(debug = True, reloader = True)

