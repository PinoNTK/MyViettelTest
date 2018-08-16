from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request, session, redirect, url_for, make_response
from fabric import *
import bcrypt
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import gen_accounts
import time, datetime
application = Flask(__name__)

application.config['SECRET_KEY']='kpro096'


client = MongoClient('localhost:27017')
db = client.BankAccount


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        token = session['token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, application.config['SECRET_KEY'])
            current_user = db.Users.find_one({'user_id':data['user_id']})
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
            

        return f(current_user, *args, **kwargs)

    return decorated


@application.route("/addAccount",methods=['POST'])
@token_required
def addAccount(current_user):
    try:
        if not current_user['admin']:
            return jsonify({'message' : 'Cannot perform that function!'})
        json_data = request.json['info']

        if db.Accounts.find_one({'idNumber':json_data['idNumber']}) or db.Accounts.find_one({'username':json_data['username']}) or db.Accounts.find_one({'accountNumber':json_data['accountNumber']}) or db.Accounts.find_one({'mail':json_data['mail']}) or db.Accounts.find_one({'cardNumber':json_data['cardNumber']}):
            return jsonify({'message' : 'Data invalid!'})
        accountBalance = json_data['accountBalance']
        accountNumber = json_data['accountNumber']
        address = json_data['address']
        birthday = json_data['birthday']
        cardNumber= json_data['cardNumber']
        idNumber = json_data['idNumber']
        mail = json_data['mail']
        name = json_data['name']
        password = json_data['password']
        phoneNumber = json_data['phoneNumber']
        role = json_data['role']
        username = json_data['username']
        gender = json_data['gender'] 
        memberSince = json_data['memberSince']
        db.Accounts.insert_one({
            'accountBalance':accountBalance,
            'accountNumber':accountNumber,
            'address':address,
            'birthday':birthday,
            'cardNumber':cardNumber,
            'idNumber':idNumber,
            'mail':mail,
            'name':name,
            'password':password,
            'phoneNumber':phoneNumber,
            'role':role,
            'username':username,
            'gender':gender,
            'memberSince':memberSince
            })
        return jsonify(status='OK',message='inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR',message=str(e))

@application.route('/homepages')
@token_required
def showAccountList(current_user):
    if current_user['admin']:
        return render_template('admin.html')
    return render_template('normal.html')

@application.route('/getAccount',methods=['POST'])
def getAccount():
    try:
        accountId = request.json['accountId']
        account = db.Accounts.find_one({'_id':ObjectId(accountId)})
        accountDetail = {
                'accountBalance':account['accountBalance'],
                'accountNumber':account['accountNumber'],
                'address':account['address'],
                'birthday':account['birthday'],
                'cardNumber':account['cardNumber'],
                'idNumber':account['idNumber'],
                'mail':account['mail'],
                'name':account['name'],
                'password':account['password'],
                'phoneNumber':account['phoneNumber'],
                'role':account['role'],
                'username':account['username'],
                'gender':account['gender'],
                'memberSince': account['memberSince'],
                'accountId':str(account['_id'])
                }
        return json.dumps(accountDetail)
    except Exception as e:
        return str(e)

@application.route('/updateAccount',methods=['POST'])
@token_required
def updateAccount(current_user):

    try:
        if not current_user['admin']:
            return jsonify({'message' : 'Cannot perform that function!'})

        print(current_user)    
        accountInfo = request.json['info']
        accountBalance = accountInfo['accountBalance']
        accountNumber = accountInfo['accountNumber']
        address = accountInfo['address']
        birthday = accountInfo['birthday']
        cardNumber = accountInfo['cardNumber']
        idNumber = accountInfo['idNumber']
        mail = accountInfo['mail']
        name = accountInfo['name']
        password = accountInfo['password']
        phoneNumber = accountInfo['phoneNumber']
        role = accountInfo['role']
        username = accountInfo['username']
        gender = accountInfo['gender']
        memberSince = accountInfo['memberSince']
        accountId = accountInfo['accountId'] 

        db.Accounts.update_one({'_id':ObjectId(accountId)},{'$set':{'accountBalance':accountBalance,'accountNumber':accountNumber,'address':address,'birthday':birthday,'cardNumber':cardNumber,'idNumber':idNumber,'mail':mail,'name':name,'password':password,'phoneNumber':phoneNumber,'role':role,'username':username,'gender':gender,'memberSince':memberSince}})
        return jsonify(status='OK',message='updated successfully')
    except Exception as e:
        return jsonify(status='ERROR',message=str(e))

@application.route("/getAccountList",methods=['POST'])
@token_required
def getAccountList(current_user):
    try:
        if not current_user['admin']:
            return jsonify({'message' : 'Cannot perform that function!'})
        accounts = db.Accounts.find()
        
        accountList = []
        for account in accounts:
            accountItem = {
                    'accountBalance' : account['accountBalance'],
                    'accountNumber': account['accountNumber'],
                    'address' : account['address'],
                    'birthday' : account['birthday'],
                    'cardNumber' : account['cardNumber'],
                    'idNumber' : account['idNumber'],
                    'mail' : account['mail'],
                    'name' : account['name'],
                    'password' : account['password'],
                    'phoneNumber' : account['phoneNumber'],
                    'role' : account['role'],
                    'username' : account['username'],
                    'gender' : account['gender'],
                    'memberSince' : account['memberSince'],
                    'accountId' : str(account['_id']) 
                    }
            accountList.append(accountItem)
    except Exception as e:
        return str(e)
    return json.dumps(accountList)

@application.route("/deleteAccount",methods=['POST'])
@token_required
def deleteAccount(current_user):
    try:
        if not current_user['admin']:
            return jsonify({'message' : 'Cannot perform that function!'})

        accountId = request.json['accountId']
        db.Accounts.remove({'_id':ObjectId(accountId)})
        return jsonify(status='OK',message='deletion successful')
    except Exception as e:
        return jsonify(status='ERROR',message=str(e))

@application.route('/adminsearch', methods=['POST'])
@token_required
def searchAccounts(current_user):
    try:
        if not current_user['admin']:
            return jsonify({'message' : 'Cannot perform that function!'})
        searchParameters =  request.json['searchData']
        if(searchParameters['field']=='Name'):
            searchParameters['field']='name'
        if(searchParameters['field']=='ID Number'):
            searchParameters['field']='idNumber'
        if(searchParameters['field']=='Gender'):
            searchParameters['field']='gender'
        if(searchParameters['field']=='Birthday'):
            searchParameters['field']='birthday'
        if(searchParameters['field']=='Phone'):
            searchParameters['field']='phone'
        if(searchParameters['field']=='Address'):
            searchParameters['field']='address'
        if(searchParameters['field']=='Mail'):
            searchParameters['field']='mail'
        if(searchParameters['field']=='Username'):
            searchParameters['field']='username'
        if(searchParameters['field']=='Password'):
            searchParameters['field']='password'
        if(searchParameters['field']=='Account Number'):
            searchParameters['field']='accountNumber'
        if(searchParameters['field']=='Account Balance'):
            searchParameters['field']='accountNumber'
        if(searchParameters['field']=='Role'):
            searchParameters['field']='role'
        if(searchParameters['field']=='Member Since'):
            searchParameters['field']='memberSince'
        accounts = db.Accounts.find({searchParameters['field']:searchParameters['fieldValue']})
        accountList = []
        for account in accounts:
            accountItem = {
                        'accountBalance' : account['accountBalance'],
                        'accountNumber': account['accountNumber'],
                        'address' : account['address'],
                        'birthday' : account['birthday'],
                        'cardNumber' : account['cardNumber'],
                        'idNumber' : account['idNumber'],
                        'mail' : account['mail'],
                        'name' : account['name'],
                        'password' : account['password'],
                        'phoneNumber' : account['phoneNumber'],
                        'role' : account['role'],
                        'username' : account['username'],
                        'gender' : account['gender'],
                        'memberSince' : account['memberSince'],
                        'accountId' : str(account['_id']) 
                        }
            accountList.append(accountItem)
    except Exception as e:
        return str(e)
    return json.dumps(accountList)

@application.route('/adminsearchbirth', methods=['POST'])
@token_required
def searchBirthAccounts(current_user):
    try:
        if not current_user['admin']:
            return jsonify({'message' : 'Cannot perform that function!'})
        searchParameters =  request.json['searchBirthData']
        # accounts = db.Accounts.find({'birthday':searchParameters['fieldValue']})
        accounts = db.Accounts.find()
        
        print(searchParameters['fieldValue'])
        accountList = []
        currentTimeRaw = time.localtime()
        currentTime=str(time.strftime('%d/%m/%Y', currentTimeRaw))
        print(currentTime)
        customerAge = datetime.timedelta(seconds= time.mktime(time.strptime(currentTime,"%d/%m/%Y"))-time.mktime(time.strptime(searchParameters['fieldValue'],"%d/%m/%Y"))).days//365
        print(customerAge)
        for account in accounts:
            accountAge = datetime.timedelta(seconds= time.mktime(time.strptime(currentTime,"%d/%m/%Y"))-time.mktime(time.strptime(account['birthday'],"%d/%m/%Y"))).days//365
            print(accountAge)
            if accountAge>=customerAge:
                    accountItem = {
                            'accountBalance' : account['accountBalance'],
                            'accountNumber': account['accountNumber'],
                            'address' : account['address'],
                            'birthday' : account['birthday'],
                            'cardNumber' : account['cardNumber'],
                            'idNumber' : account['idNumber'],
                            'mail' : account['mail'],
                            'name' : account['name'],
                            'password' : account['password'],
                            'phoneNumber' : account['phoneNumber'],
                            'role' : account['role'],
                            'username' : account['username'],
                            'gender' : account['gender'],
                            'memberSince' : account['memberSince'],
                            'accountId' : str(account['_id']) 
                            }
                    accountList.append(accountItem)
    except Exception as e:
        return str(e)
    return json.dumps(accountList)

@application.route('/adminsearchonebirth', methods=['POST'])
@token_required
def searchOneBirthAccount(current_user):
    try:
        if current_user['admin']:
            return jsonify({'message' : 'Cannot perform that function!'})
        searchParameters =  request.json['searchOneBirthData']
        # accounts = db.Accounts.find({'birthday':searchParameters['fieldValue']})
        accounts = db.Accounts.find()
        
        print(searchParameters['fieldValue'])
        accountList = []
        currentTimeRaw = time.localtime()
        currentTime=str(time.strftime('%d/%m/%Y', currentTimeRaw))
        print(currentTime)
        customerAge = datetime.timedelta(seconds= time.mktime(time.strptime(currentTime,"%d/%m/%Y"))-time.mktime(time.strptime(searchParameters['fieldValue'],"%d/%m/%Y"))).days
        print(customerAge)
        for account in accounts:
            accountAge = datetime.timedelta(seconds= time.mktime(time.strptime(currentTime,"%d/%m/%Y"))-time.mktime(time.strptime(account['birthday'],"%d/%m/%Y"))).days
            print(accountAge)
            if accountAge>=customerAge:
                    accountItem = {
                            'accountBalance' : account['accountBalance'],
                            'accountNumber': account['accountNumber'],
                            'address' : account['address'],
                            'birthday' : account['birthday'],
                            'cardNumber' : account['cardNumber'],
                            'idNumber' : account['idNumber'],
                            'mail' : account['mail'],
                            'name' : account['name'],
                            'password' : account['password'],
                            'phoneNumber' : account['phoneNumber'],
                            'role' : account['role'],
                            'username' : account['username'],
                            'gender' : account['gender'],
                            'memberSince' : account['memberSince'],
                            'accountId' : str(account['_id']) 
                            }
                    accountList.append(accountItem)
                    return json.dumps(accountList)
    except Exception as e:
        return str(e)
    return json.dumps(accountList)

@application.route('/normalsearch', methods=['POST'])
@token_required
def search_one_Account(current_user):
    try:
        if current_user['admin']:
            return jsonify({'message' : 'Cannot perform that function!'})
        searchParameters =  request.json['searchData']
        if(searchParameters['field']=='Name'):
            searchParameters['field']='name'
        if(searchParameters['field']=='ID Number'):
            searchParameters['field']='idNumber'
        if(searchParameters['field']=='Gender'):
            searchParameters['field']='gender'
        if(searchParameters['field']=='Birthday'):
            searchParameters['field']='birthday'
        if(searchParameters['field']=='Phone'):
            searchParameters['field']='phone'
        if(searchParameters['field']=='Address'):
            searchParameters['field']='address'
        if(searchParameters['field']=='Mail'):
            searchParameters['field']='mail'
        if(searchParameters['field']=='Username'):
            searchParameters['field']='username'
        if(searchParameters['field']=='Password'):
            searchParameters['field']='password'
        if(searchParameters['field']=='Account Number'):
            searchParameters['field']='accountNumber'
        if(searchParameters['field']=='Account Balance'):
            searchParameters['field']='accountNumber'
        if(searchParameters['field']=='Role'):
            searchParameters['field']='role'
        if(searchParameters['field']=='Member Since'):
            searchParameters['field']='memberSince'
        account = db.Accounts.find_one({searchParameters['field']:searchParameters['fieldValue']})
        accountList = []
        accountItem = {
                        'accountBalance' : account['accountBalance'],
                        'accountNumber': account['accountNumber'],
                        'address' : account['address'],
                        'birthday' : account['birthday'],
                        'cardNumber' : account['cardNumber'],
                        'idNumber' : account['idNumber'],
                        'mail' : account['mail'],
                        'name' : account['name'],
                        'password' : account['password'],
                        'phoneNumber' : account['phoneNumber'],
                        'role' : account['role'],
                        'username' : account['username'],
                        'gender' : account['gender'],
                        'memberSince' : account['memberSince'],
                        'accountId' : str(account['_id']) 
                        }
        accountList.append(accountItem)
    except Exception as e:
        return str(e)
    return json.dumps(accountList)

# @application.route('/getAccountPage')
# def getAccountOnePage():
#     paras = request.json('pageInfo')
#     pagenumber = paras['pagenumber']
#     itemsPerPage = paras['itemsPerPage']
#     accounts = db.Accounts.find()
#     total_count = db.Accounts.count()
#     accountList=[]
#     for account in accounts:
#         accountItem = {
#                         'accountBalance' : account['accountBalance'],
#                         'accountNumber': account['accountNumber'],
#                         'address' : account['address'],
#                         'birthday' : account['birthday'],
#                         'cardNumber' : account['cardNumber'],
#                         'idNumber' : account['idNumber'],
#                         'mail' : account['mail'],
#                         'name' : account['name'],
#                         'password' : account['password'],
#                         'phoneNumber' : account['phoneNumber'],
#                         'role' : account['role'],
#                         'username' : account['username'],
#                         'gender' : account['gender'],
#                         'memberSince' : account['memberSince'],
#                         'accountId' : str(account['_id']) 
#                         }
#         accountList.append(accountItem)
#     takenList=[]
#     for index, value in enumerate(accountList):
#         if index > (pagenumber-1)*itemsPerPage and index<(pagenumber-1)*itemsPerPage + itemsPerPage:
#             takenList.append(value)
#     return json.dumps(takenList)

@application.route('/')
def index():
    if 'username' in session:
            return showAccountList()
    return render_template('login.html')

@application.route('/login', methods=['POST'])
def login():
    session.clear();
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    users= db.Users

    login_user= users.find_one({'username': auth.username})
    if not login_user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    if login_user:
        if check_password_hash(login_user['password'],auth.password):
            session['username']= auth.username
            token = jwt.encode({'user_id' : login_user['user_id'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, application.config['SECRET_KEY'])           
            session['token']=token.decode('UTF-8')
            return redirect(url_for('index'))

    session.clear();
    return 'Invalid username or password'

@application.route('/logout', methods=['POST'])
def logOut():
    session.clear();
    application.config['SECRET_KEY']='new'
    return render_template('login.html')

@application.route('/register', methods=['POST','GET'])
def register():
    if request.method=='POST':
        users= db.Users
        existing_user=users.find_one({'username': request.form['username']})
        if existing_user is None:
            hashed_password = generate_password_hash(request.form['pass'], method='sha256')
            db.Users.insert({'user_id': str(uuid.uuid4()),'username': request.form['username'],'password':hashed_password,'admin':False})
            session['username']= request.form['username']
            session.clear()
            return redirect(url_for('index'))
        return 'That username already exists!'




    return render_template('register.html')

if __name__ == "__main__":

    application.run(debug=True)

