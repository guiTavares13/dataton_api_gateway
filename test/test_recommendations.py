import pytest
from src.api.recommendations import recommend_popular_articles, recommend_content_based

@pytest.fixture
def mock_recommend_popular_articles(mocker):
    mocker.patch('src.api.recommendations.recommend_popular_articles', return_value=[
        {'page': 'page1', 'url': 'url1'},
        {'page': 'page2', 'url': 'url2'},
        {'page': 'page3', 'url': 'url3'}
    ])

def test_recommend_popular_articles(mock_recommend_popular_articles):
    recommendations = recommend_popular_articles()
    assert len(recommendations) == 3
    assert recommendations[0]['page'] == 'page1'
    assert recommendations[0]['url'] == 'url1'

@pytest.fixture
def mock_recommend_content_based(mocker):
    mocker.patch('src.api.recommendations.recommend_content_based', return_value=[
        {'page': 'page3', 'url': 'url3'},
        {'page': 'page4', 'url': 'url4'}
    ])

def test_recommend_content_based(mock_recommend_content_based):
    user_id = 'user1'
    recommendations = recommend_content_based(user_id)
    assert len(recommendations) == 2
    assert recommendations[0]['page'] == 'page3'
    assert recommendations[0]['url'] == 'url3'