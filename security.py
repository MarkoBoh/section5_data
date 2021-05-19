from werkzeug.security import check_password_hash # za primerjavo passwordov
from user import User

# to nam omogoca da klicemo username_mapping['bob'] in dobimo vse podatke
# da nam ni treba presikovati prve tabele

def authenticate(username, password):
    # user= username_mapping.get(username, None) # dobimo value of the key username, 
    user= User.find_by_username(username) # dobimo value of the key username, None ;e ca ni
    if user and check_password_hash(user.password, password): # hash passworda
        return user

def identity(payload): # payload je content of jwt 
    user_id = payload['identity']
    return User.find_by_id(user_id)
