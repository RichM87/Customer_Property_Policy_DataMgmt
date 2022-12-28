from flask import Flask, render_template, url_for, request, redirect, flash
import csv, pdb, sqlite3#,cgi
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date


app = Flask(__name__)
#dbFile = "test.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///propPolicy.db'
myDB = SQLAlchemy(app)


class Policy(myDB.Model):
    id = myDB.Column(myDB.Integer, primary_key=True)
    fName = myDB.Column(myDB.String(25), nullable=False)
    lName = myDB.Column(myDB.String(25), nullable=False)
    quoteDate = myDB.Column(myDB.DateTime(20), nullable=False, default=datetime.utcnow)
    dob = myDB.Column(myDB.DateTime(20), nullable=False)
    phSex = myDB.Column(myDB.String(20), nullable=False)
    marStatus = myDB.Column(myDB.String(50), nullable=False)
    yrsOwned = myDB.Column(myDB.Integer, nullable=False)
    claims3yrs = myDB.Column(myDB.Integer, nullable=False, default=0)
    emplyStatus = myDB.Column(myDB.String(5), nullable=False)
    yrBuilt = myDB.Column(myDB.Integer, nullable=False)
    numBedrooms = myDB.Column(myDB.Integer, nullable=False)
    bizUse = myDB.Column(myDB.String(5), nullable=False)
    propUsage = myDB.Column(myDB.String(5), nullable=False)
    polStatus = myDB.Column(myDB.String(20), nullable=False)
    maxUnocc = myDB.Column(myDB.Integer, nullable=False)
    alarm = myDB.Column(myDB.String(10), nullable=False)
    deadbolts = myDB.Column(myDB.String(10), nullable=False)
    propAddress = myDB.Column(myDB.String(150), nullable=False)
    city = myDB.Column(myDB.String(50), nullable=False)
    state = myDB.Column(myDB.String(25), nullable=False)
    hoodWatch = myDB.Column(myDB.String(10), nullable=False)
    purchPrice = myDB.Column(myDB.Integer, nullable=False, default=0)
    listPrice = myDB.Column(myDB.Integer, nullable=False, default=0)
    daysOnMarket = myDB.Column(myDB.Integer, nullable=True, default=0)
    saleDate = myDB.Column(myDB.DateTime(20), nullable=False, default="0001-01-01")
    onMarket = myDB.Column(myDB.String(5), nullable=False)
    saleStatus = myDB.Column(myDB.String(5), nullable=False)
    salePrice = myDB.Column(myDB.Integer, nullable=False, default=0)


# def __repr__(self):
#     return '<Record %r>' % self.id
#     print('<Record %r>',  self.id)

def write_to_csv(custData):
    with open('./propPolicy_database.csv', mode='a', newline='') as prop_db_csv:  #needed to add /WServer to file address when working with pythonanywhere
        fName = custData['FirstName'].capitalize()
        lName = custData['LastName'].capitalize()
        quoteDate = custData['QuoteDate']
        dob = custData['DateofBirth']
        phSex = custData['PhSex'].upper()
        marStatus = custData['Married?'].upper()
        yrsOwned = custData['YearsOwned']
        claims3yrs = int(custData['Claims3Yrs'])
        emplyStatus = custData['EmplyStatus'].upper()
        yrBuilt = int(custData['YrBuilt'])
        numBedrooms = int(custData['NumBedrooms'])
        bizUse = custData['BizUse'].upper()
        propUsage = custData['PropUsage'].upper()
        polStatus = custData['PolStatus'].capitalize()
        maxUnocc = int(custData['MaxUnocc'])
        alarm = custData['Alarm'].upper()
        deadbolts = custData['Deadbolts'].upper()
        propAddress = custData['PropAddress'].upper()
        city = custData['City'].upper()
        state = custData['State'].upper()
        hoodWatch = custData['HoodWatch'].upper()
        daysOnMarket = int(custData['DaysOnMarket'])
        onMarket = custData['OnMarket'].upper()
        saleStatus = custData['SaleStatus'].upper()
        purchPrice = int(custData['PurchPrice'])
        listPrice = int(custData['ListPrice'])
        saleDate = custData['SaleDate']
        if saleDate == "None":
            saleDate = "01-01-1601"
        salePrice = custData['SalePrice']

        csv_writer = csv.writer(prop_db_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([fName,lName,quoteDate, dob, phSex, marStatus,yrsOwned, claims3yrs, emplyStatus, yrBuilt, numBedrooms,
                             bizUse, propUsage, polStatus, maxUnocc, alarm, deadbolts, propAddress, city, state,
                             hoodWatch])

    with open('./property_database.csv', mode='a', newline='') as property_csv:
        csv_writer2 = csv.writer(property_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # pdb.set_trace()
        csv_writer2.writerow([propAddress,city,state,yrBuilt,numBedrooms,deadbolts,yrsOwned,hoodWatch,
                             purchPrice,listPrice,saleDate])

    if onMarket.upper() == "Y":
        with open('./listing_database.csv', mode='a', newline='') as listing_csv:
            csv_writer3 = csv.writer(listing_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # pdb.set_trace()
            csv_writer3.writerow([propAddress,city,state,listPrice,salePrice,onMarket,daysOnMarket,saleStatus])

@app.route('/updateSearch', methods=['GET'])
def search():
    print('HELLO')
    # pdb.set_trace()
    srch = request.args.get('lnSearch')
    srch2 = request.args.get('propAddress')
    print(srch)
    print(srch2)
    # box = cgi.FieldStorage()
    # searchTerm = box.getvalue('testBox')
    # print(searchTerm)
    sqliteConnection = sqlite3.connect('propPolicy.db')
    cursor = sqliteConnection.cursor()
    sql_command = f"SELECT id FROM Policy WHERE lName LIKE '%{srch.capitalize()}%' AND propAddress LIKE '%{srch2.capitalize()}%'"
    try:
        records = []
        cursor.execute(sql_command)
        result = cursor.fetchall()
        if result:
            print(result)
            for item in result:
                x = ''.join(str(item)[1:-2])
                print(x)
                id = int(x)
                record = Policy.query.get_or_404(id)
                records.append(record)
        else:
            return "There are no records with this criteria. Go back and try again."
    except:
        return "The SQL command was not executed for some reason."

    return render_template('updateSearch.html', records=records)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        custData = request.form.to_dict()
        fName = custData['FirstName'].capitalize()
        lName = custData['LastName'].capitalize()
        quoteDate = custData['QuoteDate']
        dob = custData['DateofBirth']
        phSex = custData['PhSex'].upper()
        marStatus = custData['Married?'].upper()
        yrsOwned = int(custData['YearsOwned'])
        claims3yrs = int(custData['Claims3Yrs'])
        emplyStatus = custData['EmplyStatus'].upper()
        yrBuilt = int(custData['YrBuilt'])
        numBedrooms = int(custData['NumBedrooms'])
        bizUse = custData['BizUse'].upper()
        propUsage = custData['PropUsage'].upper()
        polStatus = custData['PolStatus'].upper()
        maxUnocc = int(custData['MaxUnocc'])
        alarm = custData['Alarm'].upper()
        deadbolts = custData['Deadbolts'].upper()
        propAddress = custData['PropAddress'].upper()
        city = custData['City'].upper()
        state = (custData['State']).upper()
        hoodWatch = custData['HoodWatch'].upper()
        saleDate = custData['SaleDate']
        onMarket = custData['OnMarket'].upper()
        saleStatus = custData['SaleStatus'].upper()
        salePrice = (custData['SalePrice'])
        if len(fName) < 1:
            return render_template('error.html', eVar=fName)
        if len(lName) < 1:
            return render_template('error.html', eVar=lName)
        if custData['PurchPrice'] == None:
            return render_template('error.html', eVar=custData['PurchPrice'])
        else:
            purchPrice = int(custData['PurchPrice'])
        if custData['ListPrice'] == None:
            return render_template('error.html', eVar=custData['ListPrice'])
        else:
            listPrice = int(custData['ListPrice'])
        if custData['DaysOnMarket'] == None:
            return render_template('error.html', eVar=custData['DaysOnMarket'])
        else:
            daysOnMarket = int(custData['DaysOnMarket'])

        if len(custData['SalePrice']) < 1:
            return render_template('error.html', eVar=custData['SalePrice'])
        else:
            salePrice = int(custData['SalePrice'])
        if quoteDate:
            if "/" in quoteDate:
                quoteDate=quoteDate.replace("/","-")
            try:
                c_qDate = (datetime.strptime(quoteDate,'%m-%d-%Y'))
            except:
                return render_template('error.html', eVar =quoteDate)

        if dob:
            if "/" in dob:
                dob=dob.replace("/","-")
            try:
                c_dob = datetime.strptime(dob,'%m-%d-%Y')
            except:
                return render_template('error.html', eVar=dob)

        if phSex.upper() not in ["M","F"]:
            return render_template('error.html', eVar=phSex)

        if (marStatus.upper() not in ["M", "S", "D", "W", "DP"]):
            return render_template('error.html', eVar=marStatus)

        if type(yrsOwned) != int:
            return render_template('error.html', eVar=yrsOwned)

        if type(claims3yrs) != int:
            return render_template('error.html', eVar=claims3yrs)

        if (emplyStatus.upper() not in ["E","R","S"]):
            return render_template('error.html', eVar =emplyStatus)

        if type(yrBuilt) != int:
            return render_template('error.html', eVar=yrBuilt)

        if type(numBedrooms) != int:
            return render_template('error.html', eVar=numBedrooms)

        if bizUse.upper() not in ["Y","N"]:
            return render_template('error.html', eVar=bizUse)

        if propUsage.upper() not in ["PH","I"]:
            return render_template('error.html', eVar=propUsage)

        if polStatus.capitalize() not in ["Live","Lapsed","Cancelled"]:
            return render_template('error.html', eVar=polStatus)

        if type(numBedrooms) != int:
            return render_template('error.html', eVar=maxUnocc)

        if alarm.upper() not in ["Y","N"]:
            return render_template('error.html', eVar=alarm)

        if deadbolts.upper() not in ["Y","N"]:
            return render_template('error.html', eVar=deadbolts)

        if len(propAddress) < 2:
            return render_template('error.html', eVar=propAddress)

        if len(city) < 1:
            return render_template('error.html', eVar=city)

        if len(state) != 2:
            return render_template('error.html', eVar=state)

        if hoodWatch.upper() not in ["Y","N"]:
            return render_template('error.html', eVar=hoodWatch)

        if len(onMarket) < 1:
            return render_template('error.html', eVar=onMarket)

        if len(saleStatus) < 1 or saleStatus.capitalize() not in ("Pending","Sold","Off"):
            return render_template('error.html', eVar=saleStatus)
        if saleDate:
            if saleDate.capitalize() == "None":
                saleDate = "01-01-0001"
            if "/" in saleDate:
                saleDate=saleDate.replace("/","-")
            try:
                c_sDate = (datetime.strptime(saleDate,'%m-%d-%Y'))
            except:
                return render_template('error.html', eVar =saleDate)
        else:
            return render_template('error.html', eVar=saleDate)

        try:
            newProperty = Policy(fName=fName,lName=lName,quoteDate=c_qDate, dob=c_dob, phSex=phSex, marStatus=marStatus, yrsOwned=yrsOwned,
                                 claims3yrs=claims3yrs, emplyStatus=emplyStatus, yrBuilt=yrBuilt, numBedrooms=numBedrooms,
                                 bizUse=bizUse, propUsage=propUsage, polStatus=polStatus, maxUnocc=maxUnocc,
                                 alarm=alarm, deadbolts=deadbolts, propAddress=propAddress, city=city, state=state,
                                 hoodWatch=hoodWatch, purchPrice=purchPrice, listPrice=listPrice, daysOnMarket=daysOnMarket,
                                 saleDate=c_sDate, onMarket=onMarket, saleStatus=saleStatus,salePrice=salePrice)
            # pdb.set_trace()
            # print(newProperty)
            myDB.session.add(newProperty)
            myDB.session.commit()
            write_to_csv(custData)
            # newProperty.__repr__()
            return redirect('/')

        except:
                return 'There was an issue adding your property policy details.'

    else:
        records = Policy.query.order_by(Policy.quoteDate).all()
        return render_template('index.html', records=records)

# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         task_content = request.form['QuoteDate']
#         new_task = Todo(content=task_content)
#
#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             #new_task.__repr__()
#             return redirect('/')
#
#         except:
#             return 'There was an issue adding your task.'
#
#     else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         return render_template('index.html', records=tasks)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    record = Policy.query.get_or_404(id)

#need to make sure the dates are properly converted from strings before the commit
    if request.method == 'POST':
        record.fName = request.form['FirstName']
        record.lName = request.form['LastName']
        record.quoteDate = request.form['QuoteDate']
        record.dob = request.form['DateofBirth']
        record.phSex = request.form['PhSex']
        record.marStatus = request.form['Married?']
        record.yrsOwned = int(request.form['YearsOwned'])
        record.claims3yrs = int(request.form['Claims3Yrs'])
        record.emplyStatus = request.form['EmplyStatus']
        record.yrBuilt = int(request.form['YrBuilt'])
        record.numBedrooms = int(request.form['NumBedrooms'])
        record.bizUse = request.form['BizUse']
        record.propUsage = request.form['PropUsage']
        record.polStatus = request.form['PolStatus']
        record.maxUnocc = int(request.form['MaxUnocc'])
        record.alarm = request.form['Alarm']
        record.deadbolts = request.form['Deadbolts']
        record.propAddress = request.form['PropAddress']
        record.city = request.form['City']
        record.state = (request.form['State']).upper()
        record.hoodWatch = request.form['HoodWatch']
        record.purchPrice = int(request.form['PurchPrice'])
        record.listPrice = int(request.form['ListPrice'])
        record.daysOnMarket = int(request.form['DaysOnMarket'])
        record.saleDate = request.form['SaleDate']
        record.onMarket = request.form['OnMarket']
        record.saleStatus = request.form['SaleStatus']
        record.salePrice = int(request.form['SalePrice'])

        if record.quoteDate:
            # print(type(record.quoteDate))
            if "/" in record.quoteDate:
                record.quoteDate=record.quoteDate.replace("/","-")
            try:
                qDate = record.quoteDate
                qDatex = qDate[5:10]+'-'+qDate[0:4]
                print(qDatex)
                c_rqDate = datetime.strptime(qDatex,'%m-%d-%Y')
                record.quoteDate = c_rqDate
            except:
                return render_template('error.html', eVar =record.quoteDate)

        if record.dob:
            if "/" in record.dob:
                record.dob = record.dob.replace("/", "-")
            try:
                rDOB = record.dob
                rDOBx = rDOB[5:10] + '-' + rDOB[0:4]
                print(rDOBx)
                c_rdob = datetime.strptime(rDOBx, '%m-%d-%Y')
                record.dob = c_rdob
            except:
                return render_template('error.html', eVar=record.dob)

        if record.saleDate:
            # print(type(record.quoteDate))
            if "/" in record.saleDate:
                record.saleDate=record.saleDate.replace("/","-")
            try:
                sDate = record.saleDate
                sDatex = sDate[5:10] + '-' + sDate[0:4]
                print(sDatex)
                c_sDate = datetime.strptime(sDatex,'%m-%d-%Y')
                record.saleDate = c_sDate
            except:
                return render_template('error.html', eVar =record.saleDate)
        else:
            return render_template('error.html', eVar=record.saleDate)

        if record.saleStatus.capitalize() not in ("Pending","Sold","Off"):
            return render_template('error.html', eVar=record.saleStatus)

        try:
            myDB.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your record.'
    else:
        return render_template('update.html', record=record)

# @app.route('/error/<string:eVar>', methods=['GET'])
# def format_error(eVar):
#     return render_template('error.html')


@app.route('/delete/<int:id>')
def delete(id):
    record_to_delete = Policy.query.get_or_404(id)

    try:
        myDB.session.delete(record_to_delete)
        myDB.session.commit()
        return redirect('/')

    except:
        return 'There was a problem deleting that record.'


if __name__ == "__main__":
    app.run(debug=True)

