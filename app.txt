from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended import JWTManager
from content_recommendation import recommend_content_based
from general_popularity import recommend_popular_articles
from login import Login
import pandas as pd

app = Flask(__name__)
app.config.from_object('config.Config')
jwt = JWTManager(app)

df_user_acc = pd.read_parquet("recommendation.parquet")  
df_news = pd.read_parquet("news_processed.parquet")  


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if Login().validade_user(username, password):
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200
    else:
        return jsonify({"msg": "Credenciais inválidas"}), 401


@app.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    user_id = request.args.get('user_id')  
    
    if user_id: 
        # Verifica se o usuário existe no DataFrame
        user_row = df_user_acc[df_user_acc['userId'] == user_id]
        if user_row.empty:
            return jsonify({"message": "User not found."}), 404

        user_type = user_row['userType'].iloc[0]
        recommendations = recommend_content_based(user_id, df_user_acc, df_news)
        if recommendations:
            # Extrai as páginas recomendadas
            recommended_pages = [article['page'] for article in recommendations]
            return jsonify({
                "userId": user_id,
                "userType": user_type,
                "history": recommended_pages
            }), 200
        else:
            return jsonify({"message": "No recommendations found for this user."}), 404
    else:
        # Caso de cold start (usuário não logado)
        recommendations = recommend_popular_articles()  
        recommended_pages = [article['page'] for article in recommendations]
        return jsonify({
                "userId": None,
                "userType": "Non-Logged",
                "history": recommended_pages
            }), 200

if __name__ == '__main__':
    app.run(debug=True)
