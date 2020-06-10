from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
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
    idUser = db.Column(db.String(100), primary_key=True, unique=True)
    name = db.Column(db.String(45))
    surname = db.Column(db.String(45))
    user = db.Column(db.String(45))
    password = db.Column(db.String(45))
    email = db.Column(db.String(45))
    phone = db.Column(db.String(45))
    userImage = db.Column(db.String(250))
    createdDate = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Events(db.Model):
    idEvent = db.Column(db.String(100), primary_key=True, unique=True)
    eventName = db.Column(db.String(45))
    eventDate = db.Column(db.DateTime)
    eventDescription = db.Column(db.String(45))
    eventImage = db.Column(db.String(250))
    createdDate = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class RelUsersEvents(db.Model):
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
            current_user = Users.query.filter_by(idUser=data['idUser']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return callback(current_user, *args, **kargs)

    return decorated


@app.route('/signup', methods=['POST'])
def create_user():
    data = request.get_json(force=True)
    print(data)
    # hashed_password = generate_password_hash(data['password'], method='sha256')
    user_exist = Users.query.filter_by(user=data['user']).first()
    if user_exist == None:
        new_user = Users(idUser=str(uuid.uuid4()), name=data['name'], surname=data['surname'], user=data['user'],
                        password=data['password'], email=data['email'], phone=data['phone'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'Nuevo usuario creado'}))
    else:
        return make_response(jsonify({'message': 'Ese nombre de usuario ya existe'}))


@app.route('/login')
def login():
    auth = request.authorization
    print(auth)
    if not auth or not auth.username or not auth.password:
        return make_response(jsonify({'message': 'Login required!'}), 401,
                             {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = Users.query.filter_by(user=auth.username).first()
    print(user)

    if not user:
        return make_response(jsonify({'message': 'User does not exists!'}), 401,
                             {'WWW-Authenticate': 'Basic realm="User does not exists!"'})

    if check_password_hash(generate_password_hash(user.password, method='sha256'), auth.password):
        token = jwt.encode(
            {'idUser': user.idUser, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10000)},
            app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response(jsonify({'message': 'Your password is wrong'}), 401,
                         {'WWW-Authenticate': 'Basic realm="Your password is wrong"'})


@app.route('/allusers', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = Users.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['name'] = user.name
        user_data['image'] = user.userImage
        user_data['email'] = user.email
        output.append(user_data)

    print(output)
    return jsonify({'users': output})


@app.route('/createEvent', methods=['POST'])
@token_required
def create_event(current_user):
    data = request.get_json(force=True)
    print(data)
    new_event = Events(idEvent=str(uuid.uuid4()), eventName=data['eventName'],
                      eventDate=datetime.datetime.strptime(data['eventDate'], '%d-%m-%Y'),
                      eventDescription=data['eventDescription'], eventImage=data['eventImage'])
    db.session.add(new_event)
    db.session.commit()
    id_event = new_event.idEvent
    final_user = []

    for user in data['eventUsers']:
        # LIMPIO ARRAY EN CASO DE NOMBRES IGUALES
        if user not in final_user:
            final_user.append(user)

    for user in final_user:
        id_user = Users.query.filter_by(name=user).all()
        print(id_user)
        if len(id_user) > 1:
            for i in range(len(id_user)):
                new_rel_users_events = RelUsersEvents(Users_idUser=id_user[i].idUser, Events_idEvent=id_event)
                db.session.add(new_rel_users_events)
                db.session.commit()

        else:
            new_rel_users_events = RelUsersEvents(Users_idUser=id_user[0].idUser, Events_idEvent=id_event)
            db.session.add(new_rel_users_events)
            db.session.commit()

    return make_response(jsonify({'message': 'okei'}))


@app.route('/allevents', methods=['GET'])
@token_required
def get_all_events(current_user):
    events_list = RelUsersEvents.query.filter_by(Users_idUser=current_user.idUser).all()
    output = []
    print(events_list)
    for event in events_list:
        events_list_info = Events.query.filter_by(idEvent=event.Events_idEvent).all()
        for eventInfo in events_list_info:
            event_data = {'eventName': eventInfo.eventName}
            output.append(event_data)

    return jsonify({'events': output})


if __name__ == '__main__':
    app.run(debug=True, port=4000)
