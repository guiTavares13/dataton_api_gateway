import pandas as pd
import os

def recommend_popular_articles():
    base_path = os.path.dirname(os.path.abspath(__file__))
    general_data_path = os.path.join(base_path, '../../general_recommendation.parquet')
    news_data_path = os.path.join(base_path, '../../news_processed.parquet')

    df = pd.read_parquet(general_data_path)
    df_news = pd.read_parquet(news_data_path)

    alpha, beta, gamma, delta = 0.1, 0.3, 0.4, 0.2

    df['popularity_score'] = (
        alpha * df['numberOfClicksHistory'] +
        beta * df['timeOnPageHistory'] +
        gamma * df['timeOnPageHistory'] +
        delta * df['pageVisitsCountHistory']
    )

    grouped_sorted = df.sort_values(by='popularity_score', ascending=False)
    recommendations = grouped_sorted.head(10)

    recommendations.rename(columns={'history': 'page'}, inplace=True)
    recommendations = recommendations.merge(df_news[['page', 'url']], on='page', how='left')
    recommendations = recommendations.dropna(subset=['url'])

    return recommendations[['page', 'url']].to_dict(orient='records')

def recommend_content_based(user_id):
    base_path = os.path.dirname(os.path.abspath(__file__))
    user_data_path = os.path.join(base_path, '../../recommendation.parquet')
    articles_data_path = os.path.join(base_path, '../../news_processed.parquet')

    df_user_acc = pd.read_parquet(user_data_path)
    df_news = pd.read_parquet(articles_data_path)

    # Imprimir os nomes das colunas para depuração
    print("Colunas em df_user_acc:", df_user_acc.columns)
    print("Colunas em df_news:", df_news.columns)

    # Verificar se as colunas necessárias estão presentes
    if 'userId' not in df_user_acc.columns:
        raise KeyError("A coluna 'userId' não foi encontrada em df_user_acc")
    if 'history' not in df_user_acc.columns:
        raise KeyError("A coluna 'history' não foi encontrada em df_user_acc")
    if 'article_types' not in df_user_acc.columns:
        raise KeyError("A coluna 'article_types' não foi encontrada em df_user_acc")
    if 'page' not in df_news.columns:
        raise KeyError("A coluna 'page' não foi encontrada em df_news")
    if 'article-type' not in df_news.columns:
        raise KeyError("A coluna 'article-type' não foi encontrada em df_news")
    if 'modified' not in df_news.columns:
        raise KeyError("A coluna 'modified' não foi encontrada em df_news")

    user_row = df_user_acc[df_user_acc['userId'] == user_id]
    if user_row.empty:
        return []

    user_history = set(user_row['history'].iloc[0])
    user_article_types = set(user_row['article_types'].iloc[0])

    potential_articles = df_news[~df_news['page'].isin(user_history)]
    recommendations = potential_articles[potential_articles['article-type'].isin(user_article_types)]
    recommendations = recommendations.sort_values(by='modified', ascending=False)

    return recommendations[['page', 'url']].head(20).to_dict(orient='records')