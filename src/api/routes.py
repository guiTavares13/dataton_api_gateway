from flask import Blueprint, jsonify, request
from api.auth import login_route, token_required
from api.lambda_client import invoke_lambda
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/login', methods=['POST'])
def login():
    return login_route()

@api_bp.route('/invoke-lambda', methods=['POST'])
@token_required
def invoke_lambda_route(current_user):
    payload = request.get_json()
    response = invoke_lambda(json.dumps(payload))
    return jsonify({"response": response}), 200

