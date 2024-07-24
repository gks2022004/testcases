from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

class TestCase(db.Model):
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/testcases', methods=['GET'])
def get_testcases():
    testcases = TestCase.query.all()
    testcase_list = [
        {'id': testcase.id, 'name': testcase.name, 'description': testcase.description, 'status': testcase.status}
        for testcase in testcases
    ]
    return jsonify({"testcases": testcase_list})

@app.route('/testcases', methods=['POST'])
def create_testcase():
    data = request.get_json()
    new_testcase = TestCase(name=data['name'], description=data['description'], status=data['status'])
    try:
        db.session.add(new_testcase)
        db.session.commit()
        socketio.emit('update', {'action': 'create', 'testcase': {
            'id': new_testcase.id,
            'name': new_testcase.name,
            'description': new_testcase.description,
            'status': new_testcase.status
        }})
        return jsonify({"message": "Test case created successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Test case with this name already exists"}), 400

@app.route('/testcases/<int:id>', methods=['PUT'])
def update_testcase(id):
    data = request.get_json()
    testcase = TestCase.query.get(id)
    if not testcase:
        return jsonify({"error": "Test case not found"}), 404

    testcase.name = data.get('name', testcase.name)
    testcase.description = data.get('description', testcase.description)
    testcase.status = data.get('status', testcase.status)

    db.session.commit()
    socketio.emit('update', {'action': 'update', 'testcase': {
        'id': testcase.id,
        'name': testcase.name,
        'description': testcase.description,
        'status': testcase.status
    }})
    return jsonify({"message": "Test case updated successfully"})

@app.route('/testcases/<int:id>', methods=['DELETE'])
def delete_testcase(id):
    testcase = TestCase.query.get(id)
    if not testcase:
        return jsonify({"error": "Test case not found"}), 404

    db.session.delete(testcase)
    db.session.commit()
    socketio.emit('update', {'action': 'delete', 'id': id})
    return jsonify({"message": "Test case deleted successfully"})

if __name__ == '__main__':
    socketio.run(app, debug=True)
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Gaurav123@localhost:5432/testing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

class TestCase(db.Model):
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/testcases', methods=['GET'])
def get_testcases():
    testcases = TestCase.query.all()
    testcase_list = [
        {'id': testcase.id, 'name': testcase.name, 'description': testcase.description, 'status': testcase.status}
        for testcase in testcases
    ]
    return jsonify({"testcases": testcase_list})

@app.route('/testcases', methods=['POST'])
def create_testcase():
    data = request.get_json()
    new_testcase = TestCase(name=data['name'], description=data['description'], status=data['status'])
    try:
        db.session.add(new_testcase)
        db.session.commit()
        socketio.emit('update', {'action': 'create', 'testcase': {
            'id': new_testcase.id,
            'name': new_testcase.name,
            'description': new_testcase.description,
            'status': new_testcase.status
        }})
        return jsonify({"message": "Test case created successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Test case with this name already exists"}), 400

@app.route('/testcases/<int:id>', methods=['PUT'])
def update_testcase(id):
    data = request.get_json()
    testcase = TestCase.query.get(id)
    if not testcase:
        return jsonify({"error": "Test case not found"}), 404

    testcase.name = data.get('name', testcase.name)
    testcase.description = data.get('description', testcase.description)
    testcase.status = data.get('status', testcase.status)

    db.session.commit()
    socketio.emit('update', {'action': 'update', 'testcase': {
        'id': testcase.id,
        'name': testcase.name,
        'description': testcase.description,
        'status': testcase.status
    }})
    return jsonify({"message": "Test case updated successfully"})

@app.route('/testcases/<int:id>', methods=['DELETE'])
def delete_testcase(id):
    testcase = TestCase.query.get(id)
    if not testcase:
        return jsonify({"error": "Test case not found"}), 404

    db.session.delete(testcase)
    db.session.commit()
    socketio.emit('update', {'action': 'delete', 'id': id})
    return jsonify({"message": "Test case deleted successfully"})

if __name__ == '__main__':
    socketio.run(app, debug=True)
