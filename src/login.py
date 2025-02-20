# allowed_uses = [{'user' : 'admin', 'password' : 'senha'}, {'user' : 'guilherme', 'password' : 'senha'},
#                 {'user' : 'lucas', 'password' : 'senha'}, {'user' : 'yago', 'password' : 'senha'}]

# class Login():

#     def validade_user(self,username:str,password:str):
#         for user in allowed_uses:
#             if (user['user'] == username) and (user['password'] == password):
#                 return True
        
#         return False
    
# src/api/login.py
from flask import request, jsonify
from werkzeug.security import check_password_hash
from utils.dynamodb import get_item_from_dynamodb
from config import DYNAMODB_TABLE

def login_user(username, password):
    user = get_item_from_dynamodb(DYNAMODB_TABLE, {'id': username})
    
    if not user:
        return None
    
    stored_password = user['password']
    if check_password_hash(stored_password, password):
        return user
    return None

def login_route():
    data = request.get_json()
    username = data.get('id')
    password = data.get('password')
    
    user = login_user(username, password)
    if user:
        return jsonify({"message": "Login successful", "user": user}), 200
    return jsonify({"message": "Invalid credentials"}), 401
