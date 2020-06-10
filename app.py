from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps



conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    idUser = db.Column(db.String(100), primary_key=True, unique = True)
    name = db.Column(db.String(45))
    surname = db.Column(db.String(45))
    user = db.Column(db.String(45))
    password = db.Column(db.String(45))
    email = db.Column(db.String(45))
    phone = db.Column(db.String(45))
    userImage = db.Column(db.String(250))
    createdDate = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Events(db.Model):
    idEvent = db.Column(db.String(100), primary_key=True, unique = True)
    eventName = db.Column(db.String(45))
    eventDate = db.Column(db.DateTime)
    eventDescription = db.Column(db.String(45))
    eventImage = db.Column(db.String(250))
    createdDate = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class relUsersEvents(db.Model):
    Users_idUser = db.Column(db.String(100), primary_key=True)
    Events_idEvent = db.Column(db.String(100), primary_key=True)

def token_required(callback):
    @wraps(callback)
    def decorated(*args, **kargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401 

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            currentUser = Users.query.filter_by(idUser = data['idUser']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return callback(currentUser, *args, **kargs)

    return decorated

@app.route('/signup', methods=['POST'])
def create_user():
    data = request.get_json(force = True)
    print(data)
    # hashed_password = generate_password_hash(data['password'], method='sha256')
    userExist = Users.query.filter_by(user = data['user']).first()
    if (userExist == None ):
        newUser = Users(idUser=str(uuid.uuid4()), name = data['name'], surname = data['surname'], user = data['user'], password = data['password'], email = data['email'], phone=data['phone'])
        db.session.add(newUser)
        db.session.commit()
        return make_response(jsonify({'message': 'Nuevo usuario creado'}))
    else:
        return make_response(jsonify({'message': 'Ese nombre de usuario ya existe'}))
    
@app.route('/login')
def login():
    auth = request.authorization
    print(auth)
    if not auth or not auth.username or not auth.password:
        return make_response(jsonify({'message':'Login required!'}), 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    
    user = Users.query.filter_by(user = auth.username).first()
    print(user)

    if not user:
        return make_response(jsonify({'message':'User does not exists!'}), 401, {'WWW-Authenticate' : 'Basic realm="User does not exists!"'})

    if check_password_hash(generate_password_hash(user.password, method='sha256'), auth.password):
        token = jwt.encode({'idUser' : user.idUser, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=10000)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response(jsonify({'message':'Your password is wrong'}), 401, {'WWW-Authenticate' : 'Basic realm="Your password is wrong"'})

@app.route('/allusers', methods=['GET'])
@token_required
def get_all_users(currentUser):

    users = Users.query.all()
    output = []
    for user in users:
        userData = {}
        userData['name'] = user.name
        userData['image'] = user.userImage
        userData['email'] = user.email
        output.append(userData)

    print(output)
    return jsonify({'users': output})
    
@app.route('/createEvent', methods=['POST'])
@token_required
def create_event(currentUser):
    data = request.get_json(force = True)
    print(data)
    newEvent = Events(idEvent = str(uuid.uuid4()), eventName = data['eventName'],  eventDate = datetime.datetime.strptime(data['eventDate'], '%d-%m-%Y'), eventDescription = data['eventDescription'], eventImage = data['eventImage'])
    db.session.add(newEvent)
    db.session.commit()
    idEvent = newEvent.idEvent
    finalUser = []

    for user in data['eventUsers']:
        # LIMPIO ARRAY EN CASO DE NOMBRES IGUALES
        if user not in finalUser:
            finalUser.append(user)

    for user in finalUser:
        idUser = Users.query.filter_by(name = user).all() 
        print(idUser)
        if (len(idUser) > 1):
            for i in range(len(idUser)):
                newRelUsersEvents = relUsersEvents(Users_idUser = idUser[i].idUser, Events_idEvent = idEvent)
                db.session.add(newRelUsersEvents)
                db.session.commit()
            
        else:
            newRelUsersEvents = relUsersEvents(Users_idUser = idUser[0].idUser, Events_idEvent = idEvent)
            db.session.add(newRelUsersEvents)
            db.session.commit()

    return make_response(jsonify({'message': 'okei'}))

@app.route('/allevents', methods=['GET'])
@token_required
def get_all_events(currentUser):
    eventsList = relUsersEvents.query.filter_by(Users_idUser = currentUser.idUser).all()
    output = []
    print(eventsList)
    for event in eventsList:
        eventsListInfo = Events.query.filter_by(idEvent = event.Events_idEvent).all()
        for eventInfo in eventsListInfo:
            eventData = {}
            eventData['eventName'] = eventInfo.eventName
            output.append(eventData)


    return jsonify({'events': output})

if __name__ == '__main__':
    app.run(debug=True, port=4000)
