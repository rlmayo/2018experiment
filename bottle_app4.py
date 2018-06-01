
from bottle import default_app, route, template, request, response
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS data
    (id INT PRIMARY KEY,
    treatment INT,
    donation FLOAT,
    email STRING,
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
        c.execute("INSERT INTO data(id, treatment, donation, email, age, gender, marital_status, income, code) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (0, 0, 0, '0', '0', '0', '0', '0', 0))
        key = c.lastrowid
        response.set_cookie('subjnum', key, secret = 'None', max_age = 3600)
    return template("""
    <html>
        <head>
            <title>Informed Consent</title>
        </head>
        <div id=consent_form>
        <center>
        <h1>Informed Consent Form</h1>
        </center>
        <h2>Research Procedures</h2>
        <p>You are being asked to take part in a research study being conducted by Concordia College, Offutt School of Business.
        This study is designed to look at the economics of decision making.
        This research will take 1-10 minute(s) of your time. </p>
        <p>As part of this research you will be asked to make decisions that may affect your earnings and the earnings of others followed by a questionnaire.
        You will be paid to read the consent form and be ready to participate.
        In addition to the money earned through reading the consent, answering question and waiting, you may earn more during the course of the experiment.
        The exact amount of your additional earnings may range from $0 to $3, depending on your decisions, the decisions of others in the experiment, or random events within the experiment.
        You may withdraw from the experiment at any time.</p>
        <h2>Risks</h2>
            <p>There are no foreseeable risks or discomforts. </p>
        <h2>Benefits</h2>
            <p>There are no direct personal benefits for participation. </p>
        <h2>Participants</h2>
            <p>You must be 18 or over to participate.
            Your participation is voluntary.
            You may refuse to take part or withdraw from the study at any time and for any reason.
            If you decide not to participate or if you withdraw from the study, there will be no penalty or loss of benefits to which you are otherwise entitled.
            There are no costs to you or any other party. </p>
        <h2>Confidentiality</h2>
            <p>All electronic files will be saved confidentially on a physically secure, password protected server.
            All paper files will be kept in a locked file cabinet inside a campus building.
            No personally-identifiable information will be reported in any published or unpublished work.
            Access to data is restricted to the academic staff of the Offutt School of Business and affiliated researchers.
            Researchers at Concordia College may use personally-identifiable information in the future only to contact you to ask if you are interested in participating in future studies. </p>
        <h2>Contact</h2>
            <p>This study is being conducted by
            Dr. Robert L. Mayo, Assistant Professor of Economics at Concordia College.
            He can be contacted at rmayo@cord.edu or 218-299-3951 for questions or to report a research-related problem.
            You may also contact the Concordia College Institutional Review Board at clarson@cord.edu, if you have any questions or comments regarding your rights as a participant in this research.</p>
        <p align=center>
            Click <a
            href="http://llilleha.pythonanywhere.com/attention"
            ><input
            type="submit"
            value="Next"
            ></input></a>
            to acknowledge reading and accepting informed consent.</p>
        </div>
        </html>
        """)


#Page: Attention Test
@route('/attention')
def attention():
    return template("""
    <html>
        <title>Human</title>
        <center>
        <br>
        <br>
        <div id=prove>
        <p>To prove you are human , please answer the question below.
        <br>
        <br>
        You have <strong>five</strong> apples. If you eat <strong>three</strong> apples, how many apples will you have left?
        <br>
        <br>
        Enter your answer here.
        <input
        id=human_test
        name="apple_amount"
        size="2"
        min="2"
        max="2"
        maxlength="1"
        </input>

        <p align=center
        > Click <a href="http://llilleha.pythonanywhere.com/question"
        ><input
            type="submit"
	        value="Next"
        ></input></a> to continue.

        </p>
        </div>
        </center>
    </html>
    """)


#Page: Question
@route('/question', method = 'GET')
def treatment():
    import random
    treatment = random.randint(1,3)
    subject = request.get_cookie('subjnum')
    if request.GET.save:
        amount = request.forms.get('amount')
        email = ''
        email = request.forms.get('email')
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO data(id, treatment, donation, email) VALUES(?, ?, ?, ?)", (subject, treatment, amount, email))
        conn.commit()
        c.close()

    elif(treatment==1):
        return template("""
        <html>
        <br>
        <br>
        <center>
        <!--Here is Treatment_A-->
        <form id="form" method="post" action="">
        <div id="Treatment_A" class="flex">
        <p>You start with <strong>$1.00</strong>. <br><br>
        You may give some, all, or none of this amount to the American Red Cross Disaster Relief Fund.  <br><br>
        Please indicate any amount you wish to give in the box below:
            <span class="currency">$</span>
            <input
            id="amount"
            name="amount"
            type="number"
            min="0.00"
            max="1.00"
            step="0.01"
            maxlength="4"
            value=""  />
        </p></form></div>
        <hr>
        <div id=email>
        <p>
            <strong>Optional: </strong>If you wish to receive an email copy of the receipt from the American Red Cross, you may enter your email address below:
        </p>
        <input type="text" name="email" placeholder="example@example.com"<br>
        </div>
        <br>
        <br>
        <hr>
        <p> Press <a
            href="http://llilleha.pythonanywhere.com/survey"
        ><input
            type="submit"
	        value="Next"
        ></input></a> to continue.</p>
        </center>
        <center>
        </html>
        """)

    elif(treatment==2):
        return template("""
        <html>
        <br>
        <br>
        <center>
        <!--Treatment_B-->
        <form id="form" method="post" action="">
        <div id="Treatment_B" class="flex">
        <p>You start with <strong>$1.00</strong>. <br><br>
        You may give some, all, or none of this amount to the American Red Cross Disaster Relief Fund.  <br><br>
        For any amount you give, the experimenter will give an additional 5% of that amount.<br>
        Examples:<br>
        <table>
            <thead>
            <tr>
                <th scope=col><u>If you give</u></th>
                <th scope=col rowspan=2><u>The American Red Cross Disaster Relief Fund will receive</u></th>
            </tr>
            </thead>
            <tbody>
            <tr align=center>
                <td>$0.00</td>
                <td>$0.00</td>
            </tr>
            <tr align=center>
                <td>$0.20</td>
                <td>$0.21</td>
            </tr>
            <tr align=center>
                <td>$0.40</td>
                <td>$0.42</td>
            </tr>
            <tr align=center>
                <td>$0.60</td>
                <td>$0.63</td>
            </tr>
            <tr align=center>
                <td>$0.80</td>
                <td>$0.84</td>
            </tr>
            <tr align=center>
                <td>$1.00</td>
                <td>$1.05</td>
            </tr>
            </tbody>
        </table>
        </p></form></div>
        <br>
        <p>Please indicate any amount you wish to give in the box below:
            <span class="currency">$</span>
        <input
            id="amount"
            name="amount"
            type="number"
            min="0.00"
            max="1.00"
            step="0.01"
            maxlength="4"
            value=""  />
        </p></form></div>
        <hr>
        <div id=email>
        <p>
            <strong>Optional: </strong>If you wish to receive an email copy of the receipt from the American Red Cross, you may enter your email address below:
        </p>
        <input type="text" name="email" placeholder="example@example.com"<br>
        </div>
        <br>
        <br>
        <hr>
        <p> Press <a
            href="http://llilleha.pythonanywhere.com/survey"
            ><input
                type="submit"
	            value="Next"
            ></input></a> to continue.</p>
        </center>
        <center>
        </html>
        """)

    elif (treatment==3):
        return template("""
        <html>
        <br>
        <br>
        <center>
        <!--Treatment_C-->
        <form id="form" method="post" action="">
        <div id="Treatment_C" class="flex">
        <p>You start with <strong>$1.00</strong>. <br><br>
        You may give some, all, or none of this amount to the American Red Cross Disaster Relief Fund.  <br><br>
        For any amount you give, the experimenter will give an additional 100% of that amount.<br>
        Examples:<br>
        <table>
            <thead>
            <tr>
                <th scope=col><u>If you give</u></th>
                <th scope=col rowspan=2><u>The American Red Cross Disaster Relief Fund will receive</u></th>
            </tr>
            </thead>
            <tbody>
            <tr align=center>
                <td>$0.00</td>
                <td>$0.00</td>
            </tr>
            <tr align=center>
                <td>$0.20</td>
                <td>$0.40</td>
            </tr>
            <tr align=center>
                <td>$0.40</td>
                <td>$0.80</td>
            </tr>
            <tr align=center>
                <td>$0.60</td>
                <td>$1.20</td>
            </tr>
            <tr align=center>
                <td>$0.80</td>
                <td>$1.60</td>
            </tr>
            <tr align=center>
                <td>$1.00</td>
                <td>$2.00</td>
            </tr>
            </tbody>
        </table>
        </p></form></div>
        <br>
        <p>Please indicate any amount you wish to give in the box below:
            <span class="currency">$</span>
            <input
            id="amount"
            name="amount"
            type="number"
            min="0.00"
            max="1.00"
            step="0.01"
            maxlength="4"
            value=""  />
        </p></form></div>
        <hr>
        <div id=email>
        <p>
            <strong>Optional: </strong>If you wish to receive an email copy of the receipt from the American Red Cross, you may enter your email address below:
        </p>
        <input type="text" name="email" placeholder="example@example.com"<br>
        </div>
        <br>
        <br>
        <hr>
        <p> Press <a
            href="http://llilleha.pythonanywhere.com/survey"
            ><input
                type="submit"
	            value="Next"
            ></input></a> to continue.</p>
        </center>
        </div>
        <center>
        </html>
        """)

    else:
        return template('error: treatment number was %s' %str(treatment))


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
        return template("""
        <html>
        <head><title>Survey</title>
        <style>
        p.s1 {
            margin: 35px;
        }
        </style>
        </head>
        <center>
        <h2>Please answer the questions below.</h2>
        <br>
        <div id=age>
        <p class="s1">What is your age?
        <br>
        <br>
            <input type="radio" id="ageChoice1" name="age" value="18-29">
            <label for="ageChoice1">18-29</label>
        <br>
            <input type="radio" id="ageChoice2" name="age" value="30-39">
            <label for="ageChoice2">30-39</label>
        <br>
            <input type="radio" id="ageChoice3" name="age" value="40-49">
            <label for="ageChoice3">40-49</label>
        <br>
            <input type="radio" id="ageChoice4" name="age" value="50-59">
            <label for="ageChoice4">50-59</label>
        <br>
            <input type="radio" id="ageChoice5" name="age" value="60-69">
            <label for="ageChoice5">60-69</label>
        <br>
            <input type="radio" id="ageChoice6" name="age" value="70 or over">
            <label for="ageChoice6">70 or over</label>
        <br>
            <input type="radio" id="ageChoice7" name="age" value="Prefer not to state">
            <label for="ageChoice7">Prefer not to state</label>
        </p>
        </div>
        <br>
        <div id=gender>
        <p>What is your gender?</p>
            <input type="radio" id="genderChoice1" name="gender" value="Male">
            <label for="genderChoice1">Male</label>
        <br>
            <input type="radio" id="genderChoice2" name="gender" value="Female">
            <label for="genderChoice2">Female</label>
        <br>
            <input type="radio" id="genderChoice3" name="gender" value="Other">
            <label for="genderChoice3">Other</label>
        <br>
            <input type="radio" id="genderChoice4" name="gender" value="Prefer not to state">
            <label for="genderChoice4">Prefer not to state</label>
        </div>
        <br>
        <div id=marital_status>
        <p>What is your marital status?</p>
            <input type="radio" id="marital_statusChoice1" name="marital_status" value="Married">
            <label for="marital_statusChoice1">Married</label>
        <br>
            <input type="radio" id="marital_statusChoice2" name="marital_status" value="Single">
            <label for="marital_statusChoice2">Single</label>
        <br>
            <input type="radio" id="marital_statusChoice3" name="marital_status" value="Divorced">
            <label for="marital_statusChoice3">Divorced</label>
        <br>
            <input type="radio" id="marital_statusChoice4" name="marital_status" value="Prefer not to state">
            <label for="marital_statusChoice4">Prefer not to state</label>
        </div>
        <br>
        <div id=income>
        <p>What is your annual household income?</p>
            <label for="incomeChoice1">Under $20,000</label>
            <input type="radio" id="incomeChoice1" name="income" value="Under $20,000">
        <br>
            <label for="incomeChoice2">$20,000 - $39,999</label>
            <input type="radio" id="incomeChoice2" name="income" value="$20,000 - $39,999">
        <br>
            <input type="radio" id="incomeChoice3" name="income" value="$40,000 - $59,999">
            <label for="incomeChoice3">$40,000 - $59,999</label>
        <br>
            <input type="radio" id="incomeChoice4" name="income" value="$60,000 - $79,999">
            <label for="incomeChoice4">$60,000 - $79,999</label>
        <br>
            <input type="radio" id="incomeChoice5" name="income" value="$80,000 - $99,999">
            <label for="incomeChoice5">$80,000 - $99,999</label>
        <br>
            <input type="radio" id="incomeChoice6" name="income" value="Over $100,000">
            <label for="incomeChoice6">Over 100,000</label>
        <br>
            <input type="radio" id="incomeChoice7" name="income" value="Prefer not to state">
            <label for="incomeChoice7">Prefer not to state</label>
        </div>
        <br>
        <br>
        <p> Press <a
            href="http://llilleha.pythonanywhere.com/earnings"
            ><input
            type="submit"
	        value="Next"
            ></input></a> to continue.
        </center>
        <div>
        </div>
        </html>
        """)


#Page: Earnings
@route('/earnings')
def earnings():
    import random
    subject = request.get_cookie('subjnum')
    #earnings = call info from sql and calculate their earnings
    code = random.randint(0,99999)
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO data(id, code)
        VALUES(?, ?)''', (subject, code))
    conn.commit()
    c.close()

    return template("""
        <html>
        <head><title>Earnings</title>
        </head>
        <center>
        <br>
        <br>
        <p>Your total earnings from this study are [$20,000].
        <br>
        <br>
        Click the button below to return to the Mturk website, then enter this code to receive payment: [Code, random 5 digit positive integer]
        <br>
        <br>
        <a
            href="https://xkcd.com/"
            ><input
                type="submit"
	            value="Return to Mturk"
            ></input></a>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
            <h3><em>Thank you for participating</em><h3>
        </center>
        </html>
        """)



application = default_app()


