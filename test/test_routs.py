import pytest
from unittest.mock import patch
from flask import Flask
from api.routes import api_bp
import pandas as pd

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_data():
    # Criando dados mock para general_recommendation.parquet
    general_data = pd.DataFrame({
        'history': ['page1', 'page2', 'page3'],
        'numberOfClicksHistory': [10, 20, 30],
        'timeOnPageHistory': [100, 200, 300],
        'pageVisitsCountHistory': [5, 10, 15]
    })

    # Criando dados mock para news_processed.parquet
    news_data = pd.DataFrame({
        'page': ['page1', 'page2', 'page3', 'page4'],
        'url': ['http://example.com/page1', 'http://example.com/page2', 'http://example.com/page3', 'http://example.com/page4'],
        'article-type': ['type1', 'type2', 'type3', 'type1'],
        'modified': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']
    })

    # Criando dados mock para recommendation.parquet
    user_data = pd.DataFrame({
        'userId': ['user1'],
        'history': [['page1', 'page2']],
        'article_types': [['type1', 'type2']]
    })

    return general_data, news_data, user_data

def test_popular_recommendations_route(client, mock_data):
    
    general_data, news_data, user_data = mock_data
    
    with patch('pandas.read_parquet') as mock_read_parquet:
        mock_read_parquet.side_effect = [general_data, news_data]

        response = client.get('/api/recommend/popular', headers={'Authorization': 'Bearer valid_token'})

        assert response.status_code == 200
        assert response.json == [{'page': 'page3', 'url': 'http://example.com/page3'}, 
                                 {'page': 'page2', 'url': 'http://example.com/page2'}, 
                                 {'page': 'page1', 'url': 'http://example.com/page1'}]


def test_content_recommendations_route(client, mock_data):

    general_data, user_data, news_data  = mock_data

    with patch('pandas.read_parquet') as mock_read_parquet:
        mock_read_parquet.side_effect = [news_data, user_data]

        response = client.post('/api/recommend/content/user1', headers={'Authorization': 'Bearer valid_token'})

        assert response.status_code == 200
        assert response.json == [{'page': 'page4', 'url': 'http://example.com/page4'}]
