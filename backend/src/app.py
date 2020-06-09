from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/flaskreactdb'
app.config['CORS_HEADERS'] = 'Content-Type'
mongo = PyMongo(app)

CORS(app)

db = mongo.db.users

@app.route('/users', methods=['POST'])
def createUser():
    print(request.data)
    id = db.insert_one({
        "name": request.json['name'],
        "email": request.json['email'],
        "password": request.json['password']
    }).inserted_id
    return jsonify(str(ObjectId(id)))

@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def getUser(id):
    user = db.find_one({'_id': ObjectId(id)})
    return jsonify({
            '_id': str(ObjectId(user['_id'])),
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
        })

@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'mesg': 'User deleted'})

@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    db.update_one({'_id': ObjectId(id)},
                         {'$set': {
                             'name': request.json['name'],
                             'email': request.json['email'],
                             'password': request.json['password']
                         }})

    return jsonify({'mesg': 'User updated'})


@app.route('/')
def index():
    return '<h1>It is working</h1>'

if __name__ == "__main__":
    app.run(debug=True)