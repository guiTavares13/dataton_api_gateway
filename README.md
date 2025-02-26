# Datathon API G1

## Grupo 87 - Integrantes:
- Guilherme Tavares RM353804
- Lucas Santos RM354552
- Yago Caetano RM353994

## Descrição

Este projeto implementa um sistema de recomendação de notícias do G1, considerando tanto o problema de **cold start** quanto as preferências de usuários
logados. Ele utiliza **Flask** para expor endpoints REST protegidos com autenticação JWT que por sua vez chamam a classe recommendations.py e suas 
respectivas funções:

recommend_popular_articles para o cold start, onde é retornado uma lista com as páginas recomendadas mais recentes baseado em alguns score como 
número de cliques, tempo gasto na página, percentual de visualização da notícia e número de vezes que visitou a página.

recommend_content_based para recomendar notícias recentes ao usuário de acordo com tipo de conteúdo presente em seu histórico.

## Tecnologias e Bibliotecas Utilizadas

- **Python**
- **Flask** (framework web)
- **Scikit-learn** (processamento de dados)
- **Pandas** (manipulação de dados)
- **Boto3** (conexão com DynamoDB)
- **JWT** (autenticação)
- **Docker** (containerização)

## Instalação e Execução

### 1. Clonar o repositório

```bash
git clone https://github.com/guiTavares13/dataton_api_gateway.git
```

### 2. Criar e ativar um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação

```bash
python app.py
```

A API estará disponível em `http://localhost:5000/api`

## Uso da API

### **Autenticação**

#### **POST /login**

**Body:**

```json
{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

**Resposta:**

```json
{
    "message": "Login successful",
    "token": "jwt-token"
}
```

### **Recomendações**

#### **Artigos populares (Cold Start)**

#### **GET  /recommend/popular**

**Headers:**

```
Authorization: Bearer <jwt-token>
```
**Resposta:**

```json
[
    { "page": "noticia1", "url": "https://g1.globo.com/noticia1" },
    { "page": "noticia2", "url": "https://g1.globo.com/noticia2" }
]
```

#### **Baseado no histórico do usuário**

#### **POST   /recommend/content/<user_id>**

**Headers:**

```
Authorization: Bearer <jwt-token>
```

**Resposta:**

```json
[
    { "page": "noticia-recomendada", "url": "https://g1.globo.com/noticia-recomendada" }
]
```

## Docker

### Construção da imagem

```bash
docker build -t dataton-api .
```

### Execução do container

```bash
docker run -p 5000:5000 dataton-api
```
