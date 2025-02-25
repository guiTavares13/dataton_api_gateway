import pytest
from unittest.mock import patch
import pandas as pd
from api.recommendations import recommend_popular_articles, recommend_content_based

@pytest.fixture
def mock_data():
    # Criando dados mock para general_recommendation.parquet
    general_data = pd.DataFrame( {
        'history': ['page1', 'page2', 'page3'],
        'numberOfClicksHistory': [10, 20, 30],
        'timeOnPageHistory': [100, 200, 300],
        'pageVisitsCountHistory': [5, 10, 15]
    })

    # Criando dados mock para news_processed.parquet
    news_data = pd.DataFrame( {
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

def test_recommend_popular_articles(mock_data):
    general_data, news_data, user_data = mock_data

    with patch('pandas.read_parquet') as mock_read_parquet:
        mock_read_parquet.side_effect = [general_data, news_data]
        
        recommendations = recommend_popular_articles()
    
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert 'page' in recommendations[0]
        assert 'url' in recommendations[0]

def test_recommend_content_based(mock_data):
    general_data, user_data, news_data  = mock_data

    with patch('pandas.read_parquet') as mock_read_parquet:
        mock_read_parquet.side_effect = [news_data, user_data]

        user_id = 'user1'

        recommendations = recommend_content_based(user_id)
        print("recommendations", recommendations)
    
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert 'page' in recommendations[0]
        assert 'url' in recommendations[0]
