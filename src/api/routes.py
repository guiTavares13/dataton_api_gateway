from flask import Blueprint, jsonify, request
from api.auth import login_route, token_required
from api.recommendations import recommend_popular_articles, recommend_content_based
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/login', methods=['POST'])
def login():
    return login_route()

@api_bp.route('/recommend/popular', methods=['GET'])
@token_required
def get_popular_recommendations():
    response = recommend_popular_articles()
    return jsonify(response), 200

@api_bp.route('/recommend/content/<user_id>', methods=['POST'])
@token_required
def get_content_recommendations(user_id):
    response = recommend_content_based(user_id)
    return jsonify(response), 200