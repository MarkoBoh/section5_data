import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password
         
    @classmethod
    def find_by_username(cls,username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query,(username,)) #mora biti tuple type

        row = result.fetchone()

        if row is not None:
            user = cls(row[0],row[1],row[2])  # kot defirnirano v init razreda
            #user = cls(*row)  # kot defirnirano v init razreda
        else:
            user = None
        
        connection.close()
        return user

    @classmethod
    def find_by_id(cls,_id):   # metoda klase
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(query,(_id,)) #mora biti tuple type

        row = result.fetchone()

        if row is not None:
            user = cls(row[0],row[1],row[2])  # kot defirnirano v init razreda
            #user = cls(*row)  # kot defirnirano v init razreda
        else:
            user = None
        
        connection.close()
        return user

class UserRegister(Resource): # ker rabimo endpoint mora biti drugi razred
    parser = reqparse.RequestParser()
    parser.add_argument('username',    # ce ostalih argumentov ne navedemo, ne bodo sprejeti!!!
        type=str,
        required=True,
        help="To polje ne more biti prazno"
    )
    parser.add_argument('password',    # ce ostalih argumentov ne navedemo, ne bodo sprejeti!!!
        type=str,
        required=True,
        help="To polje ne more biti prazno"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "User exists"},400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL,?,?)"
       
        password_hash = generate_password_hash(data['password'])
        cursor.execute(query,(data['username'],password_hash) )
        connection.commit()
        connection.close()

class Users(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users"
        result = cursor.execute(query)

        seznam =[]
        for row in result:
            seznam.append(row)

        connection.close()
        return seznam, 200


