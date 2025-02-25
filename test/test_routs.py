import pytest
import json
from src.api.recommendations import recommend_popular_articles, recommend_content_based

@pytest.fixture
def mock_recommend_popular_articles(mocker):
    mocker.patch('src.api.recommendations.recommend_popular_articles', return_value=[
        {'page': 'page1', 'url': 'url1'},
        {'page': 'page2', 'url': 'url2'}
    ])

def test_get_popular_recommendations(client, mock_recommend_popular_articles):
    response = client.get('/api/recommend/popular')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['page'] == 'page1'
    assert data[0]['url'] == 'url1'

@pytest.fixture
def mock_recommend_content_based(mocker):
    mocker.patch('src.api.recommendations.recommend_content_based', return_value=[
        {'page': 'page3', 'url': 'url3'},
        {'page': 'page4', 'url': 'url4'}
    ])

def test_get_content_recommendations(client, mock_recommend_content_based):
    user_id = 'user1'
    response = client.post(f'/api/recommend/content/{user_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['page'] == 'page3'
    assert data[0]['url'] == 'url3'