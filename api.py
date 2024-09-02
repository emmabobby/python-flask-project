from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, reqparse, fields, marshal_with, abort, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:complicated731#@localhost:3306/note_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"User(name: {self.name}, password: {self.password}, username: {self.username}"


class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"Note(title: {self.title}, content: {self.content}"


@app.route("/")
def home_page():
    return "<h1> Welcome to c20 Flask </h1>"


user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="Name is required")
user_args.add_argument("username", type=str, required=True, help="username is required")
user_args.add_argument("password", type=str, required=True, help="password is required")

userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'username': fields.String,
    'password': fields.String
}


class User(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()

        existing_user = UserModel.query.filter(
            (UserModel.username == args['username']) | (UserModel.name == args['name'])).first()

        if existing_user:
            abort(409, message="User already exist with the provided username")

        user = UserModel(name=args['name'], username=args['username'], password=args['password'])

        db.session.add(user)
        db.session.commit()
        return user, 201


api.add_resource(User, "/api/users")

note_args = reqparse.RequestParser()
note_args.add_argument("name", type=str, required=True, help="Name is required")
note_args.add_argument("title", type=str, required=True, help="title is required")
note_args.add_argument("content", type=str, required=True, help="content is required")

noteFields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String
}


class Note(Resource):
    @marshal_with(noteFields)
    def get(self):
        note = NoteModel.query.all()
        return note

    @marshal_with(noteFields)
    def post(self):
        args = note_args.parse_args()

        existing_note = NoteModel.query.filter(
            (NoteModel.title == args['title']) | (NoteModel.content == args['content'])).first()

        if existing_note:
            abort(409, message="Note already exist with the provided title")

        note = NoteModel(content=args['content'], title=args['title'])

        db.session.add(note)
        db.session.commit()
        note = UserModel.query.all()
        return note, 201


api.add_resource(Note, "/api/note")

if __name__ == "__main__":
    app.run(Debug=True)
